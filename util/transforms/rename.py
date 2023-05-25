import os

# 设置文件夹路径
png_folder = '/data/ycchen/dota_counting/images/val/images/'
txt_folder = '/data/ycchen/dota_counting/P2PNET_label/val/'

# 获取文件列表
jpg_files = sorted([f for f in os.listdir(png_folder) if f.endswith('.png')])
txt_files = sorted([f for f in os.listdir(txt_folder) if f.endswith('.txt')])

# 检查文件数量是否匹配
if len(jpg_files) != len(txt_files):
    print('Error: Number of jpg and txt files do not match')
else:
    # 重命名文件
    for i, (jpg_file, txt_file) in enumerate(zip(jpg_files, txt_files)):
        os.rename(os.path.join(png_folder, jpg_file), os.path.join(png_folder, f'IMG_{i}.png'))
        os.rename(os.path.join(txt_folder, txt_file), os.path.join(txt_folder, f'GT_IMG_{i}.txt'))

    print('Files have been successfully renamed')




