"""
Simple utility to work with and retieve images

Functions: 
    getRandomImage(parentFolder: str) -> str
"""
from tools import random_helper as rh
import os

def getRandomImage(parentFolder: str) -> str:
    """
    Gets a random image from the specified folder. Assumes the images are named 1.jpg, 2.jpg, etc.
    Args:
        parentFolder (str): The parent folder. Use tools.consts.ImageFolders 
    Returns:
        str: The path to the image
    """
    # 5 images in the thumbs_up folder named 1.jpg, 2.jpg, etc.
    parentPath = os.path.join("images", parentFolder)
    numImages = len(os.listdir(parentPath))    
    filename = rh.getRandomRange(end = numImages) + ".jpg"
    return os.path.join("images", parentFolder, filename)
    
    