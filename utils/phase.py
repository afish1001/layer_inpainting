import numpy as np
from skimage import measure


def compare_ssim(phase_a, phase_b):
    ssim = 0.0
    for y_index in range(len(phase_a)):
        ssim += measure.compare_ssim(phase_a[:, y_index, :], phase_b[:, y_index, :])
    return ssim / len(phase_a)


def get_ordered_area_list(phase_mat):
    label_stack, label_num = measure.label(phase_mat, background=0, return_num=True)
    props = measure.regionprops(label_stack, cache=True)
    area_dict = {}
    for region_index in range(len(props)):
        area_dict[props[region_index].label] = props[region_index].area
    return sorted(area_dict.items(), key=lambda d: d[1], reverse=True)


def remove_phase_noise_(phase_mat):
    label_stack, label_num = measure.label(phase_mat, background=0, return_num=True)
    props = measure.regionprops(label_stack, cache=True)
    area_dict = {}
    for region_index in range(len(props)):
        area_dict[props[region_index].label] = props[region_index].area
    max_area_label = int(sorted(area_dict.items(), key=lambda d: d[1], reverse=True)[0][0])
    phase_mat[label_stack != max_area_label] = 0
    return phase_mat


def get_surface_area(phase_mat):
    return calculateSurfaceArea(phase_mat)


def get_volume(phase_mat):
    """

    :param phase_mat:
    :return:
    """
    return np.count_nonzero(phase_mat == 255)


def getSurfaceStack(labelStack,surfaceValue=200):
    """
    功能：将LabelStack中的边缘点标记成surfaceValue，判断边缘点的方法是判断每个前景点，若其26邻域内有一个背景点，则该前景点位边缘点
    :param labelStack: 三维label矩阵
    :param surfaceValue: 需要赋给表面的值，默认200
    :return: 返回边缘标记矩阵
    """
    row = labelStack.shape[0]
    col = labelStack.shape[1]
    depth = labelStack.shape[2]
    expand = np.zeros((row + 1, col + 1, depth + 1), dtype=np.int16)
    surfaceStack = expand.copy()
    expand[1: row + 1, 1: col + 1, 1: depth + 1] = labelStack
    for x in range(1, row):
        for y in range(1, col):
            for z in range(1, depth):
                if expand[x, y, z] != 255:
                    continue
                sumValue = expand[x, y, z - 1] + expand[x, y - 1, z - 1] + expand[x, y + 1, z - 1] + \
                           expand[x - 1, y, z - 1] + expand[x - 1, y - 1, z - 1] + expand[x - 1, y + 1, z - 1] + \
                           expand[x + 1, y, z - 1] + expand[x + 1, y - 1, z - 1] + expand[x + 1, y + 1, z - 1] + \
                           expand[x, y - 1, z] + expand[x, y + 1, z] + \
                           expand[x - 1, y, z] + expand[x - 1, y - 1, z] + expand[x - 1, y + 1, z] + \
                           expand[x + 1, y, z] + expand[x + 1, y - 1, z] + expand[x + 1, y + 1, z] + \
                           expand[x, y, z + 1] + expand[x, y - 1, z + 1] + expand[x, y + 1, z + 1] + \
                           expand[x - 1, y, z + 1] + expand[x - 1, y - 1, z + 1] + expand[x - 1, y + 1, z + 1] + \
                           expand[x + 1, y, z + 1] + expand[x + 1, y - 1, z + 1] + expand[x + 1, y + 1, z + 1]
                if sumValue < 255 * 26:
                    surfaceStack[x, y, z] = surfaceValue
    return surfaceStack[1: row + 1, 1: col + 1, 1: depth + 1]


def calculateSurfaceArea(labelStack, method=0):
    """
    功能：计算表面积
    :param labelStack: 三维label矩阵，背景为0,前景为255
    :param method: 计算方法，0：仅统计边缘点数目
    :return: 表面积
    """
    area = 0
    if method == 0:
        # 仅统计边缘点数目,由于未找到三维卷积代码，自己实现统计，判断每个体素，若其26领域内有一个背景点，则本体素就是边缘点
        surfaceValue = 200
        surfaceStack = getSurfaceStack(labelStack, surfaceValue=surfaceValue)
        area = np.count_nonzero(surfaceStack == surfaceValue)
    else:
        print(" The method isn't implemented")
    return area