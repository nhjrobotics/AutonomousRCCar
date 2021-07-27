import picamera
import picamera.array
import time

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (100, 100)
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, 'rgb')
        # Show size of RGB data
        print(stream.array.shape)
