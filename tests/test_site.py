import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    for argument in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900"):
        options.add_argument(argument)
    with webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options) as driver:
        driver.get(os.environ["APP_URL"])
        yield driver


def test_title(browser):
    assert browser.title == "CI/CD Assignment | FA23-BCT-039"


def test_heading(browser):
    assert browser.find_element(By.TAG_NAME, "h1").text == "CI/CD Assignment"


def test_message_button(browser):
    browser.find_element(By.ID, "show-message").click()
    assert browser.find_element(By.ID, "message").text == "Jenkins pipeline is working!"


def test_text_submission(browser):
    browser.find_element(By.ID, "entry").send_keys("Selenium verified my text")
    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    assert browser.find_element(By.ID, "submitted").text == "Selenium verified my text"
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    assert browser.save_screenshot(str(report_dir / "selenium-text-submit.png"))
