import csv
import struct
import numpy as np
import math
import pandas as pd
import os
import os
# 指数哥伦布解码
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
def decode_frames(bitstream, quantization_step):
    # 读取编码的bitstream
    #bitstream = read_from_bin(input_file)
    # 解码残差
    # print("len of bitstreams: ", len(bitstream))
    decoded_quantized_residuals = exponential_golomb_decode(bitstream)
    # print(len(decoded_quantized_residuals))
    
    # 使用第一帧和解码的残差重建帧
    num_frames = len(decoded_quantized_residuals)
    
    # first_frame = 0.0
    reconstructed_frames = np.zeros(num_frames)

    # reconstructed_frames[0] = first_frame
    # previous_reconstructed_frame = first_frame
    for i in range(0, num_frames):
        # 将量化残差反量化
        decoded_residual = decoded_quantized_residuals[i]
        if decoded_residual %2 == 0:
            decoded_residual = (-decoded_residual)/2
        else:
            decoded_residual = (decoded_residual+1)/2
        residual = decoded_residual * quantization_step
        # 重建当前帧
        reconstructed_frames[i] = residual
        # if(len(decoded_quantized_residuals)==340):
        #     print(reconstructed_frames[i])
        # 更新上一帧重建数据
        # previous_reconstructed_frame = reconstructed_frames[i]

    return reconstructed_frames

def decode_to_csv(header, file_folder, input_folder, output_folder):
    bin_files = os.listdir(input_folder)
    os.makedirs(output_folder, exist_ok=True)
    for bin_file in bin_files:
        new_bin = 'dec_' + bin_file
        #output_file = os.path.join(output_folder, bin_file.split('.')[0]+'.csv')
        output_file = os.path.join(output_folder, new_bin.split('.')[0]+'.csv')
        #os.rename(output_file, new_output_file)
        read_file = (bin_file.split('.')[0]+'.csv').split('_', 1)[-1]
        read_file = os.path.join(file_folder, read_file)
        quantization_step = 1 / int(bin_file.split('_', 1)[0])
        with open(os.path.join(input_folder, bin_file), 'rb') as f:
            f.seek(0, 2)
            eof = f.tell()   # 上面两行将指针移动到末尾，eof返回总的字节数
            f.seek(0, 0)     # 重新将指针归零
            #num_frames_bytes = f.read(4)
            #num_frames = struct.unpack('I', num_frames_bytes)[0]
            cnt = 0
            # print("num frames ", num_frames)
            df = pd.read_csv(read_file)
            while f.tell() < eof:
                # first_frame_bytes = f.read(8)
                # if not first_frame_bytes:
                #     return
                # first_frame = struct.unpack('d', first_frame_bytes)[0]
                
                bits_len_bytes = f.read(4)
                bits_len = struct.unpack('I', bits_len_bytes)[0]

                # first_frame = 0.0719062686
                # num_frames = 437
                
                # print("first frame: ", first_frame)
                # print("bits_len", bits_len)
                byte_data    = f.read(bits_len)
                bitstream = ''.join(format(byte, '08b') for byte in byte_data)
                df[header[cnt]] = decode_frames(bitstream, quantization_step)
                cnt += 1

            df.to_csv(output_file, index=False)

if __name__ == "__main__":  
    # 解码bin文件并重建帧数据
    input_file = "encoded_data.bin"
    output_file = 'video1.csv'
    # input_folder = 'bin'
    # output_folder = 'dec'
    ENC_FILE = '30FPS'
    input_folder = os.path.join('bin', ENC_FILE)
    output_folder = os.path.join('dec', ENC_FILE)
    file_folder = os.path.join('enc', ENC_FILE)

    first_frame = 0.0719062686
    num_frames = 437
    quantization_step = 1/256  # 与编码的一致

    csv_header = [ 'EyeBlinkLeft', 'EyeLookDownLeft', 'EyeLookInLeft', 'EyeLookOutLeft', 'EyeLookUpLeft', 'EyeSquintLeft', 'EyeWideLeft', 'EyeBlinkRight', 'EyeLookDownRight', 'EyeLookInRight', 'EyeLookOutRight', 'EyeLookUpRight', 'EyeSquintRight', 'EyeWideRight', 'JawForward', 'JawRight', 'JawLeft', 'JawOpen', 'MouthClose', 'MouthFunnel', 'MouthPucker', 'MouthRight', 'MouthLeft', 'MouthSmileLeft', 'MouthSmileRight', 'MouthFrownLeft', 'MouthFrownRight', 'MouthDimpleLeft', 'MouthDimpleRight', 'MouthStretchLeft', 'MouthStretchRight', 'MouthRollLower', 'MouthRollUpper', 'MouthShrugLower', 'MouthShrugUpper', 'MouthPressLeft', 'MouthPressRight', 'MouthLowerDownLeft', 'MouthLowerDownRight', 'MouthUpperUpLeft', 'MouthUpperUpRight', 'BrowDownLeft', 'BrowDownRight', 'BrowInnerUp', 'BrowOuterUpLeft', 'BrowOuterUpRight', 'CheekPuff', 'CheekSquintLeft', 'CheekSquintRight', 'NoseSneerLeft', 'NoseSneerRight', 'TongueOut', 'HeadYaw', 'HeadPitch', 'HeadRoll', 'LeftEyeYaw', 'LeftEyePitch', 'LeftEyeRoll', 'RightEyeYaw', 'RightEyePitch', 'RightEyeRoll']
    print("header len: ", len(csv_header))

    decode_to_csv(csv_header, file_folder, input_folder, quantization_step, output_folder)
    #reconstructed_frames = decode_frames(input_file, first_frame, quantization_step, num_frames)
