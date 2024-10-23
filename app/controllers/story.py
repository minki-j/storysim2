from fasthtml.common import *

from db import db

from app.sim.main_graph import main_graph


async def generate_story(session, req, res, id: str):
    print(">>> CONTROLLER: generate_story")

    form_data = await req.form()

    config = {"configurable": {"thread_id": id}, "recursion_limit": 100}
    main_graph.update_state(
        config,
        {
            "story": form_data["story"],
        },
    )
    output = main_graph.invoke(None, config)
    updated_story = output["story"]

    db.t.stories.update(
        pk_values=id,
        updates={"content": updated_story},
    )

    return updated_story



async def delete_story(session, req, res, id: str):
    print(">>> CONTROLLER: delete_story")

    db.t.stories.delete(id)

    return None