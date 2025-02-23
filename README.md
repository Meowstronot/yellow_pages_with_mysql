# Yellow Pages Python CRUD Application for Personal Use

Yellow Pages is a personal phonebook application that allows users to perform CRUD operations on phone contact information

## Business Understanding

The Yellow Pages application is designed to assist individuals in managing and storing phone contact information. In today's digital era, many people have numerous phone contacts that need to be stored and organized.


**Benefits:**

* Convenience in managing and storing phone contact information
* Better organization in managing phone contacts
* Ability to create, read, update, and delete (CRUD) phone contact information
* Time and energy savings in managing phone contacts

**Target Users:**

The target user of the Yellow Pages application is individuals who need to manage and store phone contact information. This target user group may include:

- Individuals with numerous phone contacts
- Small to medium-sized business owners
- Individuals who need to manage and store phone contact information


## Features

* **Create:**
    * Add new contact information entries with essential details like phone number, email, name, address, and other relevant details.
    * Implement validation rules to ensure data integrity (if applicable, e.g., unique identifiers, data type checks).
* **Read:**
    - Presents a comprehensive list of stored phone contacts
    - Provides detailed information of phone contacts, including phone number, email address, name, and other relevant details
    - Facilitates users' search for specific phone contact data by phone number.
* **Update:**
    * Modify existing contact information to reflect changes in selected column.
    * Provide clear confirmation or error messages based on update success or failure.
* **Delete:**
    * Allow for the removal of unwanted Contact Information records with appropriate authorization checks.
    * Implement soft delete functionality to prevent permanent data loss.
    * Recycle Bin feature to restore contact information

## Installation

1. **Prerequisites:**
    * Python version 3.12  or later
    * `pip install tabulate`  # to show table of data

2. **Installation:**
    ```bash
    git clone https://github.com/Meowstronot/yellow_pages_crud_program.git
    cd yellow_pages_crud_program
    pip install -r requirements.txt  # If using a requirements.txt file
    ```

## Usage

1. **Run the application:**
    ```bash
    python main.py
    ```

2. **CRUD Operations:**
    * **Create:** Add a new Contact information providing necessary details like phone number, email, name, gender, address.
    * **Read:** Search and retrieve contact information by phone number, name, or address.
    * **Update:** Modify Contact details, such as updating their name, email or address details.
    * **Delete:** Implement soft delete functionality to prevent permanent data loss.


## Contributing
We welcome contributions to this project! Please feel free to open a pull request, sent to shinaruikhisan@gmail.com or submit an issue if you encounter any problems or have suggestions for improvements.
