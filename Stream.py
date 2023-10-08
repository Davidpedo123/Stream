import cv2
import http.server
import socketserver

# Parámetros de la cámara frontal
cam_id = 0  # ID de la cámara frontal, puede variar dependiendo del sistema
cam_width = 640  # Ancho de la imagen capturada
cam_height = 480  # Alto de la imagen capturada

class VideoStreamHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            capture = cv2.VideoCapture(cam_id)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

            while True:
                ret, frame = capture.read()
                if not ret:
                    break

                _, img_encoded = cv2.imencode('.jpg', frame)
                self.wfile.write(b'--frame\r\n')
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', len(img_encoded))
                self.end_headers()
                self.wfile.write(img_encoded)
                self.wfile.write(b'\r\n')

        else:
            self.send_error(404)

if __name__ == '__main__':
    try:
        server = socketserver.TCPServer(('10.0.0.199', 8085), VideoStreamHandler)
        print('Servidor en vivo iniciado en http://10.0.0.199:8085/video.mjpg  como video.mjpg')
        server.serve_forever()

    except KeyboardInterrupt:
        server.server_close()
        print('Servidor detenido')
