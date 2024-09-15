"""Find out what personal information of a user is exposed on the Internet."""

from importlib import import_module
from json import dumps
from time import time

from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from g4f.client import Client as g4f_Client
from g4f.Provider import MetaAI
from httpx import Client as httpx_Client
from httpx import HTTPStatusError, RequestError
from requests import get, post

app_api = import_module("main")  # Importing to change the osint progresses


def scrape(url: str) -> None:
    """Get the text from a website.

    Args:
        url (str): The URL to scrape.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"}
        # Use httpx with cookies enabled and follow redirects (cookie interference with g4f library)
        with httpx_Client(headers=headers, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            # Remove script, style, and other non-content elements
            for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
                element.decompose()
            # Extract text from remaining elements
            text = soup.get_text(separator=" ", strip=True)
            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            cleaned_text = "\n".join(chunk for chunk in chunks if chunk)
            # Limit the text to 500 characters
            limited_text = cleaned_text[:500]
            return limited_text
    except HTTPStatusError as e:
        return f"HTTP Error: {e}"
    except RequestError as e:
        return f"Request Error: {e}"


def generate_payload(target_name: str, additional_info: str, find_images: bool = False) -> list[str]:
    """Generate proompts for the AI.

    Args:
        target_name (str): The name of the person to get information on.
        additional_info (str): Additional background information on the target.
        find_images (bool): Whether to find images of the target. Defaults to False.

    Returns:
        list[str]: A list of AI payloads.
    """
    # Get DuckDuckGo results
    quoted_target_name = f"“{target_name}”"
    search_results = DDGS().text(quoted_target_name, max_results=9)
    additional_results = DDGS().text(f"{target_name} {additional_info}", max_results=3)
    if find_images:
        images = DDGS().images(quoted_target_name, region="sg-en", max_results=2)

    payloads = []
    payloads.append(
        "Write me a comprehensive report on a person that is as detailed as possible."
        f" Do note that the person's name is {target_name}. Perhaps you could also create a web of people relating to them and"
        " provide ANY and ALL links where the information can be found. Do also see if you can extract basic information such"
        " as past and current education statuses, location and information from ANY accounts like their username or email."
        " Here is the data with links, do remember to INCLUDE AND NUMBER THE LINKS at the bottom."
    )
    if find_images:
        payloads.append(
            "Data:\n"
            f"{' '.join(map(str, search_results))}\n"
            f" Now, with the above data, I will provide you with some image links relating to {target_name}."
            f" Do filter through all the data and give me ALL relevant links. Here is the data: {' '.join(map(str, images))}."
        )

    # Remove duplicates in search and additional results
    for item in additional_results:
        if item in search_results:
            additional_results.remove(item)
    # Get elements in result lists
    starting_data = search_results[1:6]
    check_data = search_results[5:10] + additional_results
    http = []
    for x in starting_data + check_data:
        if "href" in str(x) and not str(x).lower().endswith(".pdf"):
            http.append(x["href"])
    print("Results found: " + str(len(http)))
    starting_data = " ".join(map(str, starting_data))
    check_data = " ".join(map(str, check_data))

    print(starting_data)
    print(check_data)
    print(http)

    payloads.append(
        "Do remember to include ALL links and make verbose inferences to the best of your ability!"
        f" Here is some starting data for you. Data: {starting_data}"
    )
    # Link payload generation
    scraped_text = []
    for x in http:
        scraped_text.append(scrape(x))
    payloads.append(
        "Now for each of the links you have identified, I will give you the content for each of them. Remember to"
        f" ADD ON to your previous response, being as verbose as possible. Link: {x} {' '.join(scraped_text)}."
        " KEEP ALL content from your PREVIOUS response(s), build upon them and analyse IN DETAIL the data provided with"
        " AS MUCH inferred information and proper organisation possible."
    )
    payloads.append(
        "Here is a final data check on the report. Clean up your report and remember to KEEP ALL content from your"
        " previous response(s) and ADD ON to everything especially the links at the bottom (numbered), being as VERBOSE"
        f" as possible! Data: {check_data}"
    )
    print("Payloads:", payloads)
    return payloads


def chat(payloads: list[str], osint_id: int) -> str:
    """Send payloads to the AI and get the results.

    Args:
        payloads (list[str]): The list of payloads.
        osint_id (int): The ID of the OSINT, used to update progress.

    Returns:
        str: The final AI response.
    """
    client = g4f_Client(provider=MetaAI)
    messages = []  # Message history
    app_api.osint_progresses[osint_id].started = True
    app_api.osint_progresses[osint_id].total_payloads = len(payloads)
    for i, payload in enumerate(payloads):
        print(f"Generating report... {i}/{len(payloads)}")
        app_api.osint_progresses[osint_id].current_payload = i
        # Add user message
        messages.append({"role": "user", "content": payload})
        # Get AI response
        response = client.chat.completions.create(messages, "Meta-Llama-3-70b-instruct")
        gpt_response = response.choices[0].message.content
        print(gpt_response)
    # Return final AI response
    app_api.osint_progresses[osint_id].complete = True
    print(gpt_response)
    return gpt_response


def check_email_breaches(email: str) -> str:
    """Check whether an email address was breached in any cyber attacks.

    Args:
        email (str): The email address.

    Returns:
        str: A breakdown of known email breaches.
    """
    api = "https://webapi.namescan.io/v1/freechecks/email/breaches"
    payload = {"email": email}
    headers = {"Content-Type": "application/json"}
    response = post(api, headers=headers, data=dumps(payload))
    output = ""
    if response.status_code != 200:
        return ""
    output += "\n\n## Email Breaches\n\n"
    data = response.json()
    breaches = data.get("breaches", [])
    if breaches:
        output += "```\n"
    else:
        output += "No breaches found."
        return output
    filtered_breaches = []
    seen_titles = set()
    for breach in breaches:
        title = breach.get("title", "Unknown")
        if title not in seen_titles:
            seen_titles.add(title)
            filtered_breaches.append(
                {
                    "Title": title,
                    "Date": breach.get("date", "Unknown"),
                    "Description": breach.get("description", "No description available"),
                }
            )
    for breach in filtered_breaches:
        output += f"Title: {breach['Title']}\n"
        output += f"Date: {breach['Date']}\n"
        output += f"Description: {breach['Description']}\n"
    output += "```"
    return output


def instagram_api(username: str) -> str:
    """Get Instagram account details.

    Args:
        username (str): The Instagram username.
    """
    output = "\n\n## Instagram Details\n\n```\n"
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/info"
    querystring = {"username_or_id_or_url": username}
    headers = {
        "x-rapidapi-key": "7cef9caf7emshbcd7d852995df3cp114277jsn623179640e47",
        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com",
    }

    response = get(url, headers=headers, params=querystring)
    data = response.json().get("data", {})

    # Basic Profile Information
    username = data.get("username", "N/A")
    full_name = data.get("full_name", "N/A")
    is_private = data.get("is_private", False)
    is_verified = data.get("is_verified", False)
    follower_count = data.get("follower_count", "N/A")
    following_count = data.get("following_count", "N/A")
    media_count = data.get("media_count", "N/A")
    profile_pic_url = data.get("profile_pic_url", "")
    bio = data.get("biography", "")
    external_url = data.get("external_url", "")

    # Print Profile Summary
    output += f"Username: {username}\n"
    output += f"Full Name: {full_name}\n"
    output += f"Is Private: {'Yes' if is_private else 'No'}\n"
    output += f"Is Verified: {'Yes' if is_verified else 'No'}\n"
    output += f"Follower Count: {follower_count}\n"
    output += f"Following Count: {following_count}\n"
    output += f"Media Count: {media_count}\n"
    output += f"Profile Picture URL: {profile_pic_url}\n"

    # Print Biography and External Link
    output += f"Biography: {bio if bio else '(No Bio)'}\n"
    output += f"External URL: {external_url if external_url else '(No External URL)'}\n"

    # Location Data
    location_data = data.get("location_data", {})
    if location_data:
        city_name = location_data.get("city_name", "N/A")
        zip_code = location_data.get("zip", "N/A")
        latitude = location_data.get("latitude", "N/A")
        longitude = location_data.get("longitude", "N/A")
        output += f"Location Data:\nCity: {city_name}\nZip Code: {zip_code}\nLatitude: {latitude}\nLongitude: {longitude}\n"
    else:
        output += "Location Data: Not Provided\n"
    output += "```"
    return output


def osint(osint_id: int, target_name: str, additional_info: str, find_images: bool, email: str, instagram: str) -> str:
    """Perform an OSINT.

    Args:
        osint_id (int): The ID of the OSINT, used to update progress.
        target_name (str): The name of the person to get information on.
        additional_info (str): Additional background information on the target.
        find_images (bool): Whether to find images of the target. Defaults to False.
        email (str): An email to check for breaches.
        instagram (str): An Instagram account to get details of.
    """
    start_time = time()
    payloads = generate_payload(target_name, additional_info, find_images)
    print("Payloads generated.")
    result = chat(payloads, osint_id)
    if email:
        result += check_email_breaches(email)
    if instagram:
        result += instagram_api(instagram)
    end_time = time()
    time_taken = end_time - start_time
    print("Request completed in " + str(time_taken) + "s")
    app_api.osint_progresses[osint_id].result = result
    return result


def main() -> None:
    """The main function, when this file is run as a script."""
    target_name = input("Name: ")
    additional_info = input("Additional info: ")
    find_images = input("Find images? [y/N]: ") == "y"
    email = input("Email address: ")
    instagram = input("Instagram account: ")
    osint(0, target_name, additional_info, find_images, email, instagram)


if __name__ == "__main__":
    main()
