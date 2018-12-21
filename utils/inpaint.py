import os
import numpy as np
import cv2

BINARY_THRESHOLD = 125

INTERVAL_RADIUS = {
    1: 2,
    2: 2,
    3: 1,
    4: 3,
    5: 3,
    6: 3,
}


def _get_interval_layer(layer_img, interval, interval_value):
    """将单张层间图像变为层间缺失图像"""
    layer = layer_img.copy()
    interval_img = np.full(layer.shape, interval_value)
    interval_img[:, ::(interval + 1)] = layer[:, ::(interval + 1)]
    return interval_img


def inpaint_interval_layer(layer_img, mask, interval, mode='TELEA'):
    """修复当张层间缺失图像"""
    radius = INTERVAL_RADIUS[interval]
    if mode == 'NS':
        _mode = cv2.INPAINT_NS
    elif mode == 'TELEA':
        _mode = cv2.INPAINT_TELEA
    else:
        raise TypeError('The inpaint method is not supported.')
    return cv2.inpaint(layer_img, mask, radius, _mode)


def binary_img_(img):
    """二值化图像，会直接修改原始数据，所以在函数名后加下划线"""
    img[img < BINARY_THRESHOLD] = 0
    img[img >= BINARY_THRESHOLD] = 255


def complete_interval_mat(interval_mat, interval, mode='TELEA'):
    """修复层间缺失的3D矩阵（从z轴中抽走了interval层图像），按y轴取图像"""
    complete_mat = interval_mat.copy()
    mask = np.full(complete_mat[1, :, :].shape, 255, dtype=np.uint8)
    stride = interval + 1
    mask[::stride, :] = 0
    for y_index in range(len(complete_mat)):
        completed_layer = inpaint_interval_layer(complete_mat[:, y_index, :], mask, interval, mode)
        binary_img_(completed_layer)
        complete_mat[:, y_index, :] = completed_layer
    return complete_mat
