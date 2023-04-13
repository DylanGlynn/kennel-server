class Customer():
    '''Class for defining Customers.'''
    def __init__(self, id, full_name, address, email = "", password = ""):
        self.id = id
        self.name = full_name
        self.address = address
        self.email = email
        self.password = password
