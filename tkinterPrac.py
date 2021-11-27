from tkinter import*
from typing import List

# https://m.blog.naver.com/amethyst_lee/222012497834
root = Tk()
root.title("GUI test")
root.geometry("640x700")

def btncmd():
    print("버튼 클릭됨")
    print(txt.get("1.0", END)) # 첫번째 라인, 0:0번째 컬럼위치
    print(ent.get())
    txt.delete("1.0", END)
    ent.delete(0, END)

def change():
    label.config(text = "변경됨")

def orderGet():
    print(burger_var.get())

def printList():
    print(listbox.curselection())


btn1 = Button(root, text = "버튼1", command=change)
btn1.pack()

btn2 = Button(root, padx=10, pady=10, text = "버튼2", command = btncmd)
btn2.pack()

label = Label(root, text = "변경 전 텍스트")
label.pack()

txt = Text(root, width=30, height=10)
txt.pack()
txt.insert(END, "글자를 입력하세요")

ent = Entry(root, width=30)
ent.pack()

burger_var = IntVar()
btn_b1 = Radiobutton(root, text = "b1", value=1, variable=burger_var)
btn_b1.select()
btn_b2 = Radiobutton(root, text = "b2", value=2, variable=burger_var)
btn_b3 = Radiobutton(root, text = "b3", value=3, variable=burger_var)
btn_b4 = Radiobutton(root, text = "b4", value=4, variable=burger_var)

btn_b1.pack()
btn_b2.pack()
btn_b3.pack()
btn_b4.pack()

orderBtn = Button(root, text="order", command=orderGet)
orderBtn.pack()

cb1 = Checkbutton(root, text = "cb1")
cb1.pack()

cb2 = Checkbutton(root, text = "cb2")
cb2.pack()

listbox = Listbox(root, selectmode="extended", height = 0)
listbox.insert(0, "학교홈피")
listbox.insert(1, "명대신문")
listbox.insert(2, "도서관")
listbox.insert(3, "44")
listbox.insert(4, "55")
listbox.pack()

listBtn = Button(root, text="listBtn", command=printList)
listBtn.pack()


root.mainloop()