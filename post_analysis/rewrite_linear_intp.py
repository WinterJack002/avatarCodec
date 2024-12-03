import os
import csv
import numpy as np


# Step 1: 线性插值函数
def linear_interpolation(data, target_fps, current_fps):
    interpolated_data = []
    factor = target_fps // current_fps
    for i in range(len(data) - 1):
        interpolated_data.append(data[i])
        for j in range(1, factor):
            interpolated_row = data[i] + (data[i + 1] - data[i]) * j / factor
            interpolated_data.append(interpolated_row)
    interpolated_data.append(data[-1])  # 最后一行保持原样
    return interpolated_data


# Step 2: 读取csv文件，并进行数据插值与处理
def process_csv(ori_csv_path, dec_csv_path, n_fps, target_fps=30):
    with open(ori_csv_path, 'r') as ori_csv_file:
        ori_reader = list(csv.reader(ori_csv_file))
        ori_header = ori_reader[0]  # 保留 ori 文件的表头
        ori_cols = [row[:2] for row in ori_reader[1:]]  # 获取第1、2列的整列数据，不包括表头
        ori_length = len(ori_cols)  # 计算 ori 列的长度，用于后续补齐或删除行

    with open(dec_csv_path, 'r') as dec_csv_file:
        dec_reader = list(csv.reader(dec_csv_file))
        dec_header = dec_reader[0]  # 保留 dec 文件的表头
        # 读取 dec 文件的第三列及之后的数据内容，并转换为浮点数
        dec_data = np.array([row[2:] for row in dec_reader[1:]], dtype=float)

    # 进行线性插值处理
    interpolated_data = linear_interpolation(dec_data, target_fps, n_fps)

    if len(interpolated_data) < ori_length:
        # 如果插值后的行数少于 ori_length，则补齐行数
        for _ in range(ori_length - len(interpolated_data)):
            interpolated_data.append(interpolated_data[-1])  # 用最后一行数据补齐
    elif len(interpolated_data) > ori_length:
        # 如果插值后的行数多于 ori_length，则删除多余的行
        interpolated_data = interpolated_data[:ori_length]

    new_csv_content = [dec_header]  # 保留 dec 文件的原始表头
    for i in range(ori_length):
        # 替换第1、2列，用 ori_cols 的第1、2列数据，第三列开始使用 interpolated_data
        new_csv_content.append(ori_cols[i] + list(interpolated_data[i]))

    # 返回插值处理后的新 CSV 数据内容
    return new_csv_content


# Step 3: 批量处理并保存文件
def process_directory(ori_dir, dec_dir, output_dir, target_fps=30):
    for root, dirs, files in os.walk(dec_dir):
        for file in files:
            if file.endswith('.csv'):
                n_fps = int((os.path.basename(root)).replace('FPS', ''))  # 从目录名推断帧率
                # ori_file_name = file.split('_', 2)[-1]  # 去掉前缀得到 ori 对应的文件名
                ori_file_name = file.rsplit('_', 1)[-1]
                ori_file_path = os.path.join(ori_dir, ori_file_name)
                dec_file_path = os.path.join(root, file)

                # 处理文件并得到插值后的数据
                new_csv_content = process_csv(ori_file_path, dec_file_path, n_fps, target_fps)

                # 保存文件
                new_file_name = f"new_30fps_{file}"
                new_file_dir = os.path.join(output_dir, f"{n_fps}FPS")
                os.makedirs(new_file_dir, exist_ok=True)
                new_file_path = os.path.join(new_file_dir, new_file_name)
                with open(new_file_path, 'w', newline='') as new_file:
                    writer = csv.writer(new_file)
                    writer.writerows(new_csv_content)  # 写入新 CSV 内容


# 执行主处理流程
ori_dir = r'C:\Users\winter\Desktop\DCC_avatar\实验资源数据\csv编解码文件和bin文件\线性插值分析\latest\ori'  # ori 目录路径
dec_dir = r'C:\Users\winter\Desktop\DCC_avatar\实验资源数据\csv编解码文件和bin文件\线性插值分析\latest\dec'  # dec 目录路径
output_dir = r'C:\Users\winter\Desktop\DCC_avatar\实验资源数据\csv编解码文件和bin文件\线性插值分析\latest\new_30fps'  # 输出目录路径
process_directory(ori_dir, dec_dir, output_dir)
