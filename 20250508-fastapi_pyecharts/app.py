"""
Run with `fastapi dev`
Head to <http://localhost:8000/public>
"""
import random

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from pyecharts.charts import Pie
from pyecharts.options import PieItem

app = FastAPI()
app.mount("/public", StaticFiles(directory="static", html=True), name="static")

data = {
    category: {
        "online": random.randint(1000, 5000), 
        "offline": random.randint(1000, 5000)
    }
    for category in ["Shirts", "Cardigans", "Chiffons", "Pants", "Heels", "Socks"]
}

@app.get("/data/{name}")
def get_data_by_name(name: str):
    if name not in data:
        raise HTTPException(status_code=404, detail="Category not found")
    pie = Pie()
    pie.set_global_opts(title_opts={"text": f"{name} Sales Distribution"})
    pie_items = [PieItem(k, v) for k,v in data[name].items()]
    pie.add("Revenue", pie_items)
    return pie.dump_options()