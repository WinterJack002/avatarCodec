import struct
import numpy as np
import math
import csv
import os

ENC_FILE = '30FPS'
quantization_step = 1/256
# PRE_FRAME = 0.0


# 计算残差
def compute_residual(current_frame, previous_reconstructed_frame):
    return current_frame - previous_reconstructed_frame


# 量化残差
def quantize(data, quantization_step):
    data = np.round(data / quantization_step).astype(int)
    if data <= 0:
        data = (-data) * 2
    else:
        data = data * 2 - 1
    return data


# 指数哥伦布编码
def exponential_golomb_encode(values):
    # def test_exponential_golomb_encode(n):
    unarycode = ''
    golombCode = ''

    # values = np.array(values)  # 将列表转换为 NumPy 数组
    ###Quotient and Remainder Calculation
    groupID = np.floor(np.log2(values + 1))
    temp_ = groupID
    # print(groupID)

    while temp_ > 0:
        unarycode = unarycode + '0'
        temp_ = temp_ - 1
    unarycode = unarycode  # +'1'

    index_binary = bin(values + 1).replace('0b', '')
    golombCode = unarycode + index_binary
    return golombCode


def encode_frames(frames, quantization_step, filename):
    with open(filename, 'ab+') as f:
        # f.write(struct.pack('d', frames[0]))  # 负数
        bitstream = ''

        # 假设第一个帧不编码，直接使用原始值
        # previous_reconstructed_frame = 0.0
        for i in range(len(frames)):
            # 计算残差
            # residual = compute_residual(frames[i], previous_reconstructed_frame)
            residual = frames[i]
            # print(residual)
            # 量化残差
            quantized_residual = quantize(residual, quantization_step)
            # 指数哥伦布编码
            encoded_residual = exponential_golomb_encode(quantized_residual)
            bitstream += encoded_residual
            
            # # 重建下一帧
            # if quantized_residual % 2 == 0:
            #     quantized_residual = (-quantized_residual) / 2
            # else:
            #     quantized_residual = (quantized_residual + 1) / 2

            # if i == 0:
            #     previous_reconstructed_frame = 0 + quantized_residual * quantization_step
            # else:
            #     previous_reconstructed_frame = previous_reconstructed_frame + quantized_residual * quantization_step

            # 确保 bitstream 的长度是8的倍数

        while len(bitstream) % 8 != 0:
            bitstream += '0'
        write_bytes_len = math.ceil(len(bitstream) / 8)
        f.write(struct.pack('I', write_bytes_len))
        # print("compute cnt: ", write_bytes_len)
        byte_array = bytearray()
        write_cnt = 0
        for i in range(0, len(bitstream), 8):
            byte = bitstream[i:i + 8]
            byte_array.append(int(byte, 2))
            write_cnt += 1
        # print("write_cnt: ", write_cnt)
        if write_bytes_len != write_cnt:
            print("error!!!")
        f.write(byte_array)


def encode_from_csv(input_folder, qs, output_folder):
    quantization_step = 1/qs
    csv_files = os.listdir(input_folder)
    os.makedirs(output_folder, exist_ok=True)
    for csv_file in csv_files:
        output_file = os.path.join(output_folder, str(qs)+'_'+csv_file.split('.')[0] + '.bin')
        with open(os.path.join(input_folder, csv_file), newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        # 提取每列数据（从第三列开始），并将字符串转换为浮点数
        columns = []
        for col_index in range(2, len(data[0])):  # 从第三列开始
            column_data = [float(row[col_index]) for row in data[1:]]  # 从第二行开始读取数据
            columns.append(column_data)

        #with open(output_file, 'ab+') as f:
            # print("frames: ", len(columns[0]))
            #f.write(struct.pack('I', len(columns[0])))  # 一列数据，帧数(一种blend shape weights的帧数写成二进制格式)
        for col in columns:
            encode_frames(col, quantization_step, output_file)

if __name__ == "__main__":
    # 示例帧数据
    output_file = "encoded_data.bin"

    # 编码帧数据并保存为bin文件
    csv_file = 'video1bak.csv'  # CSV 文件路径
    #input_folder = 'enc' + ENC_FILE
    input_folder  = os.path.join('enc', ENC_FILE)
    output_folder = os.path.join('bin', ENC_FILE)
    #encode_frames(frames, quantization_step, output_file)
    encode_from_csv(input_folder, quantization_step, output_folder)
