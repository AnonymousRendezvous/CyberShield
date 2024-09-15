"""FastAPI for OSINT and Webcheck."""

from urllib.parse import unquote

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from osint import osint
from webcheck import webcheck

app = FastAPI()


class OsintDetails(BaseModel):
    """Details of an OSINT task."""

    target_name: str
    additional_info: str
    find_images: bool = False
    email: str
    instagram: str


class OsintProgress(BaseModel):
    """Progress of an ongoing OSINT task."""

    started: bool
    complete: bool
    current_payload: int
    total_payloads: int
    result: str


class WebcheckResult(BaseModel):
    """Results of webcheck."""

    label: bool
    score: float


osint_progresses: list[OsintProgress] = []


@app.post("/osint/submit")
async def osint_submit(details: OsintDetails, background_tasks: BackgroundTasks) -> int:
    """Start an OSINT task in the background."""
    id = len(osint_progresses)
    background_tasks.add_task(
        osint, id, details.target_name, details.additional_info, details.find_images, details.email, details.instagram
    )
    osint_progresses.append(OsintProgress(started=False, complete=False, current_payload=0, total_payloads=0, result=""))
    return id


@app.get("/osint/status/{task_id}")
def osint_status(task_id: int) -> OsintProgress:
    """Get the status of the OSINT for a given task."""
    return osint_progresses[task_id]


@app.get("/webcheck")
def perform_webcheck(url: str) -> WebcheckResult:
    """Perform a webcheck on the URL."""
    url = unquote(url)
    if url[0:4] != "http":
        url = "http://" + url
    result = webcheck(url)
    return WebcheckResult(label=result[0], score=result[1])
