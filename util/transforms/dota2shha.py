# dota数据集格式为:x1 y1 x2 y2 x3 y3 x4 y4 类别 difficult
# 上海人群计数数据集格式为:x y 类别
# dota数据集格式转换为上海人群计数数据集格式
import os
dota_train_label = 'D:/data/dota/train/'
dota_test_label = 'D:/data/dota/test/'
# 读取dota_train_label下的所有txt文件
dota_train_label_list = os.listdir(dota_train_label)
# 将dota_train_label下的txt文件每行数据转换为上海人群计数数据集格式，并且将转换后的数据写入到shha_train_label文件夹下
for dota_train_label_txt in dota_train_label_list:
    # 打开dota_train_label下的txt文件
    with open(dota_train_label + dota_train_label_txt, 'r') as f:
        # 读取dota_train_label下的txt文件每行数据
        dota_train_label_txt_list = f.readlines()
        # 将dota_train_label下的txt文件每行数据转换为上海人群计数数据集格式
        for dota_train_label_txt_list_line in dota_train_label_txt_list:
            # 将dota_train_label下的txt文件每行数据转换为上海人群计数数据集格式
            temp = dota_train_label_txt_list_line.split(' ')
            shha_lines_list = []
            shha_lines_list.append(temp[0] + temp[2] +temp[4] +temp[6])/4 + ' ' + (temp[1] + temp[3] +temp[5] +temp[7])/4 + ' ' + temp[8] + '\n'
            # 将shha_lines_list写入到shha_train_label文件夹下
        with open('D:/data/shha/train/' + dota_train_label_txt, 'a') as f:
            f.writelines(shha_lines_list)


