import time
import os
import argparse

import cv2
import numpy as np
from PIL import Image

from yolo import YOLO, YOLO_ONNX

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--mode", type=str, default="predict", help="Mode of operation: 'predict', 'video', 'fps', 'dir_predict', 'heatmap', 'export_onnx', 'predict_onnx'")
    parser.add_argument("--crop", type=bool, default=False, help="Crop the detected object in predict mode")
    parser.add_argument("--count", type=bool, default=False, help="Count the detected objects in predict mode")
    parser.add_argument("--video_path", type=str, default="0", help="Path to the video file or camera index")
    parser.add_argument("--video_save_path", type=str, default="", help="Path to save the output video")
    parser.add_argument("--video_fps", type=float, default=25.0, help="FPS of the saved video")
    parser.add_argument("--test_interval", type=int, default=100, help="Number of images to test FPS")
    parser.add_argument("--fps_image_path", type=str, default="img/street.jpg", help="Path to the image for FPS testing")
    parser.add_argument("--dir_origin_path", type=str, default="img/", help="Directory path for input images")
    parser.add_argument("--dir_save_path", type=str, default="output/", help="Directory path for output images")
    parser.add_argument("--heatmap_save_path", type=str, default="model_data/heatmap_vision.png", help="Path to save heatmap")
    parser.add_argument("--simplify", type=bool, default=True, help="Simplify ONNX model")
    parser.add_argument("--onnx_save_path", type=str, default="model_data/models.onnx", help="Path to save ONNX model")
    parser.add_argument("--image_path", type=str, help="Path to a single image for prediction")

    args = parser.parse_args()

    if args.mode != "predict_onnx":
        yolo = YOLO()
    else:
        yolo = YOLO_ONNX()

    if args.mode == "predict":
        if args.image_path:
            try:
                image = Image.open(args.image_path)
            except:
                print('Open Error! Try again!')
            else:
                r_image = yolo.detect_image(image, crop=args.crop, count=args.count)
                if not os.path.exists(args.dir_save_path):
                    os.makedirs(args.dir_save_path)
                r_image.save(os.path.join(args.dir_save_path, os.path.basename(args.image_path).replace(".jpg", ".png")), quality=95, subsampling=0)
        else:
            while True:
                img = input('Input image filename:')
                try:
                    image = Image.open(img)
                except:
                    print('Open Error! Try again!')
                    continue
                else:
                    r_image = yolo.detect_image(image, crop=args.crop, count=args.count)
                    r_image.show()

    elif args.mode == "video":
        capture = cv2.VideoCapture(args.video_path)
        if args.video_save_path != "":
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            out = cv2.VideoWriter(args.video_save_path, fourcc, args.video_fps, size)

        ref, frame = capture.read()
        if not ref:
            raise ValueError("none.")

        fps = 0.0
        while True:
            t1 = time.time()
            ref, frame = capture.read()
            if not ref:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(np.uint8(frame))
            frame = np.array(yolo.detect_image(frame))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            fps = (fps + (1. / (time.time() - t1))) / 2
            print("fps= %.2f" % (fps))
            frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("video", frame)
            c = cv2.waitKey(1) & 0xff
            if args.video_save_path != "":
                out.write(frame)

            if c == 27:
                capture.release()
                break

        print("Video Detection Done!")
        capture.release()
        if args.video_save_path != "":
            print("Save processed video to the path :" + args.video_save_path)
            out.release()
        cv2.destroyAllWindows()

    elif args.mode == "fps":
        img = Image.open(args.fps_image_path)
        tact_time = yolo.get_FPS(img, args.test_interval)
        print(str(tact_time) + ' seconds, ' + str(1/tact_time) + 'FPS, @batch_size 1')

    elif args.mode == "dir_predict":
        from tqdm import tqdm

        img_names = os.listdir(args.dir_origin_path)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path = os.path.join(args.dir_origin_path, img_name)
                image = Image.open(image_path)
                r_image = yolo.detect_image(image)
                if not os.path.exists(args.dir_save_path):
                    os.makedirs(args.dir_save_path)
                r_image.save(os.path.join(args.dir_save_path, img_name.replace(".jpg", ".png")), quality=95, subsampling=0)

    elif args.mode == "heatmap":
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                yolo.detect_heatmap(image, args.heatmap_save_path)

    elif args.mode == "export_onnx":
        yolo.convert_to_onnx(args.simplify, args.onnx_save_path)

    elif args.mode == "predict_onnx":
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = yolo.detect_image(image)
                r_image.show()
    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps', 'heatmap', 'export_onnx', 'dir_predict', 'predict_onnx'.")