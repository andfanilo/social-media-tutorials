# OpenAI Function Calling in Streamlit

JSON Functions to add to Assistant API:

- update_map

```json
{
  "name": "update_map",
  "description": "Update map to center on a particular location",
  "parameters": {
    "type": "object",
    "properties": {
      "longitude": {
        "type": "number",
        "description": "Longitude of the location to center the map on"
      },
      "latitude": {
        "type": "number",
        "description": "Latitude of the location to center the map on"
      },
      "zoom": {
        "type": "integer",
        "description": "Zoom level of the map"
      }
    },
    "required": ["longitude", "latitude", "zoom"]
  }
}
```

- add_markers

```json
{
  "name": "add_markers",
  "description": "Add list of markers to the map",
  "parameters": {
    "type": "object",
    "properties": {
      "longitudes": {
        "type": "array",
        "items": {
          "type": "number"
        },
        "description": "List of longitude of the location to each marker"
      },
      "latitudes": {
        "type": "array",
        "items": {
          "type": "number"
        },
        "description": "List of latitude of the location to each marker"
      },
      "labels": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of text to display on the location of each marker"
      }
    },
    "required": ["longitudes", "latitudes", "labels"]
  }
}
```

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
