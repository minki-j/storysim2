import json

from fasthtml.common import *

from db import db
from app.views.components.header import header_component


def profile_view(session, req, res):
    print("\n>>> VIEW: profile_view")
    user_id = session["user_id"]
    user_data = db.t.users.get(user_id)

    return (
        Title("Story Sim"),
        header_component(),
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            Div(id="profile-form")(
                P(user_data.profile),
                P("User id: ", session["user_id"]),
            ),
        ),
    )
