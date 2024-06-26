import requests
import os
import shutil
import subprocess
from alive_progress import alive_bar

# 下載檔案
def download_file_with_progress(url, local_filename):
    with requests.get(url, stream=True) as r, open(local_filename, 'wb') as f:
        file_size = int(r.headers.get('content-length', 0))
        chunk_size = 8192
        bar_length = file_size // chunk_size if file_size > chunk_size else 1
        with alive_bar(bar_length, bar='smooth', spinner='dots_waves', length=40, enrich_print=False) as bar:
            bar.text('下載進度')
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                bar()  # 更新進度條
        # 手動設置進度條到 100%
        bar(bar_length)

    return local_filename

# 解壓縮並重新命名
def extract_and_rename_archive(archive_path, target_directory, new_foldername):
    # 創建目標目錄（如果不存在）
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    # 7-Zip 軟體路徑
    seven_zip_path = os.path.join(target_directory, '7z', '7za.exe')
    
    # 使用 7za 解壓縮到目標文件夾
    subprocess.run([seven_zip_path, 'x', archive_path, f'-o{target_directory}'], check=True)
    
    # 獲取解壓後的文件夾名
    extracted_items = os.listdir(target_directory)
    extracted_dirs = [item for item in extracted_items if os.path.isdir(os.path.join(target_directory, item))]
    
    if not extracted_dirs:
        raise FileNotFoundError("未找到解壓後的文件夾")
    
    # 資料夾通常已 'ffmpeg-' 開頭，找到正確的文件夾名
    for folder_name in extracted_dirs:
        if folder_name.startswith('ffmpeg-'):
            old_folder_path = os.path.join(target_directory, folder_name)
            break
    else:
        raise FileNotFoundError("未找到以 'ffmpeg-' 開頭的文件夾")
    
    # 目標文件夾路徑
    new_folder_path = os.path.join(target_directory, new_foldername)
    
    # 如果目標文件夾已存在，先刪除它
    if os.path.exists(new_folder_path):
        shutil.rmtree(new_folder_path)
    
    # 重命名解壓後的文件夾為新名稱
    os.rename(old_folder_path, new_folder_path)
    
    return new_folder_path



# 設置您想要保存文件的本地路徑和文件名
ffmpeg_file_path = './driver/ffmpeg.7z'
ytdlp_file_path = './driver/yt-dlp.exe'

# 指定解壓縮後的目標資料夾和新資料夾名稱
target_directory = './driver/'
new_foldername = 'ffmpeg'

print()

# 下載文件並顯示進度條
download_file_with_progress('https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z', ffmpeg_file_path)
download_file_with_progress('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', ytdlp_file_path)

# 解壓縮並重新命名
extracted_folder_path = extract_and_rename_archive(ffmpeg_file_path, target_directory, new_foldername)

# 如果 ffmpeg.7z 存在則刪除
if os.path.exists(ffmpeg_file_path):
    os.remove(ffmpeg_file_path)

print(f'安裝更新驅動項完成。')

