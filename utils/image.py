import os
import cv2


def get_image_list(path):
    return list(filter(
        lambda x: x.endswith('.jpg') or x.endswith('.jpeg') or x.endswith('.png'),
        map(lambda x: os.path.join(path, x), os.listdir(path))))


def crop_images_with_list(image_list, size, out='./'):
    """将输入的每张图片的指定方形位置裁剪后，保存到文件夹中"""
    img = cv2.imread(image_list[0])
    # 先给每个尺寸的图片创建文件夹
    for y in range(0, img.shape[0], size):
        for x in range(0, img.shape[1], size):
            output_folder = os.path.join(out, '({},{})-({},{})'.format(x, y, x + size, y + size))
            os.makedirs(output_folder, exist_ok=True)

    # 然后迭代每张图片，将指定位置的图片放到指定文件夹
    for image in image_list:
        img = cv2.imread(image)
        for y in range(0, img.shape[0], size):
            for x in range(0, img.shape[1], size):
                output_folder = os.path.join(out, '({},{})-({},{})'.format(x, y, x + size, y + size))
                cv2.imwrite(os.path.join(output_folder, os.path.basename(image), img[y: y + size, x:  x + size]))


def crop_images_with_location(image_list, s_x, s_y, size, out='./crop'):
    output_folder = os.path.join(out, '({},{})-({},{})'.format(s_x, s_y, s_x + size - 1, s_y + size - 1))
    os.makedirs(output_folder, exist_ok=True)
    for image in image_list:
        img = cv2.imread(image)
        cv2.imwrite(os.path.join(output_folder, os.path.basename(image)), img[s_x: s_x + size, s_y: s_y + size])


def generate_video(image_list, fps, output_path, internal=0):
    shape = cv2.imread(image_list[0]).shape[:2]
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, shape)
    frame_count = 0
    for i in range(0, len(image_list), internal + 1):
        frame = cv2.imread(image_list[i])
        writer.write(frame)
        frame_count += 1
    # for image in image_list:
    #     frame = cv2.imread(image)
    #     writer.write(frame)
    #     frame_count += 1
    print('已输出视频: {}, FPS: {}, 共 {} 帧, 时长: {}s'.format(output_path, fps, frame_count, frame_count//fps))
    writer.release()


def extract_images_from_video(video_path, output_folder=None):
    output_folder = output_folder or os.path.basename(video_path).split('.')[0]
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    success, image = cap.read()
    count = 0
    while success:
        cv2.imwrite(os.path.join(output_folder, '{:0>3d}.jpg'.format(count)), image)
        count += 1
        success, image = cap.read()
