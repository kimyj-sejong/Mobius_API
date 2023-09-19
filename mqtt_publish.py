'''
***********************************************************************
* FILENAME :    mqtt_publish.py
*
* DESCRIPTION :
*       oneM2M 표준 IoT Platform(Mobius)으로 MQTT Publish 하는 코드
*
* NOTES :
*       oneM2M MQTT Publish하는 예제 코드임
*
*       Copyright - BSD License (3-Clause)
*
* AUTHOR :    Yujin Kim (kimyj.sejong@gmail.com) 
*
* HISTORY :
* 		1 Aug 2023 : Created
* 		14 Sep 2023 : Updated : Softcoding으로 내용 변경
***********************************************************************
'''

import paho.mqtt.client as mqtt
import json
import random
import configparser

# Config 파일 로드
config = configparser.ConfigParser()
config.read('./config/config.ini')

# API 섹션에서 기본 변수 로드
IOTPLATFORM_IP = config['API']['IOTPLATFORM_IP']
IOTPLATFORM_MQTT_PORT = config['API']['IOTPLATFORM_MQTT_PORT']
IOTPLATFORM_URL_MQTT = config['API']['IOTPLATFORM_URL_MQTT']


# cnt(container) 생성
def crt_cnt(URI, AE_ID, resourceName):
    rand = str(int(random.random()*100000)) 
    
    crt_cnt = {
                "to": URI,
                "fr": AE_ID,
                "op":1,
                "ty":3,
                "rqi": rand, #rqi(request id)가 동일하면 에러 발생, random 값으로 설정
                "pc":{
                    "m2m:cnt": {
                        "rn": resourceName #resourceName = cnt명
                        }
                    }
            }
    return crt_cnt


# sub(subscription) 생성
def crt_sub(URI, AE_ID, resourceName):
    rand = str(int(random.random()*100000))
    crt_sub = {
                    "to": URI,
                    "fr": AE_ID,
                    "op":1,
                    "ty":23,
                    "rqi": rand,
                    "pc":{
                        "m2m:sub": {
                            "rn": resourceName, #resourceName = sub명
                            "enc":{"net":[3]},
                            "nu":[IOTPLATFORM_URL_MQTT.format(IOTPLATFORM_IP, resourceName)] #nu값이 중요함. 여기서 resourceName == topic
                            }
                        }
                }
    return crt_sub


# cin(content instance) 생성
def crt_cin(URI, AE_ID, data):
    rand = str(int(random.random()*100000))
    crt_cin = {
            "to": URI,
            "fr": AE_ID,
            "op":1,
            "ty":4,
            "rqi": rand,
            "pc":{
                "m2m:cin": {
                    "con": data
                    }
                }
        }
    return crt_cin


# 기본 MQTT 콜백 함수
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected")

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


'''
Main 함수
create_cnt, create_sub, create_cin 중 필요한 리소스만 남기고 불필요한 리소스 주석 처리

create_cnt: URI는 /{CSE}/{AE}/{CNT} 형태로 입력, {CNT}의 경우 생성하고자 하는 위치에 따라 수정
            ex.) AE 하위 생성: /{CSE}/{AE} , CNT1 하위 생성: /{CSE}/{AE}/{CNT1}
            resourceName은 생성하고자 하는 CNT(컨테이너)명으로 표기
            
create_sub: URI는 /{CSE}/{AE}/{CNT} 형태로 입력, {CNT}의 경우 sub을 걸고 싶은 위치의 컨테이너 명까지 명시
            ex.) AE 하위 생성: /{CSE}/{AE} , CNT1 하위 생성: /{CSE}/{AE}/{CNT1}
            resourceName은 생성하고자 하는 SUB(구독)명으로 표기, SUB명으로 topic이 생성되기에 중복되지 않도록 주의
            중복되는 경우 해당 topic으로 publish한 데이터는 모두 수신됨
            
create_cin: URI는 /{CSE}/{AE}/{CNT} 형태로 입력, {CNT}의 경우 생성하고자 하는 위치에 따라 수정
            ex.) AE 하위 생성: /{CSE}/{AE} , CNT1 하위 생성: /{CSE}/{AE}/{CNT1}
            data는 생성하고자 하는 데이터 표기
'''
def publishing(URI, AE_ID, resourceName = None, data = None):
    # 새로운 클라이언트 생성
    client = mqtt.Client()

    # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    # ip_address : IOTPLATFORM_IP, port: IOTPLATFORM_MQTT_PORT 에 연결
    client.connect(IOTPLATFORM_IP, int(IOTPLATFORM_MQTT_PORT))

    # crt_cnt, crt_sub, crt_cin 함수를 통해 생성한 json 형식의 데이터를 string 형태로 변환
    create_cnt = json.dumps(crt_cnt(URI, AE_ID, resourceName))
    create_sub = json.dumps(crt_sub(URI, AE_ID, resourceName))
    create_cin = json.dumps(crt_cin(URI, AE_ID, data))

    # common topic 으로 메세지 발행
    client.publish('/oneM2M/req/' + AE_ID + '/Mobius2/json', create_cnt)
    client.publish('/oneM2M/req/' + AE_ID + '/Mobius2/json', create_sub)
    client.publish('/oneM2M/req/' + AE_ID + '/Mobius2/json', create_cin)

    # 연결 종료
    client.disconnect()


if __name__ == "__main__":
    # resourceName = {}, data = {} 형태로 입력 (키워드 인자)
    publishing('/Mobius/service400/sensor6/target', 'service400', data = 'hi')