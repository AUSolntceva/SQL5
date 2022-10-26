import psycopg2
from pprint import pprint

#Функция, создающая структуру БД (таблицы)
def create_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients_HomeworkSQL5(
    id SERIAL PRIMARY KEY, 
    client_name VARCHAR(100) NOT NULL, 
    client_surname VARCHAR(100) NOT NULL, 
    client_email VARCHAR(100) NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_phonenumbers(
    id_phonenumber SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients_HomeworkSQL5(id),
    client_phonenumber VARCHAR(20) UNIQUE);
    """)


#Функция, позволяющая добавить нового клиента
def add_new_client(cur, client_name, client_surname, client_email):
    cur.execute("""
    INSERT INTO clients_HomeworkSQL5(client_name, client_surname, client_email) VALUES(%s, %s, %s);
    """, (client_name, client_surname, client_email))


#Функция, позволяющая добавить телефон для существующего клиента
def add_new_phonenumber(cur, client_id, phonenumber):
    cur.execute("""
    INSERT INTO client_phonenumbers(client_id, client_phonenumber) VALUES(%s, %s);
    """, (client_id, phonenumber))


#Функция, позволяющая изменить данные о клиенте
def change_client_data():
    print("Какие данные введены некорректно? Введите нужную цифру: 1 - Имя; 2 - Фамилия; 3 - Электронная почта; 4 - Номер телефона")

    while True:
        command_symbol = int(input())
        if command_symbol == 1:
            input_id_for_changing_name = input("Введите id клиента: ")
            input_name_for_changing = input("Введите корректное имя: ")
            cur.execute("""
            UPDATE clients_HomeworkSQL5 SET client_name=%s WHERE id=%s;
            """, (input_name_for_changing, input_id_for_changing_name))
            break
        elif command_symbol == 2:
            input_id_for_changing_surname = input("Введите id клиента: ")
            input_surname_for_changing = input("Введите корректную фамилию: ")
            cur.execute("""
            UPDATE clients_HomeworkSQL5 SET client_surname=%s WHERE id=%s;
            """, (input_surname_for_changing, input_id_for_changing_surname))
            break
        elif command_symbol == 3:
            input_id_for_changing_email = input("Введите id клиента: ")
            input_email_for_changing = input("Введите корректный адрес электронной почты: ")
            cur.execute("""
            UPDATE clients_HomeworkSQL5 SET client_email=%s WHERE id=%s;
            """, (input_email_for_changing, input_id_for_changing_email))
            break
        elif command_symbol == 4:
            input_phonenumber_you_wanna_change = input("Введите некорректный номер: ")
            input_phonenumber_for_changing = input("Введите корректный номер: ")
            cur.execute("""
            UPDATE client_phonenumbers SET client_phonenumber=%s WHERE client_phonenumber=%s;
            """, (input_phonenumber_for_changing, input_phonenumber_you_wanna_change))
            break
        else:
            print("Команда введена некорректно")


#Функция, позволяющая удалить телефон для существующего клиента
def delete_client_phonenumber():
    input_id_for_deleting_phonenumber = input("Введите id клиента: ")
    input_phonenumber_for_deleting = input("Введите номер телефона, который нужно удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phonenumbers WHERE client_id=%s AND client_phonenumber=%s
        """, (input_id_for_deleting_phonenumber, input_phonenumber_for_deleting))


#Функция, позволяющая удалить существующего клиента
def delete_client():
    input_id_for_deleting_client = input("Введите id клиента: ")
    input_client_surname_for_deleting = input("Введите фамилию клиента: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phonenumbers WHERE client_id=%s
        """, (input_id_for_deleting_client,))
        cur.execute("""
        DELETE FROM clients_HomeworkSQL5 WHERE id=%s AND client_surname=%s
        """, (input_id_for_deleting_client, input_client_surname_for_deleting))


#Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client():
    print("Выберите параметр поиска: 1 - по имени; 2 - по фамилии; 3 - по e-mail; 4 - по номеру телефона")
    while True:
        input_command_for_finding = int(input("Выберите параметр поиска: "))
        if input_command_for_finding == 1:
            input_name_for_finding = input("Введите имя: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients_HomeworkSQL5 AS ch5
            LEFT JOIN client_phonenumbers AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_name=%s
            """, (input_name_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 2:
            input_surname_for_finding = input("Введите фамилию: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients_HomeworkSQL5 AS ch5
            LEFT JOIN client_phonenumbers AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_surname=%s
            """, (input_surname_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 3:
            input_email_for_finding = input("Введите адрес электронной почты: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients_Homework5 AS ch5
            LEFT JOIN client_phonenumbers AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_email=%s
            """, (input_email_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 4:
            input_phonenumber_for_finding = input("Введите номер телефона: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phonenumber
            FROM clients_HomeworkSQL5 AS ch5
            LEFT JOIN client_phonenumbers AS cp ON cp.id_phonenumber = ch5.id
            WHERE client_phonenumber=%s
            """, (input_phonenumber_for_finding,))
            #return cur.fetchone()[0]
            print(cur.fetchall())
        else:
            print("Команда введена некорректно")


with psycopg2.connect(database="HomeworkSQL5", user="postgres", password="copybookSQL") as conn:
    with conn.cursor() as cur:
        create_tables(cur)
        add_new_client(cur, "Иван", "Иванов", "iivanov@yandex.ru")
        add_new_client(cur, "Петр", "Петров", "ppetrov@yandex.ru")
        add_new_client(cur, "Сергей", "Сидоров", "ssidorov@yandex.ru")

        add_new_phonenumber(cur, 1, "89008007060")
        add_new_phonenumber(cur, 2, "85004003020")
        add_new_phonenumber(cur, 3, "81009008070")

        change_client_data()
        delete_client_phonenumber()
        delete_client()
        find_client()

conn.close()