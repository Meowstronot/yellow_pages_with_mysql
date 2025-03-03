import pymysql
import pymysql.cursors
from utils.data_utils import *
from utils.update_data import *
import datetime as dt
from tabulate import tabulate

def add_data(dict_config):
    """Function to add data
    """

    database = get_database_info(dict_config)
    df = pd.DataFrame(database)

    print("")
    print("Please complete contact information: ")
    print("")

    #_______________________________Input new data______________________________________1
    while True:
        phone_number = input_not_null("Please enter phone number: ")
        if phone_number.isdigit() and (len(phone_number) == 12 or len(phone_number)== 13) :
            break
        else:
            print("Input Invalid!")

    email = input_not_null("Please enter email: ").lower()
    full_name = input_not_null("Please enter full name: ").title()
    nickname = input("Please enter nickname (optional): ").title()

    print("1. Male")
    print("2. Female")
    gender = input_choose_num("Please choose 1 or 2: ",1,2)
    gender = "Male" if gender == 1 else "Female"

    state = input_not_null("Please enter state: ").title()
    city = input_not_null("Please enter city: ").title()
    address = input("Please enter address (optional): ").title()

    array_category = df["category"].unique()
    for i, val in enumerate(array_category):
        print(f"{i+1} {val}")
    print(f"{i+2} add new category")
    num_category = input_choose_num(f"Please select category contact 1-{i+2}: ",min=1, max=i+2)
    if num_category == (i+2):
        category = input_not_null("Please enter new category: ").title()
    else:
        category = array_category[num_category-1]
    
    notes = input("Please enter notes (optional): ").title()
    facebook = input("Please enter facebook (optional): ").title()
    instagram = input("Please enter instagram (optional): ").title()
    twitter = input("Please enter twitter (optional): ").title()

    inputed_data = [{"phone_number": phone_number,
                    "email": email,
                    "full_name": full_name,
                    "nickname": nickname,
                    "gender": gender,
                    "state":state,
                    "city": city,
                    "address":address,
                    "category":category,
                    "notes":notes,
                    "facebook":facebook,
                    "instagram":instagram,
                    "twitter":twitter}]
    
    #_______________________________check duplicate______________________________________2
    if df[df["phone_number"]==phone_number].empty == False:

        print("\nThe contact you inputed alreay exist!")
        show_duplikat_database = [item for item in database if phone_number in item["phone_number"]]
        print("Old data :")
        print(tabulate(show_duplikat_database, headers="keys", tablefmt="pipe"))
        print("New inputed data :")
        print(tabulate(inputed_data, headers="keys", tablefmt="pipe"))

        timpa = None
        while True:
            timpa = input("\nDid you want to replace the old data to the new data? (y/n): ")

            if timpa == "y":
                tuple_profil = (email, full_name, nickname, gender, state, city, address, show_duplikat_database[0]["email"])
                tuple_contact = (email, facebook, instagram, twitter, phone_number)
                tuple_category = (category, notes, phone_number)
                update_profil(dict_config, tuple_profil)
                update_contact(dict_config, tuple_contact)
                update_category(dict_config, tuple_category)
                print("Successfully Saved!")
                return
            elif timpa == "n":
                print("Data not replaced!")
                return
            else:
                print("Input invalid!")      

    else:
        try:
                conn = pymysql.connect(**dict_config)
                # print("Connection Success !")
                cursor = conn.cursor() 
                sql_query_profil = """
                            INSERT INTO profil(email, full_name, nickname, gender, state, city, address)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """
                cursor.execute(query=sql_query_profil, args=(email, full_name, nickname, gender, state, city, address))
                sql_query_contact = """
                            INSERT INTO contact(phone_number, email, facebook, instagram, twitter)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                cursor.execute(query=sql_query_contact, args=(phone_number, email, facebook, instagram, twitter))
                sql_query_category = """
                            INSERT INTO category(phone_number, category, notes, last_update)
                            VALUES (%s, %s, %s, NOW())
                            """
                cursor.execute(query=sql_query_category, args=(phone_number, category, notes))

                conn.commit() 
                # return hasil
                print("Contact successfully saved!")
        except Exception as e:
                print("Error !")
                conn.rollback()
                print(f"msg: {e}")
        finally:
                conn.close()