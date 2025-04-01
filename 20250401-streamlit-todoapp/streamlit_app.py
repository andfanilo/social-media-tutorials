from dataclasses import dataclass
from datetime import date
from typing import Dict
from typing import Optional

import sqlalchemy as sa
import streamlit as st
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from streamlit.connections import SQLConnection

st.set_page_config(
    page_title="Streamlit Todo App",
    page_icon="📃",
    initial_sidebar_state="collapsed",
)

##################################################
### MODELS
##################################################

TABLE_NAME = "todo"
SESSION_STATE_KEY_TODOS = "todos_data"


@dataclass
class Todo:
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    created_at: Optional[date] = None
    due_at: Optional[date] = None
    done: bool = False

    # Class method to easily create a Todo object from a database row
    @classmethod
    def from_row(cls, row):
        if row:
            return cls(**row._mapping)
        return None


# Use st.cache_resource to define the database table structure only once
# and share it across all user sessions connected to this Streamlit server process.
# This avoids redefining the table structure on every script rerun or for every user.
@st.cache_resource
def connect_table():
    metadata_obj = MetaData()
    todo_table = Table(
        TABLE_NAME,
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("title", String(30)),
        Column("description", String, nullable=True),
        Column("created_at", Date),
        Column("due_at", Date, nullable=True),
        Column("done", Boolean, nullable=True),
    )
    return metadata_obj, todo_table


##################################################
### DATA INTERACTION
##################################################


def check_table_exists(connection: SQLConnection, table_name: str) -> bool:
    inspector = sa.inspect(connection.engine)
    return inspector.has_table(table_name)


def load_all_todos(connection: SQLConnection, table: Table) -> Dict[int, Todo]:
    """Fetches all todos from the DB and returns as a dict keyed by id."""
    stmt = sa.select(table).order_by(table.c.id)
    with connection.session as session:
        result = session.execute(stmt)
        todos = [Todo.from_row(row) for row in result.all()]
        return {todo.id: todo for todo in todos if todo}


def load_todo(connection: SQLConnection, table: Table, todo_id: int) -> Optional[Todo]:
    """Fetches a single todo by id from the DB."""
    stmt = sa.select(table).where(table.c.id == todo_id)
    with connection.session as session:
        result = session.execute(stmt)
        row = result.first()
        return Todo.from_row(row)


##################################################
### STREAMLIT CALLBACKS
##################################################

# These functions handle the logic when a user interacts with a widget (button, form).
# The usual workflow for those callbacks is:
# 1. Get form input data through st.session_state form widget keys,
# 2. Perform database operations,
# 3. Refresh session state by reading from database.


def create_todo_callback(connection: SQLConnection, table: Table):
    # 1. Get form input data
    if not st.session_state.new_todo_form__title:
        st.toast("Title empty, not adding todo")
        return

    new_todo_data = {
        "title": st.session_state.new_todo_form__title,
        "description": st.session_state.new_todo_form__description,
        "created_at": date.today(),
        "due_at": st.session_state.new_todo_form__due_date,
        "done": False,
    }

    # 2. Perform database operations
    stmt = table.insert().values(**new_todo_data)
    with connection.session as session:
        # probably needs a try...except but eh
        session.execute(stmt)
        session.commit()

    # 3. Refresh session state from database
    st.session_state[SESSION_STATE_KEY_TODOS] = load_all_todos(conn, todo_table)


def open_update_callback(todo_id: int):
    st.session_state[f"currently_editing__{todo_id}"] = True


def cancel_update_callback(todo_id: int):
    st.session_state[f"currently_editing__{todo_id}"] = False


def update_todo_callback(connection: SQLConnection, table: Table, todo_id: int):
    # 1. Get form input data
    updated_values = {
        "title": st.session_state[f"edit_todo_form_{todo_id}__title"],
        "description": st.session_state[f"edit_todo_form_{todo_id}__description"],
        "due_at": st.session_state[f"edit_todo_form_{todo_id}__due_date"],
    }

    if not updated_values["title"]:
        st.toast("Title cannot be empty.", icon="⚠️")
        st.session_state[f"currently_editing__{todo_id}"] = True
        return

    # 2. Perform database operations
    stmt = table.update().where(table.c.id == todo_id).values(**updated_values)
    with connection.session as session:
        session.execute(stmt)
        session.commit()

    # 3. Refresh session state from database
    st.session_state[SESSION_STATE_KEY_TODOS][todo_id] = load_todo(
        connection, table, todo_id
    )
    st.session_state[f"currently_editing__{todo_id}"] = False


def delete_todo_callback(connection: SQLConnection, table: Table, todo_id: int):
    # 1. Get form input data

    # 2. Perform database operations
    stmt = table.delete().where(table.c.id == todo_id)
    with connection.session as session:
        session.execute(stmt)
        session.commit()

    # 3. Refresh session state from database
    st.session_state[SESSION_STATE_KEY_TODOS] = load_all_todos(conn, todo_table)
    st.session_state[f"currently_editing__{todo_id}"] = False


def mark_done_callback(connection: SQLConnection, table: Table, todo_id: int):
    # 1. Get form input data
    current_done_status = st.session_state[SESSION_STATE_KEY_TODOS][todo_id].done

    # 2. Perform database operations
    stmt = (
        table.update().where(table.c.id == todo_id).values(done=not current_done_status)
    )
    with connection.session as session:
        session.execute(stmt)
        session.commit()

    # 3. Refresh session state from database
    st.session_state[SESSION_STATE_KEY_TODOS][todo_id] = load_todo(
        connection, table, todo_id
    )


##################################################
### UI WIDGETS
##################################################

# These functions render parts of the UI.
# They take data like a Todo object and display it using Streamlit widgets.


# Function to display a single todo item as a card
def todo_card(connection: SQLConnection, table: Table, todo_item: Todo):
    todo_id = todo_item.id

    with st.container(border=True):
        display_title = todo_item.title
        display_description = todo_item.description or ":grey[*No description*]"
        display_due_date = f":grey[Due {todo_item.due_at.strftime('%Y-%m-%d')}]"

        if todo_item.done:
            strikethrough = "~~"
            display_title = f"{strikethrough}{display_title}{strikethrough}"
            display_description = f"{strikethrough}{display_description}{strikethrough}"
            display_due_date = f"{strikethrough}{display_due_date}{strikethrough}"

        st.subheader(display_title)
        st.markdown(display_description)
        st.markdown(display_due_date)

        done_col, edit_col, delete_col = st.columns(3)
        done_col.button(
            "Done" if not todo_item.done else "Redo",
            icon=":material/check_circle:",
            key=f"display_todo_{todo_id}__done",
            on_click=mark_done_callback,
            args=(conn, todo_table, todo_id),
            type="secondary" if todo_item.done else "primary",
            use_container_width=True,
        )
        edit_col.button(
            "Edit",
            icon=":material/edit:",
            key=f"display_todo_{todo_id}__edit",
            on_click=open_update_callback,
            args=(todo_id,),
            disabled=todo_item.done,
            use_container_width=True,
        )
        if delete_col.button(
            "Delete",
            icon=":material/delete:",
            key=f"display_todo_{todo_id}__delete",
            use_container_width=True,
        ):
            delete_todo_callback(connection, table, todo_id)
            st.rerun(scope="app")


# Function to display the inline form for editing an existing todo item
def todo_edit_widget(connection: SQLConnection, table: Table, todo_item: Todo):
    todo_id = todo_item.id

    with st.form(f"edit_todo_form_{todo_id}"):
        st.text_input(
            "Title", value=todo_item.title, key=f"edit_todo_form_{todo_id}__title"
        )
        st.text_area(
            "Description",
            value=todo_item.description,
            key=f"edit_todo_form_{todo_id}__description",
        )

        st.date_input(
            "Due date",
            value=todo_item.due_at,
            key=f"edit_todo_form_{todo_id}__due_date",
        )

        submit_col, cancel_col = st.columns(2)
        submit_col.form_submit_button(
            "Save",
            icon=":material/save:",
            type="primary",
            on_click=update_todo_callback,
            args=(connection, table, todo_id),
            use_container_width=True,
        )

        cancel_col.form_submit_button(
            "Cancel",
            on_click=cancel_update_callback,
            args=(todo_id,),
            use_container_width=True,
        )


# If a script rerun by widget interaction is triggered from a @st.fragment function
# Instead of a script rerun, Streamlit only reruns the fragment function

# Any widget interaction and callback that occurs within this function
# only affects the database state and session state of the input todo item
# so the fragment reruns to reload and display the state of the todo item


@st.fragment
def todo_component(connection: SQLConnection, table: Table, todo_id: int):
    # Load todo item fields from session state
    # Syncing from database to session state was done in callback
    todo_item = st.session_state[SESSION_STATE_KEY_TODOS][todo_id]

    currently_editing = st.session_state.get(f"currently_editing__{todo_id}", False)

    if not currently_editing:
        todo_card(connection, table, todo_item)

    else:
        todo_edit_widget(connection, table, todo_item)


##################################################
### USER INTERFACE
##################################################

st.title("Streamlit Todo App")

conn = st.connection("todo_db", ttl=5 * 60)
metadata_obj, todo_table = connect_table()

# --- Sidebar for Admin Actions ---
with st.sidebar:
    st.header("Admin")
    if st.button(
        "Create table",
        type="secondary",
        help="Creates the 'todo' table if it doesn't exist.",
    ):
        metadata_obj.create_all(conn.engine)
        st.toast("Todo table created successfully!", icon="✅")

    st.divider()
    st.subheader("Session State Debug", help="Is not updated by fragment rerun!")
    st.json(st.session_state)

# --- Display list of Todo items ---

# 1. Check if database table exists. Else redirect to admin sidebar for creation
if not check_table_exists(conn, TABLE_NAME):
    st.warning("Create table from admin sidebar", icon="⚠")
    st.stop()

# 2. Load database items into session state.
#    This happens on the first run or if the state was cleared.
if SESSION_STATE_KEY_TODOS not in st.session_state:
    with st.spinner("Loading Todos..."):
        st.session_state[SESSION_STATE_KEY_TODOS] = load_all_todos(conn, todo_table)


# 3. Display Todos from Session State
current_todos: Dict[int, Todo] = st.session_state.get(SESSION_STATE_KEY_TODOS, {})
for todo_id in current_todos.keys():
    # Initialize editing state for todo item
    if f"currently_editing__{todo_id}" not in st.session_state:
        st.session_state[f"currently_editing__{todo_id}"] = False
    todo_component(conn, todo_table, todo_id)

# --- Display create Todo form ---

with st.form("new_todo_form", clear_on_submit=True):
    st.subheader(":material/add_circle: New todo")
    st.text_input("Title", key="new_todo_form__title", placeholder="Add your task")
    st.text_area(
        "Description",
        key="new_todo_form__description",
        placeholder="Add more details...",
    )

    date_col, submit_col = st.columns((1, 2), vertical_alignment="bottom")
    date_col.date_input("Due date", key="new_todo_form__due_date")
    submit_col.form_submit_button(
        "Add todo",
        on_click=create_todo_callback,
        args=(conn, todo_table),
        type="primary",
        use_container_width=True,
    )
