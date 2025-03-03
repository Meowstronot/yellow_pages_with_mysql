import pymysql
import pymysql.cursors
from tabulate import tabulate
import pandas as pd
# from test import dict_config

def input_choose_num(prompt:str, min:int=1, max:int=10)-> int:
    """Function to create and validate input for choosen number
    Args:
        promt (str): caption for input
        min (int, optional): minimum number input. Defaults to 1.
        max (int, optional): maximum number input.. Defaults to 10.
    Returns:
        int: valid number
    """
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            user_input = int(user_input)
            if user_input in range(min,max+1):
                return user_input
            else:
                print("Input invalid!")
        else:
            print("Input invalid!")

def input_not_null(prompt:str) -> str:
    """Funtion to validate and create not null input
    Args:
        prompt (str): promt for input

    Returns:
        str: value input
    """
    while True:
        user_input = input(prompt)
        if user_input == "" or user_input == None or user_input == " ":
            print("Input is null, please try again!")
        else:
            return user_input


def connect_mysql(dict_config):
    """Function to login MySQL
    """
    try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        print("Connection Success !")
    
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")

    finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def get_database_info(dict_config):
    """function to get Database Yellow Pages
    Args:
        dict_config (dict): dictionary configuration MySQL
    Returns:
        str: list of dictionary data
    """
    try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        # print("Connection Success !")
        cursor = conn.cursor() # membuka gerbang akses mysql

        sql_query = """
                    SELECT 	c.phone_number,
                            p.*,
                            cr.category,
                            cr.notes,
                            c.facebook,
                            c.instagram,
                            c.twitter,
                            cr.last_update
                        FROM profil p
                        LEFT JOIN contact c
                            ON p.email = c.email
                        LEFT JOIN category cr
                            ON c.phone_number = cr.phone_number
                    """
        cursor.execute(query=sql_query)
        conn.commit() 
        hasil = cursor.fetchall()
        # print(tabulate(hasil, headers="keys", tablefmt="pipe"))
        return hasil
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
    finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def show_database(dict_config):
    """function to show Database Yellow Pages
    Args:
        dict_config (dict): MySQL dictionary configuration 
    Returns:
        str: list of dictionary data
    """
    try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        # print("Connection Success !")
        cursor = conn.cursor() # membuka gerbang akses mysql

        sql_query = """
                    SELECT 	c.phone_number,
                            p.*,
                            cr.category,
                            cr.notes,
                            c.facebook,
                            c.instagram,
                            c.twitter,
                            cr.last_update
                        FROM profil p
                        LEFT JOIN contact c
                            ON p.email = c.email
                        LEFT JOIN category cr
                            ON c.phone_number = cr.phone_number
                    """
        cursor.execute(query=sql_query)
        conn.commit() 
        print("Commit Sucsess !")
        print("")
        print("Database Yellow Pages: ")
        hasil = cursor.fetchall()
        # print(hasil, type(hasil))
        print(tabulate(hasil, headers="keys", tablefmt="pipe"))
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
    finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def filter_database(dict_config):
    """Filter Database berdasarkan menu pilihan
    """
    database = get_database_info(dict_config)
    df = pd.DataFrame(database)
    

def filter_database(dict_config):
    """Filter Database berdasarkan menu pilihan
    """
    database = get_database_info(dict_config)
    df = pd.DataFrame(database)
    option = None

    menu = ["Find with phone_number",
            "Find with email",
            "Find with full_name",
            "Find with nickname",
            "Find with gender",
            "Find with state",
            "Find with city",
            "Find with category",
            "Return to main menu"]
    print("")
    for i, val in enumerate(menu):
        i += 1
        print(f"{i}. {val}")

    while option != 9:
        option = input_choose_num("Please enter number 1-9: ",min=1, max=9)
        selected_menu = menu[option-1].split()[-1]

        if option == 1:
            phone = input_not_null("Please enter phone number: ")
            while phone.isdigit()!= True and (len(phone) != 12 or len(phone) != 13):
                print("Input Invalid!")
                phone = input_not_null("Please enter phone number: ")
            filtered_df = df[df[selected_menu].str.contains(phone, case=False, na=False)]
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))
            return

        elif option == 2:
            email = input_not_null("Please enter email: ")
            filtered_df = df[df[selected_menu].str.contains(email, case=False, na=False)]
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))
            return

        elif option == 3:
            full_name = input_not_null("Please enter full name: ")
            filtered_df = df[df[selected_menu].str.contains(full_name, case=False, na=False)]
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))
            return

        elif option == 4:
            nickname = input_not_null("Please enter nickname: ")
            filtered_df = df[df[selected_menu].str.contains(nickname, case=False, na=False)]
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))
            return

        elif option == 5:
            print("1. Male")
            print("2. Female")
            gender = input_choose_num("Please choose 1 or 2: ",1,2)
            if gender == 1:
                gender = "Male"
            elif gender == 2:
                gender = "Female"
            print(tabulate(df[df[selected_menu]==gender], headers="keys", tablefmt="pipe"))
            return

        elif option == 6:
            state = input_not_null("Please enter state: ")
            filtered_df = df[df[selected_menu].str.contains(state, case=False, na=False)]
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe")) 
            return

        elif option == 7:
            city = input_not_null("Please enter city: ")
            filtered_df = df[df[selected_menu].str.contains(city, case=False, na=False)]
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))
            return

        elif option == 8:
            array_category = df["category"].unique()
            for i, val in enumerate(array_category):
                print(f"{i+1} {val}")
            num_category = input_choose_num(f"Please enter 1-{i+1}: ",min=1, max=i+1)
            selected_category = array_category[num_category-1]
            print(tabulate(df[df[selected_menu]==selected_category], headers="keys", tablefmt="pipe"))
            return

        elif option == 9:
            return
        else:
            print("Input Invalid!")