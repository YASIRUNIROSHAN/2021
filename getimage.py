# import cv2  # defining face detector
#
# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read('model/trained_model2.yml')
# Id = 0
# ds_factor = 0.6
#
# stop = 0
# cap = cv2.VideoCapture(0)
# while True:
#     ret, img = cap.read()
#     if not ret:
#         break
#     img = cv2.resize(img, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#
#     # if faces is ():
#     #     return img, []
#
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         roi = img[y:y + h, x:x + w]
#         roi = cv2.resize(roi, (200, 200))
#
#     try:
#         face = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#         # print(face)
#         results = recognizer.predict(face)
#         print(results[0])
#         if results[1] < 500:
#             confidence = int(100 * (1 - (results[1]) / 400))
#             display_string = str(confidence) + '% Confident it is User'
#             print(display_string, confidence)
#             cv2.putText(img, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 120, 150), 2)
#         if confidence > 85:
#             stop += 1
#             print("valid User")
#             # print(UserId, results[0])
#             # if UserId == int(results[0]):
#             #     print("valid UserId")
#
#             # else:
#             #     print("Invalid User")
#             display_string1 = str(results[0]) + ' Valid User'
#             cv2.putText(img, display_string1, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
#             cv2.imshow('Face Recognition', img)
#
#         else:
#             print("Locked")
#             cv2.putText(img, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
#             cv2.imshow('Face Recognition', img)
#
#     except:
#
#         print("No Face Found")
#         cv2.putText(img, "No Face Found", (220, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
#         # cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
#         cv2.imshow('Face Recognition', img)
#         pass
#     print("stop", stop)
#     # ret, jpeg = cv2.imencode('.jpg', img)
#     return stop
#