"""
功能：读取相场模型文件（mat），根据间隔【1,2,5，6,10】在X_Z方向上生成图像
"""
import imageUtility as utility
import cv2
import numpy as np
import glob
import os

inputAddress = ".\\data\\original\\mat\\"
outputAddress = ".\\data\\interval\\"
fileList = glob.glob(inputAddress + "*.mat")
fileList.sort(reverse=True)
interval_List = [1, 2, 5, 6, 10]
interval_value = 125

for index in range(len(fileList)):
    fileName = os.path.basename(fileList[index]).split(".")[0]
    print("The filename is: {}".format(fileName))
    labelStack = utility.getLabelStackFromMat(fileList[index])
    vol = utility.calculateVolume(labelStack)
    print(" The volume is: {}".format(vol))

    # X_Z
    for interval in interval_List:
        print(" interval_{}".format(interval))
        outputFolder = outputAddress + str(fileName) + "\\X_Z\\interval_" + str(interval) + "\\"
        utility.mkoutdir(outputFolder)
        for y_index in range(0, 400):
            layer = labelStack[:, y_index, :].copy()
            tmp = np.ones(layer.shape) * interval_value
            tmp[:, ::(interval+1)] = layer[:, ::(interval+1)]
            cv2.imwrite(outputFolder + str(y_index).zfill(3) + ".png", tmp)