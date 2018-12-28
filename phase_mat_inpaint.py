"""
从原始mat文件生成所有的传统算法修复结果

Usage: python main.py --input mat_folder --output result

"""
import os
import argparse
import multiprocessing
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--input',  type=str, default='./data', help='The input mat directory.')
parser.add_argument('--output', type=str, default='./result', help='The output directory.')
parser.add_argument('--cpus',   type=int, default=1, help='The number of cpu.')

opt = parser.parse_args()
print(opt)


INTERVALS = [1, 2, 4, 6, 10, 15, 20]
INPAINT_MODE = 'TELEA'


def worker(mat_path):
    mat_name = utils.get_filename(mat_path)
    output_path = os.path.join(opt.output, mat_name)
    origin_mat = utils.mat.load_mat(mat_path)

    # 先输出原始相场图像
    origin_output_folder = os.path.join(output_path, 'Origin')
    utils.mat.generate_mat_images(origin_output_folder, origin_mat)

    for interval in INTERVALS:
        # 获取模拟层间缺失后的mat
        interval_mat = utils.mat.get_interval_mat(origin_mat, interval)

        # 先输出模拟缺失后的图像
        interval_output_folder = os.path.join(output_path, 'Interval', 'interval_{}'.format(interval))
        utils.mat.generate_mat_images(interval_output_folder, interval_mat)

        # 再对缺失mat进行修复
        completed_mat = utils.inpaint.complete_interval_mat(interval_mat, interval, INPAINT_MODE)

        # 输出修复mat的图像
        completed_output_folder = os.path.join(output_path, INPAINT_MODE)
        utils.mat.generate_mat_images(os.path.join(completed_output_folder, 'images', 'interval_{}'.format(interval)), completed_mat)

        # 输出修复的mat文件
        utils.mat.save_mat(os.path.join(completed_output_folder, 'interval_{}'.format(interval)), completed_mat)


if __name__ == '__main__':
    mat_list = utils.mat.get_mat_list(opt.input)
    worker(mat_list[0])
    pool = multiprocessing.Pool(processes=opt.cpus)
    for mat in mat_list:
        pool.apply_async(worker, (mat, ))
    pool.close()
    pool.join()


