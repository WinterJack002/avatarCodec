# 压缩视频，混流音频
import os
import subprocess

# 定义目录路径
dir1 = r"H:\DCC_avatar\音频-原视频"
dir2 = r"H:\DCC_avatar\未压缩视频"
audio_dir = os.path.join(dir1, "audio")
audio_file_name = 'MySlate_291_winter.mp4'
compression_dir = os.path.join(dir2, "compression")

ffmpeg_path = r"E:\ffmpeg-2024-10-02-git-358fdf3083-full_build\ffmpeg-2024-10-02-git-358fdf3083-full_build\bin\ffmpeg.exe"

# 创建输出目录（如果不存在）
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(compression_dir, exist_ok=True)

# 1. 从 dir1/ 提取音频并保存到 audio/ 子目录下
for filename in os.listdir(dir1):
    if filename.endswith(".mp4") or filename.endswith(".mov") or filename.endswith(".avi"):
        video_path = os.path.join(dir1, filename)
        audio_output_path = os.path.join(audio_dir, os.path.splitext(filename)[0] + ".mp4")

        # # 标准化路径，确保兼容性
        # video_path = os.path.normpath(video_path)
        # audio_output_path = os.path.normpath(audio_output_path)

        # 提取音频
        extract_audio_cmd = [
            ffmpeg_path, "-i", video_path, "-vn", "-acodec", "copy", audio_output_path
        ]
        subprocess.run(extract_audio_cmd)
        print(f"提取音频到: {audio_output_path}")

# # 2. 压缩 dir2/ 下的 .avi 视频，并保存为 mp4 到 compression/ 目录
for filename in os.listdir(dir2):
    if filename.endswith(".avi"):
        video_path = os.path.join(dir2, filename)
        compressed_video_path = os.path.join(compression_dir, os.path.splitext(filename)[0] + ".mp4")

        # 压缩视频
        compress_video_cmd = [
            ffmpeg_path, "-i", video_path, "-an", "-c:v", "libx264", "-preset", "veryslow", "-crf", "0",
            compressed_video_path
        ]
        subprocess.run(compress_video_cmd)
        print(f"压缩视频到: {compressed_video_path}")

# # 3. 将 dir1/audio/ 下的音频文件与 dir2/compression/ 下的视频文件进行混流
for filename in os.listdir(compression_dir):
    if filename.endswith(".mp4"):
        compressed_video_path = os.path.join(compression_dir, filename)
        audio_file = os.path.join(audio_dir, audio_file_name)

        # 检查对应的音频文件是否存在
        if os.path.exists(audio_file):
            final_output_path = os.path.join(compression_dir, "final_" + filename)

            # 音频和视频混流
            mix_stream_cmd = [
                ffmpeg_path, "-i", compressed_video_path, "-i", audio_file, "-c:v", "copy", "-c:a", "copy",
                "-map", "0:v:0", "-map", "1:a:0", final_output_path
            ]
            subprocess.run(mix_stream_cmd)
            print(f"生成混流文件: {final_output_path}")
        else:
            print(f"音频文件未找到: {audio_file}")
