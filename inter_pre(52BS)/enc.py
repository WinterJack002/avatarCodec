import struct
import numpy as np
import math
import csv
import os

 # 假设第一个帧不编码，直接使用原始值
previous_reconstructed_frame = [0] * 52

# 帧内预测
def predict():
    pass

# 帧间预测
def inter_prediction(current_frame, previous_reconstructed_frame):
    return int(current_frame - previous_reconstructed_frame)

# 数据偏移

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


def encode_frames(frames, quantization_step, filename, inter_flag, intra_flag):
    with open(filename, 'ab+') as f:
        # f.write(struct.pack('d', frames[0]))  # 负数
        bitstream = ''

        for i in range(len(frames)):
            if intra_flag:
                
                if inter_flag:
                    # 帧间预测
                    residual = inter_prediction(frames[i], previous_reconstructed_frame[i])
                else:
                    pass
                    # 
            else:
                
                if inter_flag:
                    # 帧间预测
                    residual = inter_prediction(frames[i], previous_reconstructed_frame[i])
                else:
                    residual = frames[i]
            
           
            # 量化残差
            quantized_residual = quantize(residual, quantization_step)
            # 指数哥伦布编码
            encoded_residual = exponential_golomb_encode(quantized_residual)
            bitstream += encoded_residual
            
            # 重建当前帧
            if intra_flag:
                
                if inter_flag:
                    # 重建下一帧
                    if quantized_residual % 2 == 0:
                        quantized_residual = int((-quantized_residual) / 2)
                    else:
                        quantized_residual = int((quantized_residual + 1) / 2)

                    # if i == 0:
                    #     previous_reconstructed_frame[i] = 0 + quantized_residual * quantization_step
                    # else:
                    previous_reconstructed_frame[i] = previous_reconstructed_frame[i] + quantized_residual * quantization_step
                else:
                    pass
            else:
                
                if inter_flag:
                    # 重建下一帧
                    if quantized_residual % 2 == 0:
                        quantized_residual = int((-quantized_residual) / 2)
                    else:
                        quantized_residual = int((quantized_residual + 1) / 2)

                    # if i == 0:
                    #     previous_reconstructed_frame = 0 + quantized_residual * quantization_step
                    # else:
                    previous_reconstructed_frame[i] = previous_reconstructed_frame[i] + quantized_residual * quantization_step
                else:
                    pass
            # 确保 bitstream 的长度是8的倍数

        while len(bitstream) % 8 != 0:
            bitstream += '0'
        write_bytes_len = math.ceil(len(bitstream) / 8)
        f.write(struct.pack('I', write_bytes_len))
        # print("compute cnt: ", write_bytes_len)
        byte_array = int(bitstream, 2).to_bytes(write_bytes_len, 'big')
        
        # write_cnt = 0
        # for i in range(0, len(bitstream), 8):
        #     byte = bitstream[i:i + 8]
        #     byte_array.append(int(byte, 2))
        #     write_cnt += 1
        # print("write_cnt: ", write_cnt)
        # if write_bytes_len != write_cnt:
        #     print("error!!!")
        f.write(byte_array)

# 左右预测
def predict_LeftR():
    pass


def encode_from_csv(input_folder, output_folder, QP, n=6, inter_flag=0, intra_flag=0):
    
    bs_scale = 10 ** n
    csv_files = os.listdir(input_folder)
    os.makedirs(output_folder, exist_ok=True)
    for csv_file in csv_files:
        output_file = os.path.join(output_folder, 'QP' + str(QP)+'_'+csv_file.split('.')[0] + '.bin')
        quantization_step = 2 ** QP
        with open(os.path.join(input_folder, csv_file), newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        rows = []  # 用于存储行数据
        for row_index in range(1, len(data)):  # 从第二行开始
            row_data = ([int(float(value) * bs_scale) for value in data[row_index][2:]])
            rows.append(row_data)

        for row in rows:
            encode_frames(row, quantization_step, output_file, inter_flag, intra_flag)

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
