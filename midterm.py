import pack.modu as lib


def main():
    users_data = lib.read_csv("users.csv")
    books_data = lib.read_json("books.json")
    if users_data and books_data:
        conn = lib.read_sqlite()
        try:
            lib.insert_into_users(conn, users_data)
            lib.insert_into_books(conn, books_data)
            if lib.login(users_data):
                while True:
                    lib.display_menu()
                    choice = input("選擇要執行的功能(Enter離開)：")
                    if choice == "":
                        break
                    lib.menu_function(choice, conn)
        finally:
            conn.close()
    else:
        print("無法讀取使用者資料或書籍資料！")


if __name__ == "__main__":
    main()
