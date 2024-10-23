import os
import json
from fasthtml.common import *

os.makedirs("./data/main_database", exist_ok=True)
db_path = os.path.join(".", "data", "main_database", "main.db")

print(f">>>> DB: initialize database at {db_path}")
db = database(db_path)

users, stories, counts = (db.t.users, db.t.stories, db.t.counts)

if users not in db.t:
    print("\n>>>> DB: Creating users table")
    users.create(
        id=str,
        name=str,
        email=str,
        profile=str,
        pk="id",
    )

if stories not in db.t:
    print("\n>>>> DB: Creating stories table")
    stories.create(
        id=str,
        user_id=str,
        content=str,
        created_at=str,
        pk="id",
        foreign_keys=(("user_id", "users")),
        if_not_exists=True,
    )


Users = users.dataclass()
Stories = stories.dataclass()

# try:
#     main_db_diagram = diagram(db.tables)
#     main_db_diagram.render(
#         "data/main_database/main_db_diagram", format="png", cleanup=True
#     )
# except:
#     print(
#         "Error on generating DB visualization. Probably graphviz executables were not found. Please install Graphviz and add it to your system's PATH."
#     )
