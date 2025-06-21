import os

from slugify import slugify

import re
from pathlib import Path
from typing import TYPE_CHECKING, List

import click
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from jinja2 import Environment, FileSystemLoader

from ..driver import get_driver
from ..main import main


if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


def read_post(elem: "WebElement"):
    col = elem.find_element(By.CSS_SELECTOR, ".col-sm-10")
    content = re.sub(r"\<div.+\>\s*", "", col.get_attribute("innerHTML")).strip()
    author = elem.find_element(By.CSS_SELECTOR, ".forum-author-info").find_element(By.TAG_NAME, "a").text
    ret = {
        "author": str(author),
        "at": col.find_element(By.CSS_SELECTOR, ".forum-post-at").text,
        "content": content,
    }
    return ret


def read_posts(elem: "WebElement"):
    posts = elem.find_elements(By.XPATH, '//section[@class="forum-anchor"]/div/div')
    posts = [read_post(post) for post in posts]
    return posts


def render(posts: List[dict], title: str) -> str:
    environment = Environment(loader=FileSystemLoader(Path(__file__).parent))
    template = environment.get_template("posts.j2")

    return template.render(posts=posts, title=title)


@main.command()
@click.argument("url", required=False, default="", nargs=1, type=str)
@click.option("-P", "--pages", type=int, default=1, prompt=True, show_default=True)
@click.option("-S", "--strip",
              help="Left strip from title until pattern (eg: '»' )",
              default='»', prompt=True, show_default=True)
def read_forum(pages: int, strip: str, url: str):
    while not url:
        url = click.prompt("Enter URL (eg. https://campus.college.ch/forum/posts/105396-unit-2-theorising-leadership)")
        if url == "q":
            click.secho("Aborting...", fg="red")
            exit(1)

    driver = get_driver(cookies=True)
    driver.get(url)

    title = driver.title
    if strip:
        title = title.split(strip)[1]

    out = slugify(title)
    out = f"{os.getenv('OUT_DIR')}/{out}.html"

    container = driver.find_element(By.CSS_SELECTOR, ".forum-container")
    posts = read_posts(container)

    for page in range(1, pages + 1):
        driver.get(f"{url}?page={page}")
        container = driver.find_element(By.CSS_SELECTOR, ".forum-container")
        posts.extend(read_posts(container))

    rendered = render(posts, title)
    Path(out).write_text(rendered, encoding="utf-8")
    click.secho(f'Saved to {out}', fg="green")
