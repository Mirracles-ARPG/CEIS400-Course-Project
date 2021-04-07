import db_conn, os, hashlib

def employeeMenu():
    #EMPLOYEE MENU CODE HERE
    print("You are an employee")

def managerMenu():
    #MANAGER MENU CODE HERE
    print("You are a manager")

def firstLoginPasswordChange(userID):
	print("This is your first time logging in. You must set your password.")
	while True:
		newPassword, verify = input("Enter a secure password: "), input("Enter your password again to verify: ")
		if newPassword == verify:
			salt = os.urandom(32)
			key = hashlib.pbkdf2_hmac('sha256', newPassword.encode('utf-8'), salt, 100000)
			db_conn.updateUser(userID, password = salt + key)
			return True
		else: print("Password entries do not match!")

def login(userID):
    inputPassword = input("Enter your password: ")
    userData = db_conn.getUser(userID)
    if userData != None:
        if userData[3] == inputPassword == db_conn.DEFAULT_PASSWORD: return firstLoginPasswordChange(userID)
        elif userData[3] != db_conn.DEFAULT_PASSWORD:
            salt, key = userData[3][:32], userData[3][32:]
            return key == hashlib.pbkdf2_hmac('sha256', inputPassword.encode('utf-8'), salt, 100000)
    else: return False

def main():
    while True:
        userID = input("Enter your ID number: ")
        if login(userID):
            if db_conn.getUser(userID)[5] == 0: employeeMenu()
            else: managerMenu()
        else: print("Incorrect ID/Password Combination!")

if __name__ == "__main__":
    main()