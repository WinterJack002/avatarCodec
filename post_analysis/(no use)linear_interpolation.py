import os
import pandas as pd
import numpy as np


def linear_interpolation(col, num):
    """ 对每一列进行线性插值，在每两个数据之间插入N个值 """
    interpolated = []
    for i in range(len(col) - 1):
        interpolated.append(col[i])  # 当前数据
        # 3倍插值
        # step = (col[i + 1] - col[i]) / 3
        # interpolated.append(col[i] + step)  # 第一个插值
        # interpolated.append(col[i] + 2 * step)  # 第二个插值

        # num 倍插值
        step = (col[i + 1] - col[i]) / num  # num -1 个插值意味着总共分成 30 份
        for j in range(1, num):  # 插入 num -1 个值
            interpolated.append(col[i] + j * step)

    interpolated.append(col[-1])  # 加入最后一个数据
    return interpolated


def process_csv_file(file_path, output_dir, num):
    # 读取 CSV 文件，从第 2 行第 2 列开始
    df = pd.read_csv(file_path).iloc[:, 1:]

    # 对每列进行插值
    interpolated_data = pd.DataFrame()
    for col in df.columns:
        interpolated_data[col] = linear_interpolation(df[col].dropna().values, num)

    # 重命名后的 CSV 文件
    file_name = os.path.basename(file_path)
    output_file = os.path.join(output_dir , f"interpolated_{file_name}")

    # 保存为 CSV 文件
    interpolated_data.to_csv(output_file, index=False)


def process_all_csv_files(directory, output_dir, num):
    # 获取目录下所有的 CSV 文件
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # 遍历每个 CSV 文件
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        process_csv_file(file_path, output_dir, num)


# 使用示例
directory_path = r'C:\Users\winter\Desktop\DCC_avatar\实验资源数据\csv编解码文件和bin文件\线性插值分析\线性插值输入目录'  # 替换为你的目录路径
output_path = r'C:\Users\winter\Desktop\DCC_avatar\实验资源数据\csv编解码文件和bin文件\线性插值分析\线性插值输出目录'
num = 30 # 几倍插值
process_all_csv_files(directory_path, output_path, num)
