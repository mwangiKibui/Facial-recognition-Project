"""start with the class for admin"""
import os
import cv2
import PIL
import numpy as np
from PIL import Image
import pickle
import sqlite3
cam = cv2.VideoCapture(0)
class System():
    cascade_classifier = cv2.CascadeClassifier("C:/Users/user/PycharmProjects/group_assignment/classifiers/haarcascade_frontalface_default.xml")

    scanner = cv2.face.LBPHFaceRecognizer_create()
    scanner2 = cv2.face.LBPHFaceRecognizer_create()
    scanner2.read("C:/Users/user/PycharmProjects/group_assignment/recognizer\data_training.yml")
    #scanner.read("C:/Users/Njuguna Ng'ang'a/PycharmProjects/facial_assignment/recognizer/new_trained.yml")
    db = sqlite3.connect('database.db')


    #update a  record in the database
    def update_images(self):
        faces_lst = []
        face_ids = []
        #start by sycing the images
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir,'images')
        for path,dirname,files in os.walk(image_path):
            for file in files:
                file_path = os.path.join(path,file)

                label = os.path.basename(os.path.dirname(file_path))
                _id = os.path.basename(os.path.dirname(file_path))
                #getting the labels
                pil_image = Image.open(file_path).convert("L")
                #sometimes resizing may not Fully  work out for images and yu just wanna pass the pil_image
                final_image = pil_image.resize((500,500),Image.ANTIALIAS)
                image_array = np.array(pil_image,"uint8")

                #detect the faces
                faces = self.cascade_classifier.detectMultiScale(image_array,scaleFactor=1.32,minNeighbors=5)

                for(x,y,w,h) in faces:
                    roi = image_array[y:y+h,x:x+w]
                    faces_lst.append(roi)
                    face_ids.append(int(_id))

        #when we are through
        # with open("new_labels.pickle","wb") as f:
        #     pickle.dump(labels_ids,f)#i have simply dumped/placed the elements of the pickle in the file
        #save the data
        if len(faces_lst) > 0 and len(np.array(face_ids)) > 0:
            self.scanner.train(faces_lst,np.array(face_ids))
            self.scanner.save('recognizer/data_training.yml')
            return "the components have been successfully updated"
        else:
            print(faces_lst)

    def update_details(self,**kwargs):
        value_lst = []
        key_lst  = []
        for key,value in kwargs.items():
            value_lst.append(value)
            key_lst.append(key)
        #first not checking the table later take it dynamically
        counter = 2
        result = None
        for elem in range(0,len(key_lst)- 2):
            #nice way to capture
            result = self.db.execute("UPDATE group_members SET '"+value_lst[1]+"'='"+value_lst[counter]+"' WHERE id='"+str(value_lst[0])+"'")
            counter += 1
        if result:
            self.db.commit()
            self.db.close()
            return "Successfully updated the details"
        else:
            return "An error occured when updating"
        # for key,value in kwargs.items():
    #insert a record in the database
    def insert_details(self,**kwargs):
        value_lst = []
        key_lst  = []
        for key,value in kwargs.items():
            value_lst.append(value)
            key_lst.append(key)
        #first not checking the table later take it dynamically
        counter = 0
        #nice way to capture
        result = self.db.execute("INSERT INTO group_members("+key_lst[0]+","+key_lst[1]+","+key_lst[2]+","+key_lst[3]+","+key_lst[4]+") VALUES('"+str(value_lst[0])+"','"+value_lst[1]+"','"+value_lst[2]+"','"+str(value_lst[3])+"','"+str(value_lst[4])+"')")

        if result:
            self.db.commit()
            self.db.close()
            return "Successfully inserted the user"
        else:
            return "an error occurred when inserting"
    #delete a record from the database
    def delete_record(self,*args):
        user_id = args[0]

        result = self.db.execute("DELETE FROM group_members WHERE id="+str(user_id))
        if result:
            print("successfully deleted the user")
        else:
            print("didn't delete the user")
    #get details
    def get_details(self,user_id):

        result = self.db.execute("SELECT * FROM group_members WHERE id="+str(user_id))
        value_lst = None
        for elem in result:
            value_lst = [x for x in elem]
        if value_lst is not None:
            return value_lst
        else:
            return False
    #verify the user
    #because we dont have a good init function always pass self
    #if the parent class has received self you dont need to send it again here if verify_user has received self
    def verify_user(self,user_id):
        if self.get_details(user_id):
            #if then it exists return and also the name
            return self.get_details(user_id)[1]
        else:
            return False
    #the login process
    def user_login(self,user_id):
        profile = self.get_details(user_id)
        while profile:
            ret,img = cam.read()
            gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = self.cascade_classifier.detectMultiScale(img,1.5,5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
                roi_gray = gray_img[y:y+h,x:x+h]
                roi_color = img[y:y+h,x:x+h]
                #we predict them
                _id,conf = self.scanner2.predict(roi_gray)
                while _id == int(user_id) and conf < 37:
                    cam.release()
                    cv2.destroyAllWindows()
                    return True




            cv2.imshow("face detection project",img)
            if cv2.waitKey(1) == ord('q'):
                cam.release()
                cv2.destroyAllWindows()





class Admin(System):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    scanner = cv2.CascadeClassifier('C:/Users/user/PycharmProjects/group_assignment/classifiers/haarcascade_frontalface_default.xml')
    conn = sqlite3.connect('facebase.db')
    def __init__(self,id,name,school,email):
        super().__init__(self,name,school,email)
        self.id = id
        self.name = name
        self.school = school
        self.email = email
    #start by adding records
    def add_record(self,account=0):
        result = System.update_images
        if result:
            #add the record to the database
            result = System.insert_details(name=self.name,school= self.school,email= self.email,account= account)
            if result:
                return "records were updated safely"
            else:
                return "there was an error updating the details"
    def update_record(self,**kwargs):
        result = System.update_images
        if result:
            #updating record in the database
            result = System.update_details(**kwargs)
            if result:
                return "details were updated safely"
            else:
                return "there was an error updating details"
    #delete the records
    def delete_record(self,*args):
        result = System.update_images
        user_id = args[0]
        if result:
            #updating record in the database
            result = System.delete_record(user_id)
            if result:
                return "details were deleted safely"
            else:
                return "there was an error updating details"

#students class
class Student(System):
    def __init__(self,id):
        self.id = id
    def checkBankDetails(self,id):
        #first get the amount by calling the get details
        #we must unpack everything failure shall lead to an error
        user_id,user_name,user_school,user_email,user_balance = System.get_details(self,id)
        #have to construct a dictionary for records
        user_dict = {
            "login id" : user_id,
            "name" : user_name,
            "school" : user_school,
            "email" : user_email,
            "Balance" : user_balance
        }
        for  key,values in user_dict.items():
            print(key+"  ->  "+ str(values))
    def Withdrawal(self,id,amount):
        amount_remaining = int(System.get_details(self,id)[4])
        if int(amount_remaining) >= amount:
            #withdrawal
            amount_remaining -= amount
            #update the database
            result = System.update_details(self,id=id,col="balance",balance=str(amount_remaining))
            if result:
                return "you have successfully withdrawn {} your account is remaining with {}.Thankyou for choosing ABC Bank".format(amount,amount_remaining)
            else:
                return "There was an error scheduling your withdrawal"
        else:
            return "Insufficient funds in account.Thankful for choosing ABC Bank"
    def deposit(self,id,amount):
        amount_remaining = int(System.get_details(self,id)[4])
        amount_remaining += amount
        #update the database
        result = System.update_details(self,id=id,col="balance",balance=str(amount_remaining))
        if result:
            return "you have successfully deposited {} your balance is {}.Thankyou for choosing ABC ".format(amount,amount_remaining)
        else:
            return "There was an error scheduling your deposit"
    def activities(self,id,amount=0):
        #this method will be returned from one logs in
        print('%100s'%("WELCOME {} TO ABC BANK KARATINA").format(System.verify_user(self,id)),end="\n")
        print('%95s'%("We are made for you"),end="\n")
        activities_dict = {1:"Check Bank Details",2:"Withdrawal",3:"Deposit"}
        for key,value in activities_dict.items():
            print(str(key) + "  ->  " + value)
        key = int(input("enter the service to access"))
        if key == 1:
            self.checkBankDetails(id)
        elif key == 2:
            withdrawal_amount = int(input("enter the amount you want to withdraw"))
            return self.Withdrawal(id,withdrawal_amount)
        else:
            deposit_amount = int(input("enter the amount you want to deposit"))
            return self.deposit(id,deposit_amount)
    def login(self,id):
        result = System.verify_user(id)
        if result:
            return self.activities(id)
    #shall continue with methods after class



person = input("enter who you are: admin or user").lower()
if person == "admin":
    system = System()
    #insert,update or delete or refresh
    activity = input("Enter the activity you want to perform i.e Insert,Update,Delete,Refresh").lower()
    if activity == "insert":
        user_id = input("enter the id")
        user_name = input("enter the name")
        user_school = input("enter the school")
        user_email = input("enter the email")

        result = system.insert_details(id=user_id,name=user_name,school=user_school,email=user_email,balance=0)#rem we use =
        print(result)

    elif activity == "update":
        update_id = input("enter the id which you want to update")
        update_elem = input("enter the component you want to update")
        update_content = input("enter what you want to update")
        result = system.update_details(id=update_id,col = update_elem,value=update_content)
        print(result)
    elif activity == "delete":
        delete_id = input("enter the id to be deleted")
        result = system.delete_record(delete_id)
        print(result)
    elif activity == "refresh":
        result = system.update_images()
        print(result)
elif person == "user":
    #checkin

    user_id = input("enter the system login id")
    #call the login method
    user = Student(int(user_id))
    result = user.user_login(user_id)
    if result:
        print(user.activities(int(user_id)))


