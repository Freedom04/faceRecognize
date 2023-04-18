import os
import cv2
from recognize_face_from_image import faceRecognize, faceLabelInImage
from getFrame import getFrame

# 将视频的美秒的第一帧保存成图片
video_path = "./video/4.MP4"
frame_output_path = "./frame"
# getFrame(video_path, frame_output_path)
people_name = []
folder_path = frame_output_path
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 800, 600)
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path) and file_name.endswith(".jpg"):
        results = faceRecognize(file_path)
        # if the current frame does not have people face
        if results is None:
            continue
        # save the name of the identified person to the people_name
        for result in results:
            subject = result.get("subjects")[0]
            name = subject['subject']
            if name not in people_name:
                people_name.append(name)

        img = cv2.imread(file_path)
        img = faceLabelInImage(img, results)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


cv2.destroyAllWindows()
print(people_name)
