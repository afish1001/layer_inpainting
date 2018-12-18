"""
层间图像修复（传统方法）
输入文件夹默认为 data
输出文件夹默认为 result

Usage: python inpaint.py

Example:
    data/
        - Pha1_00020_value/
            - interval_1/
                - 000.png
                - 001.png
                ...
            - interval_2/
            - interval_3/
    result/
        - NS/
            - Pha1_00020_value/
                - images/
                    - interval_1/
                        - 000.png
                        - 001.png
                        ...
                    - interval_2/
                    - interval_3/
                - interval_1.mat
                - interval_2.mat
                - interval_3.mat
                ...


"""

import os
import argparse
import multiprocessing
import cv2
import numpy as np
import scipy.io as io

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default='./data', help='The input image directory.')
parser.add_argument('--out', type=str, default='./result', help='The output directory.')

opt = parser.parse_args()
if not opt.out.endswith('/'):
    opt.out += '/'
print(opt)

GAP_RADIUS_MAP = {
    1: 2,
    2: 2,
    3: 1,
    4: 20,
    5: 24,
    6: 26,
}

MASK_VALUE = 125  # 图像中标记mask的值为125
INTERVAL_LIST = [1, 2, 3, 4, 5, 6]


def mkoutdir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def layer_inpainting(img, mask, interval, mode='NS'):
    """
    层间图像修复，修复用的参数从MAP中取
    :param img: 输入的图像
    :param mask: mask图像
    :param interval: 层间间隔
    :param mode: 图像恢复的算法，NS或TELEA
    :return: 修复的图像
    """
    radius = GAP_RADIUS_MAP[interval]
    if mode == 'NS':
        return cv2.inpaint(img, mask, radius, cv2.INPAINT_NS)
    elif mode == 'TELEA':
        return cv2.inpaint(img, mask, radius, cv2.INPAINT_TELEA)
    else:
        raise TypeError('The inpaint method is not supported')


def binaryzation_(img, threshold=125):
    """
    二值化图像，会直接修改原始数据，所以在函数名后加下划线
    :param img: numpy.darray
    :param threshold: number, 0~255
    :return: None
    """
    img[img < threshold] = 0
    img[img >= threshold] = 255


def get_flist(path):
    flist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('jpeg') or file.endswith('.png'):
                flist.append(os.path.join(root, file))
    return flist


def mat_inpaint_worker(pha_dir, interval, mode='TELEA'):
    """
    输入pha文件夹路径和 interval
    生成 interval_2.mat 文件和 images/interval_2/000.png-399.png
    :param pha_dir: string,     example: ./data/Pha1_00020_value
    :param interval: number,    example: 2
    :param mode: string,        example: 'NS' or 'TELEA'
    :return: None
    """
    # 获取 pha_dir 路径的名字, 如：Pha1_00020_value
    pha_name = os.path.basename(os.path.dirname(pha_dir))
    # 获取 interval 路径的名字，如：interval_2
    interval_name = 'interval_{}'.format(interval)
    # 获取各种路径
    input_folder = os.path.join(pha_dir, interval_name)
    out_folder = os.path.join(opt.out, mode, pha_name)
    img_folder = os.path.join(out_folder, 'images', interval_name)

    mkoutdir(img_folder)

    # 读取 Pha1_00020_value/interval_2 下的所有文件路径
    flist = get_flist(input_folder)

    # 从第一张图片获取mask（同一个interval下使用的mask是一样的）
    img = cv2.imread(flist[0], cv2.IMREAD_GRAYSCALE)
    mask = np.zeros(img.shape, dtype=np.uint8)
    mask[img == MASK_VALUE] = 255

    mat = []

    # 遍历flist，修复每层图像并推入mat中
    for i, file in enumerate(flist):
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        layer = layer_inpainting(img, mask, interval, mode=mode)
        binaryzation_(layer)
        cv2.imwrite(os.path.join(img_folder, os.path.basename(file)), layer)
        mat.append(layer)

    # 将mat保存为 result/Pha1_00020_value/interval_2.mat , key = interval_2
    mat = np.array(mat)
    io.savemat(os.path.join(out_folder, interval_name + '.mat'), {interval_name: mat})


if __name__ == '__main__':
    pha_list = os.listdir(opt.input)

    # 多线程
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for pha_dir in pha_list:
        for interval in INTERVAL_LIST:
            pool.apply_async(mat_inpaint_worker, (pha_dir, interval, 'TELEA'))
    pool.close()
    pool.join()
