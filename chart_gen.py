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
XPATH = By.XPATH
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
    er_box:WebElement
    stat_filters = waitForElements(XPATH, '//*[@id="root"]/div[1]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[5]', errMsg='Did not find minimum stat filters')
    for filter in stat_filters:
        if 'Energy Recharge%' in filter.text:
            er_box = waitForElement(CSS, 'input',elem = filter, errMsg='Did not find ER filter input box')
            break
        elif 'New Stat' in filter.text:
            new_stat_btn = waitForElement(CSS, 'button', elem=filter)
            new_stat_btn.send_keys(Keys.ENTER)
            dropdown_elems = waitForElements(XPATH, '//*[@id="basic-menu"]/div[3]/ul/li')
            for dropdown in dropdown_elems:
                if 'Energy Recharge' in dropdown.text:
                    dropdown.send_keys(Keys.ENTER)
                    break
            else:
                print('Did not find ER in minimum stat filter dropdown')
                quit()
            er_box = waitForElement(XPATH, '//*[@id="root"]/div[1]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[5]/div[2]/div/div[last()-1]/div/button[2]/div/input', errMsg='Did not find ER filter input box')
        else:
            pass

    target = waitForElement(XPATH, '//*[@id="root"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[2]/button/span[1]/b/span').text
    print('Looking for the %s target' % target)
    
    generate_btn = waitForElement(XPATH, '//*[@id="root"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/button[1]', errMsg='Could not find generate button')
    er = er_min
    while er <= er_max:
        er_box.send_keys(Keys.ENTER)
        er_box.send_keys(Keys.CONTROL, 'A')
        er_box.send_keys(Keys.DELETE)
        er_box.send_keys(er)
        generate_btn.send_keys(Keys.ENTER)
        try:
            while waitForElement(XPATH, '//*[@id="root"]/div[1]/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/p', timeout = timeout).text != '100.0%':
                time.sleep(1)
            print('Builds done generating!')
        except:
            pass
        time.sleep(1)
        # gets all the stats
        stats = waitForElements(XPATH, '//*[@id="root"]/div[1]/div[2]/div/div[4]/button/div/div[2]/div/div/div/div', timeout = timeout, errMsg='Could not find stats')

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
    while (len(found := elem.find_elements(searchMethod, searchTerms)) == 0) and time.time() - startTime < timeout:
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

parse = argparse.ArgumentParser('GO scraper', 'Go to https://chromedriver.chromium.org/downloads and download the version corresponding to your chrome version, extract the .exe and put it in the same folder as this file. Used to automatically check damage at ER breakpoints. Requires you to already be on the character and have all the settings set up in Genshin Optimizer. The Energy Recharge% minimum final stat filter must be the first filter. Addtionally, due to program limitations, you must close Chrome before running this')
parse.add_argument('-er_min', help='The starting ER', default=100, type=int, nargs="?")
parse.add_argument('-er_step', help='The step between ER', default=5, type=int, nargs="?")
parse.add_argument('-er_max', help='The ending ER', default=250, type=int, nargs="?")
parse.add_argument('-timeout', help='the timeout', default=20, type=int, nargs="?")
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
