import pymysql
import pymysql.cursors
from utils.data_utils import *
import datetime as dt
from tabulate import tabulate

def show_filtered_database(nomor:str,dict_config):
    """Menampilkan data dari satu nomor, nomor harus ada
    """
    database = get_database_info(dict_config)
    filtered_database = [item for item in database if nomor in item["phone_number"]]
    print("No Hp ditemukan : ")
    print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
    print("")
    return filtered_database
    

def update_profil(dict_config, tuple_value_8):
    try:
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    UPDATE profil p
                    SET 
                        p.email = %s,
                        p.full_name = %s,
                        p.nickname = %s,
                        p.gender = %s,
                        p.state = %s,
                        p.city = %s,
                        p.address = %s
                    WHERE p.email = %s
                    """ 
        cursor.execute(query=sql_query, args=tuple_value_8)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 

def update_contact(dict_config, tuple_value_5):
    try:
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    UPDATE contact c
                    SET 
                        c.email = %s,
                        c.facebook = %s,
                        c.instagram = %s,
                        c.twitter = %s
                    WHERE c.phone_number = %s
                    """ 
        cursor.execute(query=sql_query, args=tuple_value_5)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 

def update_category(dict_config, tuple_value_3):
    try:
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    UPDATE category c
                    SET 
                        c.category= %s,
                        c.notes= %s,
                        c.last_update= NOW()
                    WHERE phone_number = %s
                    """ 
        cursor.execute(query=sql_query, args=tuple_value_3)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 


def update_data(dict_config):
    """Function to change data
    """
    print("")
    print("Please enter the information to edit data!")
    print("")

    database = get_database_info(dict_config)
    df = pd.DataFrame(database)

    while True: # looping untuk cari nomor lagi

        # 1. validasi input nomor hp
        while True:
            phone_number = input_not_null("Please enter phone number: ")
            if phone_number.isdigit() and (len(phone_number) == 12 or len(phone_number)== 13) :
                break
            else:
                print("Input Invalid!")

        # 2. cari data nomor hp
        old_df = df[df["phone_number"]==phone_number].copy()
        filtered_df = df[df["phone_number"]==phone_number].copy()

        # 3. eksekusi edit
        if filtered_df.empty == False:
            # show 
            print("Contact Found:")
            print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))
            # select edited menu
            menu = ["email",
                    "full_name",
                    "nickname",
                    "gender",
                    "state",
                    "city",
                    "address",
                    "category",
                    "notes",
                    "facebook",
                    "instagram",
                    "twitter",
                    "Return to main menu"]
            print("")
            for i, val in enumerate(menu):
                i += 1
                print(f"{i}. {val}")
            option = None
            while option != len(menu):

                option = input_choose_num(f"Please select column to edit (1-{len(menu)}): ",min=1, max=len(menu))
                selected_menu = menu[option-1]
                print(selected_menu)

                if option == 1:
                    new_email = input_not_null("Please enter new email: ")
                    filtered_df[selected_menu] = new_email
                
                elif option == 2:
                    new_full_name = input_not_null("Please enter new full name: ")
                    filtered_df[selected_menu] = new_full_name  

                elif option == 3:
                    new_nickname = input("Please enter new nickname : ")
                    filtered_df[selected_menu] = new_nickname  
                
                elif option == 4:
                    print("1. Male")
                    print("2. Female")
                    new_gender = input_choose_num("Please choose 1 or 2: ",1,2)
                    new_gender = "Male" if new_gender == 1 else "Female"
                    filtered_df[selected_menu] = new_gender

                elif option == 5:
                    new_state = input_not_null("Please enter new state : ")
                    filtered_df[selected_menu] = new_state  

                elif option == 6:
                    new_city = input_not_null("Please enter new city : ")
                    filtered_df[selected_menu] = new_city  

                elif option == 7:
                    new_address = input("Please enter new adddress : ")
                    filtered_df[selected_menu] = new_address  
                
                elif option == 8:
                    array_category = df["category"].unique()
                    for i, val in enumerate(array_category):
                        print(f"{i+1} {val}")
                    print(f"{i+2} add new category")
                    num_category = input_choose_num(f"Please select category contact 1-{i+2}: ",min=1, max=i+2)
                    if num_category == (i+2):
                        new_category = input_not_null("Please enter new category: ").title()
                    else:
                        new_category = array_category[num_category-1]
                    filtered_df[selected_menu] = new_category  
            
                elif option == 9:
                    new_notes = input("Please enter new notes : ")
                    filtered_df[selected_menu] = new_notes  

                elif option == 10:
                    new_facebook = input("Please enter new facebook : ")
                    filtered_df[selected_menu] = new_facebook  

                elif option == 11:
                    new_instagram = input("Please enter new instagram : ")
                    filtered_df[selected_menu] = new_instagram  

                elif option == 12:
                    new_twitter = input("Please enter new twitter : ")
                    filtered_df[selected_menu] = new_twitter  

                elif option == 13:
                    print("Update data canceled!")

                filtered_df["last_update"] = dt.datetime.now()
                print(tabulate(filtered_df, headers="keys", tablefmt="pipe"))

                tuple_profil = (filtered_df["email"].item(), filtered_df["full_name"].item(), filtered_df["nickname"].item(), 
                                filtered_df["gender"].item(), filtered_df["state"].item(), filtered_df["city"].item(), 
                                filtered_df["address"].item(), old_df["email"].item())
                tuple_contact = (filtered_df["email"].item(), filtered_df["facebook"].item(), filtered_df["instagram"].item(), filtered_df["twitter"].item(), filtered_df["phone_number"].item())
                tuple_category = (filtered_df["category"].item(), filtered_df["notes"].item(), filtered_df["phone_number"].item())
                # print(tuple_profil)
                # print(tuple_contact)
                # print(tuple_category)
                update_profil(dict_config, tuple_profil)
                update_contact(dict_config, tuple_contact)
                update_category(dict_config, tuple_category)

                print("Successfully update!")
                return
        else:
            print("Data of phone number not found!")
            # 4. loop untuk cari lagi
            while True:
                cari_lagi = input("Try again? (y/n) :")
                if cari_lagi.lower() == "y":
                    break
                elif cari_lagi.lower() == "n":
                    return
