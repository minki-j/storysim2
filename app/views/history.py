from fasthtml.common import *

from app.views.components.header import header_component

def history_view(session, req, res):
    return (
        Title("Story Sim"),
        header_component(),
        Main(
            cls="container", style=""
        )(),
    )
