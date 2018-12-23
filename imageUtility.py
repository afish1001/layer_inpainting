import cv2
import numpy as np
import os
import scipy.io as io
import glob
import time

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

def getLabelStackFromImages(inputDir, reverseLabel=False):
    """
    功能：从图像文件夹地址读取LabelStack，把图像按层赋值到labelStack中，可控制录入顺序
    :param inputDir: string, 输入图像文件夹地址，windows后面有"//"，linxu后面有"\"
    :param reverseLabel: True,反向录入（如从100-》1），False(默认)正向录入（如从1-》100）
    :return:读取的labelStack
    """
    fileList = os.listdir(inputDir)
    fileList.sort(reverse=reverseLabel)
    image = cv2.imread(inputDir + fileList[0], 0)
    labelStack = np.zeros((image.shape[0], image.shape[1], len(fileList)), dtype=np.uint8)
    labelStack[:, :, 0] = image
    for index in range(1, len(fileList)):
        image = cv2.imread(inputDir + fileList[index], 0)
        labelStack[:, :, index] = image
    return labelStack

def saveLabelStackToImages(labelStack, outputDir, ext=".png"):
    """
    功能：将三维label矩阵按照从上到下的方式存成图像
    :param labelStack:三维label矩阵
    :param outputDir:string, 输出地址，对于windows，后面要有"//",对于linux,后面要有“\”
    :param ext:文件扩展名，默认为“.png”
    :return:
    """
    depth = labelStack.shape[2]
    mkoutdir(outputDir)
    for i in range(depth):
        fileName = str(i).zfill(3) + ext
        image = labelStack[:, :, i]
        cv2.imwrite(outputDir + fileName, image)

def getLabelStackFromMat(inputAddress):
    """
    功能：从mat文件中读取LabelStack,直接读取mat中与文件名同名的变量
    :param inputAddress:mat文件地址
    :return:读取的labelStack
    """
    fileName = os.path.basename(inputAddress).split(".")[0]
    labelStack = io.loadmat(inputAddress)[fileName]
    return labelStack

def saveLabelStackToMat(labelStack, outputDir, fileName):
    """
    功能：将三维labelStack矩阵以Mat的形式存到相应位置
    :param labelStack: 三维label矩阵
    :param outputDir: 输出文件夹地址
    :param fileName: 文件名
    :return:
    """
    outputAddress = outputDir + fileName + ".mat"
    io.savemat(outputAddress, {fileName: labelStack})

def transformTxtToMat(fileAddress):
    """
    功能：将Pha1_XXXXX_value.txt转成mat格式，默认输出本文件夹下的mat文件夹
    :param fileAddress: txt文件地址
    :return:
    """
    fileName = str(os.path.basename(fileAddress).split(".")[0])
    mkoutdir(os.path.dirname(fileAddress) + "\\mat\\")
    outputDir = os.path.dirname(fileAddress) + "\\mat\\"
    print(outputDir + fileName + ".mat")
    labelStack = np.zeros((400, 400, 400), dtype=np.uint8)
    with open(fileAddress, "r") as f:
        line = f.readline()
        while line:
            line = line[:-1]
            corr = line.split("\t")[0: 3]
            labelStack[int(corr[0]) - 1, int(corr[1]) - 1, int(corr[2]) - 1] = 255
            line = f.readline()
    saveLabelStackToMat(labelStack, outputDir, fileName)

def calculateVolume(labelStack):
    """
    功能：计算体积，统计三维label矩阵中为255的个数
    :param label3D:label的3维矩阵，背景为0
    :return:体积
    """
    vol = np.count_nonzero(labelStack == 255)
    return vol

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

def erodeLabelStack(labelStack, iteration=1):
    """
    功能：简单消除最外层边缘点，为三维骨架化预处理数据，默认背景为0，前景255，将最外层边缘设置为200,同一删除
    :param labelStack:三维标记矩阵
    :param iteration: 迭代步数，默认为1步
    :return: 消除边缘点的LabelStack
    """
    erodeStack = labelStack.copy()
    for _ in range(iteration):
        surfaceValue = 200
        surfaceStack = getSurfaceStack(erodeStack, surfaceValue=200)
        erodeStack[surfaceStack == surfaceValue] = 0
    return erodeStack


if __name__ == "__main__":
    # # 将txt批量转成mat
    # inputDir = ".\\data\\original\\"
    # fileList = glob.glob(inputDir + "*.txt")
    # for index in range(len(fileList)):
    #     print("Transforming {} to Mat".format(fileList[index]))
    #     transformTxtToMat(fileList[index])

    # 读取stack, 将其边缘腐蚀几层
    iterationNum = 5
    inputAddress = ".\\data\\original\\mat\\Pha1_00006_value.mat"
    labelStack = getLabelStackFromMat(inputAddress)
    startTime = time.time()
    erodeStack = erodeLabelStack(labelStack, iteration=iterationNum)
    endTime = time.time()
    print("Erode duration:{}'s".format(endTime - startTime))
    outputDir = ".\\result\\erodeFile\\"
    saveLabelStackToImages(erodeStack, outputDir)
