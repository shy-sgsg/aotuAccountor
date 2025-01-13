'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-13 18:05:25
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-13 18:21:05
FilePath: \autoAccountor\single_message_processor.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import re
import tkinter as tk
from tkinter import simpledialog, messagebox

# Import the process_message function from autoAccountor.py
from autoAccountor import process_message, write_log_append, write_log_overwrite, read_current_info, write_current_info, current_info

current_info_path = 'F:/autoAccountor/info/当前信息.txt'
current_info = read_current_info(current_info_path)

def get_message():
    """Prompt the user to input a message."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    message = simpledialog.askstring("输入消息", "请输入要处理的消息:")
    root.destroy()
    return message

def main():
    """Main function to process a single message."""
    global current_info
    message = get_message()
    if message:
        try:
            process_message(message)
            write_current_info(current_info_path, current_info)
            messagebox.showinfo("成功", "消息处理成功")
        except Exception as e:
            messagebox.showerror("错误", f"{str(e)}")
    else:
        messagebox.showwarning("警告", "未输入消息")

if __name__ == "__main__":
    main()
