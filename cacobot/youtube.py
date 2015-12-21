import json
import cacobot.base as base
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

with open('configs/config.json') as data:
    config = json.load(data)

@base.cacofunc
def yt(message, client, *args, **kwargs):
    """
    **.yt** <*query*> [.results *int*]
    Searches YouTube and returns the first 2 queries. This can be a video, a playlist, or a channel. If you provide .results with an integer afterwards, returns the first *int* results.
    *Example: .yt Doom E1M1 100% .results 3*
    """

    if message.content.split(" ")[-2] == ".results":
        query = message.content[4:message.content.find(".results") - 2]
        results = int(message.content.split(" ")[-1]) #The number of results to spew.
    else:
        query = message.content[4:]
        results = 2

    youtube = build(config['youtube']['API_SERVICE_NAME'], config['youtube']['API_VERSION'], developerKey=config['youtube']['DEVELOPER_KEY'])

    #This string will store the message that will eventually be sent.
    all_videos = ''

    #Limit requests if
    if results > config['youtube']['request_limit']:
        all_videos += '*I had to limit your request to {} results at the behest of my maintainer.*\n'.format(config['youtube']['request_limit'])
        results = config['youtube']['request_limit']

    #this is all pretty much from the YouTube API Python example.

    search_response = youtube.search().list(
      q = query,
      part = "id,snippet",
      maxResults = results
    ).execute()

    vids = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            vids.append('**' + search_result["snippet"]["title"] + "** | http://youtu.be/" + search_result["id"]["videoId"])
        elif search_result["id"]["kind"] == "youtube#channel":
            vids.append('_Channel -_ **' + search_result["snippet"]["title"] + "** | http://www.youtube.com/channel/" + search_result['id']['channelId'])
        elif search_result["id"]["kind"] == "youtube#playlist":
            vids.append('_Playlist -_ **' + search_result["snippet"]["title"] + "** | https://www.youtube.com/playlist?list=" + search_result['id']['playlistId'])

    for video in range(0, len(vids)):
        all_videos += vids[video] + " (Result " + str(video + 1) + " of " + str(len(vids)) + " from YouTube) \n\n"

    yield from client.send_message(message.channel, all_videos)
