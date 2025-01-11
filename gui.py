'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-10 22:58:25
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-12 01:17:47
FilePath: \autoAccountor\gui.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from tkinter import ttk

def run_script():
    try:
        result = subprocess.run(['python', 'F:/autoAccountor/autoAccountor.py'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            messagebox.showinfo("Success", "Script executed successfully:\n" + result.stdout)
            update_log_overwrite_display()  # Update log_overwrite display after running the script
        else:
            messagebox.showerror("Error", "Script execution failed:\n" + result.stderr)
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred:\n{str(e)}")

def open_customers_folder():
    try:
        os.startfile('F:/autoAccountor/customers')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open folder:\n{str(e)}")

def open_log_append():
    try:
        os.startfile('F:/autoAccountor/log/log_append.txt')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open log file:\n{str(e)}")

def open_current_info():
    try:
        os.startfile('F:/autoAccountor/info/当前信息.txt')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open current info file:\n{str(e)}")

def open_chat_record():
    try:
        os.startfile('D:/MemoTrace/data/聊天记录/聚财浮球报账群(34375022090@chatroom)/聚财浮球报账群.txt')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open chat record file:\n{str(e)}")

def update_current_info_display():
    try:
        with open('F:/autoAccountor/info/当前信息.txt', 'r', encoding='utf-8') as file:
            current_info_content = file.read()
            display_text.delete(1.0, tk.END)
            display_text.insert(tk.END, current_info_content)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read current info file:\n{str(e)}")

def update_log_overwrite_display():
    try:
        with open('F:/autoAccountor/log/log_overwrite.txt', 'r', encoding='utf-8') as file:
            log_overwrite_content = file.read()
            display_text.delete(1.0, tk.END)
            display_text.insert(tk.END, log_overwrite_content)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read log overwrite file:\n{str(e)}")

app = tk.Tk()
app.title("Run Script")
app.geometry("1000x600")  # Set the window size to 1000x600

style = ttk.Style()
style.configure("TButton", padding=20, relief="flat", background="#33ddff", font=("Helvetica", 10))

button_frame = ttk.Frame(app)
button_frame.pack(pady=10)

run_button = ttk.Button(button_frame, text="更新记账", command=run_script)
run_button.pack(side=tk.LEFT, padx=5)

open_folder_button = ttk.Button(button_frame, text="打开 客户文件夹", command=open_customers_folder)
open_folder_button.pack(side=tk.LEFT, padx=5)

open_log_button = ttk.Button(button_frame, text="打开 日志文件", command=open_log_append)
open_log_button.pack(side=tk.LEFT, padx=5)

open_info_button = ttk.Button(button_frame, text="打开 当前信息", command=open_current_info)
open_info_button.pack(side=tk.LEFT, padx=5)

open_chat_button = ttk.Button(button_frame, text="打开 聊天记录", command=open_chat_record)
open_chat_button.pack(side=tk.LEFT, padx=5)

display_text = tk.Text(app, height=20, width=80, font=("Helvetica", 12))
display_text.pack(pady=50, padx=150, fill=tk.BOTH, expand=True)

update_current_info_display()

app.mainloop()
