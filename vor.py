from PIL import Image, ImageDraw, ImageFont
import math
from scipy.spatial import Voronoi
import numpy as np
import random


points = np.array([[0, 0], [0, 1]])
points = points / 76
vor = Voronoi(points)
