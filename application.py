import db_conn, os, hashlib

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

def startSession():
    while True:
        option = input("Type 'x' to log out: ")
        if option == 'x': return

def login():
    authenticated, userID, inputPassword = False, input("Enter your ID number: "), input("Enter your password: ")
    userData = db_conn.getUser(userID)
    if userData != None:
        if userData[3] == inputPassword == db_conn.DEFAULT_PASSWORD: authenticated = firstLoginPasswordChange(userID)
        elif userData[3] != db_conn.DEFAULT_PASSWORD:
            salt, key = userData[3][:32], userData[3][32:]
            authenticated = key == hashlib.pbkdf2_hmac('sha256', inputPassword.encode('utf-8'), salt, 100000)
    if authenticated: startSession()
    else: print("Incorrect ID/Password Combination!")

if __name__ == "__main__":
    login()