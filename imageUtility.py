import cv2
import numpy as np
import os
import scipy.io as io
import glob

def mkoutdir(path):
    """
    功能：创建文件夹目录，先判断文件夹是否存在，不存在则创建
    :param path:文件夹目录
    :return:
    """
    try:
        os.makedirs(path)
    except OSError:
        pass

def transformTxtToMat(fileAddress):
    """
    功能：将Pha1_XXXXX_value.txt转成mat格式，默认输出本文件夹下的mat文件夹
    :param fileAddress: txt文件地址
    :return:
    """
    fileName = os.path.basename(fileAddress).split(".")[0]
    mkoutdir(os.path.dirname(fileAddress) + "\\mat\\")
    outAddress = os.path.dirname(fileAddress) + "\\mat\\" + fileName + ".mat"
    print(outAddress)
    label3D = np.zeros((400, 400, 400), dtype=np.uint8)
    with open(fileAddress, "r") as f:
        line = f.readline()
        while line:
            line = line[:-1]
            corr = line.split("\t")[0: 3]
            label3D[int(corr[0]) - 1, int(corr[1]) - 1, int(corr[2]) - 1] = 255
            line = f.readline()
    io.savemat(outAddress, {fileName: label3D})

def getLabelStackFromImages(inputAddress, reverseLabel=False):
    """
    功能：从图像文件夹地址读取LabelStack，把图像按层赋值到labelStack中，可控制录入顺序
    :param inputAddress: 图像文件夹地址
    :param reverseLabel: True,反向录入（如从100-》1），False(默认)正向录入（如从1-》100）
    :return:读取的labelStack
    """
    fileList = os.listdir(inputAddress)
    fileList.sort(reverse=reverseLabel)
    image = cv2.imread(inputAddress + fileList[0], 0)
    labelStack = np.zeros((image.shape[0], image.shape[1], len(fileList)), dtype=np.uint8)
    labelStack[:, :, 0] = image
    for index in range(1, len(fileList)):
        image = cv2.imread(inputAddress + fileList[index], 0)
        labelStack[:, :, index] = image
    return labelStack

def getLabelStackFromMat(inputAddress):
    """
    功能：从mat文件中读取LabelStack,直接读取mat中与文件名同名的变量
    :param inputAddress:mat文件地址
    :return:读取的labelStack
    """
    fileName = os.path.basename(inputAddress).split(".")[0]
    labelStack = io.loadmat(inputAddress)[fileName]
    return labelStack

def calculateVolume(labelStack):
    """
    功能：计算体积，统计三维label矩阵中为255的个数
    :param label3D:label的3维矩阵，背景为0
    :return:体积
    """
    vol = np.count_nonzero(labelStack == 255)
    return vol

def calculateSurfaceArea(labelStack, method=0):
    """
    功能：计算表面积
    :param labelStack: 三维label矩阵，背景为0
    :param method: 计算方法，0：仅统计边缘点数目
    :return: 表面积
    """
    area = 0
    if method == 0:
        # 仅统计边缘点数目
        pass
    else:
        print(" The method isn't implemented")
    return area



if __name__ == "__main__":
    # 将txt批量转成mat
    inputAddress = ".\\data\\original\\"
    fileList = glob.glob(inputAddress + "*.txt")
    for index in range(len(fileList)):
        print("Transforming {} to Mat".format(fileList[index]))
        transformTxtToMat(fileList[index])