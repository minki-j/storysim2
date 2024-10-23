from fasthtml.common import *

from db import db

from app.views.components.header import header_component


def story_view(session, req, res, id: str):
    story = db.t.stories.get(id)
    print("story.content: ", story.content)

    return (
        Title("Story Sim"),
        header_component(),
        Main(
            cls="container",
            style="height: calc(100vh - 100px);",
        )(
            Form(
                id="story-form",
                hx_post=f"/generate?id={id}",
                hx_target="#story",
                hx_swap="none",
                hx_push_url="false",
                style="display: flex; flex-direction: column; gap: 10px; height: 100%;",
            )(
                Div(style="flex-grow: 1;")(
                    Textarea(
                        id="story",
                        name="story",
                        placeholder="Write the first sentence of your story...",
                        style="height: 100%;",
                    )(story.content),
                ),
                Button(type="submit", cls="btn-loader btn-submit")(
                    "Cmd(⌘) + Enter"
                ),
                Script(
                    """
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('htmx:afterRequest', function(event) {
        if (event.detail.pathInfo.requestPath.startsWith('/generate')) {
            document.getElementById('story').value = event.detail.xhr.responseText;
        }
    });

    document.getElementById('story').addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) {
            event.preventDefault();
            htmx.trigger('#story-form', 'submit');
        }
    });
});
"""
                ),
            )
        ),
    )
