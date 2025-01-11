'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-10 17:13:47
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-12 01:13:21
FilePath: \autoAccountor\autoAccountor.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import datetime
import re
import sys
from colorama import init, Fore
from wcwidth import wcswidth

init(autoreset=True)
sys.stdout.reconfigure(encoding='utf-8')

LOGGING_APPEND_ENABLED = True
LOGGING_OVERWRITE_ENABLED = True

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
                    raise ValueError(f"Invalid time format: {time_str}")
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

def process_message(line):
    global current_info
    clean_line = re.sub(r'🏀', '', line)
    quantity = 0
    log_message = None

    patterns = {
        '收入': r'收.*(\d+)元',
        '支出': r'(\d+)元',
        '大球入库': r'大球.*入库|入库.*大球|大球入库',
        '小球入库': r'入库',
        '大球3.2出库': r'仓库发3.2|仓库3.2',
        '大球2.5出库': r'仓库发2.5|仓库2.5',
        '小球出库': r'仓库发|仓库'
    }

    for message_type, pattern in patterns.items():
        if re.search(pattern, clean_line):
            match = re.search(r'(\d+)包', line) if '球' in message_type else re.search(pattern, line)
            if match:
                quantity = int(match.group(1))
            if message_type == '收入':
                current_info['balance'] += quantity
                log_message = f" 收入: {quantity}"
            elif message_type == '支出':
                current_info['balance'] -= quantity
                log_message = f" 支出: {quantity}"
            elif message_type == '小球入库':
                current_info['small_ball_stock'] += quantity
                log_message = f" 小球入库: {quantity}"
            elif message_type == '小球出库':
                current_info['small_ball_stock'] -= quantity
                log_message = f" 小球出库: {quantity}"
            elif message_type == '大球入库':
                current_info['big_ball_stock'] += quantity
                log_message = f" 大球入库: {quantity}"
            elif message_type == '大球2.5出库':
                current_info['big_ball_stock'] -= quantity
                log_message = f" 大球2.5出库: {quantity}"
            elif message_type == '大球3.2出库':
                current_info['big_ball_stock'] -= quantity
                log_message = f" 大球3.2出库: {quantity}"
            break
    if log_message:
        write_log_append(log_message)
        write_log_overwrite(log_message)
    else:
        log_message = "错误: 未知的消息类型"
        write_log_append(log_message)
        write_log_overwrite(log_message)
        print(Fore.RED + f"错误: 未知的消息类型: {line}")

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
    chat_record_path = "D:/MemoTrace/data/聊天记录/聚财浮球报账群(34375022090@chatroom)/聚财浮球报账群.txt"
    if LOGGING_OVERWRITE_ENABLED:
        with open("log/log_overwrite.txt", "w", encoding="utf-8") as log_file:
            log_file.write("")
    current_info = readInfo(current_info_path)
    process_chat_record(chat_record_path, current_info['time'])
    log_current_info(current_info, log_type="overwrite")

if __name__ == "__main__":
    main()