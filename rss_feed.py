import feedparser
import re
import datetime

news_feed_list = ["http://www.abc.net.au/news/feed/2942460/rss.xml", \
                  "https://www.thestar.com.my/rss/News", \
                  "http://feeds.bbci.co.uk/news/world/rss.xml", \
                  "https://www.reddit.com/r/news/.rss"]

# Passing RSS Feed from reputable news outlets
def get_news(index, source):
    news_feed = feedparser.parse(news_feed_list[index])
    news_text = "{} \- Source : {} \n\n".format(datetime.datetime.now().strftime("%d/%m/%y"), re.escape(source))

    # Formating News Articles with Markdown Format
    for item in news_feed.entries[:10]:
        news_text += "**" + remove_html_tags_escape(item.title) + "** \n" \
            + "`" + remove_html_tags_escape(item.summary) + "` " \
            + "[Link](" + remove_html_tags_escape(item.link) + ") \n\n"

    return news_text

# Getting Anime released on that day from https://www.livechart.me/schedule/tv
def get_anime():
    anime_feed = feedparser.parse("https://www.livechart.me/feeds/episodes")
    anime_text = "**" + datetime.datetime.now().strftime("%d/%m/%y") + "** \n\n"

    for item in anime_feed.entries:
        if item.published_parsed.tm_mday is datetime.datetime.utcnow().day or datetime.datetime.utcnow().day - 1:
            anime_text += "`" + remove_html_tags_escape(item.title) + "` \n"

    return anime_text.replace("!", "\!")

def remove_html_tags_escape(text):
    clean = re.compile('<.*?>')
    return re.escape(re.sub(clean, '', text)).replace("=","\=")

