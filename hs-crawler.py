"""hs-crawler.py - Grabs HS-comments from articles"""

import asyncio
import time

import re

import pandas as pd

from crawler import Crawler

class HS_Crawler(): #pylint: disable=invalid-name
    """A class for grabbing hs-article comments"""
    def __init__(self):
        self.crawler = Crawler()
        self.raw_comments = []
        self.comments = []

    def accept_cookies(self):
        """Accept cookie form if present"""
        try:
            self.crawler.switch_to_frame("#sp_message_iframe_775178")

            #print(self.crawler.driver.page_source)

            ok_button = self.crawler.wait_for_element_presence_by_query(
                ".message-button.sp_choice_type_11"
            )

            ok_button.click()

            self.crawler.switch_back()
        except:
            print("Ok")

        self.crawler.switch_back()

    async def close_frontpage_ad(self):
        """Close frontpage ad if present"""
        async def click_close_button(delay):
            await asyncio.sleep(delay)
            print("Closing ad")
            self.crawler.click_by_js_query(".close-frontpage-ad")

        async with asyncio.TaskGroup() as tg:
            for i in range(1, 5):
                tg.create_task(click_close_button(i))

            print(f"started at {time.strftime('%X')}")

        print(f"finished at {time.strftime('%X')}")


    async def load_comments(self, title, url):
        """Load initial comments"""

        comments = []

        #self.crawler.scroll_by_pixels(100)
        self.crawler.click_by_js_query(".ab-test-to-comments-btn")

        for i in range(0, 10):
            self.crawler.click_by_js_query(".button--show-more")
            await asyncio.sleep(0.1)

            try:
                self.crawler.get_element_by_query(".button--show-more")
            except:
                break

        comment_elements = self.crawler.get_elements_by_query("article.comments article.border-t")
        for element in comment_elements:
            self.raw_comments.append({"text": element.text, "title": title, "url": url})

        return comments


    async def load_article(self, url):
        """Load an article from url"""
        self.crawler.load_page(url)

        self.accept_cookies()

        comments = []

        title = self.crawler.get_element_by_query("h1.article-headline--medium").text

        async def get_comments():
            coms = await self.load_comments(title, url)


        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.close_frontpage_ad())
            tg.create_task(get_comments())

        return comments

    async def load_articles(self, articles):
        """Load all articles from an array of urls"""
        for article in articles:
            await self.load_article(article)

    def parse_raw_comments(self):
        i = 0
        for comment in self.raw_comments:
            print(i)
            print(comment["text"])
            items = list(re.findall(r"(?s)^(.+?)\n.+?\n(.+?)\n(.+)\n.+?(\d+?).+?$", comment["text"]))[0]
            print(items)
            self.comments.append({
                "title": comment["title"],
                "url": comment["url"],
                "user": items[0],
                "timestamp": items[1],
                "text": items[2],
                "votes": items[3],
            })

            i += 1

        print("\n\n")

    def handle_comments(self):
        dataframe = pd.DataFrame.from_dict(self.comments)
        print(dataframe)
        dataframe.to_excel("kommentit.xlsx")

def get_articles():
    with open("artikkelit.txt", "r") as file:
        text = file.read()
        return text.split("\n")

async def main():
    """Run the program"""

    articles = ["https://www.hs.fi/kaupunki/art-2000009603026.html"]

    articles = get_articles()
    print(articles)

    crawler = HS_Crawler()
    await crawler.load_articles(articles)

    crawler.parse_raw_comments()

    crawler.handle_comments()

    input("Quit?")

    crawler.crawler.driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
