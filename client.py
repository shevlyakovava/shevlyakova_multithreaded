import socket
import threading

nickname = input("Как Вас зовут?")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # иницилизация сокетов
client.connect(('127.0.0.1', 5555))  # подключение по адресу и порту


def send(): # функция отправки
    while True:
        message = f'{nickname}: {input()}' # считываем сообщение пользователя
        if message.replace(' ','').split(':')[-1] == 'exit':
            client.close()
            break
        else:
            client.send(message.encode('UTF-8'))


def get(): # функция получения
    while True:
        try:
            message = client.recv(1024).decode('UTF-8') # получаем сообщение от сервера или других пользователей
            if message == 'write_name':
                client.send(nickname.encode('UTF-8'))
            else:
                print(message)
        except:
            print("Отключение от сервера")
            client.close()
            break


receive_thread = threading.Thread(target=get) # получение многопоточное (главная функция get)
receive_thread.start() # начало многопоточного получения данных от сервера

write_thread = threading.Thread(target=send) # то же самое только функция send - отправка
write_thread.start()
