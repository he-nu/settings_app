"""Simple sqlite3 command line interface application for storing and managing settings."""


import sqlite3


connection = sqlite3.connect("settings_app.db")
cursor = connection.cursor()


OPTIONS = (
    "1. Store setting",
    "2. View all settings",
    "3. View setting",
    "4. Change setting",
    "5. Delete setting",
    "6. Exit"
)


def intialise_table() -> None:
    # Alternative
    # cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
           settingId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           setting TEXT NOT NULL,
           value TEXT NOT NULL)
                   """)


def get_all() -> dict:
    """ 
    Function returns a dictionary of the stored settings in the database.
    example = {setting1: value1, setting2: value2}
    """
    all_settings_list = cursor.execute("SELECT * FROM settings").fetchall()
    all_settings_dict = {i[1]:i[2] for i in all_settings_list}

    return all_settings_dict


def prompt_user(options=OPTIONS) -> None:
    """
    Prompts user, returns validated user input.
    """
    print("What do you want to do?\n")
    for option in options:
        print(option)

    user_input = get_user_input()
    return user_input
    

def get_user_input() -> str:
    user_input = input(f"Choose between 1-{len(OPTIONS)}\n")

    while not validate_input(user_input):
        user_input = input(f"Invalid input, please use choose between 1-{len(OPTIONS)}\n")
    
    return user_input


def validate_input(usr_inp:str) -> bool:
    valid_inputs = (str(i) for i in range(1, len(OPTIONS) + 1))
    if usr_inp in valid_inputs:
        return True
    else:
        return False


def store_setting() -> None:
    all_settings = get_all()
    user_setting = input("What is the name of the setting?\n")
    if user_setting in all_settings:
        print(f"Setting for {user_setting} already found. \n")
        print(f"{user_setting}: {all_settings[user_setting]}")
        want_to_change_setting = input("Would you like to change the setting? (y/n): \n")
        if want_to_change_setting == "y":
            change_setting(user_setting)
            return None
        else:
            return None

    user_value = input("What is the value of this setting?\n")
    to_set = {
        "setting": user_setting,
        "value": user_value
    }
    cursor.execute("""INSERT INTO settings (setting, value) VALUES (:setting, :value)""", to_set)
    print(f"{user_setting} set to: {user_value}")


def view_all_settings() -> None:
    all_settings = get_all()
    if all_settings:
        for k, v in all_settings.items():
            print(f"{k}: {v}")
        print("\n")
    else:
        print("No settings stored yet.\n")


def view_setting() -> None:
    setting = input("Select item to view: ")
    cursor.execute("""SELECT * FROM settings WHERE setting = ?""", (setting,))
    settings = get_all()
    if setting in settings:
        print(f"{setting}: {settings[setting]}", "\n")
    else:
        print("Setting not found. Please check again.", "\n")


def get_setting_to_change() -> str:
    all_settings = get_all()
    get_setting = input("What setting would you like to change? ")
    if get_setting in all_settings:
        return get_setting
    else:
        print("\nSetting not found. Please check again.\n")


def change_setting(setting_to_change=None) -> None:
    if setting_to_change:
        get_value = input("What would you like to set the setting to?\n")
        cursor.execute("UPDATE settings SET value = ? WHERE setting = ?", (get_value, setting_to_change,))
        print(f"{setting_to_change} changed to {get_value}\n")
    else:
        setting_to_change = get_setting_to_change()
        if setting_to_change:
            get_value = input("What would you like to set the setting to?\n")
            cursor.execute("UPDATE settings SET value = ? WHERE setting = ?", (get_value, setting_to_change,))

            print(f"{setting_to_change} changed to {get_value}\n")


def delete_setting() -> None:
    settings = get_all()

    to_delete = input("Select item to delete:\n")

    if to_delete in settings:
        cursor.execute("""DELETE FROM settings WHERE setting = ?""", (to_delete,))
        print(f"{to_delete} removed from settings.\n")
    else:
        print(f"Setting not found. Please check again.\n")


def exit_app():
    connection.commit()
    connection.close()
    exit("Good bye!\n")


def main():
    intialise_table()

    response_structure = {
        "1": store_setting,
        "2": view_all_settings,
        "3": view_setting,
        "4": change_setting,
        "5": delete_setting,
        "6": exit_app
    }

    while True:
        user_input = prompt_user()
        # Execute order 66
        print("\n")
        response_structure[user_input]()
        connection.commit()
    

    
if __name__ == "__main__":
    main()