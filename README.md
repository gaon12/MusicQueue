# MusicQueue
유튜브 영상을 차례대로 출력하는 파이썬 코드!

# 사용 방법
## 파이썬 코드 실행
1. 본 깃허브 저장소를 [다운로드](https://github.com/gaon12/MusicQueue/archive/main.zip)하고, 파일을 압축 해제 합니다.
2. 압축 해제한 폴더로 이동 후, 쉘 또는 CMD에 다음과 같이 입력합니다. 그 전에 파이썬이 설치되어 있어야 합니다.
```shell
pip install selenium pandas pyarrow openpyxl
```
3. 영상 리스트 파일(`playlilst.tsv` 또는 `playlilst.xlsx`)을 만듭니다. `csv`나 `xls`는 지원하지 않습니다.
 - `playlilst.tsv` 와 `playlilst.xlsx` 파일이 동시에 있다면 `playlilst.tsv` 파일을 사용합니다.
 - `playlilst.tsv` 또는 `playlilst.xlsx` 파일은 파이썬 코드와 같은 폴더에 위치해 있어야 합니다.
 - 단, `https://youtu.be/`와 같이 단축 URL 형식으로 입력하면 안됩니다.
 - 또한 자동 재생이 설정되어 있어야 합니다.
 - 광고 제거 프로그램을 사용하면 더욱 쾌적하게 사용이 가능합니다.
4. 크롬/엣지 브라우저 버전을 확인합니다. 크롬/엣지 브라우저에 접속 후 다음과 같이 입력해 주세요.
```url
chrome://version
```

5. 버전에 맞는 드라이버 파일을 다운로드 합니다.
 - [크롬 드라이버](https://googlechromelabs.github.io/chrome-for-testing/) - 파이썬 코드와 동일한 폴더에 위치. 파일명은 `chromedriver.exe`로 저장
 - [엣지 브라우저 드라이버](https://developer.microsoft.com/ko-kr/microsoft-edge/tools/webdriver/) - 파이썬 코드와 동일한 폴더에 위치. 파일명은 `msedgedriver.exe`로 저장
 - 둘 중에 하나만 존재한다면 자동으로 존재하는 브라우저를 사용합니다. 둘 다 있는 경우에는 어떤 브라우저를 사용할지 물어보는 메시지가 뜹니다.

6. 파이썬 코드를 실행합니다.
```shell
python music.py
// 또는
python3 music.py
```

## 빌드된 버전 사용
빌드된 버전을 사용하면 더욱 편하게 사용할 수 있어요. 다만 일부 백신에서 오탐지 할 수 있어요. 하지만 바이러스는 전혀 없으니 걱정하지 마세요!

1. [릴리즈 페이지](https://github.com/gaon12/MusicQueue/releases)에서 최신 버전을 다운로드 받아 주세요.
2. 이후 과정은 위의 사용방법과 동일합니다.

## Puppeteer Node.js 코드 실행
1. 본 깃허브 저장소를 [다운로드](https://github.com/gaon12/MusicQueue/archive/main.zip)하고, 파일을 압축 해제 합니다.
2. 압축 해제한 폴더로 이동 후, 쉘 또는 CMD에 다음과 같이 입력합니다. 그 전에 Node.js가 설치되어 있어야 합니다.
```shell
npm i puppeteer xlsx
```
3. 이후의 과정은 파이썬과 동일합니다. 실행 시에는 다음 명령어를 사용하면 됩니다.
```
node music.js
```

## tsv/xlsx 기본 구조
[#3](https://github.com/gaon12/MusicQueue/issues/3)에서 자세한 내용을 확인할 수 있습니다.
|URL|Times|ListenNums|
|------|---|---|
|유튜브 URL을 입력합니다.|몇번 재생할 지 숫자로만 입력합니다.|몇번 재생했는지 숫자로만 입력합니다.|
|https://www.youtube.com/watch?v=sLr2rDnbN2o|2|1|

# 주의사항
브라우저 및 유튜브 정책으로 인해 사용자의 행동(클릭 등)이 있지 않으면 자동재생 되지 않습니다. 즉, 첫번째 영상에 한해서 수동으로 재생 버튼을 눌러줘야 합니다.

# 라이선스
본 프로젝트는 [MIT 라이선스](https://github.com/gaon12/MusicQueue/blob/main/LICENSE)로 배포 됩니다!
