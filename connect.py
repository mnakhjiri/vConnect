import pickle
import os
import json
import signal
import subprocess
PATH = ""




def getConnections():
    connections = []
    with open("connections.txt","r") as f:
        connections = f.readlines()
    
    
    return connections

def connect():
    connections = getConnections()
    for connection in connections:
        try:
            connection = connection.strip()
            import subprocess
            import tempfile
            with tempfile.TemporaryFile() as tempf:
                proc = subprocess.Popen(['python3', 'vmess2json.py', connections[0]], stdout=tempf)
                proc.wait()
                tempf.seek(0)
                result = tempf.read().decode('utf-8')
                resultObject = json.loads(result)
                for proxy in resultObject["inbounds"]:
                    if proxy["tag"] == "socks-in":
                        try:
                            os.system(f"gsettings set org.gnome.system.proxy.socks host '127.0.0.1'")
                            os.system(f"gsettings set org.gnome.system.proxy.socks port \'{proxy['port']}\'")
                        except:
                            print("failed to set socks proxy on your system, please set it manually")
                            print("address :127.0.0.1")
                            print(f"socks port : {proxy['port']}")

                    if proxy["tag"] == "http-in":
                        try:
                            os.system(f"gsettings set org.gnome.system.proxy.http host '127.0.0.1'")
                            os.system(f"gsettings set org.gnome.system.proxy.http port \'{proxy['port']}\'")
                        except:
                            print("failed to set http proxy on your system, please set it manually")
                            print("address :127.0.0.1")
                            print(f"http port : {proxy['port']}")
                            
                with open(f"{PATH}/config.json","w") as f:
                    f.write(result)
                # subprocess.Popen([f"{PATH}/v2ray","-config",f"{PATH}/config.json"])
                os.system(f"{PATH}/v2ray run")

        except:
            pass

if os.path.exists('vcorePath.pyc'):
    vcorePath = pickle.load(open('vcorePath.pyc','rb'))
    PATH = vcorePath
else:
    print("Please enter the path of the vcore executable file (v2ray file):")
    PATH = input()
    pickle.dump(PATH,open('vcorePath.pyc','wb'))

if not os.path.exists("connections.txt"):
    open("connections.txt","w").close()

connections = getConnections()
if len(connections) == 0:
    print("No connections found. Please add vmess url to connections.txt")

connect()

