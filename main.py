"""FastAPI for OSINT and Webcheck."""

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from osint import osint

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


osint_progresses: list[OsintProgress] = []


@app.post("/osint/submit")
async def osint_submit(details: OsintDetails, background_tasks: BackgroundTasks) -> int:
    """Start an OSINT task in the background."""
    id = len(osint_progresses)
    background_tasks.add_task(
        osint, id, details.target_name, details.additional_info, details.find_images, details.email, details.instagram
    )
    osint_progresses.append(OsintProgress(started=False, complete=False, current_payload=0, total_payloads=0))
    return id


@app.get("/osint/status/{task_id}")
def osint_status(task_id: int) -> OsintProgress:
    """Get the status of the OSINT for a given task."""
    return osint_progresses[task_id]
