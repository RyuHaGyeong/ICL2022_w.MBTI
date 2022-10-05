from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import time, json, math

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9788901232232")
time.sleep(5)

book_page = BeautifulSoup(driver.page_source, "html.parser")

# book_title = 책 제목
book_title = book_page.select_one("h1.title > strong").text.strip()
# book_writer = 책 저자
book_writer = book_page.select_one("a.detail_author").text.strip()
# book_info = 책 정보 (저자, 출판사, 출간일)
book_info = book_page.select_one("div.author").text.split("|")
# book_publisher = 책 출판사
book_publisher = book_info[-2].strip()
# book_date = 책 출간일
book_date = book_info[-1].strip().replace(" 출간", "")
# book_isbn = 책 ISBN-13
book_isbn = book_page.select_one("tbody > tr > td > span").text.strip()
# book_keyword = 책 키워드
book_keyword_list = []
for book_keyword in book_page.select("div.tag_list > a > span > em"):
    book_keyword_list.append(book_keyword.text.strip().replace("#", ""))
if book_keyword_list == []:
    book_keyword = "등록된 키워드가 없습니다."
else:
    book_keyword = ', '.join(book_keyword_list)
print(book_title, book_writer, book_publisher, book_date, book_isbn, book_keyword)

# book_detail = 책 소개
try:
    book_detail_1 = book_page.select_one("div.title_detail_basic2").text.strip().replace("\n", "")
except:
    book_detail_1 = ""
book_detail_2 = book_page.select_one("div.box_detail_article").text.strip().replace("\n", "")
try:
    book_detail_3 = book_page.select_one("div.box_detail_comment > div.box_detail_article").text.strip().replace("\n", "")
    book_detail = book_detail_1 + book_detail_2 + book_detail_3
except:
    book_detail = book_detail_1 + book_detail_2
# book_review_pub = 책 출판사 서평
book_review_pub = book_page.select("div.box_detail_article > div.content")[-1].text.strip().replace("\n", "").replace("\t\t\t\t닫기", "")
print(book_detail)
print(book_review_pub)

# book_level = Klover 평점
# book_klover = Klover 리뷰
try:
    book_level = book_page.select_one("div.popup_load > em").text.strip()
    driver.get(driver.current_url + "#review")
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "전체").click()
    time.sleep(5)
    book_klover_list = []
    x = 1
    while True:
        try:
            book_page = BeautifulSoup(driver.page_source, "html.parser")
            len_book_klover = book_page.select_one("span.kloverTotal").text.strip()
            for book_klover in book_page.select("div#box_detail_review.box_detail_review dd.comment"):
                book_klover_list.append(book_klover.text.strip().replace("\n", "").replace("크게보기", ""))
            if x == math.ceil(int(len_book_klover[1:-1]) / 5):
                break
            driver.find_elements(By.CSS_SELECTOR, "div#box_detail_review.box_detail_review a.pad")[-2].click()
            x += 1
            time.sleep(5)
        except:
            break
except:
    book_level = "-"
    book_klover_list = "등록된 리뷰가 없습니다."
    driver.get(driver.current_url + "#review")
    time.sleep(5)
print(book_level)
print(book_klover_list)

# book_blog = 북로그 리뷰
try:
    driver.find_element(By.LINK_TEXT, "전체보기").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    book_blog_list = []
    x = 1
    while True:
        try:
            book_page = BeautifulSoup(driver.page_source, "html.parser")
            for book_blog in book_page.select("div.content"):
                book_blog_list.append(book_blog.text.strip().replace("\n", "").replace("\xa0", "").replace("\u200b", ""))
            x += 1
            driver.find_element(By.XPATH, f"/html/body/div/div[2]/ul/li[{x}]/a").click()
            time.sleep(5)
        except:
            driver.close()
            break
except:
    book_blog_list = "등록된 리뷰가 없습니다."
print(book_blog_list)