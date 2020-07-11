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
    teams[4].click()
    bar = driver.find_elements_by_class_name('style_titleText__jlbrV')
    values = driver.find_elements_by_class_name('label')
    prices = driver.find_elements_by_class_name('price')

    print(bar[0].text)
    variable = 1

    for i in values:

        meta = values.index(i)

        if meta % 2 == 0 and meta > 3:
            print(bar[variable].text)
            order = i.text
            order_price = prices[meta].text
            variable += 1
        elif meta % 2 != 0 and meta > 3:
            print(f"{order} - {order_price}  ||  {i.text} - {prices[meta].text}")
            print()
        else:
            print(f"{i.text} - {prices[meta].text}")
            if meta > 2:
                print()

    time.sleep(25)
    driver.quit()








if __name__ == '__main__':
    main()
