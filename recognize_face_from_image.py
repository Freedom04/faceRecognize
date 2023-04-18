from compreface import CompreFace
from compreface.service import RecognitionService
import cv2
DOMAIN: str = 'http://localhost'
PORT: str = '8000'
RECOGNITION_API_KEY: str = '1e59602d-b3e3-49d0-88bd-628a98d3407d'


compre_face: CompreFace = CompreFace(DOMAIN, PORT, {
    "limit": 0,
    "det_prob_threshold": 0.8,
    "prediction_count": 1,
    "face_plugins": "age,gender",
    "status": False
})

recognition: RecognitionService = compre_face.init_face_recognition(
    RECOGNITION_API_KEY)


def faceRecognize(image_path: str):
    data = recognition.recognize(image_path)
    results = data.get('result')
    return results


def faceLabelInImage(frame, results):

    for result in results:
        # 获取识别出人脸的相关信息
        box = result.get('box')
        age = result.get('age')
        gender = result.get('gender')
        mask = result.get('mask')
        subjects = result.get('subjects')

        # 在图片中框出识别出的人脸，并显示识别出的人脸信息
        if box:
            cv2.rectangle(img=frame, pt1=(box['x_min'], box['y_min']),
                          pt2=(box['x_max'], box['y_max']), color=(0, 0, 255), thickness=3)
        # 显示推测出的年龄范围
        if age:
            age = f"Age: {age['low']} - {age['high']}"
            cv2.putText(frame, age, (box['x_max'], box['y_min'] + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
        # 显示推测出的性别
        if gender:
            gender = f"Gender: {gender['value']}"
            cv2.putText(frame, gender, (box['x_max'], box['y_min'] + 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        # 显示是否带了面具
        if mask:
            mask = f"Mask: {mask['value']}"
            cv2.putText(frame, mask, (box['x_max'], box['y_min'] + 75),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
        # 显示匹配度最高的人脸姓名，以及相似度
        if subjects:
            subjects = sorted(
                subjects, key=lambda k: k['similarity'], reverse=True)
            # 如果最高相似度超多0.7，则认为匹配成功，显示匹配结果
            if subjects[0]['similarity'] > 0.9:
                subject = f"Subject: {subjects[0]['subject']}"
                # print(subject)
                similarity = f"Similarity: {subjects[0]['similarity']}"
                cv2.putText(frame, subject, (box['x_max'], box['y_min'] + 105),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                cv2.putText(frame, similarity, (box['x_max'], box['y_min'] + 135),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            # 否则显示No known faces
            else:
                subject = f"No known faces"
                cv2.putText(frame, subject, (box['x_max'], box['y_min'] + 105),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

                # 如果无法匹配人脸信息，则显示No known faces
        else:
            subject = f"No known faces"
            cv2.putText(frame, subject, (box['x_max'], box['y_min'] + 105),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

    return frame
