import os
import pandas as pd

# 定义文件目录路径
input_dir = r'C:\Users\winter\Desktop\DCC_avatar\实验资源数据\csv编解码文件和bin文件\BS-PSNR分析'
output_dir = r'C:\Users\winter\Desktop\DCC_avatar\实验资源数据\csv编解码文件和bin文件\BS-PSNR分析\26个BS其余置0'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# header2 提供的表头 26个BS
header2 = ['Timecode', 'BlendshapeCount',
    'EyeBlinkLeft', 'EyeSquintLeft', 'EyeWideLeft', 'EyeBlinkRight', 'EyeSquintRight',
    'EyeWideRight', 'JawOpen', 'MouthClose', 'MouthSmileLeft', 'MouthSmileRight',
    'MouthFrownLeft', 'MouthFrownRight', 'MouthLowerDownLeft', 'MouthLowerDownRight',
    'MouthUpperUpLeft', 'MouthUpperUpRight', 'BrowDownLeft', 'BrowDownRight', 'BrowInnerUp',
    'BrowOuterUpLeft', 'BrowOuterUpRight', 'NoseSneerLeft', 'NoseSneerRight', 'HeadYaw',
    'HeadPitch', 'HeadRoll',
]

# 遍历源目录下的所有 CSV 文件
for file_name in os.listdir(input_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_dir, file_name)

        # 读取 CSV 文件，自动处理第一行作为 header1
        df = pd.read_csv(file_path)

        # 比较 header1 和 header2，找出不在 header2 中的列
        columns_to_zero = [col for col in df.columns if col not in header2]

        # 将不在 header2 中的列数据置为 0
        df[columns_to_zero] = 0

        # 输出文件路径
        output_file_path = os.path.join(output_dir, '55BS_set_0_' + file_name)

        # 将处理后的 DataFrame 写回到新的 CSV 文件
        df.to_csv(output_file_path, index=False)

        print(f"Processed and saved: {output_file_path}")
