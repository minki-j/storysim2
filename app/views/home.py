from fasthtml.common import *

from app.views.components.header import header_component


def home_view(session, req, res):
    return (
        Title("Story Sim"),
        header_component(),
        Main(cls="container", style="")(
            Form(
                hx_post="/init",
                hx_target="body",
                hx_swap="outerHTML",
                hx_push_url="true",
                hx_indicator=".btn-loader",
            )(
                Textarea(
                    id="story",
                    name="story",
                    placeholder="Write the first sentence of your story...",
                )(),
                Button(type="submit", cls="btn-loader btn-submit btn-loader")(
                    "Cmd(⌘) + Enter"
                ),
            )
        ),
    )
