"""Use an ML model to detect if a website's domain and HTML is suspicious."""

from string import printable
from typing import Union

from label_sleuth.models.util.standalone_inference import get_model_api
from requests import get as requests_get

CHARS_PER_SITE = 10000

model_path = "model"
model_api = get_model_api(model_path)
category_id_to_info = model_api.get_metadata(model_path)["category_id_to_info"]
model = model_api.load_model(model_path)


def webcheck(url: str) -> Union[tuple[bool, float], None]:
    """Perform a webcheck on the URL.

    Args:
        url (str): The URL to check.

    Returns:
        Union[tuple(bool, float), None]: The suspiciousness label and score, or None if it fails.
    """
    try:
        result = requests_get(url, timeout=10)
    except Exception:
        return None
    if len(result.text) > CHARS_PER_SITE:
        html = result.text[:CHARS_PER_SITE]
    else:
        html = result.text
    html = "".join(filter(lambda x: x in printable, html))
    html = html.replace("\n", " ").replace("\r", " ")
    items_to_infer = [{"text": url + " " + html}]
    predictions = model_api.infer(model, items_to_infer)
    pred = predictions[0]
    return (pred.label, pred.score)
