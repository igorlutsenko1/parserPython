import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def main():

    # настраиваем браузер и запускаем первую страницу
    opera_profile = r'C:\\Users\\lutse\\AppData\\Roaming\\Opera Software\\Opera Stable'
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + opera_profile)
    options._binary_location = r'C:\\Users\\lutse\\AppData\\Local\\Programs\Opera\\69.0.3686.57\\opera.exe'
    driver = webdriver.Opera(executable_path=r'C:\\Users\\lutse\\Desktop\\try\\Library\\operadriver.exe', options=options)
    driver.get('https://www.pinnacle.se/ru/esports/matchups/highlights')
    driver.maximize_window()
    time.sleep(15)

    # все матчи в актуальном
    all_actual_matches = driver.find_elements_by_class_name('style_container__uaHPr')

    counter = 0
    for actual in all_actual_matches:
        all_actual_matches = driver.find_elements_by_class_name('style_container__uaHPr')
        all_actual_matches[counter].click()
        counter += 1
        time.sleep(10)
        teams = driver.find_elements_by_class_name('style_col3__1pR1d')
        teams[-1].click()
        bar = driver.find_elements_by_class_name('style_titleText__jlbrV')
        values = driver.find_elements_by_class_name('label')
        prices = driver.find_elements_by_class_name('price')

        values_prices = {}

        for i in range(len(bar)):
            name_match = bar[i].text
            values_prices[name_match] = {values[i].text: prices[i].text, values[i+1].text: prices[i+1].text}
        print(values_prices[2:])




        variable = 1

        # Проходимся по данным и выводим в консоль
        for i in values:

            meta = values.index(i)

            if meta % 2 == 0 and meta > 3:
                print(bar[variable].text)
                variable += 1
                order = i.text
                order_price = prices[meta].text
                print(f"{order} - {order_price}  ||  {i.text} - {prices[meta + 1].text}")
            elif meta % 2 != 0 and meta > 3:
                print()
        print('МАТЧ ПРОЙДЕН')
        print('МАТЧ ПРОЙДЕН')
        print()
        driver.back()
        time.sleep(10)

    time.sleep(25)
    driver.quit()

if __name__ == '__main__':
    main()
