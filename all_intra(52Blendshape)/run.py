from fixed_fps_modify import frame_extraction
from enc import encode_from_csv
from dec import decode_to_csv
import os

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
                      'CheekSquintRight', 'NoseSneerLeft', 'NoseSneerRight', 'TongueOut', ]


if __name__ == '__main__':

    # extract_frame = [30, 10, 6, 3, 2, 1]
    extract_frame = [1]
    # quantization_step = [16, 32, 64, 128, 256, 512]
    quantization_step = [16, 128,  512]


    for exf in extract_frame:
        ENC_FILE = str(FPS // exf) + "FPS"
        enc_input_folder = os.path.join('enc', ENC_FILE)
        enc_output_folder = os.path.join('bin', ENC_FILE)
        dec_output_folder = os.path.join('dec', ENC_FILE)
        # fps
        frame_extraction('ori', enc_input_folder, FPS, exf)

        for qs in quantization_step:
            # encode
            encode_from_csv(enc_input_folder, qs, enc_output_folder)

        # decode
        decode_to_csv(csv_header, enc_input_folder, enc_output_folder,dec_output_folder)
