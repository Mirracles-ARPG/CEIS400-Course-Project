import db_conn, os, hashlib

#EMPLOYEE MENU CODE
def employeeMenu():
    print("--- Employee Menu ---\n")
    print("What would you like to do?")
    print("1. Check-out Equipment")
    print("2. Return Equipment")
    print("3. View Your Equipment Records")
    print("4. Track New Equipment Orders")
    print("5. Log Out\n")
    while True:
        userChoice = input("Enter a menu option: ")
        if userChoice == '1':
            equipID = input("\nEnter Equipment ID Number to check-out: ")
            checkout(userID, equipID)
            print("\nThis item has now been checked-out.\n\n")
            continue
        elif userChoice == '2':
            equipID = input("\nEnter Equipment ID Number to check-in: ")
            returns(userID, equipID)
            print("\nThis item has now been returned.\n\n")
            continue
        elif userChoice == '3':
            print("\nYour Equipment Records:")
            getUser(userID)
            print()
            continue
        elif userChoice == '4':
            print("\nAll New Equipment Orders:")
            generateReport(reportType, userID = None)
            print()
            continue
        elif userChoice == '5':
            cont = input("\nLog Out? (y/n): ").lower()
            while True:
                if cont == "y":
                    print("\nSuccessfully logged out.\n\n")
                    main()
                elif cont == "n":
                    print()
                    employeeMenu()
            


#MANAGER MENU CODE
def managerMenu():
    print("--- Manager Menu ---\n")
    print("What would you like to do?")
    print("1. Full Employee Equipment Report")
    print("2. Employee Information")
    print("3. Equipment Information")
    print("4. Checked-out Equipment Status")
    print("5. Update an Existing User")
    print("6. Add a New User")
    print("7. Remove a User")
    print("8. Update Existing Equipment")
    print("9. Add Equipment")
    print("10. Remove Equipment")
    print("11. Log Out\n")
    while True:
        userChoice = input("Enter a menu option: ")
        if userChoice == '1':
            print("\nFull Employee Equipment Report")
            generateReport(reportType, userID = None)
            continue
        elif userChoice == '2':
            print("\nEmployee Information")
            userID = input("\nEnter specific user ID: ")
            getUser(userID)
            continue
        elif userChoice == '3':
            print("\nEquipment Information")
            equipID = input("\nEnter the Equipment ID: ")
            getEquipment(equipID)
            continue
        elif userChoice == '4':
            print("\nChecked-out Equipment Status")
            equipID = input("\nEnter the Equipment ID: ")
            isCheckedOut(equip)
            continue
        elif userChoice == '5':
            print("\nUpdate Existing User\n")
            updateUser()
            continue
        elif userChoice == '6':
            print("\nAdd User\n")
            addUser()
            continue
        elif userChoice == '7':
            print("\nRemove User\n")
            removeUser()
            continue
        elif userChoice == '8':
            print("\nUpdate Existing Equipment\n")
            updateEquipment()
            continue
        elif userChoice == '9':
            print("\nAdd Equipment\n")
            addEquipment()
            continue
        elif userChoice == '10':
            print("\nRemove Equipment\n")
            removeEquipment()
            continue
        elif userChoice == '11':
            cont = input("\nLog Out? (y/n): ").lower()
            while True:
                if cont == "y":
                    print("\nSuccessfully logged out.\n\n")
                    main()
                elif cont == "n":
                    print()
                    managerMenu()



def firstLoginPasswordChange(userID, newPassword):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', newPassword.encode('utf-8'), salt, 100000)
    db_conn.updateUser(userID, password = salt + key)

#0 = User not found
#1 = Incorrect Password
#2 = First login
#3 = Employee authenticated
#4 = Manager authenticated
def login(userID, inputPassword):
    userData = db_conn.getUser(userID)
    if userData != None:
        userPassword = userData[3]
        if userPassword == inputPassword == db_conn.DEFAULT_PASSWORD: return 2
        elif userPassword != db_conn.DEFAULT_PASSWORD:
            salt, key = userPassword[:32], userPassword[32:]
            if key == hashlib.pbkdf2_hmac('sha256', inputPassword.encode('utf-8'), salt, 100000):
                if userData[5] == 0: return 3
                else: return 4
            else: return 1
    else: return 0

def main():
    while True:
        userID = input("Enter your ID number: ")
        password = input("Enter your password: ")
        authenticated = login(userID, password)
        if authenticated == 0 or authenticated == 1:
            print("Incorrect ID/Password Combination!")
        elif authenticated == 2:
            print("This is your first time logging in. You must change your password.")
            while True:
                newPassword = input("Enter your new password: ")
                verify = input("Verify your new password: ")
                if newPassword == verify:
                    firstLoginPasswordChange(userID, newPassword)
                    print("Password successfully changed. Please log in with your new password.")
                    break
                else: print("Passwords do not match!")
        elif authenticated == 3: employeeMenu()
        elif authenticated == 4: managerMenu()

if __name__ == "__main__":
    main()