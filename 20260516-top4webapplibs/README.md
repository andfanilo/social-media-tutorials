---
title: Readme
marimo-version: 0.23.6
---

# python-ui-inputs

Four Python UI frameworks (Streamlit, Marimo, NiceGUI, Reflex) sharing a single data loader (`data.py`) backed by the Superstore CSV in `./data`.

## Setup

```sh
uv sync
```

## Run

### Streamlit

```sh
uv run streamlit run streamlit_app.py
```

### Marimo

```sh
uv run marimo edit marimo_app.py        # editable notebook
uv run marimo run marimo_app.py         # read-only app
```

### NiceGUI

```sh
uv run python nicegui_app.py
```

### Reflex

```sh
uv run reflex run
```

## What happens when you click the dropdown?

Each framework has a fundamentally different reactivity model. Here's the path from "user picks Furniture" to "bars redraw" — in each one.

### Streamlit — full re-run

> **Model:** the script *is* the UI. Every interaction reruns it from line 1.

1. Browser sends the new value to the Streamlit server.
2. Streamlit **reruns `streamlit_app.py` top-to-bottom**.
3. `st.selectbox(...)` returns `"Furniture"` this time (instead of `"Office Supplies"`).
4. `sales_by_subcategory("Furniture")` builds a new DataFrame (`load_superstore()` is cached, so the CSV is *not* re-read).
5. `st.bar_chart(...)` ships the new data to the browser; Streamlit diffs the DOM.

No callbacks, no state class — *re-execution is the reactivity*.

### Marimo — reactive dependency graph

> **Model:** each cell is a node in a DAG. Only downstream cells re-run.

1. Browser sends the new value over a WebSocket to the marimo kernel.
2. `category.value` becomes `"Furniture"`.
3. Marimo's dependency graph identifies every cell that **references `category`** — here, just the chart cell.
4. Only that cell re-runs:
   ```python
   alt.Chart(sales_by_subcategory(category.value)).mark_bar()...
   ```
5. The new Vega-Lite spec streams to the browser; Altair redraws.

The dropdown cell does **not** re-run. The setup cell does **not** re-run. Just the affected node.

### NiceGUI — explicit callback, mutate in place

> **Model:** components live on the server. You mutate them; NiceGUI syncs.

1. Browser sends the new value over a WebSocket.
2. `on_change(e)` fires with `e.value == "Furniture"`.
3. Inside the handler:
   ```python
   chart.options.clear()
   chart.options.update(chart_options(e.value))
   chart.update()
   ```
4. `chart.update()` serializes the new ECharts options dict and pushes it over the WebSocket.
5. Browser-side ECharts applies the new options and animates between states.

Nothing re-runs. You are imperatively poking the component.

### Reflex — server-side state, computed vars, React diffs

> **Model:** state lives on the server. Components are React on the client. The two are wired by event handlers and computed vars.

1. User picks "Furniture" in the React `<Select>`.
2. Reflex's client sends an event over the WebSocket: `State.set_category("Furniture")`.
3. The `@rx.event` handler runs on the server:
   ```python
   def set_category(self, value: str):
       self.category = value
   ```
4. Reflex detects that `chart_data` (an `@rx.var`) depends on `self.category` and **recomputes** it:
   ```python
   return sales_by_subcategory(self.category).to_dict("records")
   ```
5. The new value of `chart_data` is sent to the client; React re-renders `rx.recharts.bar_chart` with the new `data` prop.

The only thing that recomputes is the `@rx.var`. The component tree is rebuilt by React on the diff, like any React app.

### One-line summary

| Framework | When you change the dropdown… |
|---|---|
| **Streamlit** | the whole script reruns. |
| **Marimo** | only the cells that depend on the dropdown rerun. |
| **NiceGUI** | a callback fires; you mutate the chart object. |
| **Reflex** | an event mutates server State; computed vars recompute; React re-renders. |