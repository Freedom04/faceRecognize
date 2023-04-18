import cv2
import os


def getFrame(video_path, output_path):
    if not os.path.exists(video_path):
        print("视频文件不存在")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # open the video file
    cap = cv2.VideoCapture(video_path)
    # get the frame rate of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    count = 0
    while True:
        # read a frame of the video
        ret, frame = cap.read()
        if not ret:
            break
        if count % (2 * fps) == 0:
            cv2.imwrite(
                "{}/frame_{}.jpg".format(output_path, count // fps), frame)

        count += 1
    cap.release()
