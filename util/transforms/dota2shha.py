# dota数据集格式为:x1 y1 x2 y2 x3 y3 x4 y4 类别 difficult
# 上海人群计数数据集格式为:x y 类别
# dota数据集格式转换为上海人群计数数据集格式
import os
dota_train_label = '/data/ycchen/DOTA_split/train/annfiles/'
dota_test_label = '/data/ycchen/DOTA_split/test/annfiles/'
# 读取dota_test_label下的所有txt文件
dota_test_label_list = os.listdir(dota_test_label)
# 将dota_test_label下的txt文件每行数据转换为上海人群计数数据集格式，并且将转换后的数据写入到shha_test_label文件夹下
for dota_test_label_txt in dota_test_label_list:
    # 打开dota_test_label下的txt文件
    with open(dota_test_label + dota_test_label_txt, 'r') as f:
        # 读取dota_test_label下的txt文件每行数据
        dota_test_label_txt_list = f.readlines()
        shha_lines_list = []
        # 将dota_test_label下的txt文件每行数据转换为上海人群计数数据集格式
        for dota_test_label_txt_list_line in dota_test_label_txt_list:
            # 将dota_test_label下的txt文件每行数据转换为上海人群计数数据集格式
            temp = dota_test_label_txt_list_line.split(' ')
            #将temp中前8个元素转换为float类型
            for i in range(8):
                temp[i] = float(temp[i])
            shha_lines_list.append(str((temp[0] + temp[2] +temp[4] +temp[6])/4) + ' ' + str((temp[1] + temp[3] +temp[5] +temp[7])/4) + ' ' + temp[8] + '\n')
            # 将shha_lines_list写入到shha_test_label文件夹下
        with open('/data/ycchen/P2PNET/val/' + dota_test_label_txt, 'a') as f:
            f.writelines(shha_lines_list)


