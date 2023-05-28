import streamlit as st
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide")
st.title("Bi Dashboard")

options_pie = {
  "title": {
    "text": 'Referer of a Website',
  },
  "tooltip": {
    "trigger": 'item'
  },
  "legend": {
    "orient": 'horizontal',
    "bottom": 'bottom',
    "selected": {
        "Search Engine": True,
        "Direct": True,
        "Email": True,
        "Union Ads": True,
        "Video Ads": True,
    },
  },
  "series": [
    {
      "name": 'Access From',
      "type": 'pie',
      "radius": '50%',
      "data": [
        { "value": 1048, "name": 'Search Engine' },
        { "value": 735, "name": 'Direct' },
        { "value": 580, "name": 'Email' },
        { "value": 484, "name": 'Union Ads' },
        { "value": 300, "name": 'Video Ads' }
      ],
      "emphasis": {
        "itemStyle": {
          "shadowBlur": 10,
          "shadowOffsetX": 0,
          "shadowColor": 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}

options_line = {
  "title": {
    "text": 'Data Detail'
  },
  "tooltip": {
    "trigger": 'axis'
  },
  "legend": {
    "orient": 'horizontal',
    "bottom": 'bottom',
    "selected": {
        "Search Engine": True,
        "Direct": True,
        "Email": True,
        "Union Ads": True,
        "Video Ads": True,
    },
  },
  "grid": {
    "bottom": '12%',
    "containLabel": True,
  },
  "xAxis": {
    "type": 'category',
    "boundaryGap": False,
    "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "name": 'Search Engine',
      "type": 'line',
      "stack": 'Total',
      "data": [820, 932, 901, 934, 1290, 1330, 1320]
    },
    {
      "name": 'Email',
      "type": 'line',
      "stack": 'Total',
      "data": [120, 132, 101, 134, 90, 230, 210]
    },
    {
      "name": 'Direct',
      "type": 'line',
      "stack": 'Total',
      "data": [320, 332, 301, 334, 390, 330, 320]
    },
    {
      "name": 'Union Ads',
      "type": 'line',
      "stack": 'Total',
      "data": [220, 182, 191, 234, 290, 330, 310]
    },
    {
      "name": 'Video Ads',
      "type": 'line',
      "stack": 'Total',
      "data": [150, 232, 201, 154, 190, 330, 410]
    },
  ]
}

c1, c2 = st.columns(2)

with c1:
    p = st_echarts(
        options=options_pie,
        events={
            "click": "function(params) { return params.name }",
        },
        height="600px",
        key="1",
    )
    if p:
        st.subheader(p)

with c2:
    p = st_echarts(
        options=options_line,
        events={
            "click": "function(params) { return params.seriesName }",
        },
        height="600px",
        key="2",
    )
    if p:
        st.subheader(p)