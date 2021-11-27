from tkinter import *
win = Tk()
win.title("daum log in")
win.geometry("400x300")
win.option_add("*Font","맑은고딕 15")



#id Label 
lab1 =  Label(win)
lab1.config(text = "ID")
lab1.pack()

#id entry
ent1 = Entry(win)
ent1.insert(0,"temp@temp.com")   

# 0은 왼쪽에 넣으라는 의미, 클릭하면 사라지게 

def entryclear(event):
    if ent1.get() == "temp@temp.com":    # 초기값인 경우 마우스클릭하면 지워지도록,...
        ent1.delete(0,len(ent1.get()))

ent1.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
ent1.pack()



#pw
lab2 =  Label(win)
lab2.config(text = "Passward")
lab2.pack()

#pw entry
ent2= Entry(win)
ent2.config(show = "*")   # 입력되는 것을 *로 보이게 하기 
ent2.pack()

#login Button
btn = Button(win)
btn.config(text="log-in")
#로그인 
# def login():
#     my_id = ent1.get()
#     my_pw = ent2.get()
#     print(my_id, my_pw)   # console에 출력 
#     lab3.config(text = "[메시지] 로그인 성공")

from selenium import webdriver
def login():
    driver = webdriver.Chrome('C:\\Users\\blues\\Downloads\\chromedriver.exe')
    url = "https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F"
    driver.get(url)
    driver.implicitly_wait(5)

    xpath1 = '//input[@name="id"]'
    driver.find_element_by_xpath(xpath1).send_keys(ent1.get())
    driver.implicitly_wait(5)

    xpath2 = '//input[@name="pw"]'
    driver.find_element_by_xpath(xpath2).send_keys(ent2.get())
    driver.implicitly_wait(5)

    xpath3 = '//button[@class="btn_comm"]'
    driver.find_element_by_xpath(xpath3).click()
    lab3.config(text = "[메시지] 로그인 성공")
        


btn.config(command = login)
btn.pack()

#message label 
lab3 = Label(win)
lab3.pack()

win.mainloop()