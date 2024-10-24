import time
from itertools import chain

from fasthtml.common import *

from app.views.components.header import header_component
from db import db


def history_view(session, req, res):
    stories = db.t.stories.rows_where(
        "user_id = ? ORDER BY created_at DESC", [session["user_id"]]
    )

    first_story = next(stories, None)
    if first_story is None:
        return (
            Title("Story Sim"),
            header_component(),
            Main(cls="container")(
                H1("No stories yet"),
                P("Generate your first story to see it here!"),
            ), 
        )

    stories = chain([first_story], stories)

    return (
        Title("Story Sim"),
        header_component(),
        Main(cls="container")(
            Grid(style="grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));")(
                *[
                    Article(
                        hx_get=f"/story?id={story['id']}",
                        hx_target="body",
                        hx_swap="outerHTML",
                        hx_push_url="true",
                        cls="story-card",
                        style="height: 200px; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.3s ease, box-shadow 0.3s ease; cursor: pointer;",
                        onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)';",
                        onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='var(--pico-card-box-shadow)';",
                        onclick="if (!event.target.closest('button')) { this.querySelector('a').click(); }"
                    )(
                        A(
                            href=f"/story?id={story['id']}",
                            style="display: none;"
                        )(),
                        P(
                            style="text-decoration: none; flex-grow: 1; overflow: hidden; text-overflow: ellipsis;"
                        )(story["content"][:150] + "..."),
                        Footer(style="text-align: right; margin-top: auto;")(
                            Div(
                                style="display: flex; justify-content: space-between; align-items: center;"
                            )(
                                Button(
                                    "Delete",
                                    hx_delete=f"/delete?id={story['id']}",
                                    hx_confirm="Are you sure you want to delete this story?",
                                    hx_target="closest article",
                                    hx_swap="outerHTML",
                                    hx_indicator=".btn-loader",
                                    hx_push_url="false",
                                    style="padding: 5px 10px; font-size: 0.8em; transition: background-color 0.3s ease;",
                                    cls="contrast",
                                    onmouseover="this.style.backgroundColor='red'; this.style.borderColor='red';",
                                    onmouseout="this.style.backgroundColor=''; this.style.borderColor='';",
                                ),
                                time.strftime(
                                    "%B %d %H:%M",
                                    time.strptime(
                                        story["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
                                    ),
                                ),
                            )
                        ),
                    )
                    for story in stories
                ]
            )
        ),
    )
