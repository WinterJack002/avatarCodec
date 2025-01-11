import cv2
import os
import numpy as np

# 输入AVI文件路径
video1_path = '../data/difference_videos/64QP_30FPS_61BS_extreme.avi'
video2_path = '../data/difference_videos/exterme expression(REFERENCE).avi'
# 输出文件夹
output_folder = '../data/frames'
# 输出MP4文件路径
output_video_path = '../data/heat_map_video/test.mp4'

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 读取视频
cap1 = cv2.VideoCapture(video1_path)
cap2 = cv2.VideoCapture(video2_path)

# 获取视频的帧宽度、高度和帧率
frame_width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap1.get(cv2.CAP_PROP_FPS))
print('width1:',frame_width, 'height1:', frame_height, 'fps1:', fps)

# 获取视频的帧宽度、高度和帧率
frame_width_2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height_2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_2 = int(cap2.get(cv2.CAP_PROP_FPS))
print('width2:',frame_width_2, 'height2:', frame_height_2, 'fps2:', fps_2)


# 创建VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者使用 cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

frame_count = 0

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    # 计算绝对差异
    difference = cv2.absdiff(frame1, frame2)

    # 转换为灰度图并生成热图
    gray_diff = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    heatmap = cv2.applyColorMap(gray_diff, cv2.COLORMAP_JET)

    # 将热图写入视频文件
    out.write(heatmap)

    frame_count += 1

cap1.release()
cap2.release()
out.release()
print(f'总共生成了 {frame_count} 帧的热图视频: {output_video_path}')
