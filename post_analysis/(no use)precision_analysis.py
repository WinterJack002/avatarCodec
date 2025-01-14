import os
import csv
from decimal import Decimal, ROUND_DOWN

# 定义输入目录和文件
input_dir = r'C:\Users\winter\Desktop\MPEG149-data\cut6'
output_suffix = '_cut6'

def round_csv_data(filename):
    input_file = os.path.join(input_dir, filename)
    output_file = os.path.join(input_dir, filename.replace('.csv', f'{output_suffix}.csv'))
    
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)  # 读取所有数据
    
    # 遍历从第二行第三列开始的数据，四舍五入到小数点后六位
    for row_idx in range(1, len(rows)):  # 从第二行（索引1）开始
        for col_idx in range(2, len(rows[row_idx])):  # 从第三列（索引2）开始
            try:
                # 四舍五入到小数点后6位
                # rows[row_idx][col_idx] = round(float(rows[row_idx][col_idx]), 6) # 四舍五入保留6位
                # rows[row_idx][col_idx] = float(f"{float(rows[row_idx][col_idx]):.6f}") # 截断取前6位小数(失效)
                # rows[row_idx][col_idx] = int(rows[row_idx][col_idx] * 10**6) / 10**6 # 速度极慢
                rows[row_idx][col_idx] = Decimal(str(rows[row_idx][col_idx])).quantize(Decimal('0.000001'), rounding=ROUND_DOWN)

            except ValueError:
                # 如果不是数值，跳过该项
                continue
    
    # 将处理后的数据写入新文件
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    
    print(f'处理后的文件已保存为: {output_file}')

# 读取目录下的所有CSV文件并处理
for file in os.listdir(input_dir):
    if file.endswith('.csv'):
        round_csv_data(file)
