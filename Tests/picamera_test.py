# import the necessary packages
from imutils.video import VideoStream
from collections import deque
import argparse
import imutils
import time
import cv2

vs = VideoStream(src=0).start()

while True:
    # grab the frame from our video stream and resize it
    frame = vs.read()
    frame = imutils.resize(frame, width=1920)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()