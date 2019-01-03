"""
将video文件变为mat文件和图片文件

Usage: python phase_video2mat.py --input ./data/phase.mp4 --output ./result

"""
import os
import argparse
import numpy as np
import cv2
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--input',  type=str, required=True, help='The input mp4 file.')
parser.add_argument('--output', type=str, default='./result', help='The output file.')

opt = parser.parse_args()
print(opt)


def video2mat(video_path):
    cap = cv2.VideoCapture(video_path)
    mat = []
    success, image = cap.read()
    while success:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        utils.inpaint.binary_img_(image)
        mat.append(image)
        success, image = cap.read()
    return np.array(mat, dtype=np.uint8)


if __name__ == '__main__':
    mat = video2mat(opt.input)
    # TODO: 批量
    folder = os.path.join(opt.output, 'Pha1_00020_value', 'SuperSloMo')
    utils.mat.generate_mat_images(os.path.join(folder, 'images', 'interval_4'), mat)
    utils.mat.save_mat(os.path.join(folder, 'interval_4.mat'), mat)
