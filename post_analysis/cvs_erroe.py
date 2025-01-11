import pandas as pd
import numpy as np

def calculate_squared_error(A_file, B_file):
    # 读取A.csv和B.csv
    A = pd.read_csv(A_file, header=None)
    B = pd.read_csv(B_file, header=None)
    
    # 确保A和B的行列数相同
    if A.shape != B.shape:
        raise ValueError("A.csv 和 B.csv 的行列数不相同")
    
    # 计算对应元素的误差平方和
    squared_error = np.sum((A - B) ** 2)  # 对应元素的差值平方并求和

    return squared_error

# 输入文件路径
A_file = r'F:\weizh2023\Avatar\研二上\新建文件夹\pre-MPEG-149\code\lossless_precision\dec\30FPS\error\dec_rounded.csv'
B_file = r'F:\weizh2023\Avatar\研二上\新建文件夹\pre-MPEG-149\code\lossless_precision\dec\30FPS\error\enc.csv'

# 调用函数计算误差平方和
squared_error = calculate_squared_error(A_file, B_file)

# 输出结果
print(f"A.csv 和 B.csv 对应元素的误差平方和: {squared_error}")
