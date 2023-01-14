# Welton Addra
# IMPORTANT COMMENT!!!!:  Before running code, please go to your terminal and type: "pip install "
# The purpose of this program is to allow the users to receive, give and trade resources in times of disaster

import PySimpleGUI as sg
import sqlite3
import random
sg.theme('LightGreen3')

def welcome(LoggedIn):  #Displays the welcoming window and helps the user navigate to the next window
    if LoggedIn:
        c.execute("SELECT Name FROM logIn WHERE Username = ?",[globalUsername])
        name = list(c.fetchone())
        c.execute("SELECT id FROM logIn WHERE Username = ?",[globalUsername])
        iD = list(c.fetchone())
        c.execute("SELECT Zipcode FROM logIn WHERE Username = ?",[globalUsername])
        zipcode = list(c.fetchone())
    else:
        name = ""
        iD = 0
        zipcode = 00000

    layout = [
        [sg.Button("Log in"),sg.Button("Sign in")],
        [sg.Text("Welcome to the resources exchange program!", justification="center")],
        [sg.Text("The purpose of this application is to exchange in case of natural disasters", justification="center")],
        [sg.Text("What would you like to do?", justification="center")],
        [sg.Button("Trade resources", size=(12, 1), mouseover_colors="White"),
         sg.Button("Give resources", size=(12, 1), mouseover_colors="White"),
         sg.Button("Get resources", size=(12, 1), mouseover_colors="White")]
    ]
    window = sg.Window("Resources exchange program", layout, size=(470, 350),grab_anywhere=True)
    while True:
        event, values = window.read()       #The event variable changes depending on what button from the window is pressed
        if event == sg.WIN_CLOSED:
            break
        if event == "Trade resources":
            window.close()
            trade(zipcode,iD,name,LoggedIn)
        elif event == "Give resources":
            window.close()
            giveResources(zipcode,iD,name,LoggedIn)
        elif event == "Get resources":
            window.close()
            getResources(LoggedIn)
        elif event == "Log in":
            window.close()
            logInPage(LoggedIn)
        elif event == "Sign in":
            window.close()
            signInPage(LoggedIn)


def createDataBase():  #Creates a database and tables to store the resources inputted by the user as well as table to store logIn information
    c.execute("""
CREATE TABLE IF NOT EXISTS logIn (
Username TEXT,
Password TEXT,
id INTEGER PRIMARY KEY,
Zipcode INTEGER,
Name TEXT
 );""")

    c.execute("""
CREATE TABLE IF NOT EXISTS GivenResources(
Fullname TEXT,
id INTEGER PRIMARY KEY,
ResourceType TEXT,
Description TEXT,
Zipcode INTEGER );
""")

    c.execute("""
CREATE TABLE IF NOT EXISTS TradeTable(
Fullname TEXT,
id INTEGER PRIMARY KEY,
ResourceType TEXT,
Description TEXT,
Zipcode INTEGER );
""")
    conn.commit()


def signInPage(LoggedIn):      #Allows the user to create an account to save their information
    name = ""
    global globalUsername
    username = ""
    password = ""
    zipcode = 0
    iD = 0
    validEntry = False
    error = ""
    LoggedIn = True
    signInLayout = [
        [sg.Text("Full name"), sg.InputText(key='_Name_')],
        [sg.Text("Zipcode"),sg.InputText(key='_Zipcode_')],
        [sg.Text("Username"),sg.InputText(key='_Username_')],
        [sg.Text("Password"),sg.InputText(key='_Password_')],
        [sg.Button("Enter")]
    ]
    signInWindow = sg.Window("SignIn window",signInLayout,size=(500,300),resizable=True)
    while True:
        event, values = signInWindow.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Enter":
            name = values['_Name_']
            zipcode = values['_Zipcode_']
            globalUsername = values['_Username_']
            password = values['_Password_']
            iD = uniqueID()
            error, invalidEntry = validateSignIn(globalUsername,password)
            if invalidEntry:
                signInWindow.close()
                errorLayout = [
                    [sg.Text(error)],
                    [sg.Button("Try again"),sg.Button("Welcome menu")]
                ]
                errorWindow = sg.Window("Error Window",errorLayout,size=(500,300))
                while True:
                    event2, values2 = errorWindow.read()
                    if event2 == sg.WIN_CLOSED:
                        break
                    if event2 == "Try again":
                        errorWindow.close()
                        signInPage(LoggedIn)
                    if event2 == "Welcome menu":
                        errorWindow.close()
                        welcome(LoggedIn)
            else:
                c.execute("INSERT INTO logIn VALUES (?,?,?,?,?)",(globalUsername,password,zipcode,iD,name))
                conn.commit()
                signInWindow.close()
                loggedIn(zipcode,iD,name,LoggedIn)


def logInPage(LoggedIn):    #Allows users to log in if they have created an account
    username = ""
    password = ""
    validLogIn = False
    logInLayout = [
        [sg.Text("Username"),sg.InputText(key='username')],
        [sg.Text("Password"), sg.InputText(key='password')],
        [sg.Button("Enter")]
    ]
    logInWindow = sg.Window("Log in page",logInLayout,size=(500,300))
    while True:
        event,values = logInWindow.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Enter":  #Saves the values entered by the user when the enter button is pressed
            username = values['username']
            password = values['password']
            logInWindow.close()
            isValidLogIn(username,password,LoggedIn)


def isValidLogIn(username,password,LoggedIn):  #Checks if the username and password are correct
    c.execute("SELECT Username FROM logIn")
    usernames = c.fetchall()    #Stores all the usernames in the logIn table
    found = False
    errorLayout = [
        [sg.Text("Invalid LogIn")],
        [sg.Button("Try again"),sg.Button("Welcome menu")]
    ]
    index = 0
    c.execute("SELECT Password from logIn WHERE Username =?", [username])
    if c.fetchone():
        c.execute("SELECT Password from logIn WHERE Password =?", [password])
        if c.fetchone():
            LoggedIn = True
            global globalUsername
            globalUsername = username
            c.execute("SELECT Name FROM logIn WHERE Username = ?",[username])
            name = str(c.fetchone())
            c.execute("SELECT id FROM logIn WHERE Username = ?",[username])
            iD = str(c.fetchone())
            c.execute("SELECT Zipcode FROM logIn WHERE Username = ?",[username])
            zipcode = str(c.fetchone())
            loggedIn(zipcode,iD,name,LoggedIn)
        else:
            errorWindow = sg.Window("Error Window",errorLayout,size=(150,150))
            while True:
                event, values = errorWindow.read()
                if event == sg.WIN_CLOSED:
                    break
                if event == "Try again":
                    errorWindow.close()
                    logInPage(LoggedIn)
                if event == "Welcome menu":
                    errorWindow.close()
                    welcome(LoggedIn)
                errorWindow = sg.Window("Error Window",errorLayout,size=(150,150))
    else:
        errorWindow = sg.Window("Error Window",errorLayout,size=(200,200))
        while True:
            event, values = errorWindow.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Try again":
                errorWindow.close()
                logInPage(LoggedIn)
            if event == "Welcome menu":
                errorWindow.close()
                welcome(LoggedIn)


def validateSignIn(username,password):      #Input validation for username and password
    error = ""
    tryAgain = False
    if len(username) < 6 or len(password) < 6:
        error = "Your username/password should be at least 6 characters long, please try again."
        tryAgain = True

    elif checkUsername(username):
        error = "This username is already taken, please try again"
        tryAgain = True
    return error,tryAgain


def checkUsername(username):    #checks if the username inputted is already taken
    usernameRepeats = False
    c.execute("SELECT Username FROM logIn")
    allUsernames = c.fetchall()
    for names in allUsernames:
        if names == username:
            usernameRepeats = True
    return usernameRepeats


def loggedIn(zipcode,iD,name,LoggedIn):     #Creates a new window for when users log in or sign in
    LoggedIn = True
    loggedInLayout = [
        [sg.Text("You have successfully logged in! What would you like to do next?")],
        [sg.Button("Trade resources", size=(12, 1), mouseover_colors="White"),
         sg.Button("Give resources", size=(12, 1), mouseover_colors="White"),
         sg.Button("Get resources", size=(12, 1), mouseover_colors="White")],
        [sg.Button("All donations", size=(12, 1), mouseover_colors="White")]
    ]
    loggedInWindow = sg.Window("Logged in window",loggedInLayout, size=(500,200),resizable=True)
    while True:
        event, values = loggedInWindow.read()       #The event variable changes depending on what button from the Window is pressed
        if event == sg.WIN_CLOSED:
            break
        if event == "Trade resources":
            loggedInWindow.close()
            trade(zipcode,iD,name,LoggedIn)
        elif event == "Give resources":
            loggedInWindow.close()
            giveResources(zipcode,iD,name,LoggedIn)
        elif event == "Get resources":
            loggedInWindow.close()
            getResources(LoggedIn)
        elif event == "All donations":
            loggedInWindow.close()
            allDonations(LoggedIn,iD)


def uniqueID():     #Creates a random ID and makes sure that the ID does not repeat
    keepChecking = True
    stopLoop = False
    while keepChecking:
        counter = 0
        countEach = 0   #Counts how many times x is does not equal id
        ID = random.randrange(000000,999999)
        c.execute("SELECT id FROM logIn")
        logInIds = c.fetchall()
        if len(logInIds) == 0:
            logInIds.append(000000)
        c.execute("SELECT id FROM GivenResources")

        givenIds = c.fetchall()
        if len(givenIds) == 0:
            givenIds.append(200002)

        c.execute("SELECT id FROM TradeTable")
        if len(logInIds) == 0:
            logInIds.append(300003)

        tradeIds = c.fetchall()

        while not stopLoop:
            for log in logInIds:
                counter += 1
                if log == ID:
                    stopLoop = True
                elif log != ID:
                    countEach += 1
                if counter == countEach:
                    counter = 0
                    countEach = 0
                    for y in givenIds:
                        counter += 1
                        if y == ID:
                            stopLoop = True
                        elif y != ID:
                            countEach += 1
                        if counter == countEach:
                            counter = 0
                            countEach = 0
                            for z in tradeIds:
                                counter += 1
                                if z == ID:
                                    stopLoop = True
                                elif z != ID:
                                    countEach += 1
                                if counter == countEach:
                                    keepChecking = False
                                    counter = 0
                                    countEach = 0
                                    stopLoop = True
                                    return ID


def strip(Input):
    output = ""
    for each in Input:
        if each != "(" and each != ")" and each != "," and each != "/" and each != "\\" and each != "'":
            output += each
    return output


def allDonations(LoggedIn,iD):
    headings = ["Fullname", "Id", "Resource Type",
                "Description","Zipcode"]  # These are the headers for the table that will display the trade values
    allDonationsLst = []
    c.execute("SELECT * FROM GivenResources WHERE id = ?",iD)
    rows = c.fetchall()
    for row in rows:
        allDonationsLst.append(list(row))

    c.execute("SELECT * FROM TradeTable WHERE id = ?",iD)
    rows = c.fetchall()
    for row in rows:
        allDonationsLst.append(list(row))

    allDonationsLayout = [
        [sg.Table(
            values=allDonationsLst,
            headings=headings,
            max_col_width=35,
            auto_size_columns=True,
            display_row_numbers=True,
            justification='center',
            key='-tradeTable-',
            num_rows=4,
            row_height=35)],
        [sg.Button("Welcome menu")]
    ]
    allDonationsWindow = sg.Window("All donations", allDonationsLayout, size=(500, 300),resizable=True)

    while True:
        event, values = allDonationsWindow.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Welcome menu":
            allDonationsWindow.close()
            welcome(LoggedIn)


def trade(zipcode,iD,name,LoggedIn):    #Creates a window for users trying to trade resources and saves the data into the right table
    if not loggedIn:
        name = ""
        zipcode = 0
    resourceType = ""
    description = ""
    tradeLayout = [  # This window will get inputs from the user and then put them into a table
        [sg.Text("Name"), sg.InputText(key='_Name_')],
        [sg.Text("Description of resource"), sg.InputText(key='_Description_')],
        [sg.Text("Zipcode"),sg.Input(key='_Zipcode_')],
        [sg.Text("Resource Type"),
         sg.Radio("Housing", "resourceType", default=True, key='_Housing_'),
         sg.Radio("Food", "resourceType", default=False),
         sg.Radio("Clothing", "resourceType", default=False),
         sg.Radio("Other", "resourceType", default=False)],
        [sg.Button("Go back"), sg.Button("Next")]
    ]
    tradeLayoutLoggedIn = [  # This window will get inputs from the user and then put them into a table
        [sg.Text("Description of resource"), sg.InputText(key='_Description_')],
        [sg.Text("Resource Type"),
         sg.Radio("Housing", "resourceType", default=True, key='_Housing_'),
         sg.Radio("Food", "resourceType", default=False),
         sg.Radio("Clothing", "resourceType", default=False),
         sg.Radio("Other", "resourceType", default=False)],
        [sg.Button("Go back"), sg.Button("Next")]
    ]

    if not loggedIn:
        tradeWindow = sg.Window("Give resources", tradeLayout, size=(700, 500),resizable=True)
        while True:
            event, values = tradeWindow.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Go back":
                tradeWindow.close()
                welcome(LoggedIn)
            if values['_Housing_'] == "Housing":
                resourceType = "Housing"
            elif values[0]:
                resourceType = "Food"
            elif values[1]:
                resourceType = "Clothing"
            elif values[2]:
                resourceType = "Other"
            if event == "Next":
                name = str(values['_Name_'])
                description = str(values['_Description_'])
                zipcode = values['_Zipcode_']
                iD = uniqueID()
                iD = int(strip(iD))
                name = str(strip(name))
                zipcode = int(strip(zipcode))
                c.execute("INSERT INTO TradeTable VALUES (?,?,?,?,?)", (name, iD, resourceType, description,zipcode))
                conn.commit()
                tradeWindow.close()
                thankYouForDonation(LoggedIn)
    else:
        tradeWindowLoggedIn = sg.Window("Give resources", tradeLayoutLoggedIn, size=(700, 500),resizable=True)
        while True:
            event, values = tradeWindowLoggedIn.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Go back":
                tradeWindowLoggedIn.close()
                welcome(LoggedIn)
            if values['_Housing_'] == "Housing":
                resourceType = "Housing"
            elif values[0]:
                resourceType = "Food"
            elif values[1]:
                resourceType = "Clothing"
            elif values[2]:
                resourceType = "Other"
            if event == "Next":
                description = str(values['_Description_'])
                c.execute("INSERT INTO TradeTable VALUES (?,?,?,?,?)", (name, iD, resourceType, description,zipcode))
                conn.commit()
                tradeWindowLoggedIn.close()
                thankYouForDonation(LoggedIn)


def tradeTable(LoggedIn):   #Displays a window of all the trade values inputted by users
    headings = ["Fullname", "Id", "Resource Type",
                "Description","Zipcode"]  # These are the headers for the table that will display the trade values
    tradeTableLst = []
    c.execute("SELECT * FROM TradeTable")
    rows = c.fetchall()
    for row in rows:
        tradeTableLst.append(list(row))

    tableLayout = [
        [sg.Table(
            values=tradeTableLst,
            headings=headings,
            max_col_width=35,
            auto_size_columns=True,
            display_row_numbers=True,
            justification='right',
            key='-tradeTable-',
            num_rows=4,
            row_height=35)],
        [sg.Text("Enter the row number of the person you would like to trade with.")],
        [sg.Input(key="_ID_"), sg.Button("Enter")]
    ]
    tableWindow = sg.Window("Trade table", tableLayout, size=(700, 700),resizable=True)

    while True:
        event, values = tableWindow.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Enter":
            tableWindow.close()
            backToWelcome(LoggedIn)


def giveResources(zipcode,iD,name,LoggedIn):  #Shows a window that allows users to give resources and stores that information into the appropriate table
    if not LoggedIn:
        name = ""
        zipcode = 0
    resourceType = ""
    description = ""
    giveResourcesLayout = [  # This window will get inputs from the user and then put them into a table
        [sg.Text("Name"), sg.InputText(key='_Name_')],
        [sg.Text("Description of resource"), sg.InputText(key='_Description_')],
        [sg.Text("Zipcode"),sg.Input(key='_Zipcode_')],
        [sg.Text("Resource Type"),
         sg.Radio("Housing", "resourceType", default=True, key='_Housing_'),
         sg.Radio("Food", "resourceType", default=False),
         sg.Radio("Clothing", "resourceType", default=False),
         sg.Radio("Other", "resourceType", default=False)],
        [sg.Button("Go back"), sg.Button("Next")]
    ]
    giveResourcesLayoutLoggedIn = [  # This window will get inputs from the user and then put them into a table
        [sg.Text("Description of resource"), sg.InputText(key='_Description_')],
        [sg.Text("Resource Type"),
         sg.Radio("Housing", "resourceType", default=True, key='_Housing_'),
         sg.Radio("Food", "resourceType", default=False),
         sg.Radio("Clothing", "resourceType", default=False),
         sg.Radio("Other", "resourceType", default=False)],
        [sg.Button("Go back"), sg.Button("Next")]
    ]

    if not LoggedIn:
        giveTableWindow = sg.Window("Give resources", giveResourcesLayout, size=(700, 500),resizable=True)
        while True:
            event, values = giveTableWindow.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Go back":
                giveTableWindow.close()
                welcome(LoggedIn)
            if values['_Housing_'] == "Housing":
                resourceType = "Housing"
            elif values[0]:
                resourceType = "Food"
            elif values[1]:
                resourceType = "Clothing"
            elif values[2]:
                resourceType = "Other"
            if event == "Next":
                name = str(values['_Name_'])
                description = str(values['_Description_'])
                zipcode = values['_Zipcode_']
                Id = uniqueID()
                c.execute("INSERT INTO GivenResources VALUES (?,?,?,?,?)", (name, iD, resourceType, description,zipcode))
                conn.commit()
                giveTableWindow.close()
                thankYouForDonation(LoggedIn)
    else:
        giveTableWindowLoggedIn = sg.Window("Give resources", giveResourcesLayoutLoggedIn, size=(700, 500),resizable=True)
        while True:
            event, values = giveTableWindowLoggedIn.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Go back":
                giveTableWindowLoggedIn.close()
                welcome(LoggedIn)
            if values['_Housing_'] == "Housing":
                resourceType = "Housing"
            elif values[0]:
                resourceType = "Food"
            elif values[1]:
                resourceType = "Clothing"
            elif values[2]:
                resourceType = "Other"
            if event == "Next":
                description = str(values['_Description_'])
                iD = int(strip(iD))
                name = str(strip(name))
                zipcode = int(strip(zipcode))
                c.execute("INSERT INTO GivenResources VALUES (?,?,?,?,?)", (name, iD, resourceType, description,zipcode))
                conn.commit()
                giveTableWindowLoggedIn.close()
                thankYouForDonation(LoggedIn)


def getResources(LoggedIn):     #Displays all the values in the give resources table so the user can pick what resources they need
    headings = ["Full name", "Id", "Resource Type",
                "Description","Zipcode"]  # These are the headers for the table that will display the trade values
    getResourcesTable = []
    c.execute("SELECT * FROM GivenResources")
    getResourcesRows = c.fetchall()
    for row in getResourcesRows:
        getResourcesTable.append(list(row))

    tableLayout = [
        [sg.Table(
            values=getResourcesTable,
            headings=headings,
            max_col_width=35,
            auto_size_columns=True,
            display_row_numbers=True,
            justification='right',
            key='-tradeTable-',
            num_rows=4,
            row_height=35)],
        [sg.Text("Enter the row number of the resource you would like to receive")],
        [sg.Input(key="_ID_"), sg.Button("Enpter")]
    ]
    tableWindow = sg.Window("Resources table", tableLayout, size=(700, 700))

    while True:
        event, values = tableWindow.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Enter":
            tableWindow.close()
            backToWelcome(LoggedIn=LoggedIn)


def backToWelcome(LoggedIn):
    lastLayout = [
        [sg.Text("Thank you for your contribution!")],
        [sg.Text("Please enter your contact information so we can contact you."), sg.Input()],
        [sg.Button("Welcome menu")]
    ]
    lastWindow = sg.Window("Last window", lastLayout, size=(500, 300))
    while True:
        event, values = lastWindow.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Welcome menu":
            lastWindow.close()
            welcome(LoggedIn)


def thankYouForDonation(LoggedIn):
    thankYouLayout = [
        [sg.Text("Thank you so much for your donation!")],
        [sg.Button("Welcome Window")]
    ]
    thankYouWindow = sg.Window("Thank you for your donation", thankYouLayout, size=(350, 200))
    while True:
        event, values = thankYouWindow.read()
        if event == "Welcome Window":
            thankYouWindow.close()
            welcome(LoggedIn=LoggedIn)


if __name__ == '__main__':
    isLoggedIn = False
    global conn
    conn = sqlite3.connect('Resources.db')
    global c
    c = conn.cursor()
    createDataBase()
    welcome(isLoggedIn)
