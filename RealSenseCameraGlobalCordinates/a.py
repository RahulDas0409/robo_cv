import requests
from requests.auth import HTTPDigestAuth , HTTPBasicAuth

#uriPrefix = 'http://192.168.125.1'
UserName = 'Default'
Password = 'password'
#Auth = HTTPDigestAuth(UserName, Password)
Auth = HTTPBasicAuth(UserName, Password)
session = requests.Session()
session.auth = Auth
head = {
    'Content-Type': 'application/json',
}
# session.headers = head


def GetSpeedRatio():
    response = session.get(uriPrefix + "/rw/panel/speedratio?json=1")
    s = response.json()
    print(s['_embedded']['_state'][0]['speedratio'])
    print(response)
    return response
    


def SetSpeedRatio(speed):
    sparam = {
        'speed-ratio': speed
    }
    response = session.post(uriPrefix + "/rw/panel/speedratio?action=setspeedratio", data=sparam)
    print(response)


def UpdateData(DataName, Value):
    sparam = {
        'value': Value
    }
    response = session.post(uriPrefix + "/rw/rapid/symbol/data/RAPID/T_ROB1/Declaration/" + DataName + "/?action=set",data=sparam)
    print(response)


def GetData(DataName):
    response = session.get(uriPrefix + "/rw/rapid/symbol/data/RAPID/T_ROB1/Declaration/" + DataName + "?json=1")
    s = response.json()
    g = s['_embedded']['_state'][0]['value']
    print(g)
    return g
    
def gotoxyzE(gcoord):
    xyzdata= {"position": {"x": str(gcoord[0]),"y": str(gcoord[1]+150),"z": str(gcoord[2])}, "angle": {"x": str(gcoord[3]),"y": str(gcoord[4]),"z": str(gcoord[5])}}
#     xyzdata=  {
#     "position": {
#     "x": 870,
#     "y": 400,
#     "z": 900
#     },
#   "angle": {
#     "x": 0,
#     "y": 90,
#     "z": 0
#   }
# }
    response = session.post('http://10.240.9.209:8082/api/RobotMotion/MoveJ_E',json=xyzdata,headers=head)
    print (response)

def gotoxyzLE(gcoord):
    xyzdata= {"position": {"x": str(gcoord[0]),"y": str(gcoord[1]),"z": str(gcoord[2])}, "angle": {"x": str(gcoord[3]),"y": str(gcoord[4]),"z": str(gcoord[5])}}
    response = session.post('http://10.240.9.209:8082/api/RobotMotion/MoveL_E',json=xyzdata,headers=head)
    print (response)

def opengripper():
    response = session.post('http://10.240.9.209:8082/api/Gripper/OpenGripper',json=1,headers=head)
    print (response)


def closegripper():
    response = session.post('http://10.240.9.209:8082/api/Gripper/CloseGripper',json=1,headers=head)
    print (response)


def gotoxyzstore():
#    xyzdata= {"position": {"x": -512,"y": -92,"z": 600}, "angle": {"x": 0,"y": 90,"z": 0}}
#    response = session.post('http://10.240.9.209:8082/api/RobotMotion/MoveJ_E',json=xyzdata,headers=head)
#    print (response)
    xyzdata= {"position": {"x": -512,"y": -118,"z": 278}, "angle": {"x": -179.32,"y": 8.51,"z": 16.50}}
#   xyzdata= {"position": {"x": 400,"y": -400,"z": 400}, "angle": {"x": 0,"y": 90,"z": 0}}
#   xyzdata= {"position": {"x": 400,"y": -400,"z": 400}, "angle": {"x": 60,"y": 32,"z": 108}}
    response = session.post('http://10.240.9.209:8082/api/RobotMotion/MoveL_E',json=xyzdata,headers=head)
    print (response)

def startmain():
    response = session.post('http://10.240.9.209:8082/api/RobotBasicOpr/StartMain',json=1,headers=head)
    print (response)

def gohome():
    response = session.post('http://10.240.9.209:8082/api/RobotMotion/MoveHome',json=1,headers=head)#session.post('http://10.240.9.209:8082/api/RobotMotion/MoveHome',json=1,headers=head)
    print (response)    

#if __name__ == '__main__':
#    gohome()
 #   startmain()
  #  gohome()
#     gotoxyzE()
    #UpdateData('pViaPath','[230.87,808.8,56.98]')
    #SetSpeedRatio(20)
    #a=GetSpeedRatio()

# def SetSpeedRatio(speed):
#     sparam = {
#         'speed-ratio': speed
#     }
#     response = session.post(uriPrefix + 
    #print( a)
    #GetData('pViaPath')
    #while True:
        #print("Waiting")

