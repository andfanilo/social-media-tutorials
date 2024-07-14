"""
File-system based router inspired from Next.js, where folders are used to define routes.
Each folder with a page.py maps to a URL segment.
The title for the page in the navigation menu is the argument of the first `st.title` call.


Example Directory Structure: 

 ├── app
 │   ├── page.py             <- @/
 │   ├── admin               
 │   |   └── page.py         <- @/admin
 │   └── dashboard           
 │       ├── page.py         <- @/dashboard
 │       └── settings
 │           └── page.py     <- @/dashboard/settings
 |
 └── streamlit_app.py        <- Router


Inspiration: https://nextjs.org/docs/app/building-your-application/routing/defining-routes
"""
import ast
from pathlib import Path
from typing import List

import streamlit as st


def find_all_pages() -> List[Path]:
    """Finds all files named `page.py` in the `app` directory."""
    app_path = Path("./app")
    return list(app_path.rglob("page.py"))


@st.cache_data
def extract_page_uri(path_str: Path):
    """Extracts the URI from a file path for Streamlit multipage."""
    parts = path_str.parts

    # first part is app, last part is page.py
    uri = "/".join(parts[1:-1])
    return uri


@st.cache_data
def find_first_st_title_call(file_path: Path):
    """Finds the first `st.title` call in a Python file using ast."""
    with open(file_path, "r") as f:
        source_code = f.read()
        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if (
                        node.func.attr == "title"
                        and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "st"
                    ):
                        return node.args[0].s  # Extract the title string

        return "Page"  # No st.title call found, put default title


all_page_files = find_all_pages()
all_pages = [
    st.Page(
        page,
        title=find_first_st_title_call(page),
        url_path=extract_page_uri(page),
        default=(extract_page_uri(page) == ""),
    )
    for page in all_page_files
]

pg = st.navigation(all_pages)
pg.run()
