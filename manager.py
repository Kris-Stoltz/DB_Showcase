import json
import os.path
from tabulate import tabulate


def numerical_options(options):
    for index, item in enumerate(options):
        print(f'{index + 1}) {item}')  # dynamically creates a number and description for each option

    while True:  # a loop that makes sure the user input is valid, in this case a number displayed in the options
        user_input = input('>> ')
        try:
            int(user_input)
        except ValueError:
            print(f'{user_input} is not a valid integer. Please select a valid integer.')
        else:
            if int(user_input) == 0 or int(user_input) > len(options):
                print('The option you have selected does not exist.')
            else:
                break

    return int(user_input)  # returns the user input after converting it to an integer


def boolean_options(prompt):
    while True:  # a loop that makes sure the user input is valid, in this case either y or n
        user_input = input(prompt)
        if user_input.lower() == 'y' or user_input.lower() == 'n':
            break
        else:
            print('Please select either Y or N.')

    return user_input


def display_menu():
    # displays the main menu of the application
    print('\033[1m' + 'Menu' + '\033[0m')
    return numerical_options(['Display Database', 'Sort Database', 'Add User', 'Delete User', 'Edit User', 'Quit'])


class Manager:

    def __init__(self):
        if not os.path.exists("db.json"):
            with open("db.json", "w+") as db:  # creates database file if it does not exist
                init = {'entries': []}  # creates the "entries" array in the json object
                json.dump(init, db, indent=2)
        with open('db.json') as db:
            self.db = json.load(db)
            self.data = self.db['entries']
        self.sort_opt = ['firstname', 'lastname', 'number']
        self.sort = 0  # holds a value as an index position for sort_opt
        self.data = sorted(self.data, key=lambda x: x[self.sort_opt[self.sort]])  # initially sorts the database

    def add_user(self):
        print('\033[1m' + 'Add User' + '\033[0m')

        name = input('Firstname: ')
        surname = input('Lastname: ')
        number = input('Number: ')

        new_entry = {
            'firstname': name,
            'lastname': surname,
            'number': number
        }

        self.db['entries'].append(new_entry)  # updates the database variable with all the entries

        with open('db.json', 'w') as new_db:
            json.dump(self.db, new_db, indent=2)  # updates the actual json file

        self.data = sorted(self.data, key=lambda x: x[self.sort_opt[self.sort]])  # sorts the database again

    def delete_user(self):
        print('\033[1m' + 'Delete User' + '\033[0m')
        options = [f'{user["firstname"]}, {user["lastname"]} - {user["number"]}' for user in self.data]
        options.append('Cancel')  # displays users to deletes and adds "cancel" as one of the options
        selection = numerical_options(options)

        if selection == len(options):
            display_menu()  # checks if cancel was selected
        else:
            confirm = boolean_options(
                f'Are you sure you want to delete {self.data[selection - 1]["firstname"]} '
                f'{self.data[selection - 1]["lastname"]}? This action cannot be undone. (Y/N) '
            )  # creates the confirmation question
            if confirm.lower() == 'y':
                del self.data[selection - 1]
                self.db['entries'] = self.data  # deletes the user from the data and updates the database
                with open('db.json', 'w') as new_db:  # updates the actual database file
                    json.dump(self.db, new_db, indent=2)

    def display_db(self):
        users = [[user[self.sort_opt[0]], user[self.sort_opt[1]], user[self.sort_opt[2]]] for user in self.data]
        # creates a list of all the users from the database, sorted by name, surname and number to pass into tabulate ^
        print('\033[1m' + f'Database, sorted by {self.sort_opt[self.sort]}' + '\033[0m')
        print(tabulate(users, headers=['Firstname', 'Lastname', 'Number'], tablefmt='fancy_grid'))

    def edit_user(self):
        print('\033[1m' + 'Edit User' + '\033[0m')
        print('Which user would you like to edit?')
        options = [f'{user["firstname"]}, {user["lastname"]} - {user["number"]}' for user in self.data]
        # Puts user in an array so that they can be displayed as options to select
        selected_user = numerical_options(options) - 1

        name = self.data[selected_user]['firstname']
        lastname = self.data[selected_user]['lastname']
        number = self.data[selected_user]['number']

        while True:
            print('\033[1m' + name + ' ' + lastname + ' - ' + number + '\033[0m')  # shows user including all changes
            selection = numerical_options(['Firstname', 'Lastname', 'Number', 'Save', 'Cancel'])

            if selection == 1:
                name = input('Enter a new name. ')
            elif selection == 2:
                lastname = input('Enter a new lastname. ')
            elif selection == 3:
                number = input('Enter a new number. ')
            elif selection == 4:
                save = boolean_options('Do you want to save? (Y/N) ')
                if save.lower() == 'y':
                    self.data[selected_user]['firstname'] = name
                    self.data[selected_user]['lastname'] = lastname
                    self.data[selected_user]['number'] = number

                    self.db['entries'] = self.data

                    with open('db.json', 'w') as new_db:
                        json.dump(self.db, new_db, indent=2)  # saves all changes made to the user and updates file
                    break
            else:
                cancel = boolean_options('Are you sure you want to cancel? All changes made will be lost. (Y/N) ')
                if cancel.lower() == 'y':  # asks user whether they want to cancel the edit
                    break

    def sort_db(self):
        print('\033[1m' + 'Sort Database' + '\033[0m')
        print('How would you like to sort the database?')
        self.sort = numerical_options(['Firstname', 'Lastname', 'Number']) - 1

        self.data = sorted(self.data, key=lambda x: x[self.sort_opt[self.sort]])
        self.display_db()
