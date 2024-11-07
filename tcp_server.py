from socket import *
import threading

def handle_client(connectionSocket, addr):
    print(f"클라이언트 {addr}와 연결되었습니다.")
    while True:
        try:
            sentence = connectionSocket.recv(1024)
            if not sentence:
                # 클라이언트가 연결을 종료한 경우
                print(f"클라이언트 {addr}가 연결을 종료했습니다.")
                break

            decoded_sentence = sentence.decode()
            print(f"받은 메시지 from {addr}: {decoded_sentence}")

            # 클라이언트가 'exit'을 보낸 경우 연결 종료
            if decoded_sentence.lower() == 'exit':
                print(f"클라이언트 {addr}가 종료 명령을 보냈습니다.")
                break

            capitalizedSentence = decoded_sentence.upper()
            connectionSocket.send(capitalizedSentence.encode())
        except Exception as e:
            print(f"클라이언트 {addr}와의 통신 중 에러 발생: {e}")
            break

    connectionSocket.close()
    print(f"클라이언트 {addr}와의 연결이 종료되었습니다.")

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)  # 동시에 최대 5개의 연결을 대기
    print('서버가 메시지를 받을 준비가 되었습니다.')

    try:
        while True:
            connectionSocket, addr = serverSocket.accept()
            # 클라이언트 처리를 별도의 스레드로 실행
            client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
    finally:
        serverSocket.close()

if __name__ == "__main__":
    main()
