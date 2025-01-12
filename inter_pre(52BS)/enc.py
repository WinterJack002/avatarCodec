import struct
import numpy as np
import math
import csv
import os
import sys 

 # 假设第一个帧不编码，直接使用原始值
previous_reconstructed_frame = [0] * 52

referenceTable = [
        [ 0, 1,  2,  3,  4,  5,  6,  14, 15, 16, 17,   18, 19, 20, 21, 22, 23, 25,  27,  31, 32, 33, 35,  39, 41, 43, 46, 47, 49, 51],
        [ 7, 8, 10,  9, 11, 12, 13,  29, -1, -1, 37,   -1, -1, -1, -1, -1, 24, 26,  28,  -1, -1, 34, 36,  40, 42, 44, -1, 48, 50, -1],
        [-1,-1, -1, -1, -1, -1, -1,  30, -1, -1, 38,   -1, -1, -1, -1, -1, -1, -1,  -1,  -1, -1, -1, -1,  -1, -1, 45, -1, -1, -1, -1]
    ]

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

    unarycode = ''
    golombCode = ''

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
        bitstream = ''
        rec_intra_bs = ['none'] * 52       
        for i in range(len(frames)):
            if intra_flag:
                if   i in referenceTable[0]:
                    intra_bs = frames[i]

                elif i in referenceTable[1]:
                    intra_bs = frames[i] - rec_intra_bs[referenceTable[0][referenceTable[1].index(i)]]
                else:
                    intra_bs = frames[i] - rec_intra_bs[referenceTable[0][referenceTable[2].index(i)]]
                
            else:
                intra_bs = frames[i] 
        
            if inter_flag:
                residual = inter_prediction(intra_bs, previous_reconstructed_frame[i])
            else:
                residual = intra_bs
            
           
            # 量化残差
            quantized_residual = quantize(residual, quantization_step)
            # 指数哥伦布编码
            encoded_residual = exponential_golomb_encode(quantized_residual)
            bitstream += encoded_residual
            
            if inter_flag:
                # 重建下一帧
                if quantized_residual % 2 == 0:
                    quantized_residual = int((-quantized_residual) / 2)
                else:
                    quantized_residual = int((quantized_residual + 1) / 2)

                previous_reconstructed_frame[i] = previous_reconstructed_frame[i] + quantized_residual * quantization_step
                give = previous_reconstructed_frame[i]
            else:
                if quantized_residual % 2 == 0:
                        quantized_residual = int((-quantized_residual) / 2)
                else:
                        quantized_residual = int((quantized_residual + 1) / 2)
                give = quantized_residual * quantization_step
            # 重建当前帧
            if intra_flag:
                if   i in referenceTable[0]:
                    rec_intra_bs[i] = give
                elif i in referenceTable[1]:
                    rec_intra_bs[i] = give + rec_intra_bs[referenceTable[0][referenceTable[1].index(i)]]
                else:
                    rec_intra_bs[i] = give + rec_intra_bs[referenceTable[0][referenceTable[2].index(i)]]
            else:
                rec_intra_bs[i] = give
                
            # 确保 bitstream 的长度是8的倍数
        for i in range(len(rec_intra_bs)):
            if rec_intra_bs[i] == 'none':
                print("error: reconstruction error!")
                sys.exit(1)  # 打印错误信息后终止程序，并返回非零状态码
        
        while len(bitstream) % 8 != 0:
            bitstream += '0'
        write_bytes_len = math.ceil(len(bitstream) / 8)
        f.write(struct.pack('I', write_bytes_len))
        # print("compute cnt: ", write_bytes_len)
        byte_array = int(bitstream, 2).to_bytes(write_bytes_len, 'big')
        
        f.write(byte_array)

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
