from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os


def main():
    path = input("Укажите путь до драйвера оперы,"
                 " например C:\\Users\\lutse\\Desktop\\try\\Library\\operadriver.exe: ")

    browser_opera = input("Укажите путь до оперы,"
                 " например 'C:\\Users\\lutse\\AppData\\Local\\Programs\\Opera\\69.0.3686.57\\opera.exe': ")

    opera_prof = input("Укажите путь до профиля оперы,"
                 " например C:\\Users\\lutse\\AppData\\Roaming\\Opera Software\\Opera Stable: ")

    discipline = input("По какой дисциплине парсить данные? csgo / dota / legends: ")
    print()

    # настраиваем браузер и запускаем первую страницу

    if opera_prof:
        opera_profile = opera_prof
    else:
        opera_profile = f'C:\\Users\\lutse\\AppData\\Roaming\\Opera Software\\Opera Stable'

    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + opera_profile)

    if browser_opera:
        options._binary_location = browser_opera
    else:
        options._binary_location = f'C:\\Users\\lutse\\AppData\\Local\\Programs\\Opera\\69.0.3686.57\\opera.exe'

    if path:
        driver = webdriver.Opera(executable_path=path,
                                 options=options)
    else:
        driver = webdriver.Opera(executable_path=f'C:\\Users\\lutse\\Desktop\\try\\Library\\operadriver.exe',
                                 options=options)

    os.system('cls')
    driver.get('https://www.pinnacle.se/ru/esports/matchups/highlights')
    driver.maximize_window()
    timeout = 10

    # Создаем файл для дальнейшей записи матчей
    file = open(f'database_pinnacle_{discipline}.txt', 'w', encoding='utf - 16')
    file.close()

    # Матчи, которые мы уже спарсили
    completed_matches = []
    os.system('cls')
    while True:

        # Ждем загрузки основной страницы
        refresh_count = 0
        while True:
            try:
                refresh_count += 1
                element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_container__uaHPr'))
                WebDriverWait(driver, timeout).until(element_present)
                break
            except TimeoutException:
                if refresh_count == 2:
                    driver.refresh()
                    refresh_count = 0
                else:
                    print("Timed out waiting for page to load")

        list_of_matches = driver.find_elements_by_class_name('style_container__uaHPr')
        all_links = [x.get_attribute('href') for x in list_of_matches]
        all_links_cleared = [x.get_attribute('href') for x in list_of_matches if discipline in x.get_attribute('href')]

        # Сохраняем названия команд в матче
        time.sleep(1)
        category_of_match = driver.find_elements_by_class_name('style_participants__1OLhG')
        category_of_match = [x.text for x in category_of_match]

        if len(completed_matches) >= len(all_links_cleared):
            break

        for match_link in all_links_cleared:
            if match_link not in completed_matches:
                completed_matches.append(match_link)
                working_link = match_link
                driver.get(working_link)

                # Ищем индекс матча в списке, чтобы сохранить полное название команд
                for elem in all_links:
                    if elem == working_link:
                        index = all_links.index(elem)
                        teams_name = category_of_match[index].splitlines()
                        break
                break
            else:
                continue

        refresh_count = 0
        while True:
            try:
                refresh_count += 1
                element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_grid__5OWBH'))
                WebDriverWait(driver, timeout).until(element_present)
                break
            except TimeoutException:
                if refresh_count == 2:
                    driver.refresh()
                    refresh_count = 0
                else:
                    print("Timed out waiting for page to load")

        teams = driver.find_elements_by_class_name('style_flexButton__2bj5t')
        teams = [x for x in teams if len(x.text) != 0]
        teams_checker = [x.text for x in teams if len(x.text) != 0]
        print()
        print(f'Парсим "{teams_name[0]} VS {teams_name[1]}" матч')
        print(f'Осталось {len(all_links_cleared) - len(completed_matches)} матчей(а)')
        print()

        # Проверяем, есть Team в матче
        if 'Teams' not in teams_checker:
            with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
                print(f'Парсинг для матча "{teams_name[0]} VS {teams_name[1]}" не выполнен, нет вкладки Teams', file=f)
                print('_' * 50, file=f)
            driver.back()
            continue
        elif 'Teams' in teams_checker:
            time.sleep(2)
            teams[-1].click()
        else:
            driver.back()
            continue

        checker_for_teams = True
        refresh_count = 0
        while True:
            try:
                refresh_count += 1
                element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_container__1MuSF'))
                WebDriverWait(driver, timeout).until(element_present)
                break
            except TimeoutException:
                if refresh_count == 2:
                    driver.back()
                    print(f'Не получилось спарсить линию Teams для "{teams_name[0]} VS {teams_name[1]}"'
                          f'. Превышено время ожидания')
                    print()
                    checker_for_teams = False
                    break
                else:
                    print("Timed out waiting for page to load")

        if checker_for_teams:
            pass
        else:
            continue

        with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
            print(f'Парсинг для матча "{teams_name[0]} VS {teams_name[1]}" выполнен!', file=f)
            print(' ', file=f, end='\n')

        count_for_content = 0
        labels = driver.find_elements_by_class_name('style_title__2Y8r7')
        content = driver.find_elements_by_class_name('style_content__eJ182')
        date_time = driver.find_element_by_class_name('style_datetimeContainer__3KXS7').text
        content = [x.text for x in content]
        league_name = driver.find_elements_by_class_name('style_desktop_textLabel__2RMmF')
        league_name = [x.text for x in league_name]

        with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
            print(f"{teams_name[0]} VS {teams_name[1]}", file=f)
            print(f"League - {league_name[2]}", file=f)
            print(date_time, file=f)
            print(' ', file=f)

        for element_label in labels:
            with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
                print(f"{element_label.text}", file=f)
            content_for_element_label = content[count_for_content].splitlines()
            i = 0

            while i + 1 < len(content_for_element_label):
                with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
                    print(f"{content_for_element_label[i]} - {content_for_element_label[i + 1]}", file=f)
                i += 2

            with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
                print(' ', file=f)

            count_for_content += 1

        with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
            print('_' * 50, file=f)
        driver.back()

    with open(f'database_pinnacle_{discipline}.txt', 'a', encoding='utf - 16') as f:
        print(f"Все матчи по {discipline} пройдены и загружены", file=f)
    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    main()