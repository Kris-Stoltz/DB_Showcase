from manager import *

DBM = Manager()  # initialising the class

app_on = True
while app_on:
    selection = display_menu()  # displaying the main menu as long as the app is running

    if selection == 1:  # executing the correct method dependent on user selection
        DBM.display_db()
    elif selection == 2:
        DBM.sort_db()
    elif selection == 3:
        DBM.add_user()
    elif selection == 4:
        DBM.delete_user()
    elif selection == 5:
        DBM.edit_user()
    else:
        app_on = False

