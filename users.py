class UserCredentials():

    def __init__(self):
        self.pass_file = open("credentials.txt", "r")
        self.file_lines = self.pass_file.readlines()
        self.username = self.file_lines[0]
        self.password = self.file_lines[1]
        self.mta_username = self.file_lines[2][0:-1]
        self.mta_password = self.file_lines[3]
        self.pass_file.close()

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_mta_username(self):
        return self.mta_username

    def get_mta_password(self):
        return self.mta_password
