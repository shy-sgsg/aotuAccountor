'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-10 17:13:47
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-12 23:16:45
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

# Initialize Tkinter root
root = Tk()
root.withdraw()  # Hide the root window

init(autoreset=True)
sys.stdout.reconfigure(encoding='utf-8')

LOGGING_APPEND_ENABLED = True
LOGGING_OVERWRITE_ENABLED = True

def show_error_prompt(error_message):
    return messagebox.askyesno("错误", f"{error_message}\n是否忽略错误并继续执行？")

def readInfo(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if "截止" in line:
                # 提取时间信息
                time_str = line.strip().split("截止 ")[1]
                try:
                    datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    data['time'] = time_str
                except ValueError:
                    error_message = f"Invalid time format: {time_str}"
                    if not show_error_prompt(error_message):
                        raise ValueError(error_message)
            elif "账户余额" in line:
                # 提取账户余额信息，并将其转换为整数
                balance_str = line.strip().split("账户余额：")[1].replace("元", "")
                data['balance'] = int(balance_str)
            elif "小球库存" in line:
                # 提取小球库存信息，并将其转换为整数
                small_ball_str = line.strip().split("小球库存：")[1].replace("包", "")
                data['small_ball_stock'] = int(small_ball_str)
            elif "大球库存" in line:
                # 提取2.5大球库存信息，并将其转换为整数
                big_ball_2_5_str = line.strip().split("大球库存：")[1].replace("包", "")
                data['big_ball_stock'] = int(big_ball_2_5_str)
    log_current_info(data, log_type="all")
    return data

def locate_chat_record(chat_record_path, time):
    target_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    with open(chat_record_path, 'r', encoding='utf-8') as file:
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
    if LOGGING_APPEND_ENABLED:
        with open("log/log_append.txt", "a", encoding="utf-8") as log_file:
            if fixed_length:
                message = adjust_to_fixed_length(message, fixed_length)
            log_file.write(message + ("\n" if newline else ""))

def write_log_overwrite(message, mode="a", newline=True, fixed_length=None):
    if LOGGING_OVERWRITE_ENABLED:
        with open("log/log_overwrite.txt", mode, encoding="utf-8") as log_file:
            if fixed_length:
                message = adjust_to_fixed_length(message, fixed_length)
            log_file.write(message + ("\n" if newline else ""))

def adjust_to_fixed_length(message, fixed_length):
    current_length = wcswidth(message)
    if current_length < fixed_length:
        message = message.ljust(fixed_length - current_length + len(message))
    elif current_length > fixed_length:
        while wcswidth(message) > fixed_length:
            message = message[:-1]
    return message

def log_current_info(data, log_type="all"):
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

def write_current_info(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(
            f"截止 {data['time']}\n"
            f"账户余额：{data['balance']}元\n"
            f"小球库存：{data['small_ball_stock']}包\n"
            f"大球库存：{data['big_ball_stock']}包\n"
            
        )

def extract_number(text):
    # Create a copy of the text to avoid modifying the original message
    text_copy = re.sub(r'\d{1,2}\.\d{1,2}|\d+年', '', text)
    match = re.search(r'\d+', text_copy)
    if match:
        return int(match.group(0))
    return 0

def process_message(line):
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

    # Check for clear account flag
    if re.search(r'清账|全清|已清|至.*清账', line):
        clear_account_flag = 1

    # Remove commas not between "包" and "费" or after "元"
    line = re.sub(r'(?<!包)(?<!元)，(?!费)', '', line)

    # Remove content before "一共"
    if re.search(r'一共', line):
        line = re.sub(r'.*一共', '一共', line)

    # Split the line by commas and process each part separately
    parts = line.split('，')
    for part in parts:
        for message_type, pattern in patterns.items():
            if re.search(pattern, part):
                if '球' in message_type:
                    quantity = extract_number(part)
                else:
                    if re.search(r'(\d+)元', part):
                        quantity = int(re.search(r'(\d+)元', part).group(1))  # Corrected to group(1)
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
                if message_type == '收入': 
                    log_message = re.sub(r'入', '', log_message) + '元'
                else:
                    log_message = '发' + re.sub(r'出库', '', log_message) + '包'
                log_to_customer_file(customer_name, log_message, part)
        elif not clear_account_flag:
            log_message = "错误: 未知的消息类型"
            write_log_append(log_message)
            write_log_overwrite(log_message)
            error_message = f"错误: 未知的消息类型: {part}"
            if not show_error_prompt(error_message):
                raise ValueError(error_message)

def extract_customer_name(text):
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
    match = re.search(r'\d{1,2}\.\d{1,2}|\d{1,2},\d{1,2}', text)
    if match:
        return match.group(0)
    return None

def log_to_customer_file(customer_name, message, line):
    date = extract_date(line)
    if date:
        formatted_message = f"{date}号 {message}"
    else:
        formatted_message = f"错误：未找到日期"
        print(Fore.RED + f"错误: 未找到日期: {line}")
    customer_file_path = f"customers/{customer_name}.txt"
    with open(customer_file_path, 'a', encoding='utf-8') as file:
        file.write(formatted_message + '\n')

def is_time_line(line):
    return re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line) is not None

def process_chat_record(chat_record_path, target_time):
    skip_processing = False
    start_line = locate_chat_record(chat_record_path, target_time)
    if start_line == -1:
        write_log_append("No records found after the target time.\n\n\n")
        write_log_overwrite("No records found after the target time.\n\n\n")
        return
    with open(chat_record_path, 'r', encoding='utf-8') as file:
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

def main():
    global current_info
    current_info_path = "info/当前信息.txt"
    chat_record_path = "D:/MemoTrace/data/聊天记录/聚财浮球报账群(34375022090@chatroom)/聚财浮球报账群.txt"
    if LOGGING_OVERWRITE_ENABLED:
        with open("log/log_overwrite.txt", "w", encoding="utf-8") as log_file:
            log_file.write("")
    current_info = readInfo(current_info_path)
    process_chat_record(chat_record_path, current_info['time'])
    log_current_info(current_info, log_type="overwrite")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_message = f"运行失败: {str(e)}"
        # if not show_error_prompt(error_message):
        messagebox.showerror("错误", error_message)
        raise e  # Raise the exception to exit with a non-zero code