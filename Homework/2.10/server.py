
import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 5000

tasks = []

tasks_lock = threading.Lock()


def process_command(command):
    parts = command.strip().split(maxsplit=1)

    if not parts:
        return "Пустая команда", False

    action = parts[0].lower()

    if action == "/add":
        if len(parts) < 2 or not parts[1].strip():
            return "Ошибка: укажите текст задачи", False

        task_text = parts[1].strip()

        with tasks_lock:
            tasks.append({
                "text": task_text,
                "done": False
            })
            number = len(tasks)

        return f"Задача №{number} добавлена", False

    elif action == "/list":
        with tasks_lock:
            if not tasks:
                return "Список задач пуст", False

            result = []

            for number, task in enumerate(tasks, start=1):
                status = "Выполнена" if task["done"] else "Не выполнена"
                result.append(
                    f'{number}. {task["text"]} — {status}'
                )

        return "\n".join(result), False

    elif action == "/done":
        if len(parts) < 2:
            return "Ошибка: укажите номер задачи", False

        try:
            number = int(parts[1])
        except ValueError:
            return "Ошибка: номер должен быть числом", False

        with tasks_lock:
            if number < 1 or number > len(tasks):
                return "Такой задачи не существует", False

            tasks[number - 1]["done"] = True

        return f"Задача №{number} выполнена", False

    elif action == "/delete":
        if len(parts) < 2:
            return "Ошибка: укажите номер задачи", False

        try:
            number = int(parts[1])
        except ValueError:
            return "Ошибка: номер должен быть числом", False

        with tasks_lock:
            if number < 1 or number > len(tasks):
                return "Такой задачи не существует", False

            deleted = tasks.pop(number - 1)

        return f'Удалена задача: {deleted["text"]}', False

    elif action == "/quit":
        return "Отключение от сервера", True

    else:
        return "Неизвестная команда", False


def handle_client(conn, address):
    print(f"Подключился клиент: {address}")

    try:
        reader = conn.makefile("r", encoding="utf-8")

        for line in reader:
            command = line.rstrip("\r\n")

            response, should_quit = process_command(command)

            response_data = json.dumps(
                {"response": response},
                ensure_ascii=False
            ) + "\n"

            conn.sendall(response_data.encode("utf-8"))

            if should_quit:
                break

    except (ConnectionError, OSError) as error:
        print(f"Ошибка соединения: {error}")

    finally:
        conn.close()
        print(f"Клиент отключился: {address}")


def start_server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Сервер запущен на {HOST}:{PORT}")

        while True:
            conn, address = server_socket.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True
            )

            client_thread.start()

    except KeyboardInterrupt:
        print("Остановка сервера")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()

