from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


# 파이썬 gui tkinter
# https://pythonguides.com/python-tkinter-todo-list/

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
    print(lb.get(0, lb.size()))
    print(listbox.curselection())
    
    
root = Tk() # 전체 화면
root.geometry('500x770+850+5') # 가로 x 세로 + x좌표 + y좌표
root.title('명지대 크롤러')
root.config(bg='#3c72b5') # background 배경, config 변경
root.resizable(width=False, height=False)

'''lab_d = Label(root)
img = ImageTk.PhotoImage(file = "C:\\Users\\blues\\OneDrive\바탕화~1-DESKTOP-9RO8JPH-8531-DESKTOP-9RO8JPH\lizard\\5_5.jpg", master= root)
#img = img.subsample(10)
lab_d.config(image =img)
lab_d.pack()'''
width = 100
height = 100
canvas = Canvas(root, width=width, height=height)
canvas.pack()
img_path = ImageTk.PhotoImage(file = "img\mju.jpg", master= root)
shapes = canvas.create_image(width/2, height/2, image = img_path)


entId = Entry(root, width=30) # 아이디 입력
entId.insert(0, "enter id")
def entryclear(event):
    if entId.get() == "enter id":    # 초기값인 경우 마우스클릭하면 지워지도록,...
        entId.delete(0,len(entId.get()))
entId.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
entId.pack(pady=10)

entPw = Entry(root, show="*", width=30) # 비밀번호 입력
entPw.insert(0, "password")
def entryclear(event):
    if entPw.get() == "password":    # 초기값인 경우 마우스클릭하면 지워지도록,...
        entPw.delete(0,len(entPw.get()))
entPw.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
entPw.pack(pady=10)
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
      

#insta_btn.config(command = login) # id, pw입력하고 insta버튼 누르면 로그인 실행
insta_btn.pack(fill=BOTH, expand=True, side=LEFT)

root.mainloop()