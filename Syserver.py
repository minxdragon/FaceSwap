
import cv2
import Syphon
import glfw
import os
import argparse
import os
import cv2
import logging
import argparse

from face_detection import select_face
from face_swap import face_swap

src_img='interactive/data/dream.jpg'
parser = argparse.ArgumentParser(description='FaceSwap Video')
parser.add_argument('--src_img', required=False, default=src_img, help='Path for source image')
parser.add_argument('--video_path', default=0,help='Path for video')
parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
parser.add_argument('--show', default=False, action='store_true', help='Show')
parser.add_argument('--save_path', required=False, default= "test/test.avi", help='Path for storing output video')
args = parser.parse_args()

dir_path = os.path.dirname(args.save_path)
if not os.path.isdir(dir_path):
    os.makedirs(dir_path)

class VideoHandler(object):
    def __init__(self, video_path=0, img_path=None, args=None):
        self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
        if self.src_points is None:
            print('No face detected in the source image !!!')
            exit(-1)
        self.args = args
        self.video = cv2.VideoCapture(video_path)

    def start(self):
            # window details
        size = (640, 400)
        server2 = Syphon.Server("python", size, show=False)
        while self.video.isOpened():
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            _, dst_img = self.video.read()
            dst_points, dst_shape, dst_face = select_face(dst_img, choose=False)
            if dst_points is not None:
                dst_img = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, dst_img, self.args, 68)

        self.video.release()
        #self.writer.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(lineno)d:%(message)s")

    parser = argparse.ArgumentParser(description='FaceSwap Video')
    parser.add_argument('--src_img', required=False, default='interactive/data/dream.jpg',
                        help='Path for source image')
    parser.add_argument('--video_path', default=0,
                        help='Path for video')
    parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
    parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
    parser.add_argument('--show', default=False, action='store_true', help='Show')
    parser.add_argument('--save_path', required=False, default="test/test.avi", help='Path for storing output video')
    args = parser.parse_args()

    dir_path = os.path.dirname(args.save_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def main():

    # window details
    size = (640, 400)

    # window setup
    server1 = Syphon.Server("Server RGB", size, show=False) # Syphon.Server("window and syphon server name", frame size, show)
    server2 = Syphon.Server("face", size, show=False)


    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        raise("IO Error")
        
    # loop
    while not server1.should_close() and not server2.should_close():
        while not server2.should_close():
            class VideoHandler(object):
                def __init__(self, video_path=0, img_path=None):
                    self.src_points, self.src_shape, self.src_face = select_face(cv2.imread(img_path))
                    if self.src_points is None:
                        print('No face detected in the source image !!!')
                        exit(-1)
                    self.args = args
                    self.video = cv2.VideoCapture(video_path)

                    cap = cv2.VideoCapture(0)

                    while True:
                        _, frame = cap.read()
                        dst_points, dst_shape, dst_face = select_face(frame, choose=False)
                        if dst_points is not None:
                            frame = face_swap(self.src_face, dst_face, self.src_points, dst_points, dst_shape, frame, args, 68)
                        
                        resized = cv2.resize(frame, (640, 400))
                        cv2.imshow("python", resized)
                        server2.publish_frame(resized)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    cap.release()
                    cv2.destroyAllWindows()


        if __name__ == '__main__':
            logging.basicConfig(level=logging.INFO,
                                format="%(levelname)s:%(lineno)d:%(message)s")

            parser = argparse.ArgumentParser(description='FaceSwap Video')
            parser.add_argument('--src_img', required=False, default='interactive/data/dream.jpg',
                                help='Path for source image')
            parser.add_argument('--video_path', default=0,
                                help='Path for video')
            parser.add_argument('--warp_2d', default=False, action='store_true', help='2d or 3d warp')
            parser.add_argument('--correct_color', default=False, action='store_true', help='Correct color')
            parser.add_argument('--show', default=False, action='store_true', help='Show')
            parser.add_argument('--save_path', required=False, default="test/test.avi", help='Path for storing output video')
            args = parser.parse_args()

            dir_path = os.path.dirname(args.save_path)
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

            VideoHandler(video_path=0, img_path='interactive/data/dream.jpg')

    glfw.terminate()
    cv2.destroyAllWindows()
    exit()


if __name__ == "__main__":
    main()
