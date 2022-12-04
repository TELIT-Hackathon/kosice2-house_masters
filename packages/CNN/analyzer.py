from __future__ import division

import os
import time
import torch
import glob
import cv2 
import torch 
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

from torch.autograd import Variable
from util import *
from darknet import Darknet
from preprocess import prep_image, letterbox_image
from tensorflow.python.client import device_lib
device_lib.list_local_devices()

# os.chdir('/content/out')

ROOT_DIR = os.getcwd()
MODEL_CFG_DIR = "cfg/yolov3.cfg"
WEIGHTS = 'model/yolov3.weights'
ASSETS = 'assests/coco.names'
OUTPUT_DIR = 'out/'

def DrawRectangles(x, img, classes):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    color = (0,0,255)
    cv2.rectangle(img, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), color, 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    return img

def arg_parse():
    """
    Parse arguements to the detect module
    """
    parser = argparse.ArgumentParser(description='YOLO v3 Video Detection Module')
   
    parser.add_argument("--video", dest = 'video', help = 
                        "Video to run detection upon",
                        default = "/content/Khare_testvideo_01.mp4", type = str)
    parser.add_argument("--dataset", dest = "dataset", help = "Dataset on which the network has been trained", default = "pascal")
    parser.add_argument("--confidence", dest = "confidence", help = "Object Confidence to filter predictions", default = 0.5)
    parser.add_argument("--nms_thresh", dest = "nms_thresh", help = "NMS Threshhold", default = 0.4)
    parser.add_argument("--cfg", dest = 'cfgfile', help = 
                        "Config file",
                        default = "/content/cfg/yolov3.cfg", type = str)
    parser.add_argument("--weights", dest = 'weightsfile', help = 
                        "weightsfile",
                        default = "/content/drive/MyDrive/hackathon/yolov3.weights", type = str)
    parser.add_argument("--reso", dest = 'reso', help = 
                        "Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
                        default = "704", type = str)
    
    args = parser.parse_args(args=[])
    
    return args

def GenerateResponseJson(boundries, cars_count, empty_spots):
    finalJSON = {
        "no_cars" : int(cars_count),
        "empty_spots" : int(empty_spots),
        "boundries" : []
    }

    for x in boundries:
        c1 = x[1:3].int()
        c2 = x[3:5].int()
        finalJSON["boundries"].append([c1[0], c1[1], c2[0], c2[1]])
    
    # print(finalJSON)

def AnalyzeImage(frame, capacity, save=False):
    args = arg_parse()
    confidence = float(args.confidence)
    nms_thesh = float(args.nms_thresh)

    CUDA = torch.cuda.is_available()
    num_classes = 1
    CUDA = torch.cuda.is_available()
    bbox_attrs = 5 + num_classes
    
    model = Darknet(MODEL_CFG_DIR)
    model.load_weights(WEIGHTS)
    print("Network successfully loaded with pretrained weights")

    model.net_info["height"] = args.reso
    inp_dim = int(model.net_info["height"])

    if CUDA:
        model.cuda()
        
    model(get_test_input(inp_dim, CUDA), CUDA)
    model.eval()
    
    img, orig_im, dim = prep_image(frame, inp_dim)
    im_dim = torch.FloatTensor(dim).repeat(1,2)                        

    if CUDA:
      im_dim = im_dim.cuda()
      img = img.cuda()

    with torch.no_grad():   
        output = model(Variable(img), CUDA)
        output = write_results(output, confidence, num_classes, nms = True, nms_conf = nms_thesh)
        cars_detected = output.size(0)
        print("count cars {}".format(cars_detected))

        im_dim = im_dim.repeat(output.size(0), 1)
        scaling_factor = torch.min(inp_dim/im_dim,1)[0].view(-1,1)

        output[:,[1,3]] -= (inp_dim - scaling_factor*im_dim[:,0].view(-1,1))/2
        output[:,[2,4]] -= (inp_dim - scaling_factor*im_dim[:,1].view(-1,1))/2

        output[:,1:5] /= scaling_factor

        for i in range(output.shape[0]):
            output[i, [1,3]] = torch.clamp(output[i, [1,3]], 0.0, im_dim[i,0])
            output[i, [2,4]] = torch.clamp(output[i, [2,4]], 0.0, im_dim[i,1])

        classes = load_classes("{}/coco.names".format(ASSETS))
        colors = pkl.load(open("{}/pallete".format(ASSETS), "rb"))

        list(map(lambda x: DrawRectangles(x, orig_im, classes), output))
        empty = capacity - cars_detected
        cv2.putText(orig_im, "Total empty spots: " + str(empty), (5,30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 3, 12)
        plt.imshow(orig_im, cmap='gray')

        if save:
            cv2.imwrite('{}/out.png'.format(OUTPUT_DIR), frame)

        return GenerateResponseJson(output, cars_detected, empty)

#### MAIN
input = {
    "filename" : '/content/test_img1.jpg',
    "capacity" : 24
}

# filename = '/content/test1.jpg'
# filename = '/content/test_img1.jpg'
# filename = '/content/test_img3.png'
frame = cv2.imread(input["filename"]) 
out = yolo_AnalyzeImage(frame, input["capacity"])

print(out)