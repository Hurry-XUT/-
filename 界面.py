import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

from 借阅情况增删改查.bor增删改查 import borrow_book, query_borrow_records, return_book


# 数据库连接函数
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # 替换为你的数据库主机
            user="root",       # 替换为你的数据库用户名
            password="deng1217",  # 替换为你的数据库密码
            database="library_management"  # 替换为你的数据库名称
        )
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None

# 创建主窗口
root = tk.Tk()
root.title("图书管理系统")
root.geometry("600x400")

# 帮助函数：弹出消息框
def show_message(message):
    messagebox.showinfo("操作结果", message)

# 借书功能
def borrow_book_gui():
    book_id = book_id_entry.get()
    student_id = student_id_entry.get()

    if not book_id or not student_id:
        show_message("请填写书籍ID和学生ID！")
        return

    # 转换为整数
    try:
        book_id = int(book_id)
        student_id = int(student_id)
    except ValueError:
        show_message("书籍ID和学生ID必须是整数！")
        return

    borrow_book(book_id, student_id)  # 调用借书功能
    show_message("图书借出成功！")

# 归还图书功能
def return_book_gui():
    record_id = record_id_entry.get()

    if not record_id:
        show_message("请填写借阅记录ID！")
        return

    try:
        record_id = int(record_id)
    except ValueError:
        show_message("借阅记录ID必须是整数！")
        return

    return_book(record_id)  # 调用还书功能
    show_message("图书归还成功！")

# 查询借阅记录功能
def query_borrow_records_gui():
    query_borrow_records()  # 调用查询借阅记录功能

# 创建输入框、标签和按钮
book_id_label = tk.Label(root, text="书籍ID:")
book_id_label.pack(pady=5)
book_id_entry = tk.Entry(root)
book_id_entry.pack(pady=5)

student_id_label = tk.Label(root, text="学生ID:")
student_id_label.pack(pady=5)
student_id_entry = tk.Entry(root)
student_id_entry.pack(pady=5)

borrow_button = tk.Button(root, text="借出图书", command=borrow_book_gui)
borrow_button.pack(pady=10)

record_id_label = tk.Label(root, text="借阅记录ID:")
record_id_label.pack(pady=5)
record_id_entry = tk.Entry(root)
record_id_entry.pack(pady=5)

return_button = tk.Button(root, text="归还图书", command=return_book_gui)
return_button.pack(pady=10)

query_button = tk.Button(root, text="查询借阅记录", command=query_borrow_records_gui)
query_button.pack(pady=10)

# 运行主窗口
root.mainloop()
