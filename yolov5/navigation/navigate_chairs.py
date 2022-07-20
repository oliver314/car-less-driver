# Navigate through chairs using simple object detection

import os
from utils.general import LOGGER
from utils.plots import Annotator

# Display the bounding boxes of chairs in the image only
def isRectangleOverlap(R1, R2):
    if (R1[0]>=R2[2]) or (R1[2]<=R2[0]) or (R1[3]<=R2[1]) or (R1[1]>=R2[3]):
        return False
    else:
        return True
