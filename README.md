# ytMP3 Youtube MP3 下載器

## 使用方法:
1. 先使用 Updata 更新驅動項目
2. 把要下載的連結都放置在 ytMP3.txt 當中(多網址請換行)
3. 運行 ytMP3.py


## 檔案結構:
driver/ → 驅動項目
├── 7z/
├── ffmpeg/
└── yt-dlp/
output/ → 下載位置
Updata.py → 安裝或更新驅動項目(不含7z)
ytMP3.py → 主下載程序
ytMP3.txt → 放置下載網址
錯誤連結.txt → 錯誤的網址紀錄

## 驅動項目(手動):
https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z
https://www.7-zip.org/a/7z2407-extra.7z
