from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


def main():

    # настраиваем браузер и запускаем первую страницу
    opera_profile = r'C:\\Users\\lutse\\AppData\\Roaming\\Opera Software\\Opera Stable'
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + opera_profile)
    options._binary_location = r'C:\\Users\\lutse\\AppData\\Local\\Programs\Opera\\69.0.3686.57\\opera.exe'
    driver = webdriver.Opera(executable_path=r'C:\\Users\\lutse\\Desktop\\try\\Library\\operadriver.exe',
                             options=options)
    driver.get('https://www.pinnacle.se/ru/esports/matchups/highlights')
    driver.maximize_window()
    timeout = 5

    # Ждем загрузки основной страницы с матчами
    while True:

        try:
            element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_container__uaHPr'))
            WebDriverWait(driver, timeout).until(element_present)
            break

        except TimeoutException:
            print("Timed out waiting for page to load")

    # все матчи в актуальном
    all_actual_matches = driver.find_elements_by_class_name('style_container__uaHPr')

    # Проходимся по всем матчам из актуального
    counter = 0
    while counter <= len(all_actual_matches) - 1:

        while True:

            try:
                element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_container__uaHPr'))
                WebDriverWait(driver, timeout).until(element_present)
                break

            except TimeoutException:
                print("Timed out waiting for page to load")

        all_actual_matches = driver.find_elements_by_class_name('style_container__uaHPr')
        all_actual_matches = [x for x in all_actual_matches if len(x.text) != 0]

        action = ActionChains(driver)
        action.move_to_element(all_actual_matches[counter])
        action.click().perform()

        while True:

            try:
                element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_flexButton__2bj5t'))
                WebDriverWait(driver, timeout).until(element_present)
                break

            except TimeoutException:

                an_error = driver.find_element_by_class_name('style_noSupportBox__az8GQ style_withBorders__9yyqY')
                if an_error:
                    print('Линии для этого матча недоступны')
                    time.sleep(5)
                    driver.back()
                    continue

                else:
                    print("Timed out waiting for page to load")

        teams = driver.find_elements_by_class_name('style_flexButton__2bj5t')
        teams = [x for x in teams if len(x.text) != 0]
        teams_checker = [x.text for x in teams if len(x.text) != 0]

        if 'Teams' not in teams_checker:

            print(f'Парс для матча {counter + 1} не выполнен, нет вкладки Teams')
            driver.back()
            counter += 1
            continue

        elif 'Teams' in teams_checker:

            teams[-1].click()

        else:

            driver.back()
            continue

        print(f"Парс для команды {counter + 1} выполнен!")
        counter += 1

        count_for_content = 0
        labels = driver.find_elements_by_class_name('style_title__2Y8r7')
        content = driver.find_elements_by_class_name('style_content__eJ182')

        for element_label in labels:

            print(f"label - {element_label.text}")
            print(f"сам контент - {content[count_for_content].text}")
            count_for_content += 1
            print()

        driver.back()

    time.sleep(25)
    driver.quit()


if __name__ == '__main__':
    main()
