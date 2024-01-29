import os
import sys
import time
import re
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import SessionNotCreatedException

def clear_screen():
    # 터미널 화면을 지우는 함수
    os.system('cls' if os.name == 'nt' else 'clear')

def get_driver_filenames():
    # OS에 따라 적절한 드라이버 파일 이름을 반환하는 함수
    if os.name == 'nt':  # Windows
        return 'chromedriver.exe', 'msedgedriver.exe'
    else:  # Linux and MacOS
        return 'chromedriver', 'msedgedriver'

def check_driver_existence(chrome_driver, edge_driver):
    # 드라이버 파일의 존재 여부를 확인하는 함수
    chrome_exists = os.path.exists(chrome_driver)
    edge_exists = os.path.exists(edge_driver)
    return chrome_exists, edge_exists

def initialize_driver(browser_choice, chrome_driver, edge_driver):
    # 선택한 브라우저에 따라 드라이버를 초기화하는 함수
    try:
        if browser_choice == 'chrome':
            service = ChromeService(executable_path=chrome_driver)
            options = ChromeOptions()
            return webdriver.Chrome(service=service, options=options)
        elif browser_choice == 'edge':
            service = EdgeService(executable_path=edge_driver)
            options = EdgeOptions()
            return webdriver.Edge(service=service, options=options)
    except SessionNotCreatedException as e:
        print(f"현재 설치되어 있는 {browser_choice.title()}의 버전에 맞는 {browser_choice.title()} 드라이버를 사용해 주세요!")
        return None

chrome_driver, edge_driver = get_driver_filenames()
chrome_exists, edge_exists = check_driver_existence(chrome_driver, edge_driver)

if not chrome_exists and not edge_exists:
    print("크롬 또는 엣지 브라우저 드라이버가 없습니다.")
    sys.exit()

browser_choice = 'chrome' if chrome_exists and not edge_exists else 'edge' if edge_exists and not chrome_exists else None

if not browser_choice:
    while True:
        user_choice = input("Which browser do you want to use? (1) Chrome (2) Edge: ")
        if user_choice == '1':
            browser_choice = 'chrome'
            break
        elif user_choice == '2':
            browser_choice = 'edge'
            break
        else:
            print("Invalid input. Please enter 1 for Chrome or 2 for Edge.")
            time.sleep(5)
            clear_screen()
            
def extract_youtube_id(url):
    # YouTube URL에서 영상 ID를 추출하는 함수
    parsed_url = urlparse(url)
    if parsed_url.netloc in ["youtube.com", "www.youtube.com", "music.youtube.com", "www.youtube-nocookie.com", "youtube-nocookie.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif parsed_url.netloc in ["youtu.be"]:
        return parsed_url.path[1:]
    return None

driver = initialize_driver(browser_choice, chrome_driver, edge_driver)
if driver is None:
    sys.exit()

while True:
    with open('music.txt', 'r') as f:
        urls = [url.strip() for url in f.readlines()]  # Read the URLs

    if not urls:
        print("No music to play. Exiting...")
        break

    url = urls[0]
    video_id = extract_youtube_id(url)
    if video_id is None:
        print("Invalid YouTube URL.")
        break

    driver.get(url)  # Play the music

    while True:
        time.sleep(0.001)  # Wait for 0.001 seconds
        current_video_id = extract_youtube_id(driver.current_url)
        if current_video_id != video_id:  # Check if the video ID has changed
            break

    # Remove the played music from the file by re-reading and writing everything except first line
    lines = open('music.txt', 'r').readlines()
    open('music.txt', 'w').writelines(lines[1:])
