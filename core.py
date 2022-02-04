import base64
from re import S
import cv2
import numpy as np
import os

def arr_to_str(arr):
    bs = arr.tobytes()
    b64 = base64.urlsafe_b64encode(bs)
    return str(b64,'utf-8')

def str_to_arr(s):
    bs = base64.urlsafe_b64decode(bytes(s,'utf-8'))
    return np.frombuffer(bs,np.uint8)

def save_img(filename,i,frame):
    filename = os.path.splitext(filename)[0]
    dirs = "H:\\ad\\"+ filename+ "\\"
    fullname = dirs + str(i) + '.jpg'
    if os.path.exists(fullname):
        return
    if i == 0 :
        os.makedirs(dirs)
    cv2.imwrite(fullname, frame)

def is_video(filename):
    ext = os.path.splitext(filename)[-1]
    return ext == '.mp4' or ext == '.avi' or ext == '.ts' or ext == '.avi' or ext == '.mkv' or ext == '.mov';

def is_like(hash1,hash2):
    if hash1.size == 0:
        return False
    hamming = cv2.norm(hash1, hash2, cv2.NORM_HAMMING)
    return hamming < 15

def filter_like(allHashs,i,hash2):
    def like(frameHashs):
        hash1 = frameHashs[i]
        return is_like(hash1,hash2)
    return list(filter(like,allHashs))