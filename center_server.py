import socket
import pickle

class CenterServer(object):
    IP = "192.168.1.55"
    PORT = 20099
    GAME_VERSION = "1.3.0"
    LISTA_SERVERS = [
                        ("2.85.253.85","15000","20000"),
                        ("2.85.253.85","15000","20001"),
                        ("2.85.253.85","15000","20002"),
                        ("2.85.253.85","15000","20003")
    ]
    z = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    z.bind((IP,PORT))
    print(f"Server Started: {IP}  {PORT}")

    @classmethod
    def run(cls):
        while True:
            data , address = CenterServer.z.recvfrom(5120)
            print(data.decode())
            if data.decode() == "version":
                CenterServer.z.sendto(CenterServer.GAME_VERSION.encode(),address)
            if data.decode() == "Servers":
                CenterServer.z.sendto(pickle.dumps(CenterServer.LISTA_SERVERS),address)



if __name__ == "__main__":
    CenterServer.run()
