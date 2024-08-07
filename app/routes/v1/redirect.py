from fastapi import status, HTTPException, APIRouter, Request, Header
from fastapi import Path, Depends
from fastapi.responses import Response
from typing import List
from typing_extensions import Annotated

from models.JiraTicketModel import requestedIssueForm

"""
    lets assume that the JIRA Integration and XSOAR return values
    are more look like this one :


"""

incident_handler = APIRouter(prefix="/app/handler", tags=['Incident Handler'])

@incident_handler.post(path="/jira-ticket", status_code=status.HTTP_200_OK)
async def submit_jira_ticket(request: Request, jiraForm: requestedIssueForm):
    if request.headers.get("X-Oauth2-Authentication"):
        pass
    else:
        return False
    
    return jiraForm


@incident_handler.get("/imtec/{user}")
async def read_heaer(user: Annotated[str, Path(title="Something")]):
    return {"User-Agent": user}

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@incident_handler.get("/item")
async def get_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons