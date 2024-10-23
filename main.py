import uvicorn
import os
import uuid
from uvicorn.config import Config
from fasthtml.common import *
from db import db
from css import main_css


def user_auth_before(req, session):
    if "session_id" not in session:
        print("initializing session")
        session["session_id"] = str(uuid.uuid4())
    auth = req.scope["auth"] = session.get("user_id", None)
    user = next(db.t.users.rows_where("id = ?", [auth]), None)
    if not auth or not user:
        print("\n>>> No auth, redirecting to login")
        return RedirectResponse("/login", status_code=303)

beforeware = Beforeware(
    user_auth_before,
    skip=[
        r"/favicon\.ico",
        r"/static/.*",
        r".*\.css",
        r".*\.js",
        "/login",
        "/auth_redirect",
    ],
)

app, _ = fast_app(
    live=True,
    hdrs=(
        picolink,
        Link(
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
            type="text/css",
        ),
        MarkdownJS(),
        Script(
            src="https://unpkg.com/htmx-ext-response-targets@2.0.0/response-targets.js"
        ),
        Style(main_css),
    ),
    exception_handlers={
        404: lambda req, exc: Main(
            Titled("Page not found"),
            P("The page you are looking for does not exist."),
            cls="container",
        ),
    },
    before=beforeware,
)

setup_toasts(app)


from app.views import home as home_views
from app.views import auth as auth_views

from app.controllers import init as init_controller
from app.controllers import auth as auth_controller
from app.views import profile as profile_views
from app.views import history as history_views
from app.controllers import profile as profile_controller
from app.views import story as story_views
from app.controllers import story as story_controller           

# Managements
app.get("/")(home_views.home_view)
app.get("/login")(auth_views.login_view)
app.get("/profile")(profile_views.profile_view)
app.get("/history")(history_views.history_view)

app.get("/auth_redirect")(auth_controller.auth_redirect)
app.get("/logout")(auth_controller.logout)
app.post("/update_profile")(profile_controller.update_profile)

# Simulation
app.get("/story")(story_views.story_view)

app.post("/init")(init_controller.initialize_story)
app.post("/generate")(story_controller.generate_story)
app.delete("/delete")(story_controller.delete_story)

running_on_server = os.environ.get("RAILWAY_ENVIRONMENT_NAME") == "production"
serve(
    reload=not running_on_server,
    reload_excludes=["data/**"],
)
