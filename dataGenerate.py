import imageUtility as utility
import cv2
import numpy as np
import glob
import os
import scipy.io as io

inputAddress = ".\\data\\original\\mat\\"
outputAddress = ".\\reult\\"
fileList = glob.glob(inputAddress + "*.mat")
fileList.sort(reverse=True)
interval_List = [1, 2, 5, 6, 10]
interval_value = 125

for index in range(len(fileList)):
    fileName = os.path.basename(fileList[index]).split(".")[0]
    print("The filename is: {}".format(fileName))
    # label3D = np.zeros((400, 400, 400), dtype=np.uint8)
    # with open(fileList[index], "r") as f:
    #     line = f.readline()
    #     while line:
    #         line = line[:-1]
    #         corr = line.split("\t")[0: 3]
    #         label3D[int(corr[0])-1, int(corr[1])-1, int(corr[2])-1] = 255
    #         line = f.readline()
    label3D = io.loadmat(fileList[index])[fileName]
    vol = utility.calculateaVolume(label3D)
    print(" The volume is: {}".format(vol))

    # X_Z
    for interval in interval_List:
        outputFolder = outputAddress + str(fileName) + "\\X_Z\\interval_" + str(interval) + "\\"
        print(outputFolder)
        utility.mkoutdir(outputFolder)
        for y_index in range(0, 400):
            layer = label3D[:, y_index, :].copy()
            tmp = np.ones(layer.shape) * interval_value
            tmp[:, ::(interval+1)] = layer[:, ::(interval+1)]
            cv2.imwrite(outputFolder + str(y_index).zfill(3) + ".png", tmp)
    input()