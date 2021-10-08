from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typing import List
import time
import os
import argparse
import sys

driver: WebDriver
CSS = By.CSS_SELECTOR


def gen(er_min:int, er_step:int, er_max:int):
    x = []
    y = []

    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--user-data-dir=' + os.path.abspath(
        os.path.expandvars('%APPDATA%/../Local/Google/Chrome/User Data/')))
    driver = webdriver.Chrome(options=options)
    driver.get('https://frzyc.github.io/genshin-optimizer/#/build')
    time.sleep(2)
    # first button
    assert waitForElement(
        CSS, '#input-group-dropdown-1 > span').text == 'Energy Recharge%'

    target = waitForElement(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div.d-flex.justify-content-between.mb-2.row > div:nth-child(2) > div > button > span > b > span').text
    print('Looking for the %s target' % target)
    er_box = waitForElement(
        CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div.card-body > div > div:nth-child(1) > div > input')
    generate_btn = waitForElement(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div.d-flex.justify-content-between.mb-2.row > div:nth-child(1) > div > button.h-100.btn.btn-success')
    er = er_min
    while er <= er_max:
        er_box.send_keys(Keys.CONTROL, 'A')
        er_box.send_keys(Keys.DELETE)
        er_box.send_keys(er)
        generate_btn.click()

        while waitForElement(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div:nth-child(3) > div > div > div').text != '100%':
            time.sleep(1)

        # gets all the stats
        stats = waitForElements(CSS, '#content > div > div:nth-child(3) > div > div > div.list-group > div:nth-child(1) > button > div > div > div > div.card-body > div > div > div', timeout = 120)

        found_er = 0
        for stat in stats:
            if 'Energy Recharge' in (text:=stat.text):
                if '+' in text:
                    found_er = sum([percent_to_float(x) for x in text.rsplit(maxsplit=1)[-1].split('+')])
                    print('found_er %i' %  found_er)
        for stat in stats:
            if target in (text:=stat.text):
                damage = float(text.rsplit(maxsplit=1)[-1])
                x.append(er)
                y.append(damage)
                print('damage %i' % damage)
                while er + er_step <= found_er:
                    er += er_step
                    x.append(er)
                    y.append(damage)
        er += er_step
    print('x = ' + str(x))
    print('y = ' + str(y))

def percent_to_float(percent:str):
    return float(percent.strip('%'))

def waitForElement(searchMethod, searchTerms, timeout=5, elem=None) -> WebElement:

    if len(x := waitForElements(searchMethod, searchTerms, timeout, elem)) > 0:
        return x[0]
    else:
        return None


def waitForElements(searchMethod, searchTerms, timeout=5, elem=None) -> List[WebElement]:
    startTime = time.time()
    if elem == None:
        elem = driver
    found: List[WebElement]
    while (len(found := driver.find_elements(searchMethod, searchTerms)) == 0 or not found[0].is_displayed()) and time.time() - startTime < timeout:
        time.sleep(0.1)

    if time.time() - startTime >= timeout:
        print("Error, didn't find " + searchTerms + " using " + searchMethod)
        driver.close()
        sys.exit()
    return found

parse = argparse.ArgumentParser('Go to https://chromedriver.chromium.org/downloads and download the version corresponding to your chrome version, extract the .exe and put it in the same folder as this file. Used to automatically check damage at ER breakpoints. Requires you to already be on the character and have all the settings set up in Genshin Optimizer. The Energy Recharge% minimum final stat filter must be the first filter. Addtionally, due to program limitations, you must close Chrome before running this')
parse.add_argument('er_min', help='The starting ER', default=100, type=int, nargs="?")
parse.add_argument('er_step', help='The step between ER', default=5, type=int, nargs="?")
parse.add_argument('er_max', help='The ending ER', default=250, type=int, nargs="?")
args = parse.parse_args()
try:
    gen(args.er_min,args.er_step, args.er_max)
except:
    try:
        driver.close()
    except:
        pass
