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

from state import (
    OverallState,
    OutputState,
    Scene,
)

from llm_models import chat_model_small, chat_model


class GenerateSentenceOutput(BaseModel):
    rationale: str
    next_sentence: Scene


def generate_sentence(state: OverallState):
    # print("\n>>> NODE: generate_sentence")

    chain = (
        (
            ChatPromptTemplate.from_template(
                """
You are a novelist writing a story that has the reader as the main character. You can't directly ask the reader about their thoughts, feelings, or preferences. However, you can write a story that has choices so that the reader can reveal themselves through their choices.

I'll give you a previous sentence of the story. You need to write the next sentence ending with a blank for the reader to fill in.

----

Example1.

Previous sentence: It was a rainy day.
Next sentence: (
    rationale="Ok... I need to know how the reader feels in a rainy day.",
    next_sentence=Scene(
        sentence="The sky was grey and the rain poured down like a waterfall. I felt <blank>",
        blank=OpenEndedQuestion(question="How would you feel in a rainy day?", answer="")
    ))


Example2.

Previous sentence: I just woke up from a long nap. I dreamed about my project. 
Next sentence: (
    rationale="I need to know what project the reader is working on.",
    next_sentence=Scene(
        sentence="The project that I've been working on for <blank>",
        blank=OpenEndedQuestion(question="How long have you been working on the project?", answer="")
    ))


Example3.

Previous sentence: I decided that I would stop worrying because nothing changed. I took a deep breath and thought about everything that had been weighing on my mind. I realized that I needed to retreat, and that meant I had to leave my partner. I knew that leaving my partner was the right thing to do, even though it was a difficult decision. 
Next sentence: (
    rationale="The reader has some problems with their partner. I need to know the detail about it.",
    next_sentence=Scene(
        sentence="My partner and I have some problems. I always ask him to do <blank>",
        blank=OpenEndedQuestion(question="What is the problem?", answer="")
    ))

----

Now, it's your turn!

Previous sentence: {story}
Next sentence:"""
            )
        )
        | chat_model.with_structured_output(GenerateSentenceOutput)
    )

    story = " ".join([scene.completed_sentence for scene in state.story])

    response = chain.invoke({"story": story})

    return {
        "story": [response.next_sentence],
    }


g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, "ask_reader")

g.add_node("ask_reader", RunnablePassthrough())
g.add_edge("ask_reader", n(generate_sentence))

g.add_node(generate_sentence)
g.add_edge(n(generate_sentence), "ask_reader")

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["ask_reader"])

with open("./graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
