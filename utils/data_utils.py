import pymysql
import pymysql.cursors
from tabulate import tabulate
# from test import dict_config

def input_not_null(prompt:str) -> str:
    """Funtion untuk membuat input box yang tidak boleh kosong

    Args:
        prompt (str): Caption untuk input box

    Returns:
        str: nilai dari input box
    """
    while True:
        user_input = input(prompt)
        if user_input == "" or user_input == None or user_input == " ":
            print("Input box tidak boleh kosong. Silakan masukkan input lagi.")
        else:
            return user_input


def connect_mysql(dict_config):
    """Function untuk login MySQL
    """
    try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        print("Connection Success !")
        # cursor = conn.cursor() # membuka gerbang akses query mysql

        # sql_query = """
        #             SELECT * FROM users
        #             """

        # cursor.execute(query=sql_query)
        # conn.commit() 
        # print("Commit Sucsess !")
        # hasil = cursor.fetchall()
        # print(hasil)
    
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")

    finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def show_database(dict_config):
   """function untuk menampilkan Database Yellow Pages

    Args:
        dict_config (dict): dictionary configuration untuk login MySQL

    Returns:
        str: list of dictionary data
    """
   try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        # print("Connection Success !")

        cursor = conn.cursor() # membuka gerbang akses mysql

        sql_query = """
                    SELECT * FROM users
                    """

        cursor.execute(query=sql_query)
        conn.commit() 
        print("Commit Sucsess !")
        print("")
        print("Database Yellow Pages: ")
        hasil = cursor.fetchall()
        print(tabulate(hasil, headers="keys", tablefmt="pipe"))
   except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
   finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()
