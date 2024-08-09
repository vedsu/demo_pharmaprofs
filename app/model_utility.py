# Utilities
from app import mongo
from datetime import datetime, timedelta
from app import mail
from flask import render_template_string
from flask_mail import Message
class Utility():
    
    @staticmethod
    def subscribe_list(subscriber_email, subscriber_name, subscription_type, subscriber_jobtitle):
       current_datetime = datetime.now()
       try:
            mongo.db.subscriber_list.insert_one({"email":subscriber_email, "name":subscriber_name,"jobtitle":subscriber_jobtitle,"subscription_type":subscription_type,"type":"subscriber", "date":current_datetime})
            return ({"success": True, "message": "subscribed successfully"}),201
       except Exception as e:
            return ({"success": False, "message": str(e)}), 403

    @staticmethod
    def unsubscribe_list(unsubscriber):
       current_datetime = datetime.now()
       try:
            mongo.db.subscriber_list.insert_one({"email":unsubscriber, "type":"unsubscriber", "date":current_datetime})
            return ({"success": True, "message": "unsubscribed successfully"}),201
       except Exception as e:
            return ({"success": False, "message": str(e)}), 403
       
    @staticmethod
    def forgotpassword(email, website):
        try:
            usercredentails =list(mongo.db.user_data.find({"$and":[{"email":email},{"website":website}]}))
            if usercredentails:
               try:
                    usercredentail = usercredentails[0]
                    email = usercredentail["email"]
                    password = usercredentail["password"]
                    websiteUrl = usercredentail["websiteUrl"]
                    
                    msg = Message('Your Account Credentials', sender = 'registration@pharmaprofs.com', recipients = [email])
                    
                    msg.body = f"""
                                   Dear Customer,

                                   Welcome to our website!

                                   Here are your account credentials:

                                   Email: {email}
                                   Password: {password}
                                   Website: {websiteUrl}

                                   Please keep this information secure and do not share it with anyone.

                                   Thanks & Regards!
                                   Webinar Organizer Team
                                   
                                   """
                    msg.html = render_template_string("""
                                   <p>Dear Customer,</p>
                                   <p>Welcome to our website!</p>
                                   <p>Here are your account credentials:</p>
                                   <ul>
                                        <li><b>Email:</b> {{ email }}</li>
                                        <li><b>Password:</b> {{ password }}</li>
                                        <li><b>Website:</b> <a href="{{ website }}">{{ website }}</a></li>
                                   </ul>
                                   <p>Please keep this information secure and do not share it with anyone.</p>
                                   <p>Thanks & Regards!<br>Webinar Organizer Team</p>
                                   """, email=email, password=password, website=websiteUrl)
                    mail.send(msg)
                    return ({"success": True, "message": "email sent successfully"}),200
               except Exception as e:
                   return ({"success": False, "message": str(e)}), 403

            else:
               return ({"success": False, "message": "User doesnot exists"}), 200
        except Exception as e:
            return ({"success": False, "message": str(e)}), 403
        
         

      
