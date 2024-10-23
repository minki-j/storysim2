import uuid
from typing import Annotated, List
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

# ===========================================
#                VARIABLE SCHEMA
# ===========================================

# ===========================================
#                REDUCER FUNCTIONS
# ===========================================

# ===========================================
#                    STATE
# ===========================================


class OverallState(BaseModel):
    story: str = Field(default="")
