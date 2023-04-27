import cv2 as cv
import numpy as np

# Function to greyscale an image
def greyscale(image):
    # Convert image to greyscale
    grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return grey

# Convert image to RGB
def convert_to_rgb(image):
    # Convert image to RGB
    rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    return rgb

# Threshold an image
def apply_threshold(image):
    # Apply threshold to image
    ret, thresh = cv.threshold(image, 220, 255, cv.THRESH_BINARY)
    return thresh

# Dilate an image using an elliptical kernel
def apply_dilate(image):
    # Create kernel
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    # Dilate image
    dilated = cv.dilate(image, kernel, iterations=3)
    return dilated

# Function to apply contrast to an image
def apply_contrast(image):
    # Apply contrast to image
    contrast = cv.convertScaleAbs(image, alpha=0.75, beta=0)
    return contrast
