import urllib
import time
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import lxml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getValidCode(driver):
    try:
        valid_img = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#inputForm > p.validate > span > img')))
        driver.save_screenshot('pics/screenshot.png')
        left = valid_img.location['x']
        top = valid_img.location['y']
        right = valid_img.location['x'] + valid_img.size['width']
        bottom = valid_img.location['y'] + valid_img.size['height']
        img = Image.open('pics/screenshot.png')
        img = img.crop((left, top, right, bottom))
        img.save('pics/validcode.png')
    except Exception as te:
        print(te)

def register(phone):
    url = "https://www.creditease.cn/a/user/forgetPasswordStep1"
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="utils/chromedriver.exe", chrome_options=chrome_options)
    driver.get(url)
    # driver.implicitly_wait(10)
    # soup = BeautifulSoup(driver.page_source, "lxml")
    # valid_img = soup.find(name="img", attrs={"class": "mid validateCode"})
    getValidCode(driver)
    driver.find_element_by_id('mobile').send_keys(phone)
    driver.find_element_by_id('validate').send_keys('v_code')
    driver.find_element_by_id('nextBtn').click()
    time.sleep(2)
    url_now = driver.current_url
    if url_now == url:
        soup = BeautifulSoup(driver.page_source, "lxml")
        err = soup.find(name="em", attrs={"class": "error"})
        if err is not None:
            err_message = err.getText()
            while err_message != "":
                print(err_message)
                if err_message == "手机号码未注册":
                    print(err_message)
                elif err_message =="手机号码不正确":
                    print(err_message)
                elif err_message == "验证码不正确":
                    driver.find_element_by_id('validate').clear()
                    getValidCode(driver)
                    driver.find_element_by_id('validate').send_keys('v_code')
                    driver.find_element_by_id('nextBtn').click()
    driver.quit()


def main():
    phone = '15600699152'
    register(phone)


if __name__ == '__main__':
    main()
