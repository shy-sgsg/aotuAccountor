'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-12 20:43:47
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-13 00:16:19
FilePath: \autoAccountor\process_customers.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

from autoAccountor import read_current_info, write_current_info

current_info_path = 'F:/autoAccountor/info/当前信息.txt'
current_info = read_current_info(current_info_path)

def process_customer_file(file_path):
    """Process a single customer file and return the total number of packages."""
    total = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(r'(\d+)包', line)
            if match:
                total += int(match.group(1))
    return total

def process_all_customers(folder_path):
    """Process all customer files in the specified folder and return a dictionary of totals."""
    customer_totals = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            total = process_customer_file(file_path)
            customer_totals[filename] = total
    return customer_totals

def main():
    """Main function to process all customer files and print the totals."""
    global current_info
    folder_path = 'F:/autoAccountor/customers'
    customer_totals = process_all_customers(folder_path)
    for customer, total in customer_totals.items():
        print(f"{customer}: {total}包")
    write_current_info(current_info_path, current_info)

if __name__ == "__main__":
    main()
