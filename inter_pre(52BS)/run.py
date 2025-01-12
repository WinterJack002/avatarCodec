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
    # bs_reference = [
    #     [0, 1, 2,  3, 4,  5,  6,  15, 16, 18, 19, 20, 21, 22, 23, 25, 27, 29, 31, 32, 33, 35, 37, 39, 41, 44, 46, 47, 49, 51],
    #     [7, 8, 10, 9, 11, 12, 13, -1, -1, -1, -1, -1, -1, -1, 24, 26, 28, 30, -1, -1, 34, 36, 38, 40, 42, 45, -1, 48, 50, -1],
    #     [-1, -1, -1, -1,  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, 17, -1, -1, 43, -1, -1, -1, -1]   
    # ]
#     bs_reference_dict = {
#     '0': 7,
#     '1': 8,
#     '2': 10,
#     '3': 9,
#     '4': 11,
#     '5': 12,
#     '6': 13,
#     '14': 29,
#     '15': 'none',
#     '16': 'none',
#     '17': 37,
#     '18': 'none',
#     '19': 'none',
#     '20': 'none',
#     '21': 'none',
#     '22': 'none',
#     '23': 24,
#     '25': 26,
#     '27': 28,
#     '29': 30,
#     '30': 31
# }
    # 预测模式
    inter_flag = 1
    intra_flag = 0

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

        # # encode time cost
        # enc_last = time.time()
        # enc_time = enc_last - start_time
        # print(f"编码时间: {enc_time:.4f} 秒")
        # decode
        decode_to_csv(csv_header, enc_input_folder, enc_output_folder,dec_output_folder, n, inter_flag, intra_flag)
