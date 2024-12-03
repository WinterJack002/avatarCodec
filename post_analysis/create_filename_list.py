import os
import re


def sort_key(filename):
    """
    从文件名中提取数字部分，形成排序规则：
    dec_后面的数字 -> FPS前面的数字 -> femaleEmotion后的数字
    如果未匹配，则返回一个非常大的数值，保证它们排在后面
    """
    pattern = r"dec_(\d+)_(\d+)FPS_femaleEmotion(\d+)"
    match = re.search(pattern, filename)

    if match:
        # 返回 (dec_后的数字, FPS前的数字, femaleEmotion后的数字)
        return tuple(map(int, match.groups()))
    return (float('inf'), float('inf'), float('inf'))  # 返回大值元组，保证无法匹配的文件排在后面


def save_sorted_mp4_filenames(directory):
    # 获取所有 .mp4 文件
    mp4_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]

    # 按照自定义的规则排序
    mp4_files_sorted = sorted(mp4_files, key=sort_key)

    # 打开或创建 filename_list.txt 文件
    with open('filename_list.txt', 'w', encoding='utf-8') as file:
        # 将排序后的文件名写入 filename_list.txt，每行一个
        for filename in mp4_files_sorted:
            file.write(filename + '\n')

        # 输出 .mp4 文件数量
        print(f"一共有 {len(mp4_files_sorted)} 个 .mp4 文件。")


# 使用你想要的文件夹路径
# folder_path = 'path_to_your_directory'  # 替换为你想要统计的文件夹路径
# save_sorted_mp4_filenames(folder_path

# 使用你想要的文件夹路径
folder_path = r'H:\DCC_avatar\pretraining\FPS-male'  # 替换为你想要统计的文件夹路径
save_sorted_mp4_filenames(folder_path)