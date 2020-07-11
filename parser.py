import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
from selenium import webdriver
import time


def main():

    opera_profile = r'C:\\Users\\lutse\\AppData\\Roaming\\Opera Software\\Opera Stable'
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + opera_profile)
    options._binary_location = r'C:\\Users\\lutse\\AppData\\Local\\Programs\Opera\\69.0.3686.57\\opera.exe'
    driver = webdriver.Opera(executable_path=r'C:\\Users\\lutse\\Desktop\\try\\Library\\operadriver.exe', options=options)
    driver.get('https://www.pinnacle.se/ru/esports/matchups/highlights')
    time.sleep(10)


    action_button = driver.find_element_by_class_name("style_container__uaHPr")
    action_button.click()
    time.sleep(10)
    teams = driver.find_elements_by_class_name('style_col3__1pR1d')
    print(teams)
    print(len(teams))
    teams[4].click()
    bar = driver.find_elements_by_class_name('style_titleText__jlbrV')
    values = driver.find_elements_by_class_name('label')
    prices = driver.find_elements_by_class_name('price')

    print(bar[0].text)

    for i in values:
        meta = values.index(i)


        print(f"{i.text} - {prices[meta].text}")



    time.sleep(25)
    driver.quit()








if __name__ == '__main__':
    try:
        main()
    except:
        main()