import os
import argparse
import cv2
import utils


parser = argparse.ArgumentParser()
parser.add_argument('--data',  type=str, required=True, help='The input images folder.')
parser.add_argument('--size', type=int, default=400, help='The sub video size.')
parser.add_argument('--output', type=str, default='./videos', help='The output folder.')
parser.add_argument('--save-crop', type=bool, default=False, help='Save crop images?')
parser.add_argument('--crop-output', type=str, default='./crops', help='The middle crop images output folder.')

opt = parser.parse_args()
print(opt)

os.makedirs(opt.output, exist_ok=True)

image_list = utils.image.get_image_list(opt.data)
images = []

for image_path in image_list:
    images.append(cv2.imread(image_path))


fps = 1
image_shape = images[0].shape[:2]
for x in range(0, image_shape[0], opt.size):
    for y in range(0, image_shape[1], opt.size):
        output_path = os.path.join(opt.output, '({},{})-({},{}).mp4'.format(x, x + opt.size, y, y + opt.size))
        writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (opt.size, opt.size))
        frame_count = 0
        for image in images:
            frame = image[x: x + opt.size, y: y + opt.size]
            writer.write(frame)
            frame_count += 1
        writer.release()
        print('已输出视频: {}, FPS: {}, 共 {} 帧, 时长: {}s'.format(output_path, fps, frame_count, frame_count // fps))
