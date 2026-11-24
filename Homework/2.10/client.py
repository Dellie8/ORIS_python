
import socket
import json

HOST = "127.0.0.1"
PORT = 5000


def start_client():
    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as client_socket:

            client_socket.connect((HOST, PORT))

            reader = client_socket.makefile(
                "r",
                encoding="utf-8"
            )

            print("Вы подключились к серверу задач!")

            print("\nДоступные команды:")
            print("/add <текст> - добавить задачу")
            print("/list - показать задачи")
            print("/done <номер> - выполнить задачу")
            print("/delete <номер> - удалить задачу")
            print("/quit - выйти")

            while True:
                command = input("\nВведите команду: ").strip()

                if not command:
                    print("Введите команду")
                    continue

                client_socket.sendall(
                    (command + "\n").encode("utf-8")
                )

                response_line = reader.readline()

                if not response_line:
                    print("Сервер закрыл соединение")
                    break

                response_data = json.loads(response_line)

                print("\n" + response_data["response"])

                if command.split(maxsplit=1)[0].lower() == "/quit":
                    break

    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу.")
        print("Сначала запустите server.py.")

    except (OSError, json.JSONDecodeError) as error:
        print(f"Ошибка клиента: {error}")


if __name__ == "__main__":
    start_client()
