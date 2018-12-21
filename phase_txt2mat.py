"""
功能：将相场模型的.txt文件转换为.mat文件加快读取速度
输入：数据路径文件夹（里面存放了n个.txt文件）
输出：文件夹，里面放了n个.mat文件

Usage: python phase_txt2mat.py --input data --output result --cpus 4

"""
import numpy as np
import scipy.io as io
import os
import argparse
import multiprocessing
import utils

X, Y, Z = 400, 400, 400
FRONT_VALUE = 255

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True, help='The folder path of phase.txt.')
parser.add_argument('--output', type=str, default='./result', help='The output folder.')
parser.add_argument('--cpus', type=int, default=1, help='The number of cpu you can use.')

opt = parser.parse_args()
print(opt)


def get_txt_list(folder):
    return list(filter(lambda x: x.endswith('.txt'), map(lambda x: os.path.join(folder, x), os.listdir(folder))))


def convert_worker(file_path):
    mat_name = os.path.basename(file_path).split('.')[0]
    phase_mat = np.zeros((X, Y, Z), dtype=np.uint8)
    with open(file_path, 'r') as fd:
        # 这一步可能会爆内存，可以改成 while fd.readline() 按行读取
        lines = fd.readlines()
        for line in lines:
            _line = line[:-1]
            corr = _line.split('\t')[0: 3]
            phase_mat[int(corr[0]) - 1, int(corr[1]) - 1, int(corr[2]) - 1] = FRONT_VALUE
    utils.mat.save_mat(os.path.join(opt.output, mat_name + '.mat'), phase_mat)


if __name__ == '__main__':
    file_list = get_txt_list(opt.input)
    assert file_list
    print(file_list)
    os.makedirs(opt.output, exist_ok=True)
    # convert_worker(file_list[0])
    # 多线程
    pool = multiprocessing.Pool(processes=opt.cpus)
    for file in file_list:
        pool.apply_async(convert_worker, (file, ))
    pool.close()
    pool.join()
