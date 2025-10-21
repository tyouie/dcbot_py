API_key='AIzaSyBkLZCNCURkiHDczJ4vdT2Zgi2ymnhCixI'
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
try:
    youtube = build('youtube', 'v3', developerKey=API_key)
except Exception as ex:
    print(ex)

def search_songUrl(u):
    result =youtube.search().list(q=u,part='snippet',type='video',maxResults=10)
    re=result.execute()
    reTitle=re['items'][0]['snippet']['title']
    reUrl=re['items'][0]['id']['videoId']
    return reUrl,reTitle




