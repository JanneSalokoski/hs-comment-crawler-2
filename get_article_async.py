"""get-article-async.py - Asynchronously load a single HS article and parse it's comments"""

import logging
import logging.config
import tomllib
import argparse
import asyncio
import time
import re

import pandas as pd

from crawler import Crawler

def init_config(config_file):
    """Read configuration from `config_file`"""
    with open(config_file, "rb") as file:
        return tomllib.load(file)

def init_logger(config):
    """Initialize a logger instance"""
    logging.config.dictConfig(config)
    return logging.getLogger("get-article-async")

def init_argparser():
    """Initialize argparser"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        help="URL of the article to be parsed",
        default="https://www.hs.fi/hyvinvointi/art-2000009533142.html"
    )

    parser.add_argument(
        "-v", "--verbose",
        help="Run in verbose mode. Same as --loglevel=DEBUG",
        action="store_true"
    )

    parser.add_argument("-s", "--silent",
        help="Run in silent mode. Same as --loglevel=SILENT",
        action="store_true"
    )

    parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "SILENT"],
        help="Set which log messages are to be written"
    )

    return parser.parse_args()

async def get_articles():
    """Get article urls from file"""
    with open("artikkelit.txt", "r") as file:
        text = file.read()
        articles = text.split("\n")

        return list(dict.fromkeys(articles))

async def write_articles_file(articles):
    """Write articles file"""
    with open("artikkelit.txt", "w") as file:
        file.write("\n".join(articles))

class AsyncArticleCrawler():
    """A class for handling an article asynchronously"""
    def __init__(self, url):
        self.config = init_config("config.toml")
        self.log = init_logger(self.config["log"])

        self.url = url

        self.crawler = Crawler()

        self.dataframe = None

        self.raw_comments = []
        self.comments = []

        self.log.info("Started an AsyncArticleCrawler for '%s'", self.url)

    async def load_article(self):
        """Load the page provided by url"""
        self.log.debug("Loading article")
        self.crawler.load_page(self.url)
        self.log.debug("Article loaded")

    async def get_title(self):
        """Get title of the article"""
        title = ""
        try:
            title = self.crawler.get_element_by_query("h1.article-headline--medium").text
        except:
            title = self.crawler.get_element_by_query("h1.article-headline--large").text

        self.title = title

    async def close_frontpage_ad(self):
        """Try to close the frontpage ad"""
        self.log.debug("Trying to close frontpage_ad")
        return self.crawler.click_by_js_query(".close-frontpage-ad")

    async def accept_cookies(self):
        """Try to close the cookie dialog"""
        self.log.debug("Trying to accept cookies")
        self.crawler.switch_to_frame("#sp_message_iframe_775178")
        ret = self.crawler.click_by_js_query(".message-button.sp_choice_type_11")
        self.crawler.switch_back()
        
        return ret

    async def show_more(self):
        """Try to click show-more button"""
        self.log.debug("Trying to click show-more button")
        return self.crawler.click_by_js_query(".button--show-more")


    async def interval_runner(self, interval, maximum, name, function):
        """Run function with intervals"""
        for i in range(0, maximum):
            ret = await function()
            if ret == True:
                break

            await asyncio.sleep(interval)

    async def get_comments(self):
        """Get comments"""
        self.crawler.click_by_js_query(".ab-test-to-comments-btn")
        more_task = asyncio.create_task(self.interval_runner(0.2, 20, "more", self.show_more))
        await more_task

        comment_elements = self.crawler.get_elements_by_query("article.comments article.border-t")
        for element in comment_elements:
            com = {
                "artikkeli": self.title,
                "osoite": self.url,
                "käyttäjä": self.crawler.get_element_by_query(
                    "a > span.ui-text-300", root=element).text,
                "aikaleima": self.crawler.get_element_by_query(
                    ".timestamp-label", root=element).text,
                "kommentti": self.crawler.get_element_by_query(
                    "div.py-16.ui-text-400", root=element).text,
                "hyvin argumentoitu": self.crawler.get_element_by_query(
                    "button > span.text-button-plain", root=element).text
                        .replace("(", "").replace(")", "")
            }

            self.comments.append(com)

    async def handle_articles_file(self):
        """Handle articles file"""
        articles = await get_articles()
        if self.url in articles:
            self.log.debug("Article '%s' already in articles file", self.url)
        else:
            articles.append(self.url)
            await write_articles_file(articles)

    async def run(self):
        """Run the class asynchronously"""
        articles_file_task = asyncio.create_task(self.handle_articles_file())
        await articles_file_task

        load_task = asyncio.create_task(self.load_article())
        await load_task

        title_task = asyncio.create_task(self.get_title())
        await title_task

        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.interval_runner(1, 5, "cookies", self.accept_cookies))
            tg.create_task(self.interval_runner(0.2, 10, "frontpage_ad", self.close_frontpage_ad))
            tg.create_task(self.get_comments())

        self.dataframe = pd.DataFrame.from_dict(self.comments)
        self.dataframe.to_excel(f"Kommentit/{self.title.replace(': ', ' - ')}.xlsx")
        print(self.dataframe)

        self.log.info("All done.")

async def main():
    """Load one article"""
    args = init_argparser()

    #url = "https://www.hs.fi/hyvinvointi/art-2000009533142.html"
    crawler = AsyncArticleCrawler(args.url)

    run_task = asyncio.create_task(crawler.run())
    await run_task


if __name__ == "__main__":
    asyncio.run(main())
