import struct
import numpy as np
import math
import csv
import os

# 帧内第一帧初始重建
rec_intra_frame = [0] * 52
# 帧间第一帧初始重建值
rec_inter_frame = [0] * 52
# 参考映射表
referenceTable = [
        [0, 1, 2,  3, 4,  5,  6,  15, 16, 18, 19, 20, 21, 22, 23, 25, 27, 29, 31, 32, 33, 35, 37, 39, 41, 44, 46, 47, 49, 51],
        [7, 8, 10, 9, 11, 12, 13, -1, -1, -1, -1, -1, -1, -1, 24, 26, 28, 30, -1, -1, 34, 36, 38, 40, 42, 45, -1, 48, 50, -1],
        [-1, -1, -1, -1,  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, 17, -1, -1, 43, -1, -1, -1, -1]
    ]
# 帧内预测
def intra_prediction(frames, rec_intra_frame):
    res_frames = ['none'] * 52
    for i in range(len(frames)):
        if   i in referenceTable[0]:
            res_frames[i] = frames[i]
    for i in range(len(frames)):
        if   i in referenceTable[1]:
            res_frames[i] = frames[i] - rec_intra_frame[referenceTable[0][i]]
    for i in range(len(frames)):
        if   i in referenceTable[2]:
            res_frames[i] = frames[i] - rec_intra_frame[referenceTable[0][i]]    
    for i in range(len(res_frames)):
        if res_frames[i] == 'none':
            print("error: intra_prediction, reference mapping error")
    
    return res_frames   
# 帧内重建
def rec_intra_prediction(quantized_residual, quantization_step):
    rec_intra_frame = ['none'] * 52
    for i, value in quantized_residual:
        if   i in referenceTable[0]:
            if value % 2 == 0:
                value = int((-value) / 2)
            else:
                value = int((value + 1) / 2)
            rec_intra_frame[i] =  value * quantization_step
    for i, value in quantized_residual:
        if   i in referenceTable[1]:
            if value % 2 == 0:
                value = int((-value) / 2)
            else:
                value = int((value + 1) / 2)
            rec_intra_frame[i] =  value * quantization_step + rec_intra_frame[referenceTable[0][i]]     
    for i, value in quantized_residual:
        if   i in referenceTable[2]:
            if value % 2 == 0:
                value = int((-value) / 2)
            else:
                value = int((value + 1) / 2)
            rec_intra_frame[i] =  value * quantization_step + rec_intra_frame[referenceTable[0][i]] 
    return rec_intra_frame

# 帧间预测
def inter_prediction(current_frame, previous_reconstructed_frame):
    residual = []
    for i in range(len(current_frame)):
        residual.append(int(current_frame[i]- previous_reconstructed_frame[i])) 
    return residual
# 帧间重建
def rec_inter_prediction(quantized_residual, quantization_step):
    for i, value in quantized_residual:
            if value % 2 == 0:
                value = int((-value) / 2)
            else:
                value = int((value + 1) / 2)

            rec_inter_frame[i] = rec_inter_frame[i] + value * quantization_step
    return rec_inter_frame

# 数据偏移


# 量化残差
def quantize(data, quantization_step):
    quantized_data = []
    for value in data:
        rounded_value = np.round(value / quantization_step)
        int_value = int(rounded_value)
        if int_value > 0:
            # 正数变为正奇数
            quantized_value = int_value * 2 - 1
        else:
            quantized_value = (-int_value) * 2
        quantized_data.append(quantized_value)
    return quantized_data


# 指数哥伦布编码
def exponential_golomb_encode(values):
    frame = ''
    for value in values:
        unarycode = ''
        golombCode = ''
        groupID = np.floor(np.log2(value + 1))
        temp_ = groupID
        # print(groupID)

        while temp_ > 0:
            unarycode = unarycode + '0'
            temp_ = temp_ - 1
        unarycode = unarycode  # +'1'

        index_binary = bin(value + 1).replace('0b', '')
        golombCode = unarycode + index_binary

        frame = frame + golombCode
    return frame


def encode_frames(frames, quantization_step, filename, inter_flag, intra_flag):
    with open(filename, 'ab+') as f:
        # f.write(struct.pack('d', frames[0]))  # 负数
        bitstream = ''
        rec_intra_frame = frames

        if intra_flag:
            frames = intra_prediction(frames, rec_intra_frame)
        else:
            pass 
      
        if inter_flag:
            residual = inter_prediction(frames, rec_inter_frame)
        else:
            residual = frames
             
        # 量化残差
        quantized_residual = quantize(residual, quantization_step)
        # 指数哥伦布编码
        encoded_residual = exponential_golomb_encode(quantized_residual)
        bitstream += encoded_residual
            
        # 帧间重建   
        if inter_flag:
            # 重建下一帧
            rec_inter_frame = rec_inter_prediction(quantized_residual, quantization_step)  
        else:
            pass
        
        if intra_flag:
            rec_intra_frame = rec_intra_prediction(quantized_residual, quantization_step)
        else:
            pass 
                

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

        f.close()

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
