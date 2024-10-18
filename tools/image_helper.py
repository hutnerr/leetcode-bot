from tools import random_helper as rh
import os

def getRandomThumbsUpImage():
    images = ["1" , "2", "3", "4", "5"]
    filename = rh.getRandom(images) + ".jpg"
    return os.path.join("images", "thumbs_up", filename)
    
    