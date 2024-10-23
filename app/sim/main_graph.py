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

import app.sim.prompts as prompts
from app.sim.state import OverallState
from app.sim.llm_models import chat_model_small, chat_model


def generate_sentence(state: OverallState):
    print("\n>>> NODE: generate_sentence")

    chain = (
        (ChatPromptTemplate.from_template(prompts.SENTENCE_GEN))
        | chat_model
        | StrOutputParser()
    )

    next_sentence = chain.invoke({"story": state.story})

    return {
        "story": state.story.strip() + " " + next_sentence.strip(),
    }


g = StateGraph(OverallState)
g.add_edge(START, n(generate_sentence))

g.add_node(generate_sentence)
g.add_edge(n(generate_sentence), "ask_reader")

g.add_node("ask_reader", RunnablePassthrough())
g.add_edge("ask_reader", n(generate_sentence))

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["ask_reader"])

with open("./app/sim/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
