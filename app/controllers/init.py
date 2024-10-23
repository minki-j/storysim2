import json
import uuid
from datetime import datetime
from pprint import pprint
from fasthtml.common import *
from app.views.components.error_responses import error_modal

from app.sim.main_graph import main_graph

from db import db, Users, Stories


async def initialize_story(session, request: Request):
    print("\n>>> CNTRL initialize_story")

    story_id = str(uuid.uuid4())

    form_data = await request.form()
    print("first sentence: ", form_data["story"])

    print("\n>>> Invoke main_graph")
    response = main_graph.invoke(
        input={
            "story": form_data["story"],
        },
        config={"configurable": {"thread_id": story_id}, "recursion_limit": 100},
    )

    if response:
        db.t.stories.insert(
            id=story_id,
            user_id=session["user_id"],
            content=response["story"],
            created_at=datetime.now().isoformat(),
        )
        print(f"\n>>> Story inserted with id: {story_id}")

        return RedirectResponse(url=f"/story?id={story_id}", status_code=303)
    else:
        return error_modal("An error happened at generate_plot")
