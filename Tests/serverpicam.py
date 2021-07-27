import io
import socket
import struct
from PIL import Image
import redis
import cv2
import numpy

def toRedis(r,a,n):
   """Store given Numpy array 'a' in Redis under key 'n'"""
   h, w = a.shape[:2]
   shape = struct.pack('>II',h,w)
   encoded = shape + a.tobytes()

   # Store encoded data in Redis
   r.set(n,encoded)
   return

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
server_socket = socket.socket()
server_socket.bind(('', 8485))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)
        print(type(image))
        image.verify()
        print('Image is verified')
        image = Image.open(image_stream)
        frame_bgr = numpy.array(image)
        frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        #cv2.imshow("frame", frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
        toRedis(r, frame, 'webcam')

finally:
    connection.close()
    server_socket.close()
    #cv2.destroyAllWindows()