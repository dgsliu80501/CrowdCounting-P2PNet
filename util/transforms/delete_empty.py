# 将标签文件夹中的空文件夹删除，并且将对应的图片也删除
import os
import shutil
# 设置文件夹路径
png_folder = '/home/ipad_remote/P2PNET_ROOT/dota_split/DOTA_split_small/val/images'
txt_folder = '/home/ipad_remote/P2PNET_ROOT/dota_split/DOTA_split_small/val/gt'
# 获取文件列表
jpg_files = sorted([f for f in os.listdir(png_folder) if f.endswith('.png')])
txt_files = sorted([f for f in os.listdir(txt_folder) if f.endswith('.txt')])
# 检查文件数量是否匹配
if len(jpg_files) != len(txt_files):
    print('Error: Number of jpg and txt files do not match')
else:
    # 重命名文件
    for i, (jpg_file, txt_file) in enumerate(zip(jpg_files, txt_files)):
        if os.path.getsize(os.path.join(txt_folder, txt_file)) == 0:
            os.remove(os.path.join(txt_folder, txt_file))
            os.remove(os.path.join(png_folder, jpg_file))
            print('Files have been successfully deleted')
        else:
            continue
    print('Files have been successfully deleted')