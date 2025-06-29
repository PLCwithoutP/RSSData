import feedparser
import requests

rss_url = "https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml"

# Get content and decode safely
response = requests.get(rss_url)
response.encoding = 'utf-8'  # force correct encoding

# Now parse manually decoded content
feed = feedparser.parse(response.text)

# Check for parsing errors
if feed.bozo:
    print("Failed to parse RSS feed. Error:")
    print(feed.bozo_exception)
elif 'title' not in feed.feed:
    print("No feed title found. The feed might be malformed or unavailable.")
else:
    print(f"Feed Title: {feed.feed.title}\n")

    for entry in feed.entries[:5]:
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Published: {entry.published if 'published' in entry else 'N/A'}")
        print(f"Summary: {entry.summary[:150]}..." if 'summary' in entry else "No summary available.")
        print("-" * 80)
