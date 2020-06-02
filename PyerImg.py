import cv2
import numpy as np
from PyerPointRecognize import *

def get_border(img):
    img2 = img[:,:,2]
    ret,img2th1 = cv2.threshold(img2, 180, 255, cv2.THRESH_TOZERO)
    ret,img2th2 = cv2.threshold(img2th1, 190, 255, cv2.THRESH_TOZERO_INV)
    result = cv2.medianBlur(img2th2, 9)
    whereid = np.where(result > 0)
    whereid = whereid[::-1]
    coords = np.column_stack(whereid)
    (x,y),(w,h),angle = cv2.minAreaRect(coords)
    if angle < -45:
        angle = angle + 90
    return (x,y),(w,h),angle

def set_border(filename, img):
    img2 = img[:,:,2]
    ret,img2th1 = cv2.threshold(img2, 180, 255, cv2.THRESH_TOZERO)
    ret,img2th2 = cv2.threshold(img2th1, 190, 255, cv2.THRESH_TOZERO_INV)
    result = cv2.medianBlur(img2th2, 9)
    whereid = np.where(result > 0)
    whereid = whereid[::-1]
    coords = np.column_stack(whereid)
    (x,y),(w,h),angle = cv2.minAreaRect(coords)
    if angle < -45:
        angle = angle + 90
    vis = img.copy()
    box = cv2.boxPoints(((x,y), (w,h), angle))
    box = np.int0(box)
    cv2.drawContours(vis,[box],0,(0,0,255),2)
    cv2.imwrite(filename, vis)

def get_circles(img):
    '''
    '''
    if(img.shape[0]<1920):
        minRadius=20
    else:
        minRadius=25
    gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gimg = cv2.medianBlur(gimg, 7)
    circles = cv2.HoughCircles(gimg, cv2.HOUGH_GRADIENT, \
        1, 10, param1=100, param2=30, minRadius=minRadius, maxRadius=30)
    return circles

def get_vias_lnglat(x,y,w,h,angle,cl,shape):
    # 重排顺序
    ap = [None for _ in range(cl['length'])]
    for i in range(cl['length']):
        pos = cl['class'][i]
        ap[pos-1] = cl['center'][i]
    # 计算位置矢量, AB是整张图片左上角/左下角
    ap1 = np.array([v[0] for v in ap])
    ap2 = np.array([v[1] for v in ap],dtype=np.int32)
    d = round(0.0403*shape[1])
    ap2 = -ap2
    ap2 = ap2-d
    ap = np.vstack((ap1,ap2)).T
    
    ao = np.array([x,-y])
    ba = np.array([0,shape[0]])
    o = ba + ao
    p = ba + ap
    op = p - o
    # 构造旋转矩阵
    theta = 2*np.pi*angle/360
    rot = [[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]]
    rot = np.array(rot)
    opr = (rot@op.T).T
    # p1p2p3分别是校园的左上角/左下角/右下角的经纬度
    p1 = np.array([121.495947,30.832191])
    p2 = np.array([121.501225,30.824949])
    p3 = np.array([121.51174,30.830717])
    mat = np.vstack(((p3-p2)/w, (p1-p2)/h)).T
    fin = (p1+p3)/2 + (mat@opr.T).T
    return {'total':cl['length'],'vias':fin.tolist()}


if __name__=="__main__":
    img1 = cv2.imread('img/sample.jpg',1)
    print(get_circles(img1))
    # (x,y),(w,h),angle = get_border(img1)
    # cl = get_point(img1)
    # result = get_vias_lnglat(x,y,w,h,angle,cl,img1.shape)
    # print(result)
    # set_border('tian.jpg',img1)
    # print(img1.shape)
    # img2 = cv2.imread('img/test9.jpg',1)
    # img3 = cv2.imread('img/sample.jpg',1)
    # imgs = [img1,img2,img3]
    # for img in imgs:
    #     print(get_border(img))
