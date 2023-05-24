"""hs-crawler.py - Grabs HS-comments from articles"""

import asyncio

import pandas as pd

from get_article_async import AsyncArticleCrawler

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

async def main():
    """Run the program"""
    articles_task = asyncio.create_task(get_articles())
    articles = await articles_task

    await write_articles_file(articles)

    frames = []

    for article in articles:
        crawler = AsyncArticleCrawler(article)
        article_task = asyncio.create_task(crawler.run())
        await article_task

        frames.append(crawler.dataframe)
  
    print("Moi")
    df = pd.concat(frames)
    print(df)
    df.to_excel("Kommentit/Kaikki kommentit.xlsx")

if __name__ == "__main__":
    asyncio.run(main())
