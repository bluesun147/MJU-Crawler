from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import sys
import re

def faceCrawl():

    # ========================== Pre-Declare==========================
    # 크롬에서의 웹 자동화를 위한 드라이버
    DRIVER = 'C:\\Users\\blues\\Downloads\\chromedriver.exe'
    URL = 'https://facebook.com'
    DATA_FILE = 'data.txt'

    # Input user and password here will not ask user to input uname and password
    # 먼저 입력 시 묻지 않음
    USER = ''
    PASSWORD = ''

    # ========================== File Process ==========================
    # 파일이 존재하는지 체크하는  메소드
    def is_file_exist():
        try:
            open(DATA_FILE, 'r') # 읽기 모드로 오픔
            return True
        except:
            return False

    def write_to_text(list_links):
        if not is_file_exist():# 파일이 존재하지 않는다면 
            open(DATA_FILE, 'w').close() # 쓰기모드로 파일 생성

        data = open(DATA_FILE, 'r').read()
        file = open(DATA_FILE, 'a')  #추가 모드
        for link in list_links:
            if link not in data: # 파일에 없는 링크는 추가
                file.write(link + '\n')
            # else:

    # ========================== Browser Process ==========================
    def chrome_options():# 크롬 옵션 설정
        options = webdriver.ChromeOptions()
        # options.add_argument('--no-sandbox') # This will prevent malicious code, not useful, just note to remember.
        options.headless = True # This will make the chrome executed in hidden process
        # options.add_argument('--headless') # This is another way of the upper
        options.add_experimental_option('excludeSwitches', ['enable-logging']) # This will disable print the console information
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2}) # Disable the asking allow notification or block
        return options

    def page_down(driver): # 페이지 스크롤
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()

    # ========================== Data Process ==========================
    # 로그인 할지 여부
    def required_login():
        opinion = input('[*] Do you want to login (Y/N): ')
        opinion = opinion.lower()
        if 'yes' in opinion or 'y' in opinion:
            return True
        elif 'no' in opinion or 'n' in opinion:
            return False
        else:
            print('[!] Wrong option.')
            return required_login()

    def check_length():
        try:
            # 원하는 양의 포스트
            length = int(input('[*] Length of post you want to get (Interger Only!): '))
            return length
        except:
            print('\n[!] Wrong input. Please re-type.')
            return check_length()

    def get_links():
        url = input('[*] Enter the link to crawl: ')
        if 'https://' not in url:
            print('[!] The tool need URL to crawl.')
            return get_links()
        return url

    def checking_unwantted_link(post):
        if '/announcements/' not in post and 'page_internal' not in post:
            if '/posts/' in post or '/groups/' in post or '/photos/' in post or '/videos/' in post:
                if 'facebook.com' not in post:
                    post = r'https://www.facebook.com' + post
                    # 문자열 치환. re.sub（정규 표현식, 대상 문자열 , 치환 문자）
                    '''
                    text = "I like apble And abple"
                    text_mod = re.sub('apble|abple',"apple",text)
                    print (text_mod) ==> I like apple And apple
                    '''
                post = re.sub(r'[?&]comment_id=.+?\[0\].*[/]{0,1}', '', post)
                post = re.sub(r'[?&]__cft__.*[/]{0,1}', '', post)
                post = re.sub(r'[?&]__xts__.*[/]{0,1}', '', post)
                post = re.sub(r'[?&]type=.*[/]{0,1}', '', post)
                post = re.sub(r'[?&]comment_id=.*[/]{0,1}', '', post)
                return post
        return ''

    # ============================= Main Section =============================
    if __name__ == '__main__':
        # 명령행 인자받기
        # python test.py 
        if len(sys.argv) == 1: 
            link = get_links()
            sys.argv.append(link)
        if len(sys.argv) > 2:
            sys.exit('[-] Too many arguments. Could not parse.')

        # Prepage process
        opinion = required_login()
        length_crawling_post = check_length()
        print('\n[*] Okay! Executing...\n')

        # Declare the driver (Must follow the version of browser)
        # Chrome driver: https://sites.google.com/a/chromium.org/chromedriver/downloads
        # Other driver, get here: https://selenium-python.readthedocs.io/installation.html#drivers
        browser = webdriver.Chrome(DRIVER, chrome_options=chrome_options())

        # if user press yes, this option will run
        # 로그인을 한다고 했을 때 (y)
        if opinion:
            # Checking if the Username or Password is entered
            # id, pw 비어있다면 입력받음
            if USER == '' or PASSWORD == '':
                print('======= PLEASE ENTER YOUR INFORMATION =======')
                USER = input('[*] Enter Username: ')
                PASSWORD = input('[*] Enter Password: ')


            browser.get(URL) # URL = 'https://facebook.com'
            # Entering the username
            userID = browser.find_element_by_id('email')
            userID.send_keys(USER)

            # Entering the password
            passwordID = browser.find_element_by_id('pass')
            passwordID.send_keys(PASSWORD)

            # This will get the ID of login button
            loginID = re.search(r'name="login" data-testid="royal_login_button" type="submit" id="(.+?)"',
                                browser.page_source).group(1)

            # Clicking on login button
            button = browser.find_element_by_id(loginID)
            button.click()

        # ============= Get Post links in groups =============
        sleep(1)
        # link append한 것이 argv[1]
        browser.get(sys.argv[1])
        sleep(1.5)

        # This loop help you roll down 10 times
        # 입력한 만큼 스크롤 내림
        for i in range(length_crawling_post):
            page_down(browser)
            sleep(0.1*randint(3, 5))
        # soup에 파싱한 데이터 저장
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # Find all tag <a>, and parse each link.
        list_links_post = [] # 여기에 저장
        # soup에서 모든 a태그 찾음
        for link in soup.find_all('a'):
            try:
                get_post = link.get('href')
                post = checking_unwantted_link(get_post)
                #print("post is " + post)
                if post not in list_links_post and post != '': # 저장된 것이 아니면 
                    list_links_post.append(post)
            except:
                pass

        write_to_text(list_links_post)
        print(f'[+] We got {len(list_links_post)} links')

        # Closing the browser
        browser.close()

#faceCrawl()