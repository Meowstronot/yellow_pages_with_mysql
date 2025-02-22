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

show_database(dict_config)