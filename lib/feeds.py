import xml.etree.ElementTree as xml
from datetime import datetime
from pathlib import Path
import requests
import json, csv

feed_path = Path.home() / '.ytfeed'

def fetch_videos(subscriptions_path):
    feeds = []
    with open(subscriptions_path) as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            feed = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={row.get('Channel Id')}")
            feeds.append({"title": row.get('Channel Title'), "content": feed.content})
            print(f"Downloaded {row.get('Channel Title')}'s feed! :D")
    return feeds

def parse_videos(feed):
    tree = xml.fromstring(feed)
    videos = []
    for entry in tree.findall('{http://www.w3.org/2005/Atom}entry'):
        author = entry.find('{http://www.w3.org/2005/Atom}author').find('{http://www.w3.org/2005/Atom}name').text
        video_id = entry.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        time = entry.find('{http://www.w3.org/2005/Atom}published').text
        videos.append({"author": author, "video_id": video_id, "title": title, "time": time})
    return videos

def create_feed(subscriptions_path):
    feeds = fetch_videos(subscriptions_path)
    videos = []
    for feed in feeds:
        parsed_feed = parse_videos(feed['content'])
        videos.extend(parsed_feed)
    sorted_feed = sorted(videos, key = lambda x: datetime.fromisoformat(x['time']))
    return sorted_feed

def create_feed_file(subscriptions_path):
    feed = create_feed(subscriptions_path)
    with open(feed_path, 'w') as file:
        json.dump(feed, file)

def get_feed():
    if not feed_path.is_file():
        create_feed_file()
    with open(feed_path, 'r') as file:
        feed = json.load(file)
    return feed
