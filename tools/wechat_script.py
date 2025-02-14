import os
import sys
import time

try:
    import pyautogui
except ImportError:
    print("pyautogui module is not installed. Please install it using 'pip install pyautogui'")
    sys.exit(1)

try:
    import cv2
except ImportError:
    print("opencv-python module is not installed. Please install it using 'pip install opencv-python'")
    sys.exit(1)

# Define base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WECHAT_PATH = 'C:/Program Files (x86)/Tencent/WeChat/WeChat.exe'
MEMOTRACE_PATH = 'D:/MemoTrace/MemoTrace.exe'
PIC_DIR = os.path.join(BASE_DIR, 'pic')

def log_error(message):
    """Log an error message to a log file."""
    log_file_path = os.path.join(BASE_DIR, 'error_log.txt')
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        print(f"Failed to write to log file: {str(e)}")

def log_info(message):
    """Log an info message to a log file."""
    log_file_path = os.path.join(BASE_DIR, 'info_log.txt')
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        print(f"Failed to write to log file: {str(e)}")

def open_wechat():
    """Open WeChat application."""
    try:
        os.startfile(WECHAT_PATH)
        time.sleep(1)  # Wait for WeChat to open
    except Exception as e:
        error_message = f"Error opening WeChat: {str(e)}"
        print(error_message)
        log_error(error_message)

def click_button(image_name, wait_time=1):
    """Locate and click a button specified by the image name."""
    image_path = os.path.join(PIC_DIR, f'{image_name}.png')
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

def locate_image(image_name, confidence=0.8):
    """Locate an image on the screen."""
    image_path = os.path.join(PIC_DIR, f'{image_name}.png')
    try:
        return pyautogui.locateOnScreen(image_path, confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None

def logout_wechat():
    """Logout WeChat application by clicking the specified symbol and navigating to the logout option."""
    try:
        # Locate and click the buttons
        click_button('WeChat001')
        click_button('WeChatSettings')
        click_button('WeChatLogout')
        click_button('WeChatConfirmLogout')
    except Exception as e:
        error_message = f"Error logging out of WeChat: {str(e)}"
        print(error_message)
        log_error(error_message)

def login_wechat():
    """Login to WeChat application by clicking the login button."""
    # Locate and click the login button
    if not click_button('WeChatLogin'):
        click_button('WeChatLogin2')
    
    # Wait until the logging in screen appears
    while True:
        if locate_image('WeChat001'):
            break
        time.sleep(1)
    log_info("WeChat login successful")

def open_memotrace():
    """Open MemoTrace application."""
    try:
        os.startfile(MEMOTRACE_PATH)
        time.sleep(5)  # Wait for MemoTrace to open
    except Exception as e:
        error_message = f"Error opening MemoTrace: {str(e)}"
        print(error_message)
        log_error(error_message)

def parse_info():
    # Locate and click the buttons
    click_button('toolbox')
    click_button('GetInfo')
    click_button('GetInfo_yes', wait_time=5)
    while True:
        if locate_image('none'):
            click_button('GetInfo')
            click_button('GetInfo_yes', wait_time=5)
        else:
            break
        time.sleep(1)

    # Click the "增量解析" button
    click_button('ParseIncrement', wait_time=5)
    while True:
        if locate_image('ok'):
            click_button('ok')
            break
        time.sleep(1)
    time.sleep(3)

def search_and_export():
    """Search for '学习资料' in the search bar and click the '导出聊天记录' button."""
    try:
        # Locate and click the buttons
        click_button('data', wait_time=1)
        click_button('export', wait_time=1)
        click_button('choose', wait_time=1)
        click_button('lastchoice', wait_time=1)
        while True:
            if locate_image('lastchoice'):
                click_button('start')
                break
            else:
                click_button('choose', wait_time=1)
                click_button('lastchoice', wait_time=1)
            time.sleep(1)
        # click_button('start')
        while True:
            if locate_image('yes'):
                click_button('yes')
                break
            time.sleep(1)
        # click_button('close')
    except Exception as e:
        error_message = f"Error searching and exporting chat records: {str(e)}"
        print(error_message)
        log_error(error_message)

def main():
    """Main function to open WeChat, logout, login again, open MemoTrace, and perform actions."""
    open_wechat()
    logout_wechat()
    login_wechat()
    open_memotrace()
    parse_info()
    search_and_export()
    
if __name__ == "__main__":
    main()
