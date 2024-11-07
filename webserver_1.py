from socket import *
import sys

# 프록시 서버 설정
proxyPort = 6789
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind(('', proxyPort))
proxySocket.listen(5)

print("The proxy server is ready to receive")

while True:
    clientConnection, clientAddress = proxySocket.accept()
    try:
        # 클라이언트 요청 수신
        message = clientConnection.recv(2048).decode()
        print("Client Request:")
        print(message)

        # 요청에서 URL 추출
        url = message.split()[1]
        host = url.split("//")[1].split("/")[0]
        print("Requested host:", host)

        # 원격 서버와 연결할 소켓 생성
        remoteServerSocket = socket(AF_INET, SOCK_STREAM)
        remotePort = 80  # 기본 HTTP 포트
        remoteServerSocket.connect((host, remotePort))
        
        # 원격 서버로 요청 전달
        remoteServerSocket.send(message.encode())
        
        # 원격 서버의 응답을 받아 클라이언트로 중계
        while True:
            response = remoteServerSocket.recv(2048)
            if len(response) > 0:
                clientConnection.send(response)
            else:
                break
            

        # 연결 종료
        remoteServerSocket.close()
        clientConnection.close()

    except Exception as e:
        print("Error:", e)
        clientConnection.close()

proxySocket.close()
sys.exit()
