import pandas as pd
import matplotlib.pyplot as plt
import os

# 读取 CSV 文件
file1 = '../data/mse/csv_mse/reference/61BS_30FPS_extreme expression.csv'
file2 = '../data/mse/csv_mse/reference/61BS_30FPS_talking video.csv'

data1 = pd.read_csv(file1)
data2 = pd.read_csv(file2)

# 从第三列开始
columns = data1.columns[2:]

# 提取文件名
filename1 = os.path.basename(file1).replace('.csv', '')
filename2 = os.path.basename(file2).replace('.csv', '')

# 遍历每一列并绘制折线图
for col in columns:
    plt.figure(figsize=(12, 6))  # 设置图形大小
    plt.plot(data1[col], label=f'{filename1} - {col}', marker='o')
    plt.plot(data2[col], label=f'{filename2} - {col}', marker='x')

    plt.title(f'Comparison of {col}')
    plt.xlabel('Row Index')
    plt.ylabel(col)
    plt.legend()
    plt.grid()

    # 保存图表，设置 DPI 为 256
    plt.savefig(f'../data/talking_vs_emotion_img/{col}_comparison.png', dpi=256)
    plt.close()  # 关闭图形以释放内存
