import uuid
from typing import Annotated, List
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

# ===========================================
#                VARIABLE SCHEMA
# ===========================================
class Option(BaseModel):
    chosen: bool = False
    content: str = Field(default="")


class MultipleChoiceQuestion(BaseModel):
    question: str = Field(default="")
    options: List[Option]


class OpenEndedQuestion(BaseModel):
    question: str = Field(default="")
    answer: str = Field(default="")


class Scene(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sentence: str
    questions: List[MultipleChoiceQuestion | OpenEndedQuestion]


# ===========================================
#                REDUCER FUNCTIONS
# ===========================================
def update_story(original: List[Scene], new: List[Scene]):

    if len(original) == 0:
        return new

    for scene in new:
        found = False
        for original_scene in original:
            if scene.id == original_scene.id:
                original_scene.sentence = scene.sentence
                original_scene.questions = scene.questions
                found = True
                break
        if not found:
            original.append(scene)

    return original


# ===========================================
#                    STATE
# ===========================================
class OutputState(BaseModel):
    title: str = Field(default="")
    story: Annotated[List[Scene], update_story] = Field(default_factory=lambda: [])


class OverallState(OutputState):
    story_draft: str = Field(default="")
    messages: Annotated[list[AnyMessage], add_messages]
