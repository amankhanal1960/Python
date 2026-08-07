##---------------- This is how any class is defined-----------#
# class Student():
    
#     # here the name in the right is what we send in the parameter and 
#     # self.name is what is being created inside object 
#     def __init__(self, name, marks):
#         self.name = name
#         self.marks = marks
#         print("Adding new student in database..")
 
# # here s1 and s2 represent object also called instance of class  

# # storing the name and marks in class 
# s1 = Student("Aman", 97)

# print(s1.name, s1.marks)

# #---------- class attributes and objct attributes -------------#
# class Car():
    
#     # This is class attribute
#     Brand = "Mercedes"
    
#     def __init__(self, name, price):
        
#         # These are object attributes
#         self.name = name
#         self.price = price

# c1 = Car("Maybach", 300 )
# c2 = Car("Mercedes-Benz S-Class", 300)

# print(c1.Brand, c2.name, c2.price)

# -------------------- Methods ----------------------- #
class Student():
    college_name = "Thapathali Campus"
    
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
    
    def welcome(self):
        print("Welcome Back!", self.name)
        
    def get_marks(self):
        return self.marks
        
s1 = Student("Aman", 99)
print(s1.get_marks())