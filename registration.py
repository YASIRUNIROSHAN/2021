import cv2

# Initialize Webcam
import trian_model

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_extractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    # print(faces)
    if faces is ():
        print("none")
        return None

    # Crop all faces found
    for (x, y, w, h) in faces:
        # print("work")
        cropped_face = img[y:y + h, x:x + w]
        # print(cropped_face)
    return cropped_face


def get_fr(name, id):
    cap = cv2.VideoCapture(0)
    count = 0
    username = name
    Id = id
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        k = cv2.waitKey(1)
        if face_extractor(frame) is not None:
            count += 1
            face = cv2.resize(face_extractor(frame), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # Save file in specified directory with unique name
            file_name_path = './faces/user/' + username + "." + str(Id) + '.' + str(count) + '.jpg'
            cv2.imwrite(file_name_path, face)

            # Put count on images and display live count
            cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Face Cropper', face)

            # else:
            #     print("Face not found")
            #     pass

            if cv2.waitKey(1) == 13 or count == 10:  # 13 is the Enter Key

                break

    cap.release()
    cv2.destroyAllWindows()
    trian_model.testing()
    print("Collecting Samples Complete")
    return count
