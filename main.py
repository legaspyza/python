import cv2
from pyzbar.pyzbar import decode
import requests

def retrieve_data():
    try:
        response = requests.get("http://127.0.0.1:5000/api/qr_data")
        if response.status_code == 200:
            qr_values = response.json()
            return set(qr_values)
        else:
            print("Error fetching data from API:", response.text)
            return set()
    except Exception as e:
        print("Error fetching data from API:", str(e))
        return set()

def main():
    capture = cv2.VideoCapture(0)
    qr_values = retrieve_data()

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            x, y, w, h = obj.rect
            qr_data = obj.data.decode('utf-8')

            if qr_data in qr_values:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
