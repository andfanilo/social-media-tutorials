# Streamlit CSS Beauty Pass

![](./render.png)

## CSS Hacking with `<span>`

Put widgets you want to style: 
- inside containers/columns
- preceded by a span hidden element

```python
with st.container():
    st.html(f'<span class="watchlist_symbol_name"></span>')
    st.markdown(f"{symbol_name}")
```

You can then, upon some HTML Inspection, target the element using the `:has` CSS Selector:

```html
<style>
  div[data-testid="stVerticalBlock"]:has(> div > .stHtml > .watchlist_symbol_name) {
    & p {
      color: #174c4f;
      font-family: "Open Sans", sans-serif;
      font-size: 1em;
      font-weight: 700;
      margin-bottom: 0;
    }
  }
</style>
```
