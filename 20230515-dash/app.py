import json
import os
import pickle

import dash
import plotly.express as px

from datetime import datetime, timedelta
from dash import html, dcc
from dash.dependencies import Input, Output, State
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/yt-analytics.readonly']
CREDENTIALS_FILE = 'client_secret.json'

def authenticate_youtube_api(credentials_file, scopes):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_video_ids_and_titles(credentials):
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Get the channel ID
    channel_response = youtube.channels().list(
        part='id,snippet',
        mine=True
    ).execute()
    
    channel_id = channel_response['items'][0]['id']
    
    # Get the videos in the channel
    video_ids_and_titles = []
    next_page_token = None
    
    while True:
        playlistitems_response = youtube.playlistItems().list(
            part='snippet',
            maxResults=50,
            playlistId=f'UU{channel_id[2:]}',  # Convert channel ID to uploads playlist ID
            pageToken=next_page_token
        ).execute()
        
        for item in playlistitems_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            video_ids_and_titles.append((video_id, title))
        
        next_page_token = playlistitems_response.get('nextPageToken')
        if next_page_token is None:
            break
    
    return video_ids_and_titles

def get_video_views_last_3_months(credentials, video_ids):
    youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
    
    # Calculate the date 3 months ago
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=90)
    
    video_views_data = {}
    for video_id in video_ids:
        response = youtube_analytics.reports().query(
            ids='channel==MINE',
            startDate=start_date.strftime('%Y-%m-%d'),
            endDate=end_date.strftime('%Y-%m-%d'),
            metrics='views',
            dimensions='day',
            filters=f'video=={video_id}'
        ).execute()
        
        daily_views = {}
        if 'rows' in response:
            for row in response['rows']:
                date, views = row
                daily_views[date] = views
        
        video_views_data[video_id] = daily_views
    
    return video_views_data

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Hello Fanilo!", className='title'),
    html.P("This is a basic Dash app with a title and a paragraph."),
    html.Button('Load Videos', id='load-videos-button'),
    dcc.Graph(id='video-views-bar-chart'),
    dcc.Graph(id='selected-video-daily-views'),

    dcc.Store(id='youtube-data-store'),
])

@app.callback(
    [Output('video-views-bar-chart', 'figure'),
     Output('youtube-data-store', 'data')],
    [Input('load-videos-button', 'n_clicks')]
)
def load_videos(n_clicks):
    if n_clicks is None:
        return px.bar(title="Video Views"), None

    creds = authenticate_youtube_api(CREDENTIALS_FILE, SCOPES)
    video_ids_and_titles = get_video_ids_and_titles(creds)
    video_ids = [video_id for video_id, title in video_ids_and_titles]
    video_views_data = get_video_views_last_3_months(creds, video_ids)

    video_titles = [title for video_id, title in video_ids_and_titles]
    total_views = [sum(views.values()) for views in video_views_data.values()]

    fig = px.bar(x=video_titles, y=total_views, labels={'x': 'Video Name', 'y': 'Total Views'}, title="Video Views")
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False})

    store_data = {
        'video_ids_and_titles': video_ids_and_titles,
        'video_views_data': video_views_data
    }

    return fig, json.dumps(store_data)

@app.callback(
    Output('selected-video-daily-views', 'figure'),
    [Input('video-views-bar-chart', 'clickData')],
    [State('youtube-data-store', 'data')]
)
def display_clicked_video_daily_views(clickData, store_data):
    if clickData is None or store_data is None:
        return px.line(title="Daily Views")

    store_data = json.loads(store_data)
    video_ids_and_titles = store_data['video_ids_and_titles']
    video_views_data = store_data['video_views_data']

    point_index = clickData['points'][0]['pointIndex']
    selected_video_title = video_ids_and_titles[point_index][1]

    video_id = video_ids_and_titles[point_index][0]
    daily_views_data = video_views_data[video_id]
    dates = list(daily_views_data.keys())
    daily_views = list(daily_views_data.values())

    daily_views_fig = px.line(x=dates, y=daily_views, labels={'x': 'Date', 'y': 'Daily Views'}, title=f"Daily Views for {selected_video_title}")
    return daily_views_fig

if __name__ == '__main__':
    app.run_server(debug=True)
