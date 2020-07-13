from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import getpass
import time


def main():

    path = input("Укажите путь до драйвера оперы, например C:\\Users\\lutse\\Desktop\\try\\Library\\operadriver.exe: ")
    name = getpass.getuser()
    discipline = input("По какой дисциплине парсить данные? csgo / dota: ")
    print()

    # настраиваем браузер и запускаем первую страницу
    opera_profile = f'C:\\Users\\{name}\\AppData\\Roaming\\Opera Software\\Opera Stable'
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + opera_profile)
    options._binary_location = f'C:\\Users\\{name}\\AppData\\Local\\Programs\Opera\\69.0.3686.57\\opera.exe'

    if path:
        driver = webdriver.Opera(executable_path=path,
                                 options=options)
    else:
        driver = webdriver.Opera(executable_path=f'C:\\Users\\{name}\\Desktop\\try\\Library\\operadriver.exe',
                                 options=options)

    driver.get('https://www.pinnacle.se/ru/esports/matchups/highlights')
    driver.maximize_window()
    timeout = 10

    # Ждем загрузки основной страницы с матчами
    while True:

        try:
            element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_container__uaHPr'))
            WebDriverWait(driver, timeout).until(element_present)
            break
        except TimeoutException:
            print("Timed out waiting for page to load")

    # все матчи в актуальном
    list_of_matches = driver.find_elements_by_class_name('style_container__uaHPr')

    # Проходим по всем матчам
    counter = 0
    while counter <= len(list_of_matches) - 1:

        while True:
            try:
                element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_container__uaHPr'))
                WebDriverWait(driver, timeout).until(element_present)
                break

            except TimeoutException:
                print("Timed out waiting for page to load")

        all_actual_matches = driver.find_elements_by_class_name('style_container__uaHPr')
        working_link = all_actual_matches[counter].get_attribute('href')
        link = working_link.split('/')
        finding_csgo = []

        for i in link:
            new_link = i.split('-')
            if discipline in new_link:
                finding_csgo.append(new_link)
                break

        if finding_csgo:
            driver.get(working_link)
        else:
            counter += 1
            continue

        while True:

            try:
                element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_flexButton__2bj5t'))
                WebDriverWait(driver, timeout).until(element_present)
                break
            except TimeoutException:
                print("Timed out waiting for page to load")

        teams = driver.find_elements_by_class_name('style_flexButton__2bj5t')
        teams = [x for x in teams if len(x.text) != 0]
        teams_checker = [x.text for x in teams if len(x.text) != 0]

        if 'Teams' not in teams_checker:
            print(f'Парс для матча {counter + 1} не выполнен, нет вкладки Teams')
            print('_' * 50)
            driver.back()
            counter += 1
            continue
        elif 'Teams' in teams_checker:
            teams[-1].click()
        else:
            driver.back()
            continue

        print(f"Парс для команды {counter + 1} выполнен!")
        print()
        counter += 1

        count_for_content = 0
        labels = driver.find_elements_by_class_name('style_title__2Y8r7')
        content = driver.find_elements_by_class_name('style_content__eJ182')
        teams_name = driver.find_elements_by_class_name('style_participants__3SkHT')
        teams_name = [x.text for x in teams_name]
        teams_name = teams_name[0].splitlines()
        content = [x.text for x in content]
        league_name = driver.find_elements_by_class_name('style_desktop_textLabel__2RMmF')
        league_name = [x.text for x in league_name]

        print(f"{teams_name[1]} VS {teams_name[2]}")
        print(f"League - {league_name[2]}")
        print()

        for element_label in labels:
            print(element_label.text)
            content_for_element_label = content[count_for_content].splitlines()
            i = 0

            while i + 1 < len(content_for_element_label):
                print(f"{content_for_element_label[i]} - {content_for_element_label[i + 1]}")
                i += 2

            print()
            count_for_content += 1

        print('_' * 50)
        driver.back()

    print(f"Все матчи по {discipline} пройдены и загружены")
    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    main()
