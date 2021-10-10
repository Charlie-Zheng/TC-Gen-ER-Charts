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
x = []
y = []

def gen(er_min:int, er_step:int, er_max:int, timeout:int):

    global x
    global y
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
    driver.execute_script("document.body.style.zoom='100%'")
    er_box:WebElement
    stat_filters = waitForElements(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div.card-body > div > div', errMsg='Did not find minimum stat filters')
    for filter in stat_filters:
        if 'Energy Recharge%' in filter.text:
            er_box = waitForElement(CSS, 'input',elem = filter, errMsg='Did not find ER filter input box')
            break
        elif 'New Stat' in filter.text:
            new_stat_btn = waitForElement(CSS, 'button', elem=filter)
            new_stat_btn.send_keys(Keys.ENTER)
            dropdown_elems = waitForElements(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div.card-body > div > div > div > div > div > a')
            for dropdown in dropdown_elems:
                if 'Energy Recharge' in dropdown.text:
                    dropdown.send_keys(Keys.ENTER)
                    break
            else:
                print('Did not find ER in minimum stat filter dropdown')
                quit()
            er_box = waitForElement(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div.card-body > div > div:nth-last-child(2) > div > input', errMsg='Did not find ER filter input box')
        else:
            del_btn = waitForElement(CSS, 'button.btn.btn-danger', elem=filter)
            del_btn.send_keys(Keys.ENTER)
            pass

    target = waitForElement(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div.d-flex.justify-content-between.mb-2.row > div:nth-child(2) > div > button > span > b > span').text
    print('Looking for the %s target' % target)
    
    generate_btn = waitForElement(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div.d-flex.justify-content-between.mb-2.row > div:nth-child(1) > div > button.h-100.btn.btn-success', errMsg='Could not find generate button')
    er = er_min
    while er <= er_max:
        er_box.send_keys(Keys.CONTROL, 'A')
        er_box.send_keys(Keys.DELETE)
        er_box.send_keys(er)
        generate_btn.send_keys(Keys.ENTER)
        try:
            while waitForElement(CSS, '#content > div > div.mt-2.mb-2.row > div > div > div.card-body > div:nth-child(3) > div > div > div').text != '100%':
                time.sleep(1)
        except:
            pass
        time.sleep(1)
        # gets all the stats
        stats = waitForElements(CSS, '#content > div > div:nth-child(3) > div > div > div.list-group > div:nth-child(1) > button > div > div > div > div.card-body > div > div > div', timeout = timeout, errMsg='Could not find stats')

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
    driver.close()

def percent_to_float(percent:str):
    return float(percent.strip('%'))

def waitForElement(searchMethod, searchTerms, timeout=10, elem=None, errMsg:str=None) -> WebElement:

    if len(x := waitForElements(searchMethod, searchTerms, timeout, elem, errMsg)) > 0:
        return x[0]
    else:
        return None


def waitForElements(searchMethod, searchTerms, timeout=10, elem=None, errMsg:str=None) -> List[WebElement]:
    startTime = time.time()
    if elem == None:
        elem = driver
    found: List[WebElement]
    while (len(found := elem.find_elements(searchMethod, searchTerms)) == 0 or not found[0].is_displayed()) and time.time() - startTime < timeout:
        time.sleep(0.1)

    if time.time() - startTime >= timeout:
        if errMsg == None:
            print("Error, didn't find " + searchTerms + " using " + searchMethod)
        else:
            print(errMsg)
        quit()
    return found

def quit():
    print('x = ' + str(x))
    print('y = ' + str(y))
    try:
        driver.close()
    except:
        pass
    sys.exit()

parse = argparse.ArgumentParser('Go to https://chromedriver.chromium.org/downloads and download the version corresponding to your chrome version, extract the .exe and put it in the same folder as this file. Used to automatically check damage at ER breakpoints. Requires you to already be on the character and have all the settings set up in Genshin Optimizer. The Energy Recharge% minimum final stat filter must be the first filter. Addtionally, due to program limitations, you must close Chrome before running this')
parse.add_argument('-er_min', help='The starting ER', default=100, type=int, nargs="?")
parse.add_argument('-er_step', help='The step between ER', default=5, type=int, nargs="?")
parse.add_argument('-er_max', help='The ending ER', default=250, type=int, nargs="?")
parse.add_argument('-timeout', help='the timeout', default=120, type=int, nargs="?")
args = parse.parse_args()
try:
    print(args.er_min,args.er_step, args.er_max, args.timeout)
    gen(args.er_min,args.er_step, args.er_max, args.timeout)
except Exception as e:
    try:
        import traceback
        traceback.print_exc()
        print('x = ' + str(x))
        print('y = ' + str(y))
        driver.close()
    except:
        pass
