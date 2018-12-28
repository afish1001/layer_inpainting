import os
import cv2
import numpy as np
import scipy.io as io


INTERVAL_VALUE = 125


def save_mat(mat_path, mat):
    mat_name = os.path.basename(mat_path).split('.')[0]
    return io.savemat(mat_path, {mat_name: mat})


def load_mat(mat_path):
    mat_name = os.path.basename(mat_path).split('.')[0]
    return io.loadmat(mat_path)[mat_name]


def get_mat_list(path):
    return list(filter(lambda x: x.endswith('.mat'), map(lambda x: os.path.join(path, x), os.listdir(path))))


def get_interval_mat(phase_mat, interval):
    """生成层间图像缺失的3D矩阵, 先将interval_mat填满空值，然后从phase_mat中的z轴隔行取"""
    interval_mat = np.full(phase_mat.shape, INTERVAL_VALUE, dtype=np.uint8)
    stride = interval + 1
    interval_mat[::stride, :, :] = phase_mat[::stride, :, :].copy()
    # interval_mat = phase_mat.copy()
    # for y_index in range(len(interval_mat)):
    #     layer = interval_mat[:, y_index, :]
    #     _tmp = np.full(layer.shape, INTERVAL_VALUE)
    #     _tmp[:, ::(interval + 1)] = layer[:, ::(interval + 1)]
    #     interval_mat[:, y_index, :] = _tmp
    return interval_mat


def generate_mat_images(folder, mat):
    """生成mat的每层图像并放入folder中"""
    os.makedirs(folder, exist_ok=True)
    for y_index in range(len(mat)):
        img_path = os.path.join(folder, '{:0>3d}.png'.format(y_index))
        cv2.imwrite(img_path, mat[:, y_index, :])
