import cv2
import numpy as np

# UserId = int(input())
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('model/trained_model2.yml')
Id = 0


# def face_detector(img, size=0.5):
#     # Convert image to grayscale
#     print(img)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_classifier.detectMultiScale(gray, 1.3, 5)
#
#     if faces is ():
#         return img, []
#
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
#         roi = img[y:y + h, x:x + w]
#         roi = cv2.resize(roi, (200, 200))
#
#     print(roi)
#     return img, roi


# Open Webcam


def get_frame(id):
    cap = cv2.VideoCapture(0)
    count = 0
    invalidUser = 0
    while True:
        # ret, frame = cap.read()

        ret, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        # if faces is ():
        #     return img, []

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi = img[y:y + h, x:x + w]
            roi = cv2.resize(roi, (200, 200))

        try:
            face = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # print(face)
            # Pass face to prediction model
            # "results" comprises of a tuple containing the label and the confidence value
            results = recognizer.predict(face)

            if results[1] < 500:
                confidence = int(100 * (1 - (results[1]) / 400))

            if confidence > 80:

                cv2.putText(img, str(results[0]), (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                # cv2.imshow('Face Recognition', img)
                print(int(results[0]))
                if int(id) == int(results[0]):
                    print(results[0])
                    display_string = str(confidence) + '% Confident it is User'
                    cv2.putText(img, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 120, 150), 2)
                    cv2.imshow('Face Recognition', img)
                    print("valid UserId")
                    count += 1
                else:
                    display_string = 'Invalid UserId'
                    cv2.putText(img, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face Recognition', img)
                    invalidUser += 1
                    print("Invalid UserId")
            else:
                cv2.putText(img, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Recognition', img)
                invalidUser += 1

        except:
            cv2.putText(img, "No Face Found", (220, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Recognition', img)
            invalidUser += 1
            pass

        if cv2.waitKey(1) == 13 or count == 20 or invalidUser == 50:  # 13 is the Enter Key
            break

    cap.release()
    cv2.destroyAllWindows()
    return count, invalidUser
