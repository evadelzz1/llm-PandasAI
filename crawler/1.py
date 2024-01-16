# https://mememeing.tistory.com/195

import time
from selenium import webdriver
from openpyxl import Workbook
from bs4 import BeautifulSoup

# Selenium으로 웹사이트 접속
driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get('https://workey.codeit.kr/music')
# driver.find_element_by_id('close_btn').click()
time.sleep(2)

# ========================== : 페이지 끝까지 스크롤 #
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# ========================== : 스크롤 완료 #

# 현재 웹사이트 HTML 코드 가져오기 : driver.page_source
music_page = driver.page_source
driver.quit()

# 가져온 HTML 코드로 BeautifulSoup 만들기
soup = BeautifulSoup(music_page, 'html.parser')

playlists = soup.select('.playlist__meta')


wb = Workbook(write_only=True)
ws = wb.create_sheet('플레이리스트')
ws.append(['제목', '태그', '좋아요 수', '노래 수'])

for playlist in playlists:
    title = playlist.select_one('h3.title').get_text()
    hashtags = playlist.select_one('p.tags').get_text()
    like_count = playlist.select_one('span.data__like-count').get_text()
    music_count = playlist.select_one('span.data__music-count').get_text()
    ws.append([title, hashtags, like_count, music_count])
    
wb.save('플레이리스트.xlsx')
