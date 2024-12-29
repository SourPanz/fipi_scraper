from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException, TimeoutException

import time

from os import mkdir

def open_web_page() -> webdriver:
    
    '''Открывает страницу фипи. Возвращает webdriver Firefox.'''
    
    driver = webdriver.Firefox()
    driver.maximize_window()
    # физика огэ
    driver.get('https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B')
    # математика егэ
    # driver.get('https://ege.fipi.ru/bank/index.php?proj=AC437B34557F88EA4115D2F374B0A07B')
    
    return driver

def wait_for_element(driver, locator) -> bool:
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(locator))
        print('Element found and visible')
        
        return True
    
    except TimeoutException:
        print(f"Element with locator {locator} not visible within the timeout period.")
        
        return False
        

def get_themes(driver: webdriver) -> list:
    
    '''Выбирает тему вопросов. Возвращает список вебэлементов чекбоксов Разделы КЭС.'''
    
    xpath = '//form[@id="filters"]/child::div[2]/descendant::label'
    themes = driver.find_elements(By.XPATH, xpath)
    
    return themes



def select_page(driver: webdriver, page: int):
    
    '''Переходит на введенную страницу.'''
    print('Page number:', page)
    page_xpath = f'//div[@class="pager-panel"]/ul/li[@p="{page}"]'
    locator = (By.XPATH, page_xpath)
    
    try:
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(locator)).click()
    except StaleElementReferenceException:
        print(f'Page {page} is stale, trying again')
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(locator)).click()
    except ElementNotInteractableException:
        print('Already first page')
    
    
    # if wait_for_element(driver, locator):
    
    #     button = driver.find_element(*locator)
    #     button.click()
    
    
        
    
def get_questions(driver: webdriver, directory: str) -> None:
    
    '''Собирает блоки с вопросами в список. Возвращает список вебэлементов вопросов на текущей странице.'''
    locator = (By.CSS_SELECTOR, '#questions_container')
    if wait_for_element(driver, locator):
        iframe = driver.find_element(*locator)
        driver.switch_to.frame(iframe)
        xpath = '//div[starts-with(@id,"q") and @class = "qblock" or @class = "qblock hide-form"]'
        locator = (By.XPATH, xpath)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(locator))
        questions = driver.find_elements(*locator)
        
        create_screenshot(questions, directory)
        
        driver.switch_to.default_content()
        # return questions
    
    return []

def create_screenshot(questions, directory):
    
    '''Делает скриншоты каждого блока с вопросом отдельным файлом.'''
    
    for q in questions:
        try:
            q_id = q.get_attribute('id')
            file_name = directory + f'/{q_id}.png'
            q.screenshot(file_name)
        except StaleElementReferenceException:
            print(f"Element is stale, skipping screenshot for {q_id}")
        except Exception as e:
            print(f"Error taking screenshot: {e}")


def select_theme(driver: webdriver, theme):
    
    '''Переключает темы.'''
    
    arrow = driver.find_element(By.CLASS_NAME, 'filter-button-arrow')
    reset_button = driver.find_element(By.CLASS_NAME, 'button-clear')
    find_button = driver.find_element(By.CLASS_NAME, 'button-find')
    
    arrow.click()
    reset_button.click()
    theme.click()
    find_button.click()

def check_active_theme(theme) -> bool:
    check_box = theme.find_element(By.TAG_NAME, 'input')
    title = check_box.get_attribute('title')
    
    if title == 'Нет заданий по данной теме':
            print(title + 'отсутствует')
            return True
    
    return False
        
    
        
if __name__ == '__main__':
    driver = open_web_page()
    themes = get_themes(driver)

    for theme in themes:
        
        if check_active_theme(theme):
            continue
        
        theme_name = theme.get_attribute("textContent")
        directory = f'D:/Py_projects/fipi_scraper/screenshots/{theme_name}'
        try:
            mkdir(directory)
        except FileExistsError:
            print(theme_name + ' уже существует')
            
        
        select_theme(driver, theme)
        
        locator = (By.XPATH, '//ul[@class="pager"]/descendant::*[last()]')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(locator))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(locator))
        pages_amount = int(
            driver.find_element(*locator).get_attribute('p')
            )
        print(f'''
              Pages: {pages_amount}
              ''')    
        
        for i in range(1, pages_amount+1):
            time.sleep(1)
            if i > pages_amount:
                break
            select_page(driver, i)
            questions = get_questions(driver, directory)
            driver.execute_script("window.scrollTo(0, 0);")
            
    
    print('OK')
        
    
    
    
   

