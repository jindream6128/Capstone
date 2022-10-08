import cv2
from datetime import datetime
import threading
import time
import boto3

s3=boto3.client('s3', #업로드될 s3의 정보
   aws_access_key_id='', #access ID KEY
   aws_secret_access_key='') #PASSWORD


    
def test():
    cam=cv2.VideoCapture("") #캡처할 카메라 저희의 프로젝트는 CCTV를 사용하였고, RTSP통신을 사용함
    _,img=cam.read()
    ret, img =cam.read()
    now =datetime.now()
    realti=str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)
    cv2.imwrite("image"+realti+".jpg",img)
    filename1='image'+realti+'.jpg'
    filename2=realti+'.jpg'
    
    bucket_name='ras1'
    # s3.upload_file(filename1,bucket_name,filename2)
    s3.upload_file(filename1,bucket_name, filename2)
    print(ret)
    threading.Timer(70,test).start() #70초 간격으로 반복
    
test()