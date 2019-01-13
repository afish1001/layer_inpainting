"""
将mat文件生成为mp4文件，原始fps为20

Usage: python phase_mat2video.py --input ./data/phase.mat --output ./result/phase.mp4

"""
import os
import argparse
import cv2
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--input',  type=str, default='./data', help='The input mat directory.')
parser.add_argument('--output', type=str, default='./result', help='The output directory.')

opt = parser.parse_args()
print(opt)

# INTERVALS = [0, 1, 2, 4, 6, 10, 15, 20]
INTERVALS = [0, 1, 3, 4, 9, 19]


def worker(_mat_path, _output_path, _interval):
    _mat_name = utils.get_filename(_mat_path)
    mat = utils.mat.load_mat(_mat_path)

    # fps = 20 // (interval + 1)
    fps = 1
    writer = cv2.VideoWriter(_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, mat[0].shape)
    frame_count = 0
    for layer in mat[::(_interval + 1), :, :]:
        frame = cv2.cvtColor(layer, cv2.COLOR_GRAY2RGB)
        writer.write(frame)
        frame_count += 1
    print('已输出视频: {}, FPS: {}, 共 {} 帧, 时长: {}s'.format(_output_path, fps, frame_count, frame_count//fps))
    writer.release()


if __name__ == '__main__':
    mat_list = utils.mat.get_mat_list(opt.input)
    for mat_path in mat_list:
        mat_name = utils.get_filename(mat_path)
        output_folder = os.path.join(opt.output, mat_name, 'IntervalVideo')
        os.makedirs(output_folder, exist_ok=True)
        for interval in INTERVALS:
            output_path = os.path.join(output_folder, 'interval_{}.mp4'.format(interval))
            worker(mat_path, output_path, interval)
