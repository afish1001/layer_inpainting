import cv2
import numpy as np
import os
import scipy.io as io

def mkoutdir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

def calculate_volume(label3D):
    """
    功能：计算体积，统计三维label矩阵中为255的个数
    :param label3D:
    :return:
    """
    vol = np.count_nonzero(label3D == 255)
    return vol

def calculateSurfaceArea():
    pass

def transformTxtToMat(fileAddress):
    fileName = os.path.basename(fileAddress).split(".")[0]
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

if __name__ == "__main__":
    test3D = np.zeros((10, 10, 10), dtype=np.uint8)
    test3D[1, 5, 6] = 255
    test3D[1, 4, 6] = 255
    test3D[1, 3, 6] = 255
    vol = calculateaVolume(test3D)
    print(vol)

    fileAddress = ".\\data\\original\\Pha1_00020_value.txt"
    transformTxtToMat(fileAddress)