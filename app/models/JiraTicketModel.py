from pydantic import BaseModel
from typing_extensions import Optional, Dict, List, Any

class IssueType(BaseModel):
    issueId: int
    issueCategory: str
    issueTitle: str
    issueStatus: str
    issueAtIP: List = None


class requestedIssueForm(BaseModel):
    issues: List[IssueType]


class IssuesResponse(BaseModel):
    status_code: int
    message: str