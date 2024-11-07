from socket import *
import time
import statistics 

def main():
    serverName = 'localhost'
    serverPort = 12000

    ping_count = 10
    sent_packets = 0
    received_packets = 0
    rtt_list = []

    try:
        # 클라이언트 소켓 생성 및 서버에 연결
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.settimeout(2)  # 수신 대기 시간 2초로 설정

        print(f"서버({serverName}:{serverPort})에 연결되었습니다.")
        print(f"{ping_count}개의 메시지를 전송한 후 연결이 종료됩니다.")

        for i in range(1, ping_count + 1):
            sentence = input(f'[{i}/{ping_count}] 전송할 메시지를 입력하세요 (종료하려면 "exit"): ')

            if sentence.lower() == 'exit':
                print("사용자에 의해 연결이 종료되었습니다.")
                break

            try:
                start_time = time.time()
                clientSocket.send(sentence.encode())
                sent_packets += 1

                # 서버로부터 응답 수신
                modifiedSentence = clientSocket.recv(1024)
                end_time = time.time()

                if modifiedSentence:
                    print('서버로부터 응답:', modifiedSentence.decode())
                    rtt = (end_time - start_time) * 1000  # RTT를 밀리초로 계산
                    rtt_list.append(rtt)
                    received_packets += 1
                else:
                    print("서버로부터 응답이 없습니다.")
            except timeout:
                print(f"[{i}] 요청이 타임아웃되었습니다.")
            except Exception as e:
                print(f"[{i}] 에러 발생: {e}")
                break

        # 통계 출력
        print("\n--- Ping 통계 ---")
        print(f"{sent_packets}개의 패킷이 전송되었고, {received_packets}개의 패킷이 수신되었습니다. "
              f"패킷 손실률: {((sent_packets - received_packets) / sent_packets * 100):.1f}%")
        if rtt_list:
            print(f"RTT (최소/평균/최대/표준편차): "
                  f"{min(rtt_list):.2f}/{sum(rtt_list) / len(rtt_list):.2f}/"
                  f"{max(rtt_list):.2f}/{statistics.stdev(rtt_list):.2f} ms")

    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
    except Exception as e:
        print(f"예상치 못한 에러: {e}")
    finally:
        clientSocket.close()
        print("클라이언트 소켓이 종료되었습니다.")

if __name__ == "__main__":
    main()
