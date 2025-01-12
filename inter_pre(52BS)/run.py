from fixed_fps_modify import frame_extraction
from enc import encode_from_csv
from dec import decode_to_csv
import os
import time
# 抽帧函数
FPS = 30
# dec_output_folder = os.path.join(r'C:\Users\winter\Desktop\dec_csv')
csv_header = ['EyeBlinkLeft', 'EyeLookDownLeft', 'EyeLookInLeft', 'EyeLookOutLeft', 'EyeLookUpLeft',
                      'EyeSquintLeft', 'EyeWideLeft', 'EyeBlinkRight', 'EyeLookDownRight', 'EyeLookInRight',
                      'EyeLookOutRight', 'EyeLookUpRight', 'EyeSquintRight', 'EyeWideRight', 'JawForward', 'JawRight',
                      'JawLeft', 'JawOpen', 'MouthClose', 'MouthFunnel', 'MouthPucker', 'MouthRight', 'MouthLeft',
                      'MouthSmileLeft', 'MouthSmileRight', 'MouthFrownLeft', 'MouthFrownRight', 'MouthDimpleLeft',
                      'MouthDimpleRight', 'MouthStretchLeft', 'MouthStretchRight', 'MouthRollLower', 'MouthRollUpper',
                      'MouthShrugLower', 'MouthShrugUpper', 'MouthPressLeft', 'MouthPressRight', 'MouthLowerDownLeft',
                      'MouthLowerDownRight', 'MouthUpperUpLeft', 'MouthUpperUpRight', 'BrowDownLeft', 'BrowDownRight',
                      'BrowInnerUp', 'BrowOuterUpLeft', 'BrowOuterUpRight', 'CheekPuff', 'CheekSquintLeft',
                      'CheekSquintRight', 'NoseSneerLeft', 'NoseSneerRight', 'TongueOut',  ]


if __name__ == '__main__':

    # extract_frame = [30, 10, 6, 3, 2, 1]
    extract_frame = [1]
    QP = [11, 13, 14, 15] # 对应[512, 128, 64, 32]
    # quantization_step = [1953, 7812, 15625, 31250]
    # quantization_step = (int(2 ** value) for value in QP)
    # 尺度因子
    n = 6
    # shift = []

    # reference mapping
    
    # 预测模式
    inter_flag = 1
    intra_flag = 1

    start_time = time.time() # 记录运行时间

    for exf in extract_frame:
        ENC_FILE = str(FPS // exf) + "FPS"
        enc_input_folder = os.path.join('enc', ENC_FILE)
        enc_output_folder = os.path.join('bin', ENC_FILE)
        dec_output_folder = os.path.join('dec', ENC_FILE)
        # fps
        frame_extraction('ori', enc_input_folder, FPS, exf)

        for qs in QP:
            # encode
            encode_from_csv(enc_input_folder, enc_output_folder, qs, n, inter_flag, intra_flag)
        print("编码结束！")
        # # encode time cost
        # enc_last = time.time()
        # enc_time = enc_last - start_time
        # print(f"编码时间: {enc_time:.4f} 秒")
        # decode
        decode_to_csv(csv_header, enc_input_folder, enc_output_folder,dec_output_folder, n, inter_flag, intra_flag)
        print("解码结束")