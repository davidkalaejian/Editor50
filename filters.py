from PIL import Image, ImageFilter, ImageEnhance
from flask import flash

# tools = [original, enhance, color, contrast, brightness, blur, details, sharpen, smooth]

# Try to open the image uploaded by the user
def open_image(copypath):
    try:
        inputimage = Image.open(copypath)
        return inputimage
    # Show an alert if the uploaded image could not be opened
    except:
        flash('Unable to load image')

# Enhancement filter
def enhance_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    newimage = inputimage.filter(ImageFilter.EDGE_ENHANCE)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)

# Color correction filter
def color_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    tempimage = ImageEnhance.Color(inputimage)
    newimage = tempimage.enhance(2.0)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)

# Contrast filter
def contrast_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    tempimage = ImageEnhance.Contrast(inputimage)
    newimage = tempimage.enhance(2.0)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)

# Brightness filter
def brightness_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    tempimage = ImageEnhance.Brightness(inputimage)
    newimage = tempimage.enhance(2.0)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)

# Blur filter
def blur_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    newimage = inputimage.filter(ImageFilter.BLUR)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)

# Details filter
def details_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    newimage = inputimage.filter(ImageFilter.DETAIL)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)

# Sharpening filter
def sharpen_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    newimage = inputimage.filter(ImageFilter.SHARPEN)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)

# Smoothing filter
def smooth_filter(copypath):
    inputimage = open_image(copypath)

    # Apply the filter to the opened image
    newimage = inputimage.filter(ImageFilter.SMOOTH)

    # Replace the copied image in the uploads directory of that user
    newimage.save(copypath)