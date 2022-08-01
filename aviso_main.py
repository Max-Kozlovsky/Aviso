"""
скрипт для работы на буксе Aviso.bz
скрипт обеспечивает серфинг и просмотр видео.
"""
import pickle
from config import name, password
import time  # импортируем модуль тайм
import random  # импортируем модуль рандом
from selenium import webdriver  # импортируем селениум
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # импорт для взаимодействия с элементами сайта
from selenium.webdriver.common.keys import Keys  # импорт взаимодействия с клавиатурой
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, \
    ElementNotInteractableException, WebDriverException, \
    NoSuchFrameException, ElementClickInterceptedException  # импорт возможных исключений


def aviso_log():  # функция для авторизации на авизо
    browser.get("https://aviso.bz/")  # передаем адрес сайта авизо
    browser.implicitly_wait(5)  # ожидаем появления кнопки входа
    browser.find_element(By.XPATH, "//a[contains(@href, '/login')]").click()  # жмем кнопку входа
    time.sleep(3)  # задержка
    browser.find_element(By.XPATH, "//input[contains(@type, 'text')]").send_keys(name)  # ввод логина
    time.sleep(3)  # задержка
    browser.find_element(By.XPATH, "//input[contains(@type, 'password')]").send_keys(password)  # ввод пароля
    time.sleep(3)  # задержка
    browser.find_element(By.XPATH, "//button[contains(@id, 'button-login')]").click()  # жмем кнопку входа
    try:  # если вместо инициализации появляется капча, перехватываем исключение
        time.sleep(3)  # задержка для загрузки изменений
        if browser.find_element(By.XPATH, "//div//iframe[contains(@src, 'hcaptcha')]"):
            # проверяем страницу на наличие капчи
            print('RUN RECAPTCHA')
            time.sleep(100)  # время для решения капчи
    except NoSuchElementException:
        pass
    browser.implicitly_wait(5)  # ожидаем появления меню
    browser.find_element(By.XPATH, "//span[contains(@id, 'mnu_title1')]").click()  # жмем заработать в меню
    print('Успешный вход в аккаунт')
    time.sleep(3)  # задержка для загрузки изменений


def aviso_serf():  # функция для серфинга
    try:
        browser.find_element(By.XPATH, "//span[contains(@class, 'close-notify')]").click()  # закрываем уведомления
        time.sleep(2)
    except NoSuchElementException:  # если уведомлений нет, перехватываем исключение
        print('Уведомлений нет')
        pass
    browser.find_element(By.XPATH, "//div[contains(@id, 'mnu_tblock1')]//child::a[2]").click()  # переход в серфинг
    time.sleep(5)  # задержка для загрузки изменений
    serf_list = browser.find_elements(By.XPATH, "//a[contains(@onclick, 'funcjs')]")  # отбор доступных ссылок
    serf_time = browser.find_elements(By.XPATH, "//div[contains(@style, 'margin-top:5px;')]//child"
                                                "::span[@class='serf-text']")  # отбор таймера просмотров
    bot_list = dict(zip(serf_list, serf_time))
    print(f"Имеется {len(bot_list)} сайтов для серфинга")
    for serf, timer in bot_list.items():  # перебираем список ссылок
        wait_time = timer.text.split(' ')[0]  # определяем время просмотра сайта
        print(serf.text, 'Время просмотра:', wait_time, 'сек')
        try:
            serf.click()  # переход на задание
        except ElementNotInteractableException:
            print('Переход по ссылке невозможен')
            continue
        time.sleep(2)  # ожидание появления ссылки
        links = browser.find_elements(By.XPATH, "//a[contains(@class, 'start-yes-serf')]")  # определение ссылок
        count_t = len(links) - 1  # нахождение последней ссылки
        try:
            links[count_t].click()  # переход на сайт
        except IndexError:  # перехват исключения, если ссылка неактивна (недоступна или без баланса)
            print("Ссылка недоступна")
            continue
        browser.switch_to.window(browser.window_handles[1])  # переход в окно сайта
        if len(wait_time) < 1:  # проверка на наличие таймера
            print('Таймер не определен')
            continue
        browser.implicitly_wait(int(wait_time) + 3)  # ожидание просмотра
        try:
            browser.switch_to.alert.dismiss()  # отключение возможных всплывающих окон
        except NoAlertPresentException:
            pass
        try:
            browser.switch_to.frame("frminfo")  # переход во фрейм для подтверждения просмотра
        except (NoSuchElementException, NoSuchFrameException):
            print('Фрейм подтверждения не обнаружен')
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(10)
            continue
        try:
            browser.find_element(By.XPATH, "//a[contains(@class, 'btn_capt')]").click()  # подтверждаем просмотр
        except (NoSuchElementException, NoSuchFrameException):
            print('Кнопка подтверждения не обнаружена')
            pass
        browser.close()  # закрываем окно сайта
        browser.switch_to.window(browser.window_handles[0])  # возвращаемся на авизо
        print('Просмотр окончен')


def aviso_tube():  # функция просмотра видео в Youtube
    try:
        browser.find_element(By.XPATH, "//span[contains(@class, 'close-notify')]").click()  # закрываем уведомления
        time.sleep(4)
    except NoSuchElementException:  # если уведомлений нет, перехватываем исключение
        print('Уведомлений нет')
        pass
    browser.find_element(By.XPATH, "//div[contains(@id, 'mnu_tblock1')]//child::a[5]").click()  # переход в Youtube
    time.sleep(3)  # ожидание появления списка видео
    tube_links = browser.find_elements(By.XPATH, "//table[contains(@id, 'ads-link')]//ancestor::span[@onclick]")  #
    # список ссылок
    tube_timer = browser.find_elements(By.XPATH, "//span[contains(@style, 'font-size: 12px;vertical-align: "
                                                 "middle;display: inline-block;')]")  # отбор таймера просмотров
    bot_tube = dict(zip(tube_links, tube_timer))
    print(f"Имеется {len(bot_tube)} видео для просмотра")
    for links, tube_timer in bot_tube.items():  # перебираем ссылки для просмотра
        timer = tube_timer.text.split(' ')[0]  # определяем время для просмотра
        try:
            links.click()  # переход на ссылку
        except ElementNotInteractableException:
            print('Ссылка не доступна')
            continue
        print(f"{links.text}, Время просмотра: {timer} сек.")
        try:
            time.sleep(2)
            windows = browser.find_elements(By.XPATH, "//span[contains(@onclick, 'open_window')]")  # список на
            # переход
            windows[-1].click()
        except (ElementClickInterceptedException, IndexError):
            print('Видео недоступно')
            continue
        time.sleep(random.randint(2, 4))  # Ожидание открытия окна с видео
        try:
            browser.switch_to.window(browser.window_handles[1])  # Переход в окно с видео
        except IndexError:  # перехват исключения, если ссылка на видео не работает
            print("Видео не найдено")
            continue
        browser.implicitly_wait(7)  # Ожидание кнопки запуска видео
        try:
            browser.switch_to.frame("video-start")  # переход во фрейм с видео
        except NoSuchFrameException:
            print('Видео не обнаружено')
            continue
        try:
            browser.find_element(By.XPATH, "//button[contains(@class, "
                                           "'ytp-large-play-button ytp-button')]").click()  # запуск видео
        except (ElementNotInteractableException, NoSuchElementException):
            print('Запустить видео невозможно')
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue
        time.sleep(int(timer) + 4)  # ожидание просмотра видео
        try:
            browser.switch_to.frame("video-start")  # переход во фрейм с видео
            browser.find_element(By.XPATH, "//button[contains(@class, "                     # попытка повторного
                                           "'ytp-large-play-button ytp-button')]").click()  # запуска видео
            print('Подтверждаем просмотр')
            time.sleep(5)
        except (NoSuchFrameException, NoSuchElementException, WebDriverException):
            pass
        browser.close()  # закрываем видео
        print("Видео просмотрено")
        browser.switch_to.window(browser.window_handles[0])  # возвращаемся на сайт
        time.sleep(random.randint(3, 5))
    browser.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.HOME)  # возвращаемся в начало страницы авизо
    time.sleep(2)


def aviso_like():
    likes = browser.find_elements(By.XPATH, "//div[contains(@id, 'start-likes')]//ancestor::span[@onclick]")  #
    # получаем список ссылок на лайки
    print(f'{len(likes)} лайков в списке')
    for like in likes:  # перебираем ссылки на лайки
        like.click()  # нажимаем на ссылку
        try:
            browser.find_element(By.XPATH, "//span[contains(@class, 'go-link-youtube')]").click()  # переход в ютьюб
        except NoSuchElementException:
            print('Видео больше не доступно')
            continue
        time.sleep(2)
        browser.switch_to.window(browser.window_handles[1])  # активируем окно с ютьюбом
        time.sleep(2)
        try:
            browser.find_element(By.XPATH, "//button[contains(@aria-label, 'Видео понравилось')]").click()
            # ставим лайк
        except NoSuchElementException:
            print('кнопка с лайком не обнаружена')
            pass
        time.sleep(13)
        browser.close()  # закрываем вкладку с ютьюбом
        print('Лайк успешно поставлен')
        browser.switch_to.window(browser.window_handles[0])  # возвращаемся на авизо
        time.sleep(2)
        try:
            browser.find_element(By.XPATH, "//span[contains(@id, 'check-task')]").click()  # проверяем исполнение
        except ElementNotInteractableException:
            pass
        time.sleep(3)


option = Options()  # опции браузера
option.add_argument("--disable-notifications")  # отключаем уведомления
# option.add_argument('headless')  # фоновый режим
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.add_argument("--mute-audio")  # отключаем звук
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/100.0.4896.127 Safari/537.36")
browser = webdriver.Chrome(options=option)  # инициализируем браузер

print('Начинаю работу')
browser.get('https://www.youtube.com/')
time.sleep(5)
for cookie in pickle.load(open('jion_cookies', "rb")):
    browser.add_cookie(cookie)
time.sleep(5)
browser.refresh()
time.sleep(10)

try:
    aviso_log()
    while True:
        aviso_serf()
        print('Серфинг окончен')
        aviso_tube()
        print('Просмотр youtube окончен')
        aviso_like()
        print('Лайки youtube проставлены')
        rest = random.randint(160, 190)
        print(f"Отдыхаю {rest} секунд")
        time.sleep(rest)
finally:
    browser.quit()
