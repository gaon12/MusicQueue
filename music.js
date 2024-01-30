const puppeteer = require('puppeteer');
const fs = require('fs/promises');
const xlsx = require('xlsx');

const extractYouTubeId = (url) => {
    const match = url.match(/(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/watch\?.+&v=))((\w|-){11})/);
    return match ? `https://www.youtube.com/watch?v=${match[1]}` : null;
};

const readPlaylist = async (filePath) => {
    if (filePath.endsWith('.xlsx')) {
        const workbook = xlsx.readFile(filePath);
        return xlsx.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]]);
    } else if (filePath.endsWith('.tsv')) {
        const data = await fs.readFile(filePath, 'utf8');
        return data.split('\n').map(row => row.split('\t'));
    } else {
        throw new Error("지원되지 않는 파일 형식입니다.");
    }
};

const updatePlaylist = async (filePath, playlist) => {
    if (filePath.endsWith('.xlsx')) {
        const workbook = xlsx.utils.book_new();
        const worksheet = xlsx.utils.json_to_sheet(playlist);
        xlsx.utils.book_append_sheet(workbook, worksheet);
        xlsx.writeFile(workbook, filePath);
    } else if (filePath.endsWith('.tsv')) {
        const data = playlist.map(row => row.join('\t')).join('\n');
        await fs.writeFile(filePath, data, 'utf8');
    } else {
        throw new Error("지원되지 않는 파일 형식입니다.");
    }
};

const playYouTubeVideo = async (videoUrl, isLastVideo) => {
    try {
        const browser = await puppeteer.launch({
            headless: false,
            defaultViewport: null
        });
        const page = await browser.newPage();
        await page.goto(videoUrl);

        // 자동 재생을 비활성화
        await page.evaluate(() => {
            const autoplayToggle = document.querySelector('.ytp-autonav-toggle-button');
            if (autoplayToggle && autoplayToggle.getAttribute('aria-checked') === 'true') {
                autoplayToggle.click();
            }
        });

        // 비디오의 재생 상태를 확인하고 비디오가 끝날 때까지 대기
        await page.evaluate(() => {
            return new Promise((resolve) => {
                const video = document.querySelector('video');
                video.onended = resolve;
            });
        });

        if (isLastVideo) {
            await browser.close();
        }
    } catch (error) {
        console.error('Error during video playback:', error);
    }
};

const findPlaylistFile = async () => {
    try {
        const tsvExists = await fs.stat('playlist.tsv');
        return 'playlist.tsv';
    } catch (e) {
        try {
            const xlsxExists = await fs.stat('playlist.xlsx');
            return 'playlist.xlsx';
        } catch (e) {
            return null;
        }
    }
};

(async () => {
    try {
        const filePath = await findPlaylistFile();  // 사용할 파일 경로 찾기
        if (!filePath) {
            console.error('playlist.xlsx 또는 playlist.tsv 파일을 찾을 수 없습니다.');
            return;
        }

        let playlist = await readPlaylist(filePath);
        const playlistLength = playlist.length;

        for (let i = 0; i < playlistLength; i++) {
            let row = playlist[i];
            const videoUrl = extractYouTubeId(row.URL);
            if (!videoUrl) {
                console.error('유효하지 않은 YouTube URL입니다.');
                continue;
            }

            if (row.ListenNums < row.Times) {
                const isLastVideo = i === playlistLength - 1;
                await playYouTubeVideo(videoUrl, isLastVideo);
                row.ListenNums++;
                await updatePlaylist(filePath, playlist);
            }
        }
    } catch (error) {
        console.error(error);
    }
})();