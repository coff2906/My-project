from tkinter import *
import mysql.connector
import MySQLdb
import sqlconnector
from tkinter import messagebox
import subprocess


con = sqlconnector.conn()
cur = con.cursor()
main_screen = Tk()   
main_screen.geometry("300x250") 
main_screen.title("Account Login") 

def close():
    main_screen.destroy()



def loginform():
    close()
    login_screen = Tk()
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Nhập thông tin đăng nhập", pady=10 ).pack()
    # Label(login_screen, text="").pack()

    username_verify = StringVar()
    password_verify = StringVar()

    
    Label(login_screen, text="Username").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password").pack()
    password__login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password__login_entry.pack()
    Label(login_screen, text="").pack()


    def errorshow1():
        if username_verify.get() == '':
            messagebox.showinfo("Thông báo lỗi !", "Bạn cần nhập Username !")
            return
        if password_verify.get() == '':
            messagebox.showinfo("Thông báo lỗi !", "Bạn cần nhập Password !")
            return
        else:
            messagebox.showinfo("Thông báo lỗi !", "Tài khoản hoặc mật khẩu chưa đúng !")
    def run():
        login_screen.destroy()
        import doan

    def login():
        cur.execute("SELECT * FROM login WHERE Username=%s and Pass=%s",(username_verify.get(),password_verify.get()))
        row=cur.fetchone()
        if row:
            messagebox.showinfo('Thông báo!','Đăng nhập thành công')
            run()
        else:
            errorshow1()

    Button(login_screen, text="Login", width=10, height=1,command=login).pack()
    # mainscreen.close()
    
    login_screen.mainloop()

def register():
    register_screen = Toplevel(main_screen) 
    register_screen.title("Register")
    register_screen.geometry("300x250")
 

    username = StringVar()
    password = StringVar()
 

    Label(register_screen, text="Please enter details below", bg="Pink").pack()
    Label(register_screen, text="").pack()
    

    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
 

    
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
   

    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    

    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    
    Label(register_screen, text="").pack()
    def savetodatabase():
        cur.execute('INSERT INTO login(Username,Pass) values(%s,%s)',(username.get(),password.get()))
        con.commit()
    def tologin():
        register_screen.destroy()
        # loginform()
    def showerror2():
        if username.get() == '' or password.get()=='':
            messagebox.showerror("Lỗi","Bạn cần nhập đầy đủ thông tin")
            return
        else:
            messagebox.showinfo('Success',"Đăng kí tài khoản thành công!")
            savetodatabase()
            tologin()
    Button(register_screen, text="Register", width=10, height=1, bg="blue",command=showerror2).pack()



 

Label(text="Chọn đăng nhập hoặc đăng kí", bg="Pink", width="300", height="2", font=("Calibri", 13)).pack() 
Label(text="").pack() 
 

Button(text="Đăng nhập", height="2", width="30",command=loginform).pack() 
Label(text="").pack() 
 

Button(text="Đăng kí", height="2", width="30",command= register).pack()
 
main_screen.mainloop() 

