#%% This line is for enabling interactive python in VSCode
import sqlite3

#%% This line is for enabling interactive python in VSCode
#Creates the database with all proper tables, columns, and constraints
#Returns True if the initialization runs successfully
#Returns False if an exception occurs
def initialize():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    try: #Attempts to execute the following SQL commands
        #users table holds data relevant to employees and managers
        #dentification is the number that uniquely identifies an employee for all company systems
        #nameFirst and nameLast are self explanatory
        #password stores 96 bytes of authentication data. The first 32 bytes are the salt, and the last 64 the key
        #skills allows you to constrain certain equipment checkouts to only users with matching skill numbers
        #permission determines if the user has employee or manager status. Employees have permission 0. Managers have permission >0
        #Managers can only make changes to users with a lower permission number than them
        #Managers can not change a users permission to be equal to or greater than theirs
        c.execute(""" CREATE TABLE IF NOT EXISTS users (
            identification INTEGER PRIMARY KEY ,
            nameFirst TEXT NOT NULL ,
            nameLast TEXT NOT NULL ,
            password TEXT NOT NULL ,
            skills INTEGER NOT NULL ,
            permission INTEGER NOT NULL )
            WITHOUT ROWID """)
        #equipment table holds data relevant to items in the equipment depot which can be checked out
        #identification is the number that uniquely identifies a piece of equipment from other similar equipment
        #description gives a text explanation of what the equipment is
        #skills allows you to constrain certain equipment checkouts to only users with matching skill numbers
        c.execute(""" CREATE TABLE IF NOT EXISTS equipment (
            identification INTEGER PRIMARY KEY ,
            description TEXT NOT NULL ,
            skills INTEGER NOT NULL )
            WITHOUT ROWID """)
        #checkouts binds together a user and equipment for a period of time while they are in possession and responsible for it
        #user is linked to the identification column of the users table
        #equipment is linked to the identification column of the equipment table
        #checkoutDateTime stores the exact time the entry was created
        #This tables unique identifier is a combination of the user and equipment identification numbers
        #Any changes made to users or equipment entries will also apply to any relevant entries in this table
        c.execute(""" CREATE TABLE IF NOT EXISTS checkouts (
            user INTEGER ,
            equipment INTEGER UNIQUE ,
            checkoutDateTime TEXT NOT NULL ,
            PRIMARY KEY (user, equipment) ,
            FOREIGN KEY (user) REFERENCES users (identification) ON DELETE CASCADE ON UPDATE CASCADE ,
            FOREIGN KEY (equipment) REFERENCES equipment (identification) ON DELETE CASCADE ON UPDATE CASCADE )
            WITHOUT ROWID """)
        #returnLog holds a permanent record of all concluded user checkouts. When checkouts end they are automatically moved here
        #user is linked to the identification column of the users table
        #equipment is linked to the identification column of the equipment table
        #checkoutDateTime stores the exact time the prior checkout entry was created
        #returnDateTime stores the exact time the entry was created
        #This tables unique identifier is the implicit rowid column in sqlite3
        #Any changes made to users or equipment entries will also apply to any relevant entries in this table
        c.execute(""" CREATE TABLE IF NOT EXISTS returnLog (
            user INTEGER NOT NULL ,
            equipment INTEGER NOT NULL ,
            checkoutDateTime TEXT NOT NULL ,
            returnDateTime TEXT NOT NULL ,
            FOREIGN KEY (user) REFERENCES users (identification) ON DELETE CASCADE ON UPDATE CASCADE ,
            FOREIGN KEY (equipment) REFERENCES equipment (identification) ON DELETE CASCADE ON UPDATE CASCADE )""")
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Database Created Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Creating Database")
        return False  #and then notifies that this function call encountered an exception
initialize()

#%% This line is for enabling interactive python in VSCode
#Adds a new user into the users table
#Arguements userID, nameF, nameL, skills, and permission correspond to the users table columns respectively
#A default password is assigned for the user which they must change
#The user executing this command can not create a new user with permission greater than or equal to theirs
#Returns True if the command runs successfully
#Returns False if an exception occurs
def addUser(userID, nameF, nameL, skills, permission):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    defaultPassword = "Password"    #Default assigned password to be changed by user
    addUserCommand = (" INSERT INTO users VALUES (?, ?, ?, ?, ?, ?) ")  #Row insert command
    try: #Attempts to execute the following SQL commands
        c.execute(addUserCommand, [(userID), (nameF), (nameL), (defaultPassword), (skills), (permission)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception
addUser(0, "Bryan", "Mirra", 0, 0)

#%% This line is for enabling interactive python in VSCode
#Removes a user from the users table
#userID corresponds to identification column of the users table
#The user executing this command can not delete a user with permission greater than or equal to theirs
#Returns True if the command runs successfully
#Returns False if an exception occurs
def removeUser(userID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    removeUserCommand = (" DELETE FROM users WHERE identification = ? ") #Row delete command
    try: #Attempts to execute the following SQL commands
        c.execute(removeUserCommand, [(userID)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception
removeUser(0)

#%% This line is for enabling interactive python in VSCode
#Gets all data for the user with the specified ID
#userID corresponds to identification column of the users table
#Returns all data of specified user if the command runs successfully
#Returns None if an exception occurs
def getUser(userID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    getUserCommand = (" SELECT * FROM users WHERE identification = ? ") #User select command
    try: #Attempts to execute the following SQL commands
        c.execute(getUserCommand, [(userID)]) #Execute command
        user = c.fetchall() #Takes results of select command
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return user   #Return results of select command
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return None   #and then returns None
getUser(0)

#%% This line is for enabling interactive python in VSCode
# TODO: THIS
def changePassword(userID, password):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def resetPassword(userID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def changeNameF():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def changeNameL():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def changeSkillsUser():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def changePermission():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def addEquipment():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def removeEquipment():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def getEquipment():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def changeDescription():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: THIS
def changeSkillsEquipment():
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    Command = ("")  #command
    try: #Attempts to execute the following SQL commands
        c.execute(Command, []) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

#%% This line is for enabling interactive python in VSCode
#Creates a new checkout for a user and a piece of equipment
#userID and equipID correspond to the identification columns in the users and equipment tables respectively
#Time of checkout is set as the current local system time
#Returns True if the command runs successfully
#Returns False if an exception occurs
def checkout(userID, equipID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    checkoutCommand = (" INSERT INTO checkouts VALUES (?, ?, datetime('now', 'localtime')) ") #Row insert command
    try: #Attempts to execute the following SQL commands
        c.execute(checkoutCommand, [(userID), (equipID)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

#%% This line is for enabling interactive python in VSCode
#Checks whether a piece of equipment is checked out by anyone or by a specified user
#If only given an equipment ID it will check if any user has it checked out
#If given both an equipment ID and user ID it will check if the specified user has it checked out
#Returns 0 (False) if the check did not find any results
#Returns 1 (True) if the check found a result
#Returns 2 if this function encountered an exception
def isCheckedOut(equipID, userID = None):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    isCheckoutCommand = (" SELECT * FROM checkouts WHERE equipment = ? ") if userID == None else (" SELECT * FROM checkouts WHERE user = ? AND equipment = ? ") #Select command
    try: #Attempts to execute the following SQL commands
        c.execute(isCheckoutCommand, [(equipID)] if userID == None else [(userID), (equipID)]) #Execute command
        checkout = c.fetchall() #Gets select result
        db.close()  #Close the connection to database
        print("Command Executed Successfully")
        return 0 if checkout == None else 1 #Returns whether an entry was found or not
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return 2      #and then notifies that this function call encountered an exception

#%% This line is for enabling interactive python in VSCode
# TODO: WRITE COMMENT
def returns(userID, equipID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    returnCommand1 = (" SELECT checkoutDateTime FROM checkouts WHERE user = ? AND equipment = ? ") #Select DateTime command
    returnCommand2 = (" DELETE FROM checkouts WHERE user = ? AND equipment = ? ")                  #Delete checkout row command
    returnCommand3 = (" INSERT INTO returnLog VALUES (?, ?, ?, datetime('now', 'localtime')) ")    #Insert returnLog row command
    try: #Attempts to execute the following SQL commands
        c.execute(returnCommand1, [(userID), (equipID)]) #Execute command
        checkoutDateTime = c.fetchall() #Get checkout DateTime select result
        c.execute(returnCommand2, [(userID), (equipID)]) #Execute command
        c.execute(returnCommand3, [(userID), (equipID), (checkoutDateTime)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        print("Command Executed Successfully")
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        print("Error Executing Command")
        return False  #and then notifies that this function call encountered an exception

# TODO: FUNCTIONS FOR GENERATING REPORTS