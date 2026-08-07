import streamlit as st
from barfi.flow import Block
from barfi.flow import ComputeEngine
from barfi.flow.streamlit import st_flow

st.title("Barfi flow demo")

number_block = Block(name="Number")
number_block.add_output(name="Output 1")
number_block.add_option(name="number-block-option", type="number")


def number_block_func(self):
    number_value = self.get_option(name="number-block-option")
    self.set_interface(name="Output 1", value=number_value)


number_block.add_compute(number_block_func)

sum_block = Block(name="Sum")
sum_block.add_input(name="Input 1")
sum_block.add_input(name="Input 2")
sum_block.add_output(name="Output 1")


def sum_block_func(self):
    a = self.get_interface(name="Input 1") or 0
    b = self.get_interface(name="Input 2") or 0
    col_inputs.write(f"Input 1: {a}")
    col_inputs.write(f"Input 2: {b}")
    self.set_interface(name="Output 1", value=a + b)


sum_block.add_compute(sum_block_func)


def render_result_card(value):
    display_value = "(no result)" if value is None else value
    col_card.html(f"""
        <div style="
            border: 1px solid rgba(128, 128, 128, 0.3);
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            max-width: 200px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        ">
            <div style="font-size: 0.75rem; opacity: 0.65; margin-bottom: 0.15rem;">Result</div>
            <div style="font-size: 1.5rem; font-weight: 700; line-height: 1;">{display_value}</div>
        </div>
    """)


result_block = Block(name="Result")
result_block.add_input(name="Input 1")


def result_block_func(self):
    number_value = self.get_interface(name="Input 1")
    st.session_state["result_computed"] = True
    render_result_card(number_value)


result_block.add_compute(result_block_func)

base_blocks = [number_block, sum_block, result_block]
barfi_result = st_flow(base_blocks)

st.session_state["result_computed"] = False
col_card, col_inputs = st.columns(2)

if barfi_result.editor_schema:
    compute_engine = ComputeEngine(base_blocks)
    compute_engine.execute(barfi_result.editor_schema)

if not st.session_state["result_computed"]:
    render_result_card(None)
