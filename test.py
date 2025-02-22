from utils.data_utils import *

while True:
    host = input_not_null("Silahkan Masukan host MySQL :")
    user = input_not_null("Silahkan Masukan user MySQL :")
    password = input_not_null("Silahkan Masukan password MySQL :")
    database = input_not_null("Silahkan Masukan database MySQL :")
    #Configuration
    dict_config = {
                "host": host,
                "user": user,
                "password": password,
                "database": database,
                "cursorclass": pymysql.cursors.DictCursor # merubah output result menjadi list of dictionary
                }
    try:
        connect_mysql(dict_config)
        break
    except:
        print("Connection to MySQL failed!")



# import pymysql
# import pymysql.cursors
# import numpy as np
# import pandas as pd

# #Configuration
# dict_config = {
#                 "host": "localhost",
#                 "user": "root",
#                 "password": "khisan0821",
#                 "database": "exercise",
#                 "cursorclass": pymysql.cursors.DictCursor # merubah output result menjadi list of dictionary
#               }

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
    hasil = cursor.fetchall()
    print(hasil)


except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
    print("Error !")
    conn.rollback()
    print(f"msg: {e}")

finally: # code yang selalu dijalankan meskipun error atau tidak
    conn.close()
