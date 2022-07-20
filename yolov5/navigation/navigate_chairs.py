# Navigate through chairs using simple object detection

import os
from utils.general import LOGGER
from utils.plots import Annotator

# Display the bounding boxes of chairs in the image only

def region_of_interest():
    LOGGER.info('Start region of interest detection')
