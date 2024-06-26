import os
import sys
from datetime import datetime
import subprocess
import re

# 獲取執行文件所在的文件夾路徑 (exe用)
exe_dir = os.path.dirname(sys.executable)
# 獲取執行文件所在的文件夾路徑 (py用)
py_dir = os.path.dirname(os.path.realpath(__file__))

# 輸出目錄路徑
output_dir = "output"
# 連結文件路徑
file_path = 'ytMP3.txt'
error_file_path = '錯誤連結.txt'
# yt-dlp 檔案路徑
yt_dlp_path = 'driver\\yt-dlp.exe'
# ffmpeg 檔案路徑
ffmpeg_path = 'driver\\ffmpeg\\bin'


# 讀取出來的資料
valid_urls = []    # 存放符合條件的 URL
invalid_urls = []  # 存放不符合的 URL 和行號

try:
    # 確保連結文件存在
    if not os.path.exists(file_path):
        print("錯誤: 找不到連結記事本。")
        print()
        open(file_path, 'w').close() # 建立新的 ytMP3.txt
        print("已新增新的 ytMP3.txt 請輸入連結後重新運行程式。")
        print()
        os.system('pause')
        sys.exit()
    
    # 讀取文件內容
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        if not lines:  # 檢查文件是否為空
            print("錯誤: 連結記事本為空。")
            print()
            os.system('pause')
            sys.exit()
        
        # 處理文件中的每一行
        for line_number, line in enumerate(lines, 1):  # 使用 enumerate 追蹤行號
            url = line.strip()
            
            if not url:  # 檢查是否為空行
                continue
            
            if url.startswith("https://www.youtube.com"):
                valid_urls.append(url)
            elif url.startswith("https://youtu.be"):
                valid_urls.append(url)
            else:
                invalid_urls.append((line_number, url))  # 添加不符合的 URL 及其行號

except Exception as e:
    print(f'發生錯誤: {e}')
    print()
    os.system('pause')
    sys.exit()

# 檢查是否有符合的 URL 並執行下載
if valid_urls:
    total_urls = len(valid_urls)
    print(f'◆ 開始下載 {total_urls} 個檔案...')
    print()
    
    for idx, url in enumerate(valid_urls, 1):
        try:
            # 使用 subprocess 調用 yt-dlp 並帶入參數
            cmd = [
                yt_dlp_path,
                '--output', f'{output_dir}/%(title)s.%(ext)s',
                '--embed-thumbnail', '--add-metadata', '--extract-audio',
                '--audio-format', 'mp3', '--audio-quality', '320K',
                '--ffmpeg-location', ffmpeg_path,
                '--progress', '--', url  # 使用 '--' 表示 URL 的開始
            ]

            print(f'【{idx}/{total_urls}】 ───  {url} 解析中...')
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            # 遍歷輸出流，捕獲進度信息
            for stdout_line in iter(process.stdout.readline, ''):
                # 篩選出包含進度信息的行
                match = re.search(r'\[download\]\s+(\d+\.\d+)%', stdout_line.strip())
                if match:
                    progress = match.group(1)
                    print(f"         └───  下載進度: {progress}%")

            # 等待 yt-dlp 完成
            process.communicate()
            
            if process.returncode == 0:
                print(f"成功下載: {url}")
            else:
                print(f"下載失敗: {url}")
                print(f"錯誤信息: {process.stderr.read()}")

        except Exception as e:
            print(f"下載 {url} 時發生錯誤: {e}")


else:
    print("沒有符合條件的 URL。")
    print()
    os.system('pause')
    sys.exit()

print()

# 檢查是否有錯誤的 URL 並寫入到txt
if invalid_urls:
    print()
    print("------------------------------------------------------------")
    print()
    print("以下 URL 不符合要求:")
    for line_number, url in invalid_urls:
        print(f"第 {line_number} 行: {url}")

    # 獲取當前時間
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 將錯誤的 URL 寫入錯誤連結.txt 文件
    with open(error_file_path, 'a') as error_file:
        error_file.write(f"--------------------{current_time}--------------------\n")
        for line_number, url in invalid_urls:
            error_file.write(f"第 {line_number} 行: {url}\n")
        error_file.write("\n")
    
    print()
    print("------------------------------------------------------------")
    print(f"\n錯誤連結請參考: {error_file_path}")
# else:
#     print("所有 URL 都符合要求。")



print()
os.system('pause')
