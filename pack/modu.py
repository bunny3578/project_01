import csv
import json
import sqlite3


def read_csv(users_data):
    try:
        with open(users_data, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print("找不到檔案...")
    except Exception as e:
        print("開檔發生錯誤...")
        print(f"錯誤代碼為：{e.errno}")
        print(f"錯誤訊息為：{e.strerror}")
        print(f"錯誤檔案為：{e.filename}")
        return None


def read_json(books_data):
    try:
        with open(books_data, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("找不到檔案...")
    except Exception as e:
        print("開檔發生錯誤...")
        print(f"錯誤代碼為：{e.errno}")
        print(f"錯誤訊息為：{e.strerror}")
        print(f"錯誤檔案為：{e.filename}")
        return None


def read_sqlite():
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                        "user_id"    INTEGER,
                        "username"    TEXT NOT NULL,
                        "password"    TEXT NOT NULL,
                        PRIMARY KEY("user_id" AUTOINCREMENT)
                        )"""
        )
        cursor.execute(
          """CREATE TABLE IF NOT EXISTS books (
        "book_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" TEXT NOT NULL,
        "author" TEXT NOT NULL,
        "publisher" TEXT NOT NULL,
        "year" INTEGER NOT NULL
    )"""
        )
        data = cursor.fetchall()
        conn.close()
        return data
    except FileNotFoundError:
        print("找不到檔案...")
    except Exception as e:
        print("開檔發生錯誤...")
        print(f"錯誤代碼為：{e.errno}")
        print(f"錯誤訊息為：{e.strerror}")
        print(f"錯誤檔案為：{e.filename}")
        return None


def login(users_data):
    while True:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")
        for user in users_data:
            if username == user[0] and password == user[1]:
                print("登入成功！")
                return True
        print("帳號或密碼錯誤，請重新輸入。")


def insert_into_users(conn, users_data):
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                "user_id"    INTEGER PRIMARY KEY AUTOINCREMENT,
                "username"    TEXT NOT NULL,
                "password"    TEXT NOT NULL
            )"""
        )

        cursor.executemany(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            users_data
        )
        conn.commit()
        print("成功讀讀取users檔案!")
    except Exception as e:
        print("讀取users檔案時發生錯誤")
        print(f"錯誤訊息為：{str(e)}")


def insert_into_books(conn, books_data):
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
           """CREATE TABLE IF NOT EXISTS books (
        "book_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" TEXT NOT NULL,
        "author" TEXT NOT NULL,
        "publisher" TEXT NOT NULL,
        "year" INTEGER NOT NULL
    )"""
        )
        for book in books_data:
            cursor.execute(
                "INSERT INTO books (title, author, publisher, year) "
                "VALUES (?, ?, ?, ?)",
                (
                    book["title"],
                    book["author"],
                    book["publisher"],
                    book["year"],
                ),
            )
        conn.commit()
        print("成功讀取book檔案!")
    except Exception as e:
        print("讀取books檔案時發生錯誤")
        print(f"錯誤訊息為：{str(e)}")


def display_menu():
    print("-------------------")
    print("    資料表 CRUD")
    print("-------------------")
    print("    1. 增加記錄")
    print("    2. 刪除記錄")
    print("    3. 修改記錄")
    print("    4. 查詢記錄")
    print("    5. 資料清單")
    print("-------------------")


def add_record(conn):
    try:
        title = input("請輸入要新增的標題：")
        author = input("請輸入要新增的作者：")
        publisher = input("請輸入要新增的出版社：")
        year = input("請輸入要新增的年份：")
        if title and author and publisher and year:
            year = int(year)
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            query = "INSERT INTO books (title, author, publisher, year) " \
                    "VALUES ( ?, ?, ?, ? )"
            values = (title, author, publisher, year)
            cursor.execute(query, values)
            conn.commit()
            print("異動 1 記錄")
        else:
            print("給定的條件不足，無法進行新增作業")
    except Exception as e:
        print("新增記錄時發生錯誤...")
        print(f"錯誤訊息為：{str(e)}")


def delete_record(conn):
    try:
        title = input("請問要刪除哪一本書？：")
        if title:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE title=?", (title,))
            conn.commit()
            print("異動 1 記錄")
        else:
            print("給定的條件不足，無法進行刪除作業")
    except Exception as e:
        print("刪除記錄時發生錯誤...")
        print(f"錯誤訊息為：{str(e)}")


def modify_record(conn):
    try:
        title = input("請問要修改哪一本書的標題？：")
        if title:
            new_title = input("請輸入要更改的標題：")
            new_author = input("請輸入要更改的作者：")
            new_publisher = input("請輸入要更改的出版社：")
            new_year = input("請輸入要更改的年份：")
            if new_title or new_author or new_publisher or new_year:
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                update_query = "UPDATE books SET "
                update_fields = []
                if new_title:
                    update_fields.append(f"title = '{new_title}'")
                if new_author:
                    update_fields.append(f"author = '{new_author}'")
                if new_publisher:
                    update_fields.append(f"publisher = '{new_publisher}'")
                if new_year:
                    update_fields.append(f"year = {new_year}")
                update_query += ", ".join(update_fields)
                update_query += f" WHERE title = '{title}'"
                cursor.execute(update_query)
                conn.commit()
                print("異動 1 記錄")
            else:
                print("給定的條件不足，無法進行修改作業")
    except Exception as e:
        print("修改記錄時發生錯誤...")
        print(f"錯誤訊息為：{str(e)}")


def search_record(conn):
    try:
        keyword = input("請輸入想查詢的關鍵字：")
        if keyword:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM books WHERE title LIKE ? OR "
                "author LIKE ? OR publisher LIKE ? OR year LIKE ?",
                (
                    "%" + keyword + "%",
                    "%" + keyword + "%",
                    "%" + keyword + "%",
                    "%" + keyword + "%",
                ),
            )
            result = cursor.fetchall()
            if result:
                print(
                    "|" + "目錄" + "|" +
                    chr(12288) * 1 + "書名" + chr(12288) * 1 + "|" +
                    chr(12288) * 2 + "作者" + chr(12288) * 2 + "|" +
                    chr(12288) * 3 + "出版社" + chr(12288) * 3 + "|" +
                    "年份" + "|"
                )
                for row in result:
                    print("|" + "  |  ".join(map(str, row)) + "  |")
            else:
                print("查無結果")
        else:
            print("關鍵字不得為空")
    except Exception as e:
        print("查詢記錄時發生錯誤...")
        print(f"錯誤訊息為：{str(e)}")


def list_records(conn):
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        result = cursor.fetchall()
        if result:
            print(
                "|" + "目錄" + "|" +
                chr(12288) * 1 + "書名" + chr(12288) * 1 + "|" +
                chr(12288) * 3 + "作者" + chr(12288) * 3 + "|" +
                chr(12288) * 3 + "出版社" + chr(12288) * 3 + "|" +
                "年份" + "|"
            )

            for row in result:
                print("|" + "  |  ".join(map(str, row)) + "  |")

        else:
            print("資料庫中無記錄")
    except Exception as e:
        print("列出記錄時發生錯誤...")
        print(f"錯誤訊息為：{str(e)}")


def menu_function(option, conn):
    if option == "1":
        add_record(conn)
    elif option == "2":
        delete_record(conn)
    elif option == "3":
        modify_record(conn)
    elif option == "4":
        search_record(conn)
    elif option == "5":
        list_records(conn)
    elif option == "":
        print("結束程式")
    else:
        print("=>無無效的選擇")


if __name__ == "__main__":
    users_data = read_csv("users.csv")
    books_data = read_json("books.json")
    if users_data and books_data:
        conn = sqlite3.connect("library.db")
        try:
            insert_into_users(conn, users_data)
            insert_into_books(conn, books_data)
            if login(users_data):
                display_menu()
                while True:
                    try:
                        choice = input("選擇要執行的功能(Enter離開)：")
                        menu_function(choice, conn)
                        if choice == "":
                            break
                    except ValueError:
                        print("請輸入有效的選項（數字）！")
        finally:
            conn.close()
    else:
        print("無法讀取使用者資料或書籍資料！")
