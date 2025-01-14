'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-14 17:13:56
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-14 22:11:49
FilePath: \autoAccountor\wechat_script.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import time
import pyautogui

def log_error(message):
    """Log an error message to a log file."""
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error_log.txt')
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        print(f"Failed to write to log file: {str(e)}")

def log_info(message):
    """Log an info message to a log file."""
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'info_log.txt')
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        print(f"Failed to write to log file: {str(e)}")

def open_wechat():
    """Open WeChat application."""
    try:
        os.startfile('C:/Program Files (x86)/Tencent/WeChat/WeChat.exe')
        time.sleep(1)  # Wait for WeChat to open
    except Exception as e:
        error_message = f"Error opening WeChat: {str(e)}"
        print(error_message)
        log_error(error_message)

def logout_wechat():
    """Logout WeChat application by clicking the specified symbol and navigating to the logout option."""
    try:
        # Define the absolute paths for the image files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        symbol_path = os.path.join(base_dir, 'pic', 'WeChat001.png')
        settings_button_path = os.path.join(base_dir, 'pic', 'WeChatSettings.png')
        logout_button_path = os.path.join(base_dir, 'pic', 'WeChatLogout.png')
        confirm_button_path = os.path.join(base_dir, 'pic', 'WeChatConfirmLogout.png')

        # Locate and click the symbol in the bottom left corner
        if not click_button(symbol_path):
            return
        # Locate and click the settings button
        click_button(settings_button_path)
        # Locate and click the logout button
        click_button(logout_button_path)
        # Confirm logout
        click_button(confirm_button_path)
    except Exception as e:
        error_message = f"Error logging out of WeChat: {str(e)}"
        print(error_message)
        log_error(error_message)

def login_wechat():
    """Login to WeChat application by clicking the login button."""
    # Define the absolute path for the login button images
    base_dir = os.path.dirname(os.path.abspath(__file__))
    login_button_path = os.path.join(base_dir, 'pic', 'WeChatLogin.png')
    login_button2_path = os.path.join(base_dir, 'pic', 'WeChatLogin2.png')
    logging_in_path = os.path.join(base_dir, 'pic', 'WeChatLogining.png')

    # Locate and click the login button
    if not click_button(login_button_path):
        click_button(login_button2_path)
    
    # Wait until the logging in screen appears
    while True:
        try:
            if pyautogui.locateOnScreen(logging_in_path, confidence=0.8):
                break
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)
    time.sleep(10)  # Wait for WeChat to log in
    log_info("WeChat login successful")

def open_memotrace():
    """Open MemoTrace application."""
    try:
        os.startfile('D:/MemoTrace/MemoTrace.exe')
        time.sleep(5)  # Wait for MemoTrace to open
    except Exception as e:
        error_message = f"Error opening MemoTrace: {str(e)}"
        print(error_message)
        log_error(error_message)

def click_button(image_path, wait_time=0.5):
    """Locate and click a button specified by the image path."""
    try:
        button = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if button:
            pyautogui.click(button)
            time.sleep(wait_time)
            return True
        else:
            error_message = f"Image not found: {image_path}"
            print(error_message)
            log_error(error_message)
            return False
    except Exception as e:
        error_message = f"Error clicking button {image_path}: {str(e)}"
        print(error_message)
        log_error(error_message)
        return False

def parse_info():
    # Define the absolute paths for the MemoTrace button images
    base_dir = os.path.dirname(os.path.abspath(__file__))
    open_toolbox_button_path = os.path.join(base_dir, 'pic', 'toolbox.png')
    get_info_button_path = os.path.join(base_dir, 'pic', 'GetInfo.png')
    get_info_yes_button_path = os.path.join(base_dir, 'pic', 'GetInfo_yes.png')
    parse_increment_button_path = os.path.join(base_dir, 'pic', 'ParseIncrement.png')
    ok_button_path = os.path.join(base_dir, 'pic', 'ok.png')

    click_button(open_toolbox_button_path, wait_time=1)

    # Click the "获取信息" button
    click_button(get_info_button_path)  # Wait longer for information retrieval
    click_button(get_info_yes_button_path, wait_time=5)

    # Click the "增量解析" button
    click_button(parse_increment_button_path, wait_time=10)  # Wait for parsing to complete
    click_button(ok_button_path)

def main():
    """Main function to open WeChat, logout, login again, open MemoTrace, and perform actions."""
    open_wechat()
    logout_wechat()
    login_wechat()
    open_memotrace()
    parse_info()
    
if __name__ == "__main__":
    main()
