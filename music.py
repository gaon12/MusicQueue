import os
import sys
import time
import pandas as pd
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

def extract_youtube_id(url):
    # YouTube URL에서 영상 ID를 추출하는 함수
    parsed_url = urlparse(url)
    if parsed_url.netloc in ["youtube.com", "www.youtube.com", "music.youtube.com", "www.youtube-nocookie.com", "youtube-nocookie.com"]:
        video_id = parse_qs(parsed_url.query).get("v", [None])[0]
    elif parsed_url.netloc in ["youtu.be"]:
        video_id = parsed_url.path[1:]
    else:
        return None

    # 기본 YouTube URL 형식으로 반환
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return None

def read_playlist(file_path):
    # 플레이리스트 파일 읽기 (TSV 또는 XLSX)
    if file_path.endswith('.tsv'):
        return pd.read_csv(file_path, sep='\t')
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("지원되지 않는 파일 형식입니다.")

def update_playlist(file_path, playlist):
    # 플레이리스트 파일 업데이트
    if file_path.endswith('.tsv'):
        playlist.to_csv(file_path, sep='\t', index=False)
    elif file_path.endswith('.xlsx'):
        playlist.to_excel(file_path, index=False)

def find_playlist_file():
    # 플레이리스트 파일 찾기
    if os.path.exists('playlist.tsv'):
        return 'playlist.tsv', None
    elif os.path.exists('playlist.xlsx'):
        return 'playlist.xlsx', None
    elif os.path.exists('playlist.xls'):
        return None, "The xls file is not supported. Please convert to xlsx or tsv."
    return None, "playlist.tsv 또는 playlist.xlsx 파일을 찾을 수 없습니다."

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

driver = initialize_driver(browser_choice, chrome_driver, edge_driver)
if driver is None:
    sys.exit()

def initialize_playlist(file_path):
    # 플레이리스트 초기화 (Times와 ListenNums 설정)
    playlist = read_playlist(file_path)
    playlist['Times'] = playlist['Times'].fillna(1).astype(int)
    playlist['ListenNums'] = playlist['ListenNums'].fillna(0).astype(int)
    update_playlist(file_path, playlist)
    return playlist

# 플레이리스트 파일을 찾고 초기화합니다.
playlist_file, error_message = find_playlist_file()

if playlist_file is None:
    print(error_message)
    sys.exit()

playlist = initialize_playlist(playlist_file)

# 각 행에 대해 처리를 진행합니다.
for index, row in playlist.iterrows():
    if pd.isna(row['URL']):
        continue

    standard_url = extract_youtube_id(row['URL'])
    if standard_url is None:
        print("유효하지 않은 YouTube URL입니다.")
        continue

    times_to_play = row['Times']
    listen_nums = row['ListenNums']

    if listen_nums >= times_to_play:
        continue

    driver.get(standard_url)
    for _ in range(times_to_play - listen_nums):
        while True:
            time.sleep(0.001)
            current_video_id = extract_youtube_id(driver.current_url)
            if current_video_id != extract_youtube_id(standard_url):
                break
        playlist.at[index, 'ListenNums'] += 1
        update_playlist(playlist_file, playlist)  # 영상 재생 후 ListenNums 업데이트
