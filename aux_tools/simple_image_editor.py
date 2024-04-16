# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 12:05:58 2023

@author: Alejandro Gonzalez

Contains tools for easy and simple image modification

ChangeLog:
    0.1 (AG): First version
    0.2 (AG): added increase_contrast_image_gray
"""

import cv2

def increase_brightness(img, value = 30):
    """
    Moves the given RGB image to an HSV base and adds the given value to the 
    brightness parameter to increase it.

    Parameters
    ----------
    img : ndarray -- image
        The image in RGB format to be edited.
    value : float* -- optional
        The value to increase. The default is 30. *May cause trauble if a float
        is used.

    Returns
    -------
    img : ndarray -- image
        The edited image in RGB.
    """
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    return img


def increase_hue(img, value = 30):
    """
    Moves the given RGB image to an HSV base and adds the given value to the 
    hue parameter to increase it. AKA changes the base colour.

    Parameters
    ----------
    img : ndarray -- image
        The image in RGB format to be edited.
    value : float* -- optional
        The value to increase. The default is 30. *May cause trauble if a float
        is used.

    Returns
    -------
    img : ndarray -- image
        The edited image in RGB.
    """
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    h[h > lim] = 255
    h[h <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    return img


def increase_saturation(img, value = 30):
    """
    Moves the given RGB image to an HSV base and adds the given value to the 
    saturation parameter to increase it.

    Parameters
    ----------
    img : ndarray -- image
        The image in RGB format to be edited.
    value : float* -- optional
        The value to increase. The default is 30. *May cause trauble if a float
        is used.

    Returns
    -------
    img : ndarray -- image
        The edited image in RGB.
    """
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    s[s > lim] = 255
    s[s <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    return img


def increase_contrast_brightness_RGB(RGB_image, contrast_inc, brightness_int):
    """
    Changes the contrast and brightness of an RGB image using the simple 
    formula f' = f * contrast_int + brightness_int.
    
    This is not compatible with HSV/other bases.

    Parameters
    ----------
    RGB_image : ndarray -- image
        The image to be modify -- either in grayscale or in RGB format.
    contrast_inc : float
        The contrast increase.
    brightness_int : float
        The brightness increase.

    Returns
    -------
    new_image : ndarray -- image
        The edited image.
    """
    
    new_image = RGB_image * contrast_inc + brightness_int
    
    return new_image


def increase_contrast_brightness_gray(gray_image, contrast_inc, brightness_int):
    """
    Changes the contrast and brightness of an grayscale image using the simple 
    formula f' = f * contrast_int + brightness_int.
    
    This is not compatible with HSV/other bases.

    Parameters
    ----------
    gray_image : ndarray -- image
        The image to be modify -- either in grayscale or in RGB format.
    contrast_inc : float
        The contrast increase.
    brightness_int : float
        The brightness increase.

    Returns
    -------
    new_image : ndarray -- image
        The edited image.
    """
    
    new_image = gray_image * contrast_inc + brightness_int
    new_image = new_image.astype('uint8')
    
    return new_image