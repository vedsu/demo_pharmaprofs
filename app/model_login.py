# Login and Registration Component

from app import mongo
from app import mail
from flask_mail import Message

class Login():

    @staticmethod
    def register(register_email, register_password, register_confirmpassword, register_type, website):

        
        if register_password == register_confirmpassword:

            user = mongo.db.user_data.find_one({"email": register_email})
            if user:
                return ({"success": False, "message": "User already registered, Please Login"}),403
            else:
                try:
                    msg = Message('Hello', sender = 'registration@pharmaprofs.com', recipients = [register_email])
                    msg.body = f"Welcome to PharmProfs. Here are your Login Credentials for https://www.pharmaprofs.com/speaker-opportunity.php \n Username: {register_email}, Password: {register_password}.\n"
                    mail.send(msg)
                    if register_type == "Attendee":
                        mongo.db.user_data.insert_one({"email":register_email, "password":register_password, "UserType": register_type, "website":website,"history_purchased":[], "history_pending":[]})
                    else:
                        mongo.db.user_data.insert_one({"email":register_email, "password":register_password, "UserType": register_type, "website":website})
                    return ({"success": True, "message": "user registered successfully, email sent"}),201
                except Exception as e:
                    return ({"success": False, "message": str(e)}),403
        else:
            return ({"success": False, "message": "password mismatch"}),403


    @staticmethod
    def authenticate(login_email, login_password, login_type, website):

        try:
            user = mongo.db.user_data.find_one({"email":login_email, "password": login_password, "UserType": login_type,"website":website})
            if user:
                return ({"success": True, "message": "login successfull"}),200
            else:
                return ({"success": False, "message": "invalid credentials"}),403
            
        except Exception as e:
            return ({"success": False, "message":str(e)}),403      
        

    @staticmethod
    def user_order(user, order_type, webinar):
        
        try:
            if order_type == "purchased":
                mongo.db.user_data.update_one(
                {"email":user},
                {"$addToSet":{"history_purchased":webinar}}
                )
            else:
                mongo.db.user_data.update_one(
                {"email":user},
                {"$addToSet":{"history_pending":webinar}}
                )

            return ({"success": True, "message":"webinar updated for user"}),200
        except Exception as e:
            return ({"success": False, "message":str(e)}),403
