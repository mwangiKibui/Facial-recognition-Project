"""testing the elements of args and kwargs"""
import sqlite3
conn = sqlite3.connect('database.db')
def tester_args(*args):
    args_list = [arg for arg in args]
    print("the first is  {}".format(args_list[1]))
tester_args('kennedy','mwangi','kibui')
def select_details(*args):
    user_id,detail = args
    print('detail is {}'.format(detail))

#in kwargs we do not use the curly brackets just pass the element and the value and the element not in quotes
select_details(4,'kennedy mwangi')
#checking on the formatiers
print("%100s"%('WELCOME TO ABC BANK'),end="\n")
print("%100s"%("We serve you trully"))
activities_dict = {
    1 : "Check balance",
    2 : "Withdrawal",
    3 : "Deposit"
}
for key,value in activities_dict.items():
    print(str(key)+'   ->  '+value)
