import sqlite3
DEFAULT_PASSWORD = "Password"   #Global string constant for default password assignment
REPORT_TYPE_ALL_CHECKOUTS = 0   #Global integer constants for specifying report types for the generateReport function
REPORT_TYPE_ALL_RETURN_LOGS = 1
REPORT_TYPE_SPECIFIED_USER = 2

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
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly
        return False  #and then notifies that this function call encountered an exception

#Rests the database to its default state
def reset():
    with sqlite3.connect("database.db") as db:  #Connection established to database
        c = db.cursor() #Cursor object created
    c.execute("DROP TABLE IF EXISTS returnLog") #Deletes
    c.execute("DROP TABLE IF EXISTS checkouts") #everything
    c.execute("DROP TABLE IF EXISTS equipment") #in the
    c.execute("DROP TABLE IF EXISTS users")     #database
    c.execute("VACUUM") #Wipes all free space
    db.commit()     #Save all changes made to database
    db.close()      #Close the connection to database
    initialize()    #All of the tables are reinitialized
    addUser(0, "root", "user", 0, 99)   #A root user is created with an ID of 0, the default password, and a permission level of 99

#Adds a new user into the users table
#Arguements userID, nameF, nameL, skills, and permission correspond to the users table columns respectively
#A default password of 'Password' is assigned for the user which they must change
#The user executing this command can not create a new user with permission greater than or equal to theirs
#Returns True if the command runs successfully
#Returns False if an exception occurs
def addUser(userID, nameF, nameL, skills, permission):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    addUserCommand = (" INSERT INTO users VALUES (?, ?, ?, ?, ?, ?) ")  #Row insert command
    try: #Attempts to execute the following SQL commands
        c.execute(addUserCommand, [(userID), (nameF), (nameL), (DEFAULT_PASSWORD), (skills), (permission)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

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
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

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
        user = c.fetchone() #Takes results of select command
        db.close()    #Close the connection to database
        return user   #Return results of select command
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return None   #and then returns None

#Changes any column data for an existing user given their ID number
#Arguements userID, nameF, nameL, skills, and permission correspond to the users table columns respectively
#Columns will only update if given a corresponding arguement
#You may update any selection of columns you wish at once by selecting which arguements to include or omit in the function call
#To reset a users password call this with their ID and the gloabal string constant DEFAULT_PASSWORD
#The user executing this command can not change any data for users with permission greater than or equal to theirs
#Returns True if the command runs successfully
#Returns False if an exception occurs
def updateUser(userID, nameF = None, nameL = None, password = None, skills = None, permission = None):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    updateUserCommand = (" UPDATE users SET nameFirst = ?, nameLast = ?, password = ?, skills = ?, permission = ? WHERE identification = ? ") ##Update user command
    try: #Attempts to execute the following SQL commands
        currentUserData = getUser(userID) #Retrieves current user data to use for any column data that is not given
        newNameF = nameF if nameF != None else currentUserData[1] #Columns will be updated to the arguments given in function call
        newNameL = nameL if nameL != None else currentUserData[2] #If no value is given for a column it will remain as is
        newPassword = password if password != None else currentUserData[3]
        newSkills = skills if skills != None else currentUserData[4]
        newPermission = permission if permission != None else currentUserData[5]
        c.execute(updateUserCommand, [(newNameF), (newNameL), (newPassword), (newSkills), (newPermission), (userID)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

#Adds a new piece of equipment into the equipment table
#Arguements equipID, desc, and skills correspond to the equipment table columns respectively
#This command can only be executed by users with permission >0
#Returns True if the command runs successfully
#Returns False if an exception occurs
def addEquipment(equipID, desc, skills):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    addEquipCommand = (" INSERT INTO equipment VALUES (?, ?, ?) ")  #Add equipment command
    try: #Attempts to execute the following SQL commands
        c.execute(addEquipCommand, [(equipID), (desc), (skills)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

#Removes a piece of equipment from the equipment table
#equipID corresponds to identification column of the equipment table
#This command can only be executed by users with permission >0
#Returns True if the command runs successfully
#Returns False if an exception occurs
def removeEquipment(equipID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    removeEquipCommand = (" DELETE FROM equipment WHERE identification = ? ")  #Remove equipment command
    try: #Attempts to execute the following SQL commands
        c.execute(removeEquipCommand, [(equipID)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

#Gets all data for the equipment with the specified ID
#equipID corresponds to identification column of the equipment table
#Returns all data of specified equipment if the command runs successfully
#Returns None if an exception occurs or no data is found
def getEquipment(equipID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    getEquipCommand = (" SELECT * FROM equipment WHERE identification = ? ")  #Get equipment command
    try: #Attempts to execute the following SQL commands
        c.execute(getEquipCommand, [(equipID)]) #Execute command
        equip = c.fetchone() #Takes results of select command
        db.close()    #Close the connection to database
        return equip  #Return results of select command
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return None   #and then returns None

#Changes any column data for existing equipment given its ID number
#Arguements equipID, desc, and skills correspond to the equipment table columns respectively
#Columns will only update if given a corresponding arguement
#You may update any selection of columns you wish at once by selecting which arguements to include or omit in the function call
#This command can only be executed by users with permission >0
#Returns True if the command runs successfully
#Returns False if an exception occurs
def updateEquipment(equipID, desc = None, skills = None):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    updateEquipCommand = (" UPDATE equipment SET description = ?, skills = ? WHERE identification = ? ")  #Update equipment command
    try: #Attempts to execute the following SQL commands
        currentEquipData = getEquipment(equipID) #Retrieves current user data to use for any column data that is not given
        newDesc = desc if desc != None else currentEquipData[1] #Columns will be updated to the arguments given in function call
        newSkills = skills if skills != None else currentEquipData[2] #If no value is given for a column it will remain as is
        c.execute(updateEquipCommand, [(newDesc), (newSkills), (equipID)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

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
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

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
        checkout = c.fetchone() #Gets select result
        db.close()    #Close the connection to database
        return 0 if checkout == None else 1 #Returns whether an entry was found or not
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return 2      #and then notifies that this function call encountered an exception

#Deletes a specified checkout and enters it into the return logs
#userID and equipID correspond to the identification columns in the users and equipment tables respectively
#Time of checkout is taken from the checkout entry being terminated
#Time of return is set as the current local system time
#Returns True if the command runs successfully
#Returns False if an exception occurs
def returns(userID, equipID):
    with sqlite3.connect("database.db") as db: #Connection established to database
        c = db.cursor() #Cursor object created
    returnCommand1 = (" SELECT checkoutDateTime FROM checkouts WHERE user = ? AND equipment = ? ") #Select DateTime command
    returnCommand2 = (" DELETE FROM checkouts WHERE user = ? AND equipment = ? ")                  #Delete checkout row command
    returnCommand3 = (" INSERT INTO returnLog VALUES (?, ?, ?, datetime('now', 'localtime')) ")    #Insert returnLog row command
    try: #Attempts to execute the following SQL commands
        c.execute(returnCommand1, [(userID), (equipID)]) #Execute command
        checkoutDateTime = c.fetchone()[0] #Get checkout DateTime select result
        c.execute(returnCommand2, [(userID), (equipID)]) #Execute command
        c.execute(returnCommand3, [(userID), (equipID), (checkoutDateTime)]) #Execute command
        db.commit()   #Save all changes made to database
        db.close()    #Close the connection to database
        return True   #Notify that this function call completed successfully
    except Exception: #If an exception occurs
        db.close()    #this ensures the database connection closes properly 
        return False  #and then notifies that this function call encountered an exception

#Generates the specified type of report from the database tables and returns it
#reportType is the type of report to be generated, and should use the global REPORT_TYPE variables
#userID is an optional argument that should be used only when generating a report that requires it
#Returns a tuple with a list entry for every row matching the given report conditions
#Returns None if no data is found or an exception occurs
def generateReport(reportType, userID = None):
    switch = {  #Dictionary containing report queries keyed to the global REPORT_TYPE variables
        REPORT_TYPE_ALL_CHECKOUTS: (""" 
            SELECT nameFirst || ' ' || nameLast AS name, description, checkoutDateTime
            FROM checkouts JOIN users ON users.identification = checkouts.user
                JOIN equipment ON equipment.identification = checkouts.equipment
            ORDER BY checkoutDateTime """),
        REPORT_TYPE_ALL_RETURN_LOGS: ("""
            SELECT nameFirst || ' ' || nameLast AS name, description, checkoutDateTime, returnDateTime
            FROM returnLog JOIN users ON users.identification = returnLog.user
                JOIN equipment ON equipment.identification = returnLog.equipment
            ORDER BY returnDateTime """),
        REPORT_TYPE_SPECIFIED_USER: ("""
            SELECT description, checkoutDateTime, returnDateTime
            FROM returnLog JOIN equipment ON equipment.identification = returnLog.equipment
            WHERE user = ?
            UNION ALL
            SELECT description, checkoutDateTime, 'N/A' 
            FROM checkouts JOIN equipment ON equipment.identification = checkouts.equipment
            WHERE user = ?
            ORDER BY checkoutDateTime """)}
    generateReportCommand = switch.get(reportType, "x") #Selects the proper query from the dictionary
    if generateReportCommand == "x": return None    #If the report type is not in the dictionary function exits and returns None
    with sqlite3.connect("database.db") as db:  #Connection established to database
        c = db.cursor() #Cursor object created
    try:    #Attempts to execute the following SQL commands
        if userID == None: c.execute(generateReportCommand) #Report is assumed to have no arguements if userID is not given
        else: c.execute(generateReportCommand, [(userID), (userID)])    #Report uses userID arguement if it is given
        report = c.fetchall()   #Gets select result
        db.close()      #Close the connection to database
        return report   #Return results of select command
    except Exception:   #If an exception occurs
        db.close()      #this ensures the database connection closes properly 
        return None     #and then returns None