import csv
import struct
import numpy as np
import math
import pandas as pd
import os
import os
import re
import sys 
# 指数哥伦布解码
# 使用第一帧和解码的残差重建帧
num_bs= 52

# first_frame = 0.0
previous_reconstructed_frame = [0] * 52
referenceTable = [
        [ 0, 1,  2,  3,  4,  5,  6,  14, 15, 16, 17,   18, 19, 20, 21, 22, 23, 25,  27,  31, 32, 33, 35,  39, 41, 43, 46, 47, 49, 51],
        [ 7, 8, 10,  9, 11, 12, 13,  29, -1, -1, 37,   -1, -1, -1, -1, -1, 24, 26,  28,  -1, -1, 34, 36,  40, 42, 44, -1, 48, 50, -1],
        [-1,-1, -1, -1, -1, -1, -1,  30, -1, -1, 38,   -1, -1, -1, -1, -1, -1, -1,  -1,  -1, -1, -1, -1,  -1, -1, 45, -1, -1, -1, -1]
    ]
def exponential_golomb_decode(bitstream):
    values = []
    index = 0
    while index < len(bitstream):
        # 读取前缀（连续的0，直到第一个1）
        q = 0
        while index < len(bitstream) and bitstream[index] == '0':
            q += 1
            index += 1
        if index >= len(bitstream):
            break
        index += 1  # 跳过'1'
        # 读取后缀
        suffix = bitstream[index:index + q]
        m = (1 << q) + int(suffix, 2) if suffix else (1 << q)
        values.append(m-1)
        index += q

    return values # 数量不对


# 解码帧数据
def decode_frames(bitstream, quantization_step, bs_scale, inter_flag, intra_flag):
   
    decoded_quantized_residuals = exponential_golomb_decode(bitstream)
    rec_intra_bs = ['none'] * 52
    for i in range(0, num_bs):
        # 将量化残差反量化
        decoded_residual = decoded_quantized_residuals[i]
        # 重建当前帧
        if inter_flag:
                # 重建下一帧
                if decoded_residual % 2 == 0:
                    quantized_residual = int((-decoded_residual) / 2)
                else:
                    quantized_residual = int((decoded_residual + 1) / 2)

                previous_reconstructed_frame[i] = previous_reconstructed_frame[i] + quantized_residual * quantization_step
                give = previous_reconstructed_frame[i]
        else:
                if decoded_residual % 2 == 0:
                        quantized_residual = int((-decoded_residual) / 2)
                else:
                        quantized_residual = int((decoded_residual + 1) / 2)
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
    for i in range(len(rec_intra_bs)):
         if rec_intra_bs[i] == 'none':
            print('error: reconstruction failed!')
            sys.exit(1)  # 打印错误信息后终止程序，并返回非零状态码

    frame_data = [ (float(value) / bs_scale) for value in rec_intra_bs ]         
    return frame_data

def decode_to_csv(header, file_folder, input_folder, output_folder, n=6, inter_flag=0, intra_flag=0):
    bin_files = os.listdir(input_folder)
    os.makedirs(output_folder, exist_ok=True)
    bs_scale = 10 ** n
    for bin_file in bin_files:
        new_bin = 'dec_' + bin_file
        #output_file = os.path.join(output_folder, bin_file.split('.')[0]+'.csv')
        output_file = os.path.join(output_folder, new_bin.split('.')[0]+'.csv')
        #os.rename(output_file, new_output_file)
        read_file = (bin_file.split('.')[0]+'.csv').split('_', 1)[-1]
        read_file = os.path.join(file_folder, read_file)
        match = re.search(r'QP(\d+)_', bin_file)
        QP = int(match.group(1))
        quantization_step = 2 ** QP
        with open(os.path.join(input_folder, bin_file), 'rb') as f:
            f.seek(0, 2)
            eof = f.tell()   # 上面两行将指针移动到末尾，eof返回总的字节数
            f.seek(0, 0)     # 重新将指针归零
         
            cnt = 0

            row_index = 0  # 从第2行开始写数据
            df = pd.read_csv(read_file)
            while f.tell() < eof:
                
                bits_len_bytes = f.read(4)
                bits_len = struct.unpack('I', bits_len_bytes)[0]

                byte_data    = f.read(bits_len)
                bitstream = ''.join(format(byte, '08b') for byte in byte_data) # 每52个换下一行

                row_data = decode_frames(bitstream, quantization_step, bs_scale, inter_flag, intra_flag)
                # 将数据添加到 DataFrame 中
                for i, value in enumerate(row_data):
                    df.at[row_index, header[cnt + i]] = value  # 将对应的值写入当前行

                # 更新行号
                row_index += 1
                # cnt = 0
                # if row_index == 30:
                #     break
            df.to_csv(output_file, index=False)

if __name__ == "__main__":  
    # 解码bin文件并重建帧数据
    # input_file = "encoded_data.bin"
    # output_file = 'video1.csv'
    # input_folder = 'bin'
    # output_folder = 'dec'
    ENC_FILE = '30FPS'
    input_folder = os.path.join('bin', ENC_FILE)
    output_folder = os.path.join('dec', ENC_FILE)
    file_folder = os.path.join('enc', ENC_FILE)

    # first_frame = 0.0719062686
    # num_frames = 437
    # quantization_step = 1/256  # 与编码的一致

    csv_header = [ 'EyeBlinkLeft', 'EyeSquintLeft', 'EyeWideLeft', 'EyeBlinkRight', 'EyeSquintRight', 'EyeWideRight', 'JawOpen', 'MouthClose',
 'MouthSmileLeft', 'MouthSmileRight', 'MouthFrownLeft', 'MouthFrownRight', 'MouthLowerDownLeft', 'MouthLowerDownRight','MouthUpperUpLeft', 'MouthUpperUpRight',
 'BrowDownLeft', 'BrowDownRight', 'BrowInnerUp', 'BrowOuterUpLeft', 'BrowOuterUpRight', 'NoseSneerLeft', 'NoseSneerRight', 'HeadYaw', 'HeadPitch', 'HeadRoll',]
    
    print("header len: ", len(csv_header))

    decode_to_csv(csv_header, file_folder, input_folder, output_folder)
    #reconstructed_frames = decode_frames(input_file, first_frame, quantization_step, num_frames)
