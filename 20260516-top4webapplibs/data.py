"""Shared Superstore data loader for the streamlit, marimo, nicegui and reflex apps."""

from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
SUPERSTORE_CSV = DATA_DIR / "Superstore_2024.csv"


@lru_cache(maxsize=1)
def load_superstore() -> pd.DataFrame:
    return pd.read_csv(
        SUPERSTORE_CSV,
        parse_dates=["Order Date", "Ship Date"],
        date_format="%m/%d/%Y",
    )


def load_categories() -> list[str]:
    return sorted(load_superstore()["Category"].unique())


def sales_by_subcategory(category: str) -> pd.DataFrame:
    df = load_superstore()
    return (
        df[df["Category"] == category]
        .groupby("Sub-Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
