from .cookies import Cookies

from .main import main  # noqa: F401, F403
from .forum import *  # noqa: F401, F403
from .fs import *  # noqa: F401, F403


@main.command()
def login():
    driver = get_driver()
    driver.get("https://campus.college.ch")

    form = driver.find_element(By.CSS_SELECTOR, ".old-form")
    form.find_element(By.NAME, "name").send_keys(os.getenv("USERNAME"))
    form.find_element(By.NAME, "pass").send_keys(os.getenv("PASSWORD"))
    form.find_element(By.NAME, "remember").click()
    form.submit()

    Cookies().store(driver)

    click.secho("Stored cookies!", fg="green")


# from kt_odoo_ui_test.driver import get_driver


# @click.group()
# def main():
#     click.echo("All good")
#
#     # driver = get_driver()
#     # driver.get("http://www.python.org")
#     # print(1)
