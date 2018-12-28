"""
对比原始mat和修复后的mat的体积及表面积

Usage: python phase_compare.py --data ./data --result ./result --mode TELEA

"""
from __future__ import division
import os
import argparse
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--data',   type=str, default='./tmp', help='The origin mat directory.')
parser.add_argument('--result', type=str, default='./result', help='The result mat directory.')
parser.add_argument('--mode',   type=str, default='TELEA', help='The inpaint mode.')

opt = parser.parse_args()
print(opt)


def compare_phase(origin_mat_name, origin, result_mat_name, result):
    v_origin = utils.phase.get_volume(origin)
    v_result = utils.phase.get_volume(result)
    v_error = round(abs(v_origin - v_result) / v_origin, 3)
    v_accuracy = 100 - v_error
    print('{} origin volume: {}, {} volume: {}, accuracy: {}'.format(origin_mat_name, v_origin, result_mat_name, v_result, v_accuracy))
    s_origin = utils.phase.get_surface_area(origin)
    s_result = utils.phase.get_surface_area(result)
    s_error = round(abs(s_origin - s_result) / s_origin, 3)
    s_accuracy = 100 - s_error
    print('{} origin surface: {}, {} volume: {}, accuracy: {}'.format(origin_mat_name, s_origin, result_mat_name, s_result, s_accuracy))


if __name__ == '__main__':
    mat_list_data = utils.mat.get_mat_list(opt.data)
    mat_list_result = os.listdir(opt.result)

    for mat_path in mat_list_data:
        mat_name = utils.get_filename(mat_path)
        if mat_name not in mat_list_result:
            print('{} have no inpaint result')
            continue
        origin_mat = utils.mat.load_mat(mat_path)
        # 修复结果存放在 result/Phase_name/mode 文件夹下
        result_mat_list = utils.mat.get_mat_list(os.path.join(opt.result, mat_name, opt.mode))
        for result_mat_path in result_mat_list:
            result_mat = utils.mat.load_mat(result_mat_path)
            compare_phase(mat_name, origin_mat, utils.get_filename(result_mat_path), result_mat)
