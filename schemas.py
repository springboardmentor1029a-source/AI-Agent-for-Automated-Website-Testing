# schemas.py
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class ActionType(str, Enum):
    VISIT = "visit"
    SEARCH = "search"
    LOGIN = "login"
    FILL = "fill"
    CLICK = "click"
    ASSERT_TEXT = "assert_text"
    ASSERT_COUNT = "assert_count"
    CLOSE_POPUP = "close_popup"

class BaseAction(BaseModel):
    type: ActionType

class VisitAction(BaseAction):
    url: str
    type: ActionType = ActionType.VISIT

class SearchAction(BaseAction):
    query: str
    type: ActionType = ActionType.SEARCH

class LoginAction(BaseAction):
    email: str
    password: str
    expect_failure: bool = True
    type: ActionType = ActionType.LOGIN

class FillAction(BaseAction):
    selector: str
    value: str
    type: ActionType = ActionType.FILL

class ClickAction(BaseAction):
    selector: str
    type: ActionType = ActionType.CLICK

class AssertTextAction(BaseAction):
    selector: Optional[str]
    text: str
    negated: bool = False
    type: ActionType = ActionType.ASSERT_TEXT

class AssertCountAction(BaseAction):
    selector: str
    min_count: Optional[int] = None
    max_count: Optional[int] = None
    exact_count: Optional[int] = None
    type: ActionType = ActionType.ASSERT_COUNT

Action = VisitAction | SearchAction | LoginAction | FillAction | ClickAction | AssertTextAction | AssertCountAction

class TestCase(BaseModel):
    name: str
    actions: List[Action]