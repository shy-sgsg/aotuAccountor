import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from tkinter import ttk

current_file_path = 'F:/autoAccountor/info/当前信息.txt'  # Track the currently displayed file

def run_script():
    """Run the autoAccountor.py script and update the display with the log file content."""
    global current_file_path
    try:
        result = subprocess.run(['python', 'F:/autoAccountor/autoAccountor.py'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            current_file_path = 'F:/autoAccountor/log/log_overwrite.txt'  # Update the current file path
            update_display(current_file_path)  # Update display to show log_overwrite.txt
            messagebox.askyesno("成功", "运行成功")
        else:
            current_file_path = 'F:/autoAccountor/log/log_overwrite.txt'  # Update the current file path
            update_display(current_file_path)  # Update display to show log_overwrite.txt
    except Exception as e:
        error_message = f"发生错误:\n{str(e)}"
        if messagebox.askyesno("错误", f"{error_message}\n是否忽略错误并继续执行？"):
            current_file_path = 'F:/autoAccountor/log/log_overwrite.txt'  # Update the current file path
            update_display(current_file_path)  # Update display to show log_overwrite.txt

def run_process_customers():
    """Run the process_customers.py script and display the result in the text box."""
    try:
        result = subprocess.run(['python', 'F:/autoAccountor/process_customers.py'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            display_text.delete(1.0, tk.END)
            display_text.insert(tk.END, result.stdout)
        else:
            messagebox.showerror("错误", f"运行 process_customers.py 失败:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误:\n{str(e)}")

def run_single_message_processor():
    """Run the single_message_processor.py script."""
    try:
        result = subprocess.run(['python', 'F:/autoAccountor/single_message_processor.py'], capture_output=True, text=True, encoding='utf-8')
        # if result.returncode == 0:
            # pass
            # messagebox.showinfo("成功", "单步消息处理成功")
        # else:
            # messagebox.showerror("错误", f"运行 single_message_processor.py 失败:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误:\n{str(e)}")

def open_customers_folder():
    """Open the customers folder."""
    try:
        os.startfile('F:/autoAccountor/customers')
    except Exception as e:
        messagebox.showerror("错误", f"打开文件夹失败:\n{str(e)}")

def open_log_append():
    """Open the log_append.txt file and update the display."""
    global current_file_path
    try:
        current_file_path = 'F:/autoAccountor/log/log_append.txt'
        update_display(current_file_path)
    except Exception as e:
        messagebox.showerror("错误", f"打开日志文件失败:\n{str(e)}")

def open_current_info():
    """Open the 当前信息.txt file and update the display."""
    global current_file_path
    try:
        current_file_path = 'F:/autoAccountor/info/当前信息.txt'
        update_display(current_file_path)
    except Exception as e:
        messagebox.showerror("错误", f"打开当前信息文件失败:\n{str(e)}")

def open_chat_record():
    """Open the chat record file and update the display."""
    global current_file_path
    try:
        current_file_path = 'F:/autoAccountor/data/聊天记录/聚财浮球报账群(34375022090@chatroom)/聚财浮球报账群.txt'
        update_display(current_file_path)
    except Exception as e:
        messagebox.showerror("错误", f"打开聊天记录文件失败:\n{str(e)}")

def update_display(file_path):
    """Update the display with the content of the specified file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            display_text.delete(1.0, tk.END)
            display_text.insert(tk.END, content)
    except Exception as e:
        messagebox.showerror("错误", f"读取文件失败:\n{str(e)}")

def save_current_info():
    """Save the current content of the display to the current file."""
    try:
        with open(current_file_path, 'w', encoding='utf-8') as file:
            file.write(display_text.get(1.0, tk.END))
        messagebox.showinfo("成功", "内容保存成功.")
    except Exception as e:
        messagebox.showerror("错误", f"保存内容失败:\n{str(e)}")

app = tk.Tk()
app.title("运行脚本")
app.geometry("1000x600")  # Set the window size to 1000x600

style = ttk.Style()
style.configure("TButton", padding=20, relief="flat", background="#33ddff", font=("Helvetica", 10))

button_frame1 = ttk.Frame(app)
button_frame1.pack(pady=10)

button_frame2 = ttk.Frame(app)
button_frame2.pack(pady=10)

run_button = ttk.Button(button_frame1, text="更新记账", command=run_script)
run_button.pack(side=tk.LEFT, padx=5)

open_folder_button = ttk.Button(button_frame1, text="打开客户文件夹", command=open_customers_folder)
open_folder_button.pack(side=tk.LEFT, padx=5)

open_log_button = ttk.Button(button_frame1, text="打开日志文件", command=open_log_append)
open_log_button.pack(side=tk.LEFT, padx=5)

open_info_button = ttk.Button(button_frame1, text="打开当前信息", command=open_current_info)
open_info_button.pack(side=tk.LEFT, padx=5)

open_chat_button = ttk.Button(button_frame1, text="打开聊天记录", command=open_chat_record)
open_chat_button.pack(side=tk.LEFT, padx=5)

process_customers_button = ttk.Button(button_frame2, text="合计总球数", command=run_process_customers)
process_customers_button.pack(side=tk.LEFT, padx=5)

single_message_button = ttk.Button(button_frame2, text="单步执行", command=run_single_message_processor)
single_message_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(button_frame2, text="保存当前信息", command=save_current_info)
save_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the text display and scrollbar
text_frame = ttk.Frame(app)
text_frame.pack(pady=50, padx=150, fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = ttk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget with the scrollbar
display_text = tk.Text(text_frame, height=20, width=80, font=("Helvetica", 12), yscrollcommand=scrollbar.set)
display_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the scrollbar
scrollbar.config(command=display_text.yview)

update_display(current_file_path)  # Initially display 当前信息.txt

app.mainloop()
