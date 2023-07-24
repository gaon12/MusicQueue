import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 사용자에게 어떤 웹드라이버를 사용할지 물어봄
while True:
    browser_choice = input("Which browser do you want to use? (1) Chrome (2) Edge: ")

    # 선택한 브라우저에 따라 웹드라이버 설정
    if browser_choice == '1':
        service = ChromeService(executable_path='chromedriver.exe')
        options = ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        break
    elif browser_choice == '2':
        service = EdgeService(executable_path='msedgedriver.exe') # Edge를 사용하려면, Selenium WebDriver for Edge를 설치해야 합니다.
        options = EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)
        break
    else:
        print("Invalid input. Please enter 1 for Chrome or 2 for Edge.")
        time.sleep(5)
        clear_screen()

while True:
    with open('music.txt', 'r') as f:
        urls = [url.strip() for url in f.readlines()]  # Read the URLs

    if not urls:
        print("No music to play. Exiting...")
        break

    url = urls[0]
    driver.get(url)  # Play the music

    while True:
        time.sleep(0.001)  # Wait for 0.001 seconds
        if driver.current_url != url:  # Check if the current URL has changed
            break

    # Remove the played music from the file by re-reading and writing everything except first line
    lines = open('music.txt', 'r').readlines()
    open('music.txt', 'w').writelines(lines[1:])
