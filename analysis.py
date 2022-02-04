import os
import core
from re import S
import cv2
import numpy as np
import argparse

def analysis(filterHash,parent,filename): #分析单个文件
    cap = cv2.VideoCapture(os.path.join(parent,filename))
    hash1 = np.empty(0)
    # 帧的hash列表
    frameHashs = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            hash2 = cv2.img_hash.pHash(frame)[0]
            i = len(frameHashs)
            if not core.is_like(hash1,hash2):
                filterHash = core.filter_like(filterHash,i,hash2)
                if len(filterHash):
                    # 保存使用
                    core.save_img(filename,i,frame)
                frameHashs.append(hash2)
            if i > 300:
                break
            hash1 = hash2

    # 完成所有操作后，释放捕获器
    cap.release()
    cv2.destroyAllWindows()
    return frameHashs

if __name__ == "__main__":
    parser = argparse.ArgumentParser('分析视频')
    parser.add_argument('-p',type=str,default='.')
    args = parser.parse_args()
    allHashs = []
    for parent,dirnames,filenames in os.walk(args.p):
        for filename in filenames:
            if core.is_video(filename):
                frameHashs = analysis(allHashs,parent, filename)
                allHashs.append(frameHashs)
    