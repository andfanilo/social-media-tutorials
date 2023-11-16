# OpenAI Function Calling in Streamlit

Install dependencies:

```sh
pip install openai streamlit
```

Before running, create a `.streamlit/secrets.toml` file with the following entries next to the script:

```toml
OPENAI_API_KEY="sk-xxx"
OPENAI_ASSISTANT_ID="asst_xxx"
MAPBOX_TOKEN="pk.xxx"
```

To run:

```sh
streamlit run streamlit_app.py
```
