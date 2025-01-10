'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-10 17:13:47
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-11 00:27:37
FilePath: \autoAccountor\autoAccountor.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import datetime
import re
from colorama import init, Fore

init(autoreset=True)

LOGGING_APPEND_ENABLED = True
LOGGING_OVERWRITE_ENABLED = True

def readInfo(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if "截止" in line:
                # 提取时间信息
                data['time'] = line.strip().split("截止 ")[1]
            elif "账户余额" in line:
                # 提取账户余额信息，并将其转换为整数
                balance_str = line.strip().split("账户余额：")[1].replace("元", "")
                data['balance'] = int(balance_str)
            elif "小球库存" in line:
                # 提取小球库存信息，并将其转换为整数
                small_ball_str = line.strip().split("小球库存：")[1].replace("包", "")
                data['small_ball_stock'] = int(small_ball_str)
            elif "2.5大球库存" in line:
                # 提取2.5大球库存信息，并将其转换为整数
                big_ball_2_5_str = line.strip().split("2.5大球库存：")[1].replace("包", "")
                data['big_ball_2_5_stock'] = int(big_ball_2_5_str)
            elif "3.2大球库存" in line:
                # 提取3.2大球库存信息，并将其转换为整数
                big_ball_3_2_str = line.strip().split("3.2大球库存：")[1].replace("包", "")
                data['big_ball_3_2_stock'] = int(big_ball_3_2_str)
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
                    # write_log_append(f"Start Line: {i}")
                    # write_log_overwrite(f"Start Line: {i}")
                    return i
            except ValueError:
                continue
    return -1

def write_log_append(message, newline=True):
    if LOGGING_APPEND_ENABLED:
        with open("log/log_append.txt", "a", encoding="utf-8") as log_file:
            log_file.write(message + ("\n" if newline else "  "))

def write_log_overwrite(message, mode="a", newline=True):
    if LOGGING_OVERWRITE_ENABLED:
        with open("log/log_overwrite.txt", mode, encoding="utf-8") as log_file:
            log_file.write(message + ("\n" if newline else "  "))

def log_current_info(data, log_type="all"):
    info_str = (
        f"截止 {data['time']}\n"
        f"账户余额：{data['balance']}元\n"
        f"小球库存：{data['small_ball_stock']}包\n"
        f"2.5大球库存：{data['big_ball_2_5_stock']}包\n"
        f"3.2大球库存：{data['big_ball_3_2_stock']}包"
    )
    if log_type == "all":
        write_log_append(info_str)
        write_log_overwrite(info_str)
    elif log_type == "append":
        write_log_append(info_str)
    elif log_type == "overwrite":
        write_log_overwrite(info_str)

def determine_message_type(line):
    if re.search(r'收.*\d+元', line):
        return 'income'
    elif re.search(r'支出\d+元|花费\d+元|吃饭\d+元|消费\d+元|费用\d+元|花\d+元|买.*\d+元', line):
        return 'expense'
    elif re.search(r'小球.*入库', line):
        return 'small_ball_in'
    elif re.search(r'小球.*仓库发货', line):
        return 'small_ball_out'
    elif re.search(r'2.5大球入库', line):
        return 'big_ball_2_5_in'
    elif re.search(r'2.5大球仓库发货', line):
        return 'big_ball_2_5_out'
    elif re.search(r'3.2大球入库', line):
        return 'big_ball_3_2_in'
    elif re.search(r'3.2大球仓库发货', line):
        return 'big_ball_3_2_out'
    return None

def extract_number(line):
    # Exclude specific patterns like "2.5球", "3.2球", and dates like "12.30号"
    line = re.sub(r'2\.5球|3\.2球|2\.5大球|3\.2大球|\d{1,2}\.\d{1,2}号', '', line)
    match = re.search(r'(\d+)', line)
    if match:
        return int(match.group(1))
    return 0

def process_single_line(line):
    global current_info
    message_type = determine_message_type(line)
    if message_type == 'income':
        amount = extract_number(line)
        current_info['balance'] += amount
        write_log_append(f"income: {amount}")
        write_log_overwrite(f"income: {amount}")
    elif message_type == 'expense':
        amount = extract_number(line)
        current_info['balance'] -= amount
        write_log_append(f"expense: {amount}")
        write_log_overwrite(f"expense: {amount}")
    elif message_type == 'small_ball_in':
        quantity = extract_number(line)
        current_info['small_ball_stock'] += quantity
        write_log_append(f"small_ball_in: {quantity}")
        write_log_overwrite(f"small_ball_in: {quantity}")
    elif message_type == 'small_ball_out':
        quantity = extract_number(line)
        current_info['small_ball_stock'] -= quantity
        write_log_append(f"small_ball_out: {quantity}")
        write_log_overwrite(f"small_ball_out: {quantity}")
    elif message_type == 'big_ball_2_5_in':
        quantity = extract_number(line)
        current_info['big_ball_2_5_stock'] += quantity
        write_log_append(f"big_ball_2_5_in: {quantity}")
        write_log_overwrite(f"big_ball_2_5_in: {quantity}")
    elif message_type == 'big_ball_2_5_out':
        quantity = extract_number(line)
        current_info['big_ball_2_5_stock'] -= quantity
        write_log_append(f"big_ball_2_5_out: {quantity}")
        write_log_overwrite(f"big_ball_2_5_out: {quantity}")
    elif message_type == 'big_ball_3_2_in':
        quantity = extract_number(line)
        current_info['big_ball_3_2_stock'] += quantity
        write_log_append(f"big_ball_3_2_in: {quantity}")
        write_log_overwrite(f"big_ball_3_2_in: {quantity}")
    elif message_type == 'big_ball_3_2_out':
        quantity = extract_number(line)
        current_info['big_ball_3_2_stock'] -= quantity
        write_log_append(f"big_ball_3_2_out: {quantity}")
        write_log_overwrite(f"big_ball_3_2_out: {quantity}")
    else:
        print(f"\033[91mError: Unknown message type for line: {line}\033[0m")
        write_log_append("Error: Unknown message type")
        write_log_overwrite("Error: Unknown message type")

def is_time_line(line):
    # Match lines that start with a date in the format YYYY-MM-DD HH:MM:SS
    return re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line) is not None

def process_chat_record(chat_record_path, target_time):
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
                current_info['time'] = match.group(0)  # Update the current information's time
            elif line:
                write_log_append(f"{current_info['time']} {line}", newline=False)
                write_log_overwrite(f"{current_info['time']} {line}", newline=False)
                process_single_line(line)
    write_log_append("\n\n\n")  # Add a blank line at the end of each run
    write_log_overwrite("", mode="a")  # Add a blank line at the end of each run

def write_current_info(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(
            f"截止 {data['time']}\n"
            f"账户余额：{data['balance']}元\n"
            f"小球库存：{data['small_ball_stock']}包\n"
            f"2.5大球库存：{data['big_ball_2_5_stock']}包\n"
            f"3.2大球库存：{data['big_ball_3_2_stock']}包\n"
        )

def main():
    global current_info
    current_info_path = "info/当前信息.txt"
    chat_record_path = "info/聊天记录.txt"
    if LOGGING_OVERWRITE_ENABLED:
        with open("log/log_overwrite.txt", "w", encoding="utf-8") as log_file:
            log_file.write("")  # Clear the file at the start of each run
    current_info = readInfo(current_info_path)
    process_chat_record(chat_record_path, current_info['time'])
    log_current_info(current_info, log_type="overwrite")
    write_current_info(current_info_path, current_info)

if __name__ == "__main__":
    main()