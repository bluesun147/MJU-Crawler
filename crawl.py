import time
import os
import tkinter
from bs4 import BeautifulSoup
import requests
from utils.browser import Browser
from docopt import docopt
from tqdm import tqdm
import html
from tkinter import *
from tkinter import messagebox

# python crawl.py -n 3

# https://hyebit.tistory.com/49
 # 파일 경로와 데이터를 매개변수로 받아서 파일 작성.

def writeToFile(filePath, data):
    # 텍스트 모드로 쓰기
    file = open(filePath, 'w', encoding='utf8')
    for i in data:
        if type(i) is list: # i가 리스트이면 즉 data가 [[], []] 이차원 리스트
            i = "\n".join(i) # 원소 구분자를 '\n'으로. 줄 구분. 문자열
        try:
            file.write(str(i)+"\n") # i를 문자열로 변환 후 작성.
        except Exception as e:
            pass
    file.close()

 # 디렉토리 만들기.
def makeDir(dirPath):
    # 매개변수로 받은 경로가 존재하지 않을 때
    if not os.path.exists(dirPath):
        os.makedirs(dirPath) # 그 경로 생성
    else: # 존재 한다면 
        # dirPath에 있는 모든 파일 리스트의 수가 3개면
        if len(os.listdir(dirPath)) == 3: 
            return False # False 반환
    return True # 3개가 아니면 True 반환

# 날짜, 시간 추출
def extractDateTime(data):
    result = ""
    try: # data가 datetime="2021.11.13" 라고 하면 result는 2021.11.13.
        result = data.split('datetime="')[1].split('"')[0]
    except Exception as e:
        pass
        result = ""
    return result

# 본문 추출
def extractMainText(data):
    soup = BeautifulSoup(data)
    try:
        result = soup.select('div.C4VMK > span')[0].text
    except:
        result = ""
    return result

# 좋아요 수 추출
def extractLikes(data):
    soup = BeautifulSoup(data)
    try: # https://www.jungyin.com/168
        result = soup.select('div.Nm9Fw > a.zV_Nj > span')[0].text
    except:
        result = 0
    return result

# 포스트 링크 주소 추출
def extractUrl(data):
    soup = BeautifulSoup(data)
 
    result = soup.select("div.v1Nh3 a")[0]['href']
    return result

 # 이미지 링크 추출
def extractImgUrl(data):
    soup = BeautifulSoup(data)
    result = soup.select("div.KL4Bh img")[0]['srcset'].split(" ")[0]
    return result

# 이미지 저장. 이미지 url, 저장할 경로 매개변수로 받음.
def downloadImage(imageUrl, imagePath):
    # get은 http 요청. requests.get(url) 형식
    # 이미지의 url의 bytes(바이너리) 타입 데이터
    img_data = requests.get(imageUrl).content
    # imagePath경로에 바이너리 모드로 쓰기
    with open(imagePath, 'wb') as handler:
        handler.write(img_data)



def runCrawl(limitNum = 0, is_all_comments=False):
    browser = Browser("driver/chromedriver")

    # =============
    # =============
    # tklnter GUI

    def insta_func(): # insta버튼 눌렀을 때 함수
        print("instagram 버튼 클릭됨")
        print(entId.get()) # 아이디 출력
        #entId.delete(0, END) # 출력 후 지우기
        print(entPw.get()) # 비밀번호 출력
        #entPw.delete(0, END)

    def face_func(): # face버튼 눌렀을 때 함수
        print("facebook 버튼 클릭됨")
        print(entId.get()) # 아이디 출력
        #entId.delete(0, END)
        print(entPw.get()) # 비밀번호 출력
        #entPw.delete(0, END)

    def complete_func(): # 완료 버튼 눌렀을 때 함수
        print("완료 버튼 클릭됨")
        print(entEmail.get()) # 이메일 출력
        #entEmail.delete(0, END)


    def newTask(): # add task 버튼 눌렀을 때 함수
        task = entAddAccount.get()
        if task != "":
            lb.insert(END, task)
            entAddAccount.delete(0, "end")
        else:
            messagebox.showwarning("warning", "Please enter some task.")

    def deleteTask(): # delete task 버튼 눌렀을 때 함수
        lb.delete(ANCHOR)

    def printList(): # 추가 사이트 선택한것들 출력
        return lb.get(0, lb.size())
        
        
    root = Tk() # 전체 화면
    root.geometry('500x750+850+5') # 가로 x 세로 + x좌표 + y좌표
    root.title('명지대 크롤러')
    root.config(bg='#1271b5') # background 배경, config 변경
    root.resizable(width=False, height=False)

    entId = Entry(root, width=30) # 아이디 입력
    entId.insert(0, "leet41627@gmail.com")
    def entryclear(event):
        if entId.get() == "leet41627@gmail.com":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entId.delete(0,len(entId.get()))
    entId.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entId.pack(pady=20)

    entPw = Entry(root, show="*", width=30) # 비밀번호 입력
    entPw.insert(0, "bluesun")
    def entryclear(event):
        if entPw.get() == "bluesun":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entPw.delete(0,len(entPw.get()))
    entPw.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entPw.pack(pady=20)
    entPw.pack()

    sns_button_frame = Frame(root) # 인스타, 페북 버튼 두개 프레임
    sns_button_frame.pack(pady=20) # 위아래로 여백

    insta_btn = Button( # 인스타 버튼
        sns_button_frame, # root 프레임
        text='instagram',
        font=('times 14'),
        bg='#c5f776',
        padx=20, # 버튼 가로 공간
        pady=10, # 버튼 세로 공간
        #command = insta_func # 눌렀을 시 실행 메서드
    )
    # pack 해야 실제 루트에 버튼 포함 됨
    #insta_btn.pack(fill=BOTH, expand=True, side=LEFT)

    face_btn = Button( # 페북 버튼
        sns_button_frame,
        text='facebook',
        font=('times 14'),
        bg='#ff8b61',
        padx=20,
        pady=10,
        command = face_func # 눌렀을 시 실행 메서드
    )
    face_btn.pack(fill=BOTH, expand=True, side=LEFT)

    frame = Frame(root)
    frame.pack(pady=10)

    lb = Listbox(
        frame,
        width=25,
        height=6,
        font=('Times', 14),
        bd=0,
        fg='#464646', # foreground(글자 색)
        highlightthickness=0,
        selectbackground='#a6a6a6',
        activestyle="none",
        
    )
    lb.pack(side=LEFT, fill=BOTH)

    task_list = [
        'myongji_univ',
        'mju_run'
        ]

    for item in task_list:
        lb.insert(END, item)

    sb = Scrollbar(frame)
    sb.pack(side=RIGHT, fill=BOTH)

    lb.config(yscrollcommand=sb.set)
    sb.config(command=lb.yview)

    entAddAccount = Entry(root, width=30)
    entAddAccount.insert(0, "추가할 계정")
    def entryclear(event):
        if entAddAccount.get() == "추가할 계정":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entAddAccount.delete(0,len(entAddAccount.get()))
    entAddAccount.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entAddAccount.pack()

    button_frame = Frame(root)
    button_frame.pack(pady=20)

    addTask_btn = Button(
        button_frame, # root
        text='Add Task',
        font=('times 14'),
        bg='#c5f776',
        padx=20, # 버튼 가로 공간
        pady=10, # 버튼 세로 공간
        command=newTask
    )
    # pack 해야 실제 루트에 버튼 포함 됨
    addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

    delTask_btn = Button(
        button_frame,
        text='Delete Task',
        font=('times 14'),
        bg='#ff8b61',
        padx=20,
        pady=10,
        command=deleteTask # 버튼을 동작시킴. 누르면 deleteTask메서드 실행.
    )
    delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

    listbox = Listbox(root, selectmode="extended", height = 0, font=('Times', 14),)
    listbox.insert(0, "학교공지")
    listbox.insert(1, "컴공공지")
    listbox.insert(2, "명대신문")
    listbox.insert(3, "도서관")
    listbox.pack()

    listBtn = Button(root, text="listBtn", padx=10, pady=10, command=printList)
    listBtn.pack(pady=3)

    entEmail = Entry(root, width=30) # 이메일 입력
    entEmail.insert(0, "enter email")
    def entryclear(event):
        if entEmail.get() == "enter email":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entEmail.delete(0,len(entEmail.get()))
    entEmail.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entEmail.pack(pady=20)
    entEmail.pack(pady=10)

    # 완료 버튼 클릭 시 입력한 이메일로 메일 보냄
    complete_btn = Button(root, padx=10, pady=10, text = "완료", command = complete_func)
    complete_btn.pack()

    


    def login(): # 로그인 메서드
        browser.goToPage("https://www.instagram.com/accounts/login/")
        time.sleep(2.0)
        browser.driver.find_element_by_name("username").send_keys(entId.get())
        time.sleep(2.0)
        browser.driver.find_element_by_name("password").send_keys(entPw.get())
        time.sleep(2.0)
        browser.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(2.0)
        browser.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(8.0)
        browser.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        time.sleep(8.0)
        root.quit() # GUI 실행 종료되긴 하는데 응답없음 뜨고 안닫힘.
        #root.destroy() # 이거 쓰면 오류 뜸
            

    insta_btn.config(command = login) # id, pw입력하고 insta버튼 누르면 로그인 실행
    insta_btn.pack(fill=BOTH, expand=True, side=LEFT)

    root.mainloop() # 로그인 하고 tkinter 닫으면 크롤링 실행
    

    # ==========
    # ==========

    queryList = list(lb.get(0, lb.size())) # 계정 목록들 GUI에서 가져옴

    for query in queryList:
        browser.clearLink() # urlList 초기화
        makeDir("data") # data 디렉토리 생성
        makeDir("data/"+query) # data 내부에 query 생성
        
        mUrl = ""
        # query에 python / #python 들어옴.
        if query[0] == "#": # 해시태그 검색일 경우             python
            mUrl = "https://www.instagram.com/explore/tags/"+query[1:]+"/?hl=en"
        else: # 사용자 검색일 경우               pytohn
            mUrl = "https://www.instagram.com/"+query+"/?hl=en"
        
            
        browser.goToPage(mUrl) # driver.get(murl) # 주소로 이동

        print("collecting url of " + query + "...")
        browser.scrollPageToBottomUntilEnd(browser.collectDpageUrl, limitNum) # 입력 횟수만큼 페이지 전체 스크롤
        print("finish scoll collecting!")

        print("collecting data...")
        slist = list(set(browser.urlList)) # 각 포스트 url 리스트 저장




        for url in tqdm(slist): # 프로세스 바
            dirName = url.split("/")[4]
            # skip if already crawled 
            if not makeDir("data/"+query+"/"+dirName):
                continue

            browser.goToPage(url) # 포스트 하나마다 url 이동

            time.sleep(1)

            cur = browser.getPageSource() # return self.driver.page_source # 한 포스트 전체 html
           
            time.sleep(1)
            
            # extract data
            
            dateTime = extractDateTime(cur) # 날짜 추출
            mainText = extractMainText(cur) # 본문 글 추출
            likes = extractLikes(cur) # 좋아요 수 추출
            url = extractUrl(cur) # 링크 추출
            imgUrl = extractImgUrl(cur) # 이미지 링크 추출

            writeToFile(
                "data/"+query+"/"+dirName+"/info.txt", 
                [   
                    "dateTime: ", dateTime, "",
                    "mainText: ", mainText, "",
                    "likes: ", likes, "",
                    "url: ", "https://www.instagram.com" + url, ""
                ]
            )

            # download image
            imageUrl = html.unescape(imgUrl)
            downloadImage(imageUrl,"data/"+query+"/"+dirName+"/image.jpg")
            time.sleep(1)


        print("query " + query + " collecting finish")

    time.sleep(2)
    browser.driver.quit()
    print("FINISH!")
    
    
    
    

def main():
    args = docopt("""
    Usage:
        crawl.py [-n NUMBER] [--a] [-h HELP]
    
    Options:
        -n NUM    number of returned posts [default: 1000]
        --a       collect all comments
        -h HELP   show this help message and exit
    """)
    hasChromeDriver = False
    for i in os.listdir("./driver"):
        if "chromedriver" in i:
            hasChromeDriver = True
            break
    if not hasChromeDriver:
        print("ERROR! NO 'chromedriver' Found")
        print("Please install chromedriver at https://sites.google.com/a/chromium.org/chromedriver/")
        return

    limitNum = int(args.get('-n', 1000))
    is_all_comments = args.get('--a', False)
    runCrawl(limitNum=limitNum, is_all_comments=is_all_comments)

main()