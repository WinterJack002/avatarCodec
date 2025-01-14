import pandas as pd
import os

# 抽帧函数

# EXTRACT_NUM = 1
def frame_extraction(directory_path, subdir_path, FPS, num):
    """
    当前FPS/3。遍历指定目录下的所有CSV文件，并保留每num行中的第一行，然后保存到新的CSV文件中。

    :param output_directory_path: 输出的修改后的cvs目录路径
    :param directory_path: 包含CSV文件的目录路径
        :param num: 保留每num行中的第一行
    """

    # 计算子目录名称
    subdir_name = str(FPS // num) + 'FPS'  # 使用整除来得到整数结果
    # subdir_path = os.path.join(output_directory_path, subdir_name)

    # 确保子目录存在
    os.makedirs(subdir_path, exist_ok=True)

    for filename in os.listdir(directory_path):

        # 检查文件是否以.csv结尾
        if filename.endswith('.csv'):
            # 构造完整的文件路径
            file_path = os.path.join(directory_path, filename)

            # 读取CSV文件
            df = pd.read_csv(file_path)

            # 保留第一行 (表头)，然后从第二行开始每三行保留一行
            # df_filtered = pd.concat([df.iloc[:1], df.iloc[1::3]])
            df_filtered = df.iloc[::num]

            output_file_path = os.path.join(subdir_path, subdir_name + '_' + filename)
            # 将处理后的数据写入新CSV文件
            df_filtered.to_csv(output_file_path, index=False)

# 调用函数，假设你的目录路径是' path/to/your/csv/files'，并且你想保留每3行中的第一行
if __name__ == "__main__":
    frame_extraction('ori', 'enc', 3)

