class UserCredentials():
 
    def __init__(self):
        self.username = 'Trevin'
        self.passFile = open("password.txt", "r")
        self.password = self.passFile.read()
        self.passFile.close()  
 
    def get_username(self):
        return self.username
 
    def get_password(self):
        return self.password
 