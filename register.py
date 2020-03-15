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
import json
import requests
from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor


dict = {
    '0': '0', '1': '1', '2': '2', '3': '3',
    '4': '4', '5': '5', '6': '6', '7': '7',
    '8': '8', '9': '9',
    '10': 'A', '11': 'B', '12': 'C', '13': 'D',
    '14': 'E', '15': 'F', '16': 'G', '17': 'H',
    '18': 'I', '19': 'J', '20': 'K', '21': 'L',
    '22': 'M', '23': 'N', '24': 'O', '25': 'P',
    '26': 'Q', '27': 'R', '28': 'S', '29': 'T',
    '30': 'U', '31': 'V', '32': 'W', '33': 'X',
    '34': 'Y', '35': 'Z'
    }


class MonitorRegiste(object):
    def __init__(self, url, phone):
        self.url = url
        self.tmp_file = str(int(round(time.time() * 1000)))
        self.phone = phone
        self.v_code = ""
        self.chrome_options = Options()
        self.driver = webdriver.Chrome(executable_path="utils/chromedriver", chrome_options=self.chrome_options)

    def get_codejson(self):
        host = 'http://chengmai.iok.la:38450'
        path = '/upload'
        url = host + path
        files = {'file': open('pics/' + self.tmp_file + '-validcode.png', 'rb')}
        response = requests.post(url, files=files)
        content = response.text
        if (content):
            print(content)
        return content

    def json2code(self, codeJson):
        jsonDic = json.loads(codeJson)
        predict = ""
        predict_1 = jsonDic['predict_1']
        predict_2 = jsonDic['predict_2']
        predict_3 = jsonDic['predict_3']
        predict_4 = jsonDic['predict_4']
        state = jsonDic['state']
        if state == "scuccess":
            predict = dict[predict_1] + dict[predict_2] + dict[predict_3] + dict[predict_4]
        return predict

    def get_valid_code(self):
        try:
            valid_img = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#inputForm > p.validate > span > img')))
            self.driver.save_screenshot('pics/' + self.tmp_file + '-screenshot.png')
            left = valid_img.location['x']
            top = valid_img.location['y']
            right = valid_img.location['x'] + valid_img.size['width']
            bottom = valid_img.location['y'] + valid_img.size['height']
            img = Image.open('pics/' + self.tmp_file + '-screenshot.png')
            img = img.crop((left, top, right, bottom))
            img.save('pics/' + self.tmp_file + '-validcode.png')
            codeJson = self.get_codejson()
            self.v_code = self.json2code(codeJson)
        except Exception as te:
            print(te)

    def mv2err_pics(self):
        srcPath = 'pics/' + self.tmp_file + '-validcode.png'
        now_time = int(round(time.time() * 1000))
        dstPath = 'errpics/' + self.v_code + '-' + self.tmp_file + '.png'
        copyfile(srcPath, dstPath)

    def update_err_message(self):
        err_message = ""
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        err = soup.find(name="em", attrs={"class": "error"})
        if err is not None:
            err_message = err.getText()
        return err_message

    def start(self):
        self.driver.get(self.url)
        self.get_valid_code()
        self.driver.find_element_by_id('mobile').send_keys(self.phone)
        self.driver.find_element_by_id('validate').send_keys(self.v_code)
        self.driver.find_element_by_id('nextBtn').click()
        time.sleep(2)
        url_now = self.driver.current_url
        if url_now == self.url:
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            err = soup.find(name="em", attrs={"class": "error"})
            if err is not None:
                err_message = err.getText()
                while err_message != "":
                    if err_message == "手机号码未注册":
                        print(err_message)
                        err_message = ""
                    elif err_message == "手机号码不正确":
                        print(err_message)
                        err_message = ""
                    elif err_message == "验证码不正确":
                        print(err_message)
                        self.mv2err_pics()
                        time.sleep(2)
                        self.driver.find_element_by_id('validate').clear()
                        self.get_valid_code()
                        self.driver.find_element_by_id('validate').send_keys(self.v_code)
                        self.driver.find_element_by_id('nextBtn').click()
                        time.sleep(2)
                        err_message = self.update_err_message()

    def run(self):
        """ 入口函数 """
        self.start()
        self.driver.quit()


def run(phone):
    url = "https://www.creditease.cn/a/user/forgetPasswordStep1"
    policy = MonitorRegiste(url=url, phone=phone)
    policy.run()


def main():
    # phone_list = [13300109999, 13300109998, 13300109997, 13300109996, 13300109995,
    #               13300109994, 13300109993, 13300109992, 13300109991, 13300109990,
    #               13300109989, 13300109988, 13300109987, 13300109986, 13300109985,
    #               13300109984, 13300109983, 13300109982, 13300109981, 13300109980,
    #               13300109979, 13300109978, 13300109977, 13300109976, 13300109975,
    #               13300109974, 13300109973, 13300109972, 13300109971, 13300109970,
    #               13300109969, 13300109968, 13300109967, 13300109966, 13300109965,
    #               13300109964, 13300109963, 13300109962, 13300109961, 13300109960,
    #               13300109959, 13300109958, 13300109957, 13300109956, 13300109955]
    phone_list = [13300109999]
    with ThreadPoolExecutor(max_workers=1) as pool:
        pool.map(run, phone_list)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print('Success! Total Time cost: ', round(time.time() - start_time, 2), ' seconds.')