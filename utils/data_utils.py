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
    """Filter Database based on selected menu.
    """
    
    database = get_database_info(dict_config)
    df = pd.DataFrame(database)

    menu_options = {
        1: "phone_number",
        2: "email",
        3: "full_name",
        4: "nickname",
        5: "gender",
        6: "state",
        7: "city",
        8: "category",
        9: "Return to Main Menu"
    }

    while True:
        print("\nPelase select search method:")
        for key, value in menu_options.items():
            if key == 9:
                print(f"{key}. {value}")
            else:
                print(f"{key}. Search by {value.replace('_', ' ').title()}")

        option = input_choose_num("Enter a number (1-9): ", min=1, max=9)

        if option == 9:
            return

        selected_field = menu_options[option]

        if selected_field == "gender":
            print("1. Male\n2. Female")
            gender_choice = input_choose_num("Choose 1 or 2: ", min=1, max=2)
            search_value = "Male" if gender_choice == 1 else "Female"
            filtered_df = df[df[selected_field] == search_value]

        elif selected_field == "category":
            categories = df["category"].unique()
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")
            category_choice = input_choose_num(f"Enter a number (1-{len(categories)}): ", min=1, max=len(categories))
            search_value = categories[category_choice - 1]
            filtered_df = df[df[selected_field] == search_value]

        else:
            search_value = input_not_null(f"Enter {selected_field.replace('_', ' ')}: ")

            if selected_field == "phone_number":
                while not search_value.isdigit() or len(search_value) not in (12, 13):
                    print("Input is not valid!")
                    search_value = input_not_null("Enter phone number: ")
            filtered_df = df[df[selected_field].str.contains(search_value, case=False, na=False)]

        if filtered_df.empty:
            print(f"{selected_field.replace('_', ' ').title()} is not found!")
        else:
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))
            return

