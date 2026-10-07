import feedparser, datetime, re
from collections import Counter

# Simple RSS sources for AI news (replaceable)
RSS_FEEDS = [
    'https://hnrss.org/newest?q=AI+LLM',
    'https://www.reddit.com/r/MachineLearning/.rss',
    'https://ai.googleblog.com/rss.xml'
]

KEYWORDS = ['ai', 'llm', 'model', 'openai', 'google', 'agent']

def fetch_entries():
    entries = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:10]:  # top 10 per feed
                entries.append({'title': e.get('title',''), 'link': e.get('link',''), 'summary': e.get('summary','')})
        except Exception as ex:
            print(f'Error fetching {url}: {ex}')
    return entries

def score(entry):
    text = (entry['title'] + ' ' + entry['summary']).lower()
    return sum(1 for kw in KEYWORDS if kw in text)

def main():
    entries = fetch_entries()
    ranked = sorted(entries, key=lambda e: score(e), reverse=True)[:5]
    print('## Daily AI Digest -', datetime.date.today())
    for i, e in enumerate(ranked, 1):
        print(f'{i}. {e["title"]}')
        print(f'   {e["link"]}')

if __name__ == '__main__':
    main()
