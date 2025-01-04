import datetime
import frontmatter
import requests
import csv
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def create_game(name, url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser").find(id="center_column")

    post = {
        "title": soup.find(id="product_name").text, "img_url": soup.find(id="bigpic")["src"],
        "small_description": soup.find(id="short_description_content").text,
        "age": soup.select(".age > span")[0].text.strip(),
        "duration": soup.select(".duree_partie > span")[0].text.strip(),
        "players": soup.select(".nb_joueurs > span")[0].text.strip(),
        "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "philibert_url": url,
    }

    content = soup.find(id="tab-description").div
    post_obj = frontmatter.Post(md(content.prettify()), **post)
    frontmatter.dump(post_obj, f"./content/games/{name}.md")


with open('games.csv', newline='') as file:
    csv_file = csv.DictReader(file, delimiter=";")
    for line in csv_file:
        create_game(line["nom"], line["url"])