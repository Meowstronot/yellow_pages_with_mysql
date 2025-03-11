# **Yellow Pages: Your Personal Contact Manager**

Yellow Pages is a powerful yet simple phonebook application that helps you manage your contacts efficiently. With full CRUD functionality, you can easily add, search, update, and delete contact information—just like your own digital Rolodex! 🚀

## Business Understanding
Yellow Pages is a personal contact management application designed to help individuals store, organize, and manage their phone contacts efficiently. In today's digital age, where people handle numerous contacts daily, having a structured and easily accessible phonebook is essential for better communication and organization.


**Benefits:**
* **Effortless Contact Management** ✅ – Easily store, update, and organize phone contacts in one place.
* **Enhanced Organization** ✅ – Keep your contacts structured for quick and easy access.
* **Full CRUD Functionality** ✅ – Create, read, update, and delete contacts with ease.
* **Time & Energy Efficiency** ✅ – Say goodbye to messy contact lists and manual tracking!

**Target Users:**
* **Individuals with large contact lists –** Manage personal and professional contacts effortlessly.
* **Small to medium-sized business owners** – Keep track of customers, suppliers, and partners.
* **Anyone who values organized contact storage** – Never lose important numbers again!


## Features

* **Create:**
    * Add new contact information entries with essential details like phone number, email, name, address, and other relevant details.
    * Implement data validation to ensure correct formatting and prevent duplicates.
* **Read:**
    - Display a comprehensive list of saved contacts.
    - Provides detailed information of phone contacts, including phone number, email address, name, and other relevant details.
    - Search contacts quickly by phone number for easy access.
* **Update:**
    * Modify existing contact details to keep information up to date.
    * Provide clear confirmation or error messages based on update success or failure.
* **Delete:**
    * Allow for the removal of unwanted Contact Information records with appropriate authorization checks.
    * Soft delete functionality prevents accidental data loss.
    * Recycle Bin feature allows easy recovery of deleted contacts.

## Installation

1. **Requiments:**
    * Python version 3.12  or later
    * MySQL workbench 8.0.40 or later

2. **Installation:**
    ```bash
    git clone https://github.com/Meowstronot/yellow_pages_with_mysql.git
    cd yellow_pages_with_mysql
    pip install -r requirements.txt 
    ```
3. **MySQL Preparation**
    - a. Open and login MySQL Workbench on your computer 
    - b. Go to File → Open SQL Script 
    - c. Find and Select file ```yellow_pages_schema.sql```  
    - d. Click the icon⚡Execute (Run Current SQL Script)  or press (Ctrl + Shift + Enter)
    - e. Wait until the execution process is complete. 

## Usage

1. **Run the application:**
    ```bash
    cd yellow_pages_with_mysql
    python main.py
    ```

2. **Menu Descriptions & Functions:**
    * 1️⃣**Show Contact Data** – Displays the list of all saved contacts, including names, phone numbers, and other details.
    * 2️⃣**Find Contact:** Allows users to search for a specific contact based on various criteria such as phone number, name, or email..
    * 3️⃣ **Add Contact:** Enables users to add new contact information, including name, phone number, email, and address.
    * 4️⃣ **Update Contact Data:** Provides an option to modify existing contact details, ensuring the information stays up to date.
    * 5️⃣ **Delete Contact Data** – Allows users to remove unwanted or outdated contacts. Supports soft delete, so data can be recovered if needed.
    * 6️⃣ **Recycle Bin** – Stores deleted contacts temporarily, giving users the ability to restore them before permanent deletion.
    * 7️⃣ **Reset Info Login** – Resets MySQL login credentials if the connection settings need to be changed.
    * 8️⃣ **Exit Program** – Closes the application safely and ends the session.

## Other Information
1. **Table MySQL**
    * `profil` <br>
    This table contains personal details of individuals stored in the contact list.
        |Column|	Data Type|	Description|
        --- | --- | --- |
        |email|VARCHAR(50) (PK)|Primary key, unique email identifier for each profile.|
        |full_name|VARCHAR(50)|Full name of the contact.|
        |nickname|VARCHAR(50)|Nickname of the contact (optional).|
        |gender|ENUM('Male', 'Female')|Gender of the contact (Male or Female).|
        |state|VARCHAR(50)|State where the contact resides.|
        |city|VARCHAR(50)|City where the contact resides.|
        |address|VARCHAR(50)|Full address of the contact (optional).|

    * `contact` <br>
    This table holds contact details, linking phone numbers to emails from the `profil` table.
        |Column|	Data Type|	Description|
        --- | --- | --- |
        |phone_number|VARCHAR(13) (PK)|Primary key, unique phone |number identifier.
        |email|VARCHAR(50) (FK)|Foreign key referencing `profil(email)`, ensuring each contact is linked to a profile.
        |facebook|VARCHAR(50)|Facebook username or profile link (optional).
        |instagram|VARCHAR(50)|Instagram handle (optional).
        |twitter|VARCHAR(50)|Twitter handle (optional).

        Cascade Rules:
        - If a profile is deleted, all associated contact records are also deleted (ON DELETE CASCADE).
        - If an email is updated in `profil`, it automatically updates in `contact` (ON UPDATE CASCADE).
    * `category` <br>
    This table classifies contacts into categories and keeps track of updates.
        |Column|	Data Type|	Description|
        --- | --- | --- |
        phone_number|VARCHAR(13) (PK)|Primary key, references contact(phone_number).
        category|VARCHAR(50)|Category of the contact (e.g., Family, Work, Friend).
        notes|VARCHAR(50)|Additional notes about the contact (optional).
        last_update|DATETIME|Timestamp of the last update.

        Cascade Rules:
        - If a phone number is deleted from `contact`, it is also removed from `category` (ON DELETE CASCADE).
        - If a phone number is updated, it updates automatically here (ON UPDATE CASCADE).
    * `recycle_bin` <br>
    This table serves as a temporary storage for deleted contacts before they are permanently removed.

2. **Relational Database (RDB)**
This project uses a relational model to organize and manage data, with interrelated tables as shown below
![screenshot][def]

## Contributing
I'm welcoming contributions to this project! Please feel free to open a pull request, send an email to shinaruikhisan@gmail.com, or submit an issue if you encounter any problems or have suggestions for improvements.



<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://www.linkedin.com/in/muhammad-khisanul-fakhrudin-akbar-3899ba220/">
          <img src="https://i.sstatic.net/gVE0j.png" width="20"/><br>
          <strong>LinkedIn</strong>
        </a>
      </td>
      <td width="50">&nbsp;</td> <!-- Memberikan jarak antar ikon -->
      <td align="center">
        <a href="https://github.com/Meowstronot">
          <img src="https://i.sstatic.net/tskMh.png" width="20"/><br>
          <strong>GitHub</strong>
        </a>
      </td>
    </tr>
  </table>
</div>

---



[def]: Relational_Database.jpg