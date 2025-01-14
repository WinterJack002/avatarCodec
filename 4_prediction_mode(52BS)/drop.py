import pandas as pd
import os

drop_name = [ 'LeftEyeYaw', 'LeftEyePitch', 'LeftEyeRoll', 'RightEyeYaw', 'RightEyePitch',
                      'RightEyeRoll','HeadYaw', 'HeadPitch', 'HeadRoll']

# drop_name = ['EyeLookDownLeft', 'EyeLookInLeft', 'EyeLookOutLeft', 'EyeLookUpLeft', 'EyeLookDownRight', 'EyeLookInRight', 'EyeLookOutRight', 'EyeLookUpRight', 'JawForward', 'JawRight', 'JawLeft', 'MouthFunnel', 'MouthPucker', 'MouthRight', 'MouthLeft', 'MouthDimpleLeft', 'MouthDimpleRight', 'MouthStretchLeft', 'MouthStretchRight', 'MouthRollLower', 'MouthRollUpper', 'MouthShrugLower', 'MouthShrugUpper', 'MouthPressLeft', 'MouthPressRight', 'CheekPuff', 'CheekSquintLeft', 'CheekSquintRight', 'TongueOut', 'HeadYaw', 'HeadPitch', 'HeadRoll', 'LeftEyeYaw', 'LeftEyePitch', 'LeftEyeRoll', 'RightEyeYaw', 'RightEyePitch', 'RightEyeRoll']

csv_files = os.listdir('ori')
for csv_file in csv_files:
    csv_path = os.path.join('ori', csv_file)
    new_csv_path = os.path.join('ori', 'drop_55BS_'+csv_file)
    df = pd.read_csv(csv_path)
    df = df.drop(drop_name, axis=1)
    df.to_csv(new_csv_path, index=False)
