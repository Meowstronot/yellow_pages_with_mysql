import pymysql
import pymysql.cursors
from utils.data_utils import *
import datetime as dt

def add_data():
    """Function untuk add data baru ke database

       Jika data sudah ada maka bisa di update dengan yang baru
    """
    print("")
    print("Silahkan isi Data Kontak untuk dimasukan kedalam Database: ")
    print("")

    