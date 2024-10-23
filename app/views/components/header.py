from fasthtml.common import *


def header_component():
    return (
        Header(
            cls="container",
            style="display: flex; justify-content: space-between; align-items: center;",
        )(
            A(href="/", style="text-decoration: none;")(
                H1(
                    "Story Sim",
                    style="font-weight: 900; font-size: 2.8rem; color: #4A4A4A; margin: 0; text-transform: uppercase; letter-spacing: 1px;",
                )
            ),
            Div(cls="profile-section")(
                Details(cls="dropdown", style="margin: 0;")(
                    Summary("Menu"),
                    Ul(
                        Li(A(href="/profile")("Profile")),
                        Li(A(href=f"/history")("History")),
                        Li(A(href="/logout")("Logout")),
                    ),
                )
            ),
        ),
    )
