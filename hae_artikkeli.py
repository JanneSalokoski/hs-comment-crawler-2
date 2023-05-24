"""Hae artikkeli"""

import os

def main():
    """Run the program"""
    article = input("Artikkelin osoite: ")
    os.system(f"py get_article_async.py {article}")

if __name__ == "__main__":
    main()
