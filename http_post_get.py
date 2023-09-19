'''
***********************************************************************
* FILENAME :    http_post_get.py
*
* DESCRIPTION :
*       oneM2M 표준 IoT Platform(Mobius)으로 HTTP Post&Get 하는 코드
*
* NOTES :
*       oneM2M HTTP Post&Get하는 예제 코드임
*
*       Copyright - BSD License (3-Clause)
*
* AUTHOR :    Yujin Kim (kimyj.sejong@gmail.com) 
*
* HISTORY :
* 		1 Aug 2023 : Created
* 		14 Sep 2023 : Updated : Softcoding으로 내용 변경
*********************************************
**************************
'''

from requests import post, get
import json
import configparser

# Config 파일 로드
config = configparser.ConfigParser()
config.read('./config/config.ini')

# API 섹션에서 기본 변수 로드
IOTPLATFORM_IP = config['API']['IOTPLATFORM_IP']
IOTPLATFORM_HTTP_PORT = config['API']['IOTPLATFORM_HTTP_PORT']
IOTPLATFORM_URL_HTTP = config['API']['IOTPLATFORM_URL_HTTP']


#IoT Platfrom으로 HTTP POST 요청
def mobius_post(URI, AE_ID ,RI, data, ty = 4):
    URI = IOTPLATFORM_URL_HTTP.format(IOTPLATFORM_IP, IOTPLATFORM_HTTP_PORT) +  URI
    
    payload = {}
    payload["m2m:cin"] = {}
    payload["m2m:cin"]["con"] = data
    payload = json.dumps(payload)

    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': RI,
    'X-M2M-Origin': AE_ID,
    'Content-Type': 'application/vnd.onem2m-res+json ; ty = ' + ty # cnt 생성: 3, cin 생성: 4
    }   
    
    print(headers)
    
    response = post(URI, headers=headers, data=payload)

    print(response.text)


#IoT Platfrom으로 HTTP GET 요청
def mobius_get(URI, AE_ID, RI):
    URI = IOTPLATFORM_URL_HTTP.format(IOTPLATFORM_IP, IOTPLATFORM_HTTP_PORT) +  URI + "/la"

    payload = {}

    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': RI,
    'X-M2M-Origin': AE_ID
    }   
    
    response = get(URI, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    mobius_post("/Mobius/service400/sensor4/state", "service400", "service400", "hello" )
    mobius_get("/Mobius/service400/sensor4/state", "service400", "service400")