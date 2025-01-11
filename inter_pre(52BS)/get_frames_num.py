import csv
import os

# 获取帧数
def get_frames_num(input_folder, f_name, f_num, f, t):
    # quantization_step = 1/qs
    csv_files = os.listdir(input_folder)
    for csv_file in csv_files:
        file_name = csv_file.split('.')[0]
        modified_string = file_name[4:]
        f_name.append(modified_string)

        with open(os.path.join(input_folder, csv_file), newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        # 获取帧数
        num_frames = len(data) - 1
        t.append(num_frames / f)
        f_num.append(num_frames)
        # 定义主目录路径

# 获取比特数
def get_bit_num(input_floder, by_num, b_num):
    for filename in os.listdir(input_floder):
        # 检查文件扩展名是否为.bin
        if filename.endswith('.bin'):
            # 构建文件的完整路径
            file_path = os.path.join(input_floder, filename)
            # 获取文件大小（字节）
            file_size_bytes = os.path.getsize(file_path)

            by_num.append(file_size_bytes)
            # 将文件大小转换为比特数并添加到列表中
            b_num.append(file_size_bytes * 8)

frame_dir = 'dec'
bin_dir = 'bin'
# 定义要读取的子目录列表
sub_dirs = ['30FPS', '15FPS', '10FPS']
csv_file_path = 'bit_rate_output.csv'

# 遍历每个子目录
name = []
frame_num = []
byte_num = []
bit_num = []
time = []
# 统计帧数
for sub_dir in sub_dirs:
    # 构建子目录的完整路径
    fps_str = sub_dir[:sub_dir.find('FPS')]  # 提取FPS前面的部分
    fps = int(fps_str)  # 转换为整数, 获得帧数
    sub_dir_path = os.path.join(frame_dir, sub_dir)
    get_frames_num(sub_dir_path, name, frame_num, fps, time)

# 统计比特数
for sub_dir in sub_dirs:
    # 构建子目录的完整路径
    sub_dir_path = os.path.join(bin_dir, sub_dir)
    get_bit_num(sub_dir_path, byte_num, bit_num)

bit_rate = [x / y for x, y in zip(bit_num, time)]

# 写入csv文件
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    # 写入表头（可选）
    writer.writerow(['Name', 'FrameNum', 'ByteNum', 'BitNum', 'bit_rate(bps)'])

    # 使用zip函数将两个列表的元素配对，并写入CSV文件
    for nam, fm, byn, bn, br in zip(name, frame_num, byte_num, bit_num, bit_rate):
        writer.writerow([nam, fm, byn, bn, br])
# print(name)