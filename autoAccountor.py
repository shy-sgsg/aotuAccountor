'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-10 17:13:47
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-25 00:10:36
FilePath: \autoAccountor\autoAccountor.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import datetime
import re
import sys
import os
from colorama import init, Fore
from wcwidth import wcswidth
from tkinter import messagebox, Tk
import pandas as pd

# Initialize Tkinter root
root = Tk()
root.withdraw()  # Hide the root window

init(autoreset=True)
sys.stdout.reconfigure(encoding='utf-8')

LOGGING_APPEND_ENABLED = True
LOGGING_OVERWRITE_ENABLED = True

current_info = {}

def show_error_prompt(error_message):
    """Show an error prompt with the option to ignore and continue."""
    return messagebox.askyesno("错误", f"{error_message}\n是否忽略错误并继续执行？")

def read_current_info(file_path):
    """Read current information from the specified file and return it as a dictionary."""
    global current_info
    data = {}
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        for line in lines:
            if "截止" in line:
                time_str = line.strip().split("截止 ")[1]
                try:
                    datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    data['time'] = time_str
                except ValueError:
                    error_message = f"Invalid time format: {time_str}"
                    if not show_error_prompt(error_message):
                        raise ValueError(error_message)
            elif "账户余额" in line:
                balance_str = line.strip().split("账户余额：")[1].replace("元", "")
                data['balance'] = int(balance_str)
            elif "小球库存" in line:
                small_ball_str = line.strip().split("小球库存：")[1].replace("包", "")
                data['small_ball_stock'] = int(small_ball_str)
            elif "大球库存" in line:
                big_ball_str = line.strip().split("大球库存：")[1].replace("包", "")
                data['big_ball_stock'] = int(big_ball_str)
    current_info = data
    return data

def write_current_info(file_path, data):
    """Write the current information to the specified file."""
    global current_info
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(
            f"截止 {data['time']}\n"
            f"账户余额：{data['balance']}元\n"
            f"小球库存：{data['small_ball_stock']}包\n"
            f"大球库存：{data['big_ball_stock']}包\n"
        )
    current_info = data

def log_current_info(data, log_type="all"):
    """Log the current information to the specified log type."""
    info_str = (
        f"截止 {data['time']}\n"
        f"账户余额：{data['balance']}元\n"
        f"小球库存：{data['small_ball_stock']}包\n"
        f"大球库存：{data['big_ball_stock']}包"
    )
    if log_type == "all":
        write_log_append(info_str)
        write_log_overwrite(info_str)
    elif log_type == "append":
        write_log_append(info_str)
    elif log_type == "overwrite":
        write_log_overwrite(info_str)

def locate_chat_record(chat_record_path, time):
    """Locate the chat record line that is after the specified time."""
    target_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    with open(chat_record_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            parts = lines[i].strip().split()
            if len(parts) < 2:
                continue
            record_time_str = parts[0] + " " + parts[1]
            try:
                record_time = datetime.datetime.strptime(record_time_str, "%Y-%m-%d %H:%M:%S")
                if record_time > target_time:
                    return i
            except ValueError:
                continue
    return -1

def write_log_append(message, newline=True, fixed_length=None):
    """Write a message to the append log file."""
    if LOGGING_APPEND_ENABLED:
        with open("log/log_append.txt", "a", encoding="utf-8", errors='ignore') as log_file:
            if fixed_length:
                message = adjust_to_fixed_length(message, fixed_length)
            log_file.write(message + ("\n" if newline else ""))

def write_log_overwrite(message, mode="a", newline=True, fixed_length=None):
    """Write a message to the overwrite log file."""
    if LOGGING_OVERWRITE_ENABLED:
        with open("log/log_overwrite.txt", mode, encoding="utf-8", errors='ignore') as log_file:
            if fixed_length:
                message = adjust_to_fixed_length(message, fixed_length)
            log_file.write(message + ("\n" if newline else ""))

def adjust_to_fixed_length(message, fixed_length):
    """Adjust the message to a fixed length by padding or truncating."""
    current_length = wcswidth(message)
    if current_length < fixed_length:
        message = message.ljust(fixed_length - current_length + len(message))
    elif current_length > fixed_length:
        while wcswidth(message) > fixed_length:
            message = message[:-1]
    return message

def process_message(line):
    """Process a single message line and update the current information."""
    global current_info
    quantity = 0
    log_message = None
    customer_name = None
    clear_account_flag = 0

    patterns = {
        '收入': r'收.*(\d+)元',
        '支出': r'(\d+)元|(\d+)万|一共(\d+)',
        '大球入库': r'大球.*入库|入库.*大球|大球入库',
        '小球入库': r'入库',
        '大球3.2出库': r'仓库发3.2|仓库3.2',
        '大球2.5出库': r'仓库发2.5|仓库2.5',
        '小球出库': r'仓库发|仓库'
    }

    if re.search(r'清账|全清|已清|至.*清账', line):
        clear_account_flag = 1

    line = re.sub(r'(?<!包)(?<!元)，(?!费)', '', line)

    if re.search(r'一共', line):
        line = re.sub(r'.*一共', '一共', line)

    parts = line.split('，')
    for part in parts:
        for message_type, pattern in patterns.items():
            if re.search(pattern, part):
                if '球' in message_type:
                    quantity = extract_number(part)
                else:
                    if re.search(r'(\d+)元', part):
                        quantity = int(re.search(r'(\d+)元', part).group(1))
                    elif re.search(r'(\d+)万', part):
                        quantity = int(re.search(r'(\d+)万', part).group(1)) * 10000
                    elif re.search(r'一共(\d+)', part):
                        quantity = int(re.search(r'一共(\d+)', part).group(1))
                if not quantity:
                    log_message = message_type + "错误: 未提取到数字"
                    write_log_append(log_message)
                    write_log_overwrite(log_message)
                    error_message = f"{message_type}错误: 未提取到数字: {part}"
                    if not show_error_prompt(error_message):
                        raise ValueError(error_message)
                    break
                if message_type == '收入':
                    current_info['balance'] += quantity
                    log_message = f" 收入: {quantity}"
                    customer_name = extract_customer_name(part)
                    break
                elif message_type == '支出':
                    current_info['balance'] -= quantity
                    log_message = f" 支出: {quantity}"
                    break
                elif message_type == '小球入库':
                    current_info['small_ball_stock'] += quantity
                    log_message = f" 小球入库: {quantity}"
                    break
                elif message_type == '小球出库':
                    current_info['small_ball_stock'] -= quantity
                    log_message = f" 小球出库: {quantity}"
                    customer_name = extract_customer_name(part)
                    break
                elif message_type == '大球入库':
                    current_info['big_ball_stock'] += quantity
                    log_message = f" 大球入库: {quantity}"
                    break
                elif message_type == '大球2.5出库':
                    current_info['big_ball_stock'] -= quantity
                    log_message = f" 大球2.5出库: {quantity}"
                    customer_name = extract_customer_name(part)
                    break
                elif message_type == '大球3.2出库':
                    current_info['big_ball_stock'] -= quantity
                    log_message = f" 大球3.2出库: {quantity}"
                    customer_name = extract_customer_name(part)
                    break
        if log_message:
            write_log_append(log_message)
            write_log_overwrite(log_message)
            if customer_name:
                log_to_customer_excel(customer_name, message_type, quantity, part)
        elif not clear_account_flag:
            log_message = "错误: 未知的消息类型"
            write_log_append(log_message)
            write_log_overwrite(log_message)
            error_message = f"错误: 未知的消息类型: {part}"
            if not show_error_prompt(error_message):
                raise ValueError(error_message)

def extract_number(text):
    """Extract the first number found in the text."""
    text_copy = re.sub(r'\d{1,2}\.\d{1,2}|\d+年', '', text)
    match = re.search(r'\d+', text_copy)
    if match:
        return int(match.group(0))
    return 0

def extract_customer_name(text):
    """Extract the customer name from the text."""
    text_copy = re.sub(r'\d{1,2}\.\d{1,2}号|\d+年| |3.2|2.5|球|款|浮', '', text)
    match = re.search(r'发(\w+?)(?=\d|$)|收(\w+?)(?=\d|$)', text_copy)
    if match:
        return match.group(1) or match.group(2)
    else:
        match = re.search(r'仓库(\w+?)(?=\d|$)', text_copy)
        if match:
            return match.group(1) or match.group(2)
        else:
            print(Fore.RED + f"错误: 未找到客户名字: {text}")
    return None

def extract_date(text):
    """Extract the date from the text."""
    match = re.search(r'\d{1,2}\.\d{1,2}|\d{1,2},\d{1,2}', text)
    if match:
        return match.group(0)
    return None

def log_to_customer_excel(customer_name, message_type, quantity, line):
    """Log the message to the customer's Excel file."""
    date = extract_date(line)
    if not date:
        date = current_info['time'][5:16]  # Use the message record's time if date extraction fails
    
    customer_file_path = f"customers/{customer_name}.xlsx"
    if os.path.exists(customer_file_path):
        try:
            df = pd.read_excel(customer_file_path)
        except PermissionError:
            print(Fore.RED + f"错误: 无法读取文件: {customer_file_path}")
            return
    else:
        df = pd.DataFrame(columns=['日期', '收入', '小球出库', '大球2.5出库', '大球3.2出库'])
    
    new_row = pd.DataFrame({'日期': [date], message_type: [quantity]})
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Force the date column to be text type and other columns to be numeric type
    for col in df.columns:
        if col == '日期':
            df[col] = df[col].astype(str)
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.to_excel(customer_file_path, index=False)

def is_time_line(line):
    """Check if the line contains a timestamp."""
    return re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line) is not None

def process_chat_record(chat_record_path, target_time):
    """Process the chat record and update the current information."""
    skip_processing = False
    start_line = locate_chat_record(chat_record_path, target_time)
    if start_line == -1:
        write_log_overwrite("未找到目标时间之后的记录。\n\n\n")
        sys.exit(0)  # Safely exit the program
    with open(chat_record_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        for i in range(start_line, len(lines)):
            line = lines[i].strip()
            match = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
            if match:
                current_info['time'] = match.group(0)
                sender = line.split()[-1]
                if sender == "李荣芳":
                    skip_processing = True
                else:
                    skip_processing = False
            elif line and not skip_processing:
                time_str = current_info['time'][5:16]  # Exclude year and seconds
                log_message = f"{time_str}   {line}"
                write_log_append(log_message, newline=False, fixed_length=60)
                write_log_overwrite(log_message, newline=False, fixed_length=60)
                process_message(line)
    write_log_append("\n\n\n")
    write_log_overwrite("", mode="a")

def get_log_line_count(log_file_path):
    """Get the number of lines in the log file."""
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
        return len(log_file.readlines())

def truncate_log_file(log_file_path, line_count):
    """Truncate the log file to the specified number of lines."""
    with open(log_file_path, 'r+', encoding='utf-8', errors='ignore') as log_file:
        lines = log_file.readlines()
        log_file.seek(0)
        log_file.writelines(lines[:line_count])
        log_file.truncate()

def backup_customer_files():
    """Backup the contents of all customer files."""
    customer_files = {}
    for filename in os.listdir("customers"):
        if filename.endswith(".xlsx"):
            file_path = os.path.join("customers", filename)
            try:
                customer_files[file_path] = pd.read_excel(file_path)
            except PermissionError:
                print(Fore.RED + f"错误: 无法读取文件: {file_path}")
    return customer_files

def restore_customer_files(customer_files):
    """Restore the contents of all customer files from the backup."""
    for file_path, df in customer_files.items():
        df.to_excel(file_path, index=False)

def main():
    """Main function to execute the script."""
    global current_info
    current_info_path = "info/当前信息.txt"
    chat_record_path = "D:/MemoTrace/data/聊天记录/聚财浮球报账群(34375022090@chatroom)/聚财浮球报账群.txt"
    
    initial_append_log_lines = get_log_line_count("log/log_append.txt")
    customer_files_backup = backup_customer_files()
    
    if LOGGING_OVERWRITE_ENABLED:
        with open("log/log_overwrite.txt", "w", encoding="utf-8") as log_file:
            log_file.write("")
    
    try:
        current_info = read_current_info(current_info_path)
        process_chat_record(chat_record_path, current_info['time'])
        log_current_info(current_info, log_type="all")
        write_current_info(current_info_path, current_info)  # Update 当前信息.txt with current_info values
    except Exception as e:
        error_message = f"运行失败: {str(e)}"
        messagebox.showerror("错误", error_message)
        
        truncate_log_file("log/log_append.txt", initial_append_log_lines)
        restore_customer_files(customer_files_backup)
        
        raise e  # Raise the exception to exit with a non-zero code

if __name__ == "__main__":
    main()