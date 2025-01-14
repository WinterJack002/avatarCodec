import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime

# 根目录路径
root_path = r'C:\Users\winter\Desktop\MPEG149-data\计算BS-PSNR-maleTalking'  # 修改为你自己的根目录路径
# 参考文件路径
ref_file = 'Reference_maleTalking_rounded.csv'  # 修改为你的reference.csv文件名
ref_path = os.path.join(root_path, ref_file)
ref_df = pd.read_csv(ref_path)

# 获取bs名称和数据长度
bs_list = ref_df.columns
bs_list = bs_list.delete([0, 1])  # 删除前两列（假设第一列和第二列为非图像数据）
length = ref_df[bs_list[0]].size

# 子目录列表，存放压缩失真重建数据的.csv文件
subdirs = ['00', '01', '10', '11']  # 你的四个子目录
comp_list = []

# 从子目录读取压缩数据文件
for subdir in subdirs:
    subdir_path = os.path.join(root_path, subdir)
    files_list = os.listdir(subdir_path)
    for f in files_list:
        if f.endswith('.csv'):
            comp_list.append(os.path.join(subdir_path, f))

result_all = []
result_per_PSNR = {}
result_per_MSE = {}
# 计算每个压缩数据文件的PSNR
for file_path in tqdm(comp_list, total=len(comp_list), desc="Calculating PSNR"):
    comp_df = pd.read_csv(file_path)

    PSNR_list = []
    PSNR_list_to_excel = []
    MSE_list_all = []

    for i in range(length):
        MSE_list = []
        for bs in bs_list:
            MSE = (ref_df[bs][i] - comp_df[bs][i])**2
            MSE_list.append(MSE)
        MSE_mean = np.mean(MSE_list)
        MSE_list_all.append(MSE_mean)
        
        if MSE_mean == 0:
            PSNR_list_to_excel.append('inf')
        else:
            psnr = 10 * np.log10(1.0 / MSE_mean)
            PSNR_list.append(psnr)
            PSNR_list_to_excel.append(psnr)

    PSNR_mean = np.mean(PSNR_list)
    MSE_mean_all = np.mean(MSE_list_all)
    
    result_all.append([file_path.split(os.sep)[-1].split('.')[0], PSNR_mean, MSE_mean_all])
    result_per_PSNR[file_path.split(os.sep)[-1].split('.')[0]] = PSNR_list_to_excel 
    result_per_MSE[file_path.split(os.sep)[-1].split('.')[0]] = MSE_list_all
    

# 将结果写入Excel文件
time = datetime.now().strftime('%Y_%m_%d_%Hh_%Mmin_%Ssec')
df1 = pd.DataFrame(result_all, columns=['filename', 'PSNR', 'MSE_mean'])
df1.to_excel(f'./result_PSNR_{time}.xlsx', index=False, engine='openpyxl')

# 记录每帧的PSNR
df2 = pd.DataFrame(result_per_PSNR)
df2.to_excel(f'./result_PSNR_per_frames_{time}.xlsx', engine='openpyxl', index=False)

# 记录每帧的MSE
df3 = pd.DataFrame(result_per_MSE)
df3.to_excel(f'./result_MSE_per_frames_{time}.xlsx', engine='openpyxl', index=False)
# import os
# import pandas as pd
# import numpy as np
# from tqdm import tqdm
# from datetime import datetime

# # 读取文件夹
# root_path = '../maleTalking/'
# # 参考文件
# ref_file = 'Reference_maleTalking_rounded.csv'
# ref_path = os.path.join(root_path, ref_file)
# # ref_path = '../maleTalking/Reference_maleTalking_rounded.csv'
# ref_df = pd.read_csv(ref_path)
# # 获取bs名称和数据长度
# bs_list = ref_df.columns
# bs_list = bs_list.delete([0, 1])
# length = ref_df[bs_list[0]].size
# # 读取压缩数据文件
# # comp_list = os.listdir(root_path)
# files_list = os.listdir(root_path)
# comp_list = []
# for f in files_list:
#     if 'new' in f:
#         comp_list.append(f)

# result_all = []
# result_per = {}
# for file_name in tqdm(comp_list, total=len(comp_list), desc="Calculating PSNR"):
#     comp_path = os.path.join(root_path, file_name)
#     comp_df = pd.read_csv(comp_path)

#     PSNR_list = []
#     PSNR_list_to_excel = []
#     for i in range(length):
#         MSE_list = []
#         for bs in bs_list:
#             MSE_list.append((ref_df[bs][i] - comp_df[bs][i])**2)
#         MSE_mean = np.mean(MSE_list)
#         if MSE_mean == 0:
#             PSNR_list_to_excel.append('inf')
#         else:
#             psnr = 10*np.log10(1.0/MSE_mean)
#             PSNR_list.append(psnr)
#             PSNR_list_to_excel.append(psnr)
#     PSNR_mean = np.mean(PSNR_list)
#     result_all.append([file_name.split('.')[0], PSNR_mean])
#     result_per[file_name.split('.')[0]] = PSNR_list_to_excel
# df1 = pd.DataFrame(result_all, columns=['filename', 'PSNR'])
# time = datetime.now().strftime('%Y_%m_%d_%Hh_%Mmin_%Ssec')
# df1.to_excel(f'./result_PSNR_{time}.xlsx', index=False, engine='openpyxl')
# df2 = pd.DataFrame(result_per)
# df2.to_excel(f'./result_PSNR_per_frames_{time}.xlsx', engine='openpyxl', index=False)

