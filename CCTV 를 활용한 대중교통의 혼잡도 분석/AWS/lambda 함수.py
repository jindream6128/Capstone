import json
import boto3
import time
import io
from datetime import datetime
import threading
import sys
import logging
import pymysql
import dbinfo

s3= boto3.client('s3')

def detect_labels(bucket,photo):
	rekognition = boto3.client("rekognition")
	response = rekognition.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MaxLabels=10)

	return response['Labels']

def lambda_handler(event, context):
    
    now=datetime.now()
    realti=now.strftime("%Y%m%d%H%M") #yyyymmddhhmm
    grade=0
    numberpeople=""

    try:
        for record in event['Records']:
            filename = record['s3']['object']['key']
            bucket = record['s3']['bucket']['name']
            source= detect_labels(bucket,filename)
            
            for i in source:
                if 'Person' in str(i):
                    numberpeople+=str(len(i['Instances']))
                    print(len(i['Instances']))
                    break
            else:
                numberpeople=str(0)
     
        realtitxt=realti+".txt"
        # 등급
        if 0 <= int(numberpeople) <= 20:
            grade = 1 #여유
        elif 20 < int(numberpeople) <= 40:
            grade = 2 #보통
        elif 40 < int(numberpeople) <= 60:
            grade = 3 #혼잡
        elif 60 < int(numberpeople):
            grade = 4 #매우혼잡

        with open('/tmp/'+realtitxt,'w') as f:
            f.write(f'{numberpeople}  / {grade} / {realti}') #txt파일에 인원수, 등급, 시간 순으로 쓰기
            
        s3.upload_file('/tmp/'+realtitxt,'ras1',realtitxt) #s3에 txt 업로드 
        print("success")
    
    except Exception as e:
        print(e)

    result = updateDB(numberpeople, realti, grade) #DB업로드
    
    #result=true이면 DB업로드 성공, false이면 DB업로드 실패 확인
    if result:
        return "complete"
    else:
        return "fail"

def updateDB(numberpeople, realti, grade): #db올라가는 데이터 3개
    connection = pymysql.connect(host=dbinfo.db_host, port=3306, user=dbinfo.db_username, passwd=dbinfo.db_password, db=dbinfo.db_name)
    #db연동

    try:
        with connection.cursor() as cursor:
            sql = "insert into bus (num, busID,grade) values (%s, %s, %s)"  #쿼리문 작성
            cursor.execute(sql, (numberpeople, realti, grade)) #sql 쿼리문 실행 (%s, %s, %s)에 각각 numberpeople, realti, grade 값 할당
        connection.commit()
        
    except:
        print("data insert error")
        return False #데이터 삽입에 실패하면 result에 0 반환
        
    else:
        print("data insert success")
        return True #데이터 삽입에 성공하면 result에 1 반환
        
    finally:
        connection.close()