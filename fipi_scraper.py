from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

from os import mkdir

"""
to do:
1. Более точный выбор содержимого для снимка +
2. Переключение страниц +
3. Сортировка по папкам на основе темы +
4(?). Переключение предмета
5(?). Переключение тем
6. Имя файла - id вопроса +
When I try to use selenium find_element method in a loop, I get NoSuchElementException exception. What could be the problem and how to fix it?
"""

def create_web_page() -> webdriver:
    
    '''Открывает страницу фипи. Возвращает webdriver Firefox.'''
    
    driver = webdriver.Firefox()
    # физика огэ
    # driver.get('https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B')
    # математика егэ
    driver.get('https://ege.fipi.ru/bank/index.php?proj=AC437B34557F88EA4115D2F374B0A07B')
    driver.implicitly_wait(1)
    
    return driver

def get_themes(driver: webdriver) -> list:
    
    '''Выбирает тему вопросов. Возвращает список вебэлементов чекбоксов Разделы КЭС.'''
    
    xpath = '//form[@id="filters"]/child::div[2]/descendant::label'
    themes = driver.find_elements(By.XPATH, xpath)
    
    return themes



def select_page(driver: webdriver, page: int):
    
    '''Переходит на введенную страницу.'''
    
    page_xpath = f'//ul[@class="pager"]/child::li[@p="{str(page)}"]'
    
    try:
        driver = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, page_xpath))
        )
        print('Element found and visible')
    except TimeoutException:
        print('Element not found within the timeout period.')
    else:
        button = driver.find_element(By.XPATH, page_xpath)
        # if len(button) > 0:
        button.click()
    
        
    
def get_questions(driver: webdriver) -> list:
    
    '''Собирает блоки с вопросами в список. Возвращает список вебэлементов вопросов на текущей странице.'''
    
    iframe = driver.find_element(By.CSS_SELECTOR, '#questions_container')
    driver.switch_to.frame(iframe)
    xpath = '//div[starts-with(@id,"q") and @class = "qblock" or @class = "qblock hide-form"]'
    questions = driver.find_elements(By.XPATH, xpath)
    
    return questions

def create_screenshot(questions, directory):
    
    '''Делает скриншоты каждого блока с вопросом отдельным файлом.'''
    
    for q in questions:
        q_id = q.get_attribute('id')
        file_name = directory + f'/{q_id}.png'
        q.screenshot(file_name)



def select_theme(driver: webdriver, theme):
    
    '''Переключает темы.'''
    
    arrow = driver.find_element(By.CLASS_NAME, 'filter-button-arrow')
    reset_button = driver.find_element(By.CLASS_NAME, 'button-clear')
    find_button = driver.find_element(By.CLASS_NAME, 'button-find')
    
    arrow.click()
    reset_button.click()
    theme.click()
    find_button.click()
    
    
        
if __name__ == '__main__':
    driver = create_web_page()
    themes = get_themes(driver)
    page_xpath = f'//ul[@class="pager"]/child::li[@p="{str(2)}"]'
    driver.find_element(By.XPATH, page_xpath).click()

    for theme in themes:
    
        if theme.get_attribute('title') == 'Нет заданий по данной теме':
            print(theme.get_attribute('title') + 'отсутствует')
            continue
        theme_name = theme.get_attribute("textContent")
        directory = f'D:/Py_projects/fipi_scraper/screenshots/{theme_name}'
        pages_amount = int(
            driver.find_element(By.XPATH, '//ul[@class="pager"]/descendant::*[last()]').get_attribute('p')
            )
        print(f'''
              Pages: {pages_amount}
              ''')
        
        select_theme(driver, theme)
        try:
            mkdir(directory)
        except FileExistsError:
            print(theme_name + ' уже существует')
            
        
        for i in range(2, pages_amount+1):
            
            questions = get_questions(driver)
            time.sleep(1)
            create_screenshot(questions, directory)
            select_page(driver, i)
    
    # pages_amount = int(
    #         driver.find_element(By.XPATH, '//ul[@class="pager"]/descendant::*[last()]').get_attribute('p')
    #         )
    # print(f'''
    #       Pages: {pages_amount}
    #       ''')
    # print(str(themes[1]))
    # select_theme(driver, themes[1])
    # select_page(driver, 2)
            
    print('OK')
        
    
    
    
   

