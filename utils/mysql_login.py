from utils.data_utils import *
import os
import csv


file_name = "mysql_login_info.csv"

# Dapatkan lokasi asli skrip mysql_login.py
script_dir = os.path.dirname(os.path.abspath(__file__))  # Lokasi skrip

# Gabungkan dengan nama file
file_path = os.path.join(script_dir, file_name)

def cek_file(file_path)->bool:
    """Function to check if a file exists or not.
    
    Args:
        file_path (str): The file location in local storage.
    
    Returns:
        bool: True if the file exists, False if the file does not exist.
    """
    if os.path.isfile(file_path):
        return True
    else:
        return False    

def create_dict_config()->dict:
    """Function to create dictionary configuration MySQL
    Returns:
        dict: configuration MySQL
    """
    print("\nPlease enter MySQL configuration information: ")
    while True:
        host = input_not_null("Please enter host MySQL :")
        user = input_not_null("Please enter user MySQL :")
        password = input_not_null("Please enter password MySQL :")
        # database = input_not_null("Please enter database MySQL :")
        database = "yellow_pages"
        #Configuration MySQL
        dict_config = {
                    "host": host,
                    "user": user,
                    "password": password,
                    "database": database,
                    "cursorclass": pymysql.cursors.DictCursor # merubah output result menjadi list of dictionary
                    }
        return dict_config

def read_dict_from_csv(file_path:str)->dict:
    """Function to read dictionary from csv file
    Args:
        file_path (str): The file location in local storage.
    Returns:
        dict: dictionary Configuration MySQL
    """
    try:
        with open(file_path, mode='r', newline='', encoding="utf-8") as file:
            reader = csv.reader(file)
            keys = next(reader) # membaca baris pertama sebagai keys
            values = next(reader) # membaca baris kedua sebagai values
            dict_config = dict(zip(keys, values)) # menggabungkan keys dan values menjadi dictionary
            # print(f"Data Configuration MySQL berhasil dibaca di lokasi: {file_path}")
            print(f"Configuration MySQL Data Successfully Read!")
            return dict_config
    except Exception as e:
        print(f"❌ Error on reading file: {e}")
        return None

def validasi_data_csv(dict_config:dict)->bool:
    """Function to validate dict_config data 
    Args:
        dict_config (dict): Dictionary Configuration MySQL
    Returns:
        bool: True if file csv valid, False if file csv not valid
    """
    expected_keys = {"host", "user", "password", "database", "cursorclass"}
    if set(dict_config.keys()) == expected_keys:
        # print("Atribut Configuration MySQL valid!")
        return True
    else:
        # print("Atribut Configuration MySQL tidak valid!")
        return False

def save_dict_to_csv(dict_config:dict, file_path:str):
    """Function to save dictionary into csv file
    Args:
        dict_config (dict): Dictionary Configuration MySQL
        file_path (str): The file location in local storage.
    """
    try:
        with open(file_path, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            # Menulis header (nama key)
            writer.writerow(dict_config.keys())
            # Menulis nilai (value dari dictionary)
            writer.writerow(dict_config.values())
            # print(f"Data Configuration MySQL berhasil disimpan di lokasi: {file_path}")
            print(f"MySQL Configuration Data Saved!")
    except Exception as e:
        print(f"❌ Error while saving file: {e}")

def delete_file_csv(file_path:str):
    """Function to delete csv file
    Args:
        file_path (str): The file location in local storage.
    """
    try:
        if os.path.isfile(file_path):  # Cek apakah file ada
            os.remove(file_path)  # Hapus file
            print(f"✅ File '{file_name}' successfully delete.")
        else:
            print(f"❌ File '{file_name}' not found.")
    except FileNotFoundError:
        print(f"❌ File '{file_name}' not found.")
    except PermissionError:
        print(f"⚠️ Has no permission to delete '{file_name}'.")
    except Exception as e:
        print(f"❌ Error while delete: {e}")


def reset_login_info():
    """Function to reset MySQL login info
    Args:
        file_path (str): The file location in local storage.
    """
    if cek_file(file_path):
        delete_file_csv(file_path)
        dict_config = create_dict_config()
        save_dict_to_csv(dict_config, file_path)
    else:
        dict_config = create_dict_config()
        save_dict_to_csv(dict_config, file_path)


def mysql_configuration()->dict:
    """Function to generate MySQL configuration

    Returns:
        dict: MySQL configuration
    """
    while True:
        if cek_file(file_path):
            # Jika sudah ada maka akan validasi data login
            print(f"File '{file_name}' found!")
            # print(f"File '{file_name}' ditemukan di lokasi: {file_path}")

            # read csv kemudian validasi data
            dict_config = read_dict_from_csv(file_path)
            validasi_dict = validasi_data_csv(dict_config)
        else:
            # Jika belum ada maka akan meminta inputan user
            print(f"File '{file_name}' not found!")
            # print(f"File '{file_name}' tidak ditemukan di lokasi: {file_path}")

            # membuat file csv, validasi dan save
            dict_config = create_dict_config() # membuat dictionary configuration MySQL
            # print(dict_config)
            validasi_dict = validasi_data_csv(dict_config) # validasi dictionary configuration MySQL
            save_dict_to_csv(dict_config, file_path)

        if validasi_dict:
            print("MySQL Configuration Data is valid!")
            return dict_config
        else:
            print("❌MySQL Configuration Data is not valid!")
            print("\nReset MySQL Configuration Data: ")
            delete_file_csv(file_path)