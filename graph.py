import os
import asyncio
import sqlite3
from varname import nameof as n
from pydantic import BaseModel, Field
from typing import List

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableParallel

from state import OverallState, OutputState, Scene, MultipleChoiceQuestion, OpenEndedQuestion

from llm_models import chat_model_small


def apply_choices(scene: Scene):
    sentence = scene.sentence
    for i, question in enumerate(scene.questions):
        chosen_option = ""
        if isinstance(question, MultipleChoiceQuestion):
            for j, option in enumerate(question.options):
                if option.chosen:
                    chosen_option = option.content
                    break
        elif isinstance(question, OpenEndedQuestion):
            chosen_option = question.answer
        sentence = sentence.replace(f"<blank{i+1}>", chosen_option)
    return sentence


def generate_sentence(state: OverallState):
    print("\n>>> NODE: generate_sentence")

    chain = (
        ChatPromptTemplate.from_template(
            """
Write the next sentence of the story:
{story}
            """
        )
    ) | chat_model_small | StrOutputParser()

    return {
        "story_draft": chain.invoke(apply_choices(state.story[-1])),
    }

def make_choices(state: OverallState):
    print("\n>>> NODE: make_choices")

    chain = (
        (
            ChatPromptTemplate.from_template(
                """
Given the following story draft, create a Scene object with a sentence containing two blanks and two corresponding questions. The first question should be a MultipleChoiceQuestion, and the second should be an OpenEndedQuestion.

Example:
Input: It was a rainy day in the city of London.
Output: Scene(
    sentence="The rain poured down as I walked through the <blank1> streets of <blank2>.",
    questions=[
        MultipleChoiceQuestion(
            question="What type of streets?",
            options=[
                Option(content="busy"),
                Option(content="quiet"),
                Option(content="narrow"),
            ],
        ),
        OpenEndedQuestion(question="What city is the story set in?", answer=""),
    ],
)

Now, create a similar Scene object for the following story draft:
{story_draft}
            """
            )
        )
        | chat_model_small.with_structured_output(Scene)
    )

    scene = chain.invoke({"story_draft": state.story_draft})

    return {
        "story": [scene],
    }

g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, "ask_reader")

g.add_node("ask_reader", RunnablePassthrough())
g.add_edge("ask_reader", n(generate_sentence))

g.add_node(generate_sentence)
g.add_edge(n(generate_sentence), n(make_choices))

g.add_node(make_choices)
g.add_edge(n(make_choices), "ask_reader")

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["ask_reader"])

with open("./graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
