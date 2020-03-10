import urllib
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import lxml

base_url = "https://www.creditease.cn/servlet/validateCodeServlet"
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path="utils/chromedriver", chrome_options=chrome_options)
#for i in range(500):
t = time.time()
now_time = int(round(t*1000))
url = base_url# + str(now_time)
driver.get(url)
soup = BeautifulSoup(driver.page_source, "lxml")
print(soup)
"""
    all_tbody = soup.findAll(name="tbody")
    if len(all_tbody) == 4:
    all_person = all_tbody[0].findAll(name="tr")
    if len(all_person) != 0:
        for i in range(1, len(all_person)-1):
            name = all_person[i].find(name="b").getText()
            names = name.split(' ')
            lname = names[len(names)-1].lower() 
            if lastnames_all.count(lname) != 0:
                email = all_person[i].find(name="img")
                if email is not None:
                    pic_src = email.get('src')
                    pic = urllib.urlopen(pic_src)
                    picData = pic.read()
                    picFile = open('data/pic/pic-' + name + '.jpg', 'wb')
                    picFile.write(picData)
                    picFile.close()
                    print(name)
                print("\t" + firstname_x + ", " + lastname_x + ", finished.")
                time.sleep(0.5)
                except Exception as e:
                    print(e)
                    continue
                print("\t\t" + lastname_x + ", finished.")
"""
driver.quit()
