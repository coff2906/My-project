from base64 import encode
import datetime
from encodings import utf_8
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  
import sqlconnector
import MySQLdb
import csv
import subprocess

conn = sqlconnector.conn()
cur = conn.cursor()

headlabelfont = ("Times New Roman", 15, 'bold')
labelfont = ('Times New Roman', 14)
entryfont = ('Times New Roman', 14)

main = Tk()
main.title('Hệ thống quản lý sách')
main.geometry('1000x800')
main.resizable(0, 0)
lf_bg = 'Pink' 


book_strvar = StringVar()
author_strvar = StringVar()
nxb_strvar = StringVar()
btype_strvar = StringVar()


book = []

type = open('type.txt', 'r',encoding='utf-8')
for btype in type:
    btype = btype.rstrip('\n')
    book.append(btype)


Label(main, text="Hệ thống quản lý sách", font='Arial', bg='DeepPink').pack(side=TOP, fill=X)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, height=1000, width=400)
right_frame = Frame(main, bg="gray")
right_frame.place(x=400, y=30, height=1000, width=600)

#leftframe
Label(left_frame, text="Tên sách", font=labelfont, bg=lf_bg).place(x=30, y=50)
Label(left_frame, text="Tác giả", font=labelfont, bg=lf_bg).place(x=30,y=100)
Label(left_frame, text="Tên nhà xuất bản", font=labelfont, bg=lf_bg).place(x=30,y=150)
Label(left_frame, text="Thể loại", font=labelfont, bg=lf_bg).place(x=30, y=200)
Label(left_frame, text="Ngày phát hành", font=labelfont, bg=lf_bg).place(x=30, y=250)
Entry(left_frame, width=20, textvariable=book_strvar, font=entryfont).place(x=170, y=50)
Entry(left_frame, width=20, textvariable=author_strvar, font=entryfont).place(x=170, y=100)
Entry(left_frame, width=20, textvariable=nxb_strvar, font=entryfont).place(x=170,y=150)
OptionMenu(left_frame, btype_strvar,*book ).place(x=170, y=200, width=188)
date = DateEntry(left_frame, font=("Times New Roman", 14), width=15)
date.place(x=170, y=250)

#fuction
def reset_fields():
   global book_strvar, author_strvar, nxb_strvar, btype_strvar, date
   for i in ['book_strvar', 'author_strvar', 'nxb_strvar', 'btype_strvar']:
       exec(f"{i}.set('')")
   date.set_date(datetime.datetime.now().date())
def display_records():
   tree.delete(*tree.get_children())
   cur.execute('SELECT * FROM sach')
   data = cur.fetchall()
   for records in data:
       tree.insert('', END, values=records)
def add_record():
   global book_strvar, author_strvar, nxb_strvar, btype_strvar, date
   book = book_strvar.get()
   author = author_strvar.get()
   nxb = nxb_strvar.get()
   btype = btype_strvar.get()
   dateget = date.get_date()
   if not book or not author or not nxb or not btype or not dateget :
       mb.showerror('Thông báo lỗi!', "Vui lòng nhập đầy đủ thông tin!")
   else:
        cur.execute(
        'INSERT INTO sach (Ten, Tacgia, Nxb, Theloai, Ngayph) VALUES (%s,%s,%s,%s,%s)', (book, author, nxb, btype, dateget)
        )
        conn.commit()
        mb.showinfo('Thông báo', f"Đã thêm sách '{book}' vào kho")
        reset_fields()
        display_records()
def remove_record():
    if not tree.selection():
        mb.showerror('Thông báo lỗi!','Vui lòng chọn đối tượng muốn xóa')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values['values']
        tree.delete(current_item)
        cur.execute('DELETE FROM sach WHERE Ma=%d' % selection[0])
        conn.commit()
        mb.showinfo('Thông báo', 'Đã xóa sách khỏi kho')
        display_records()
def reset_form():
    global tree
    tree.delete(*tree.get_children())
    cur.execute('DELETE FROM sach where Ma >0') 
    cur.execute('ALTER TABLE sach AUTO_INCREMENT = 1')
    reset_fields()
def exportcsv():
    cur.execute('SELECT * FROM sach')
    result=cur.fetchall()
    c = csv.writer(open('Sach.csv', 'w',encoding='utf-8'))
    for x in result:
        c.writerow(x)

Button(left_frame, text='Thêm sách', font=labelfont, width=15, command= add_record).place(x=30, y=380)
Button(left_frame, text='Xóa', font=labelfont, width=15,command= remove_record).place(x=30, y=450)
Button(left_frame, text='Xem danh sách', font=labelfont, width=15,command= display_records).place(x=200, y=450)
Button(left_frame, text='Làm mới', font=labelfont, width=15,command=reset_fields).place(x=30, y=520)
Button(left_frame, text='Xóa dữ liệu', font=labelfont, width=15,command=reset_form).place(x=200, y=520)
Button(left_frame, text='Xuất file CSV',font=labelfont, width=15,command= exportcsv).place(x=200,y=380)


#rightframe
Label(right_frame, text='Kho sách', font='Arial', bg='DeepPink4', fg='LightCyan').pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('Mã sách', "Tên sách", "Tác giả", "NXB", "Thể loại", "Ngày phát hành"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Mã sách', text='Mã sách', anchor=CENTER)
tree.heading('Tên sách', text='Tên sách', anchor=CENTER)
tree.heading('Tác giả', text='Tác giả', anchor=CENTER)
tree.heading('NXB', text='NXB', anchor=CENTER)
tree.heading('Thể loại', text='Thể loại', anchor=CENTER)
tree.heading('Ngày phát hành', text='Ngày phát hành', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=100, stretch=NO)
tree.column('#3', width=180, stretch=NO)
tree.column('#4', width=60, stretch=NO)
tree.column('#5', width=60, stretch=NO)
tree.column('#6', width=90, stretch=NO)
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)


main.update()
main.mainloop()