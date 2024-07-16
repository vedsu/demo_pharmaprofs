
from app import app
from app import mongo
from flask import request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.model_login import Login
from app.model_webinar import Webinar
from app.model_speaker import Speaker
from app.model_order import Order
from app.model_utility import Utility
import string
import random
import datetime
import pytz
from app import s3_client, s3_resource
from flask_mail import Message
from app import mail


@app.route('/subscribe', methods = ['POST'])
def subscriber():
    if request.method in 'POST':
        subscriber = request.form.get("Subscriber")
        response = Utility.subscribe_list(subscriber)
        return response

@app.route('/unsubscribe', methods = ['POST'])
def unsubscriber():
    if request.method in 'POST':
        unsubscriber = request.form.get("Unsubscriber")
        response = Utility.unsubscribe_list(unsubscriber)
        return response
    

@app.route('/contactus', methods = ['POST'])
def contact_us():
    if request.method in 'POST':
        query_email = "support@pharmaprofs.com"
        name = request.form.get("Name")
        email = request.form.get("Email")
        message = request.form.get("Message")
        try:
            msg = Message('Query', sender = 'registration@pharmaprofs.com', recipients = [query_email])
            msg.body = f"We have received a query from {name} ({email}) \n Message: {message}.\n"
            mail.send(msg)
            return {"Message": "Thanks for contacting us. Our team will reach out to you shortly."}
        except Exception as e:
            return {"Message": "Failed to receive your request. Please try again later."}
            # return {"Message": str(e)}

@app.route('/speakeropportunity', methods = ['POST'])
def speaker_opportunity():
    if request.method in 'POST':
        query_email = "brian@pharmaprofs.com"
        name = request.form.get("Name")
        email = request.form.get("Email")
        education = request.form.get("Education")
        country = request.form.get("Country")
        phone = request.form.get("Phone")
        industries = request.form.get("Industries")
        bio = request.form.get("Bio")
        try:
            msg = Message('Speaker Opportunity', sender = 'registration@pharmaprofs.com', recipients = [query_email])
            msg.body = f"We have received Speaker Opportunity Query from {name} ({email}) \n Details: {education}.\n {country}.\n {phone}.\n {industries}.\n BIO : {bio}"
            mail.send(msg)
            return {"Message": "Your query has been successfully received. Our team will reach out to you shortly."}
        except Exception as e:
            return {"Message": "Failed to receive your query. Please try again later."}


@app.route('/')
def home():
    speaker_list = []
    webinar_list = []
    webinar_list = Webinar.view_webinar()
    speaker_list= Speaker.view_speaker()
    return jsonify(webinar_list, speaker_list)

@app.route('/<w_id>/<website>', methods= ['GET','PUT','POST','DELETE'])
def view_webinar(w_id,website):    
    
    webinar_data = Webinar.data_webinar(w_id,website)
    
    if request.method in ['GET']:
        
        return webinar_data,200

@app.route('/register', methods = ['POST'])
def user_register():
    if request.method in 'POST':
        register_email = request.form.get("Email")
        register_password = request.form.get("Password")
        register_confirmpassword = request.form.get("ConfirmPassword")
        register_type = request.form.get("UserType")
        website = request.form.get("Website")

        response = Login.register(register_email, register_password, register_confirmpassword, register_type, website)
        return response
        

@app.route('/login', methods=['POST'])
def user_login():
    if request.method in 'POST':
        login_email = request.form.get("Email")
        login_password = request.form.get("Password")
        login_type = request.form.get("UserType")
        website = request.form.get("Website")
        response_login = Login.authenticate(login_email, login_password, login_type, website)
        # if response_login.get("success") is True:
            # access_token = session.get('user_token')
            # session["user_email"] = login_email
            # session["user_type"] = login_type            
        return response_login





def get_current_time_ist():
    # Define the IST timezone
    ist_timezone = pytz.timezone('Asia/Kolkata')
    
    # Get the current time in UTC
    utc_now = datetime.datetime.utcnow()
    
    # Convert the UTC time to IST
    ist_now = utc_now.astimezone(ist_timezone)
    
    # Format the time as desired
    formatted_ist_now = ist_now.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_ist_now
    
@app.route('/order', methods = ['POST'])
def order():
    paymentstatus = None
    current_time_ist = None
    invoice_number = None
    session = []
    id = len(list(mongo.db.order_data.find({})))+1
    if request.method in 'POST':
        
        customeremail = request.form.get('customeremail')
        paymentstatus = request.form.get("paymentstatus")
        orderdate =  request.form.get("orderdate")
        ordertime = request.form.get("ordertime")
        ordertimezone = request.form.get("ordertimezone")
        if paymentstatus == "purchased":
            current_time_ist = get_current_time_ist()
            N= 3
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
            bucket_name = "vedsubrandwebsite"
            invoice_number = request.form.get("invoice_number")
            object_key = customeremail.split('@')[0]+"_"+invoice_number
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/websiteorder/{object_key}.pdf"
            invoice = request.files.get("invoice")
            s3_client.put_object(
                Body = invoice,
                Bucket = bucket_name,
                Key = f'websiteorder/{object_key}.pdf'
            )

            document = s3_url
        
        else:
            
            document = ""

        sessionLive =  request.form.get("sessionLive") #True /False
        priceLive = request.form.get('priceLive')
        
        if sessionLive == "True":
            session.append({"Live": priceLive})
        sessionRecording = request.form.get("sessionRecording") # True/ False
        priceRecording = request.form.get('priceRecording')
        
        if sessionRecording == "True":
            session.append({"Recording": priceRecording})
        sessionDigitalDownload = request.form.get('sessionDigitalDownload') # True or False
        priceDigitalDownload =  request.form.get('priceDigitalDownload')
        
        if sessionDigitalDownload == "True":
            session.append({"DigitalDownload": priceDigitalDownload})
        sessionTranscript = request.form.get("sessionTranscript") # True or False
        priceTranscript = request.form.get('priceTranscript')
        
        if sessionTranscript == "True":
            session.append({"Transcript":priceTranscript})
        
        
        
        order_data = {
            "id":id,
            "topic": request.form.get("topic"),
            "customeremail":  request.form.get("customeremail"), # Login email
            "paymentstatus": paymentstatus,
            "orderdate": request.form.get("orderdate"),
            "ordertime": request.form.get("ordertime"),
            "ordertimezone" : request.form.get("ordertimezone"),
            
            "webinardate": request.form.get("webinardate"),
            "session": session,# Array
            "sessionLive": request.form.get("sessionLive"), #True /False
            "priceLive": request.form.get('priceLive'),
            "sessionRecording":request.form.get("sessionRecording"), # True/ False
            "priceRecording": request.form.get('priceRecording'),
            "sessionDigitalDownload":request.form.get('sessionDigitalDownload'), # True or False
            "priceDigitalDownload": request.form.get('priceDigitalDownload'),
            "sessionTranscript":request.form.get("sessionTranscript"), # True or False
            "priceTranscript": request.form.get('priceTranscript'),
            "customername":request.form.get("customername"),
            "billingemail": request.form.get("billingemail"),
            "orderamount": request.form.get("orderamount"),
            "country": request.form.get("country"),
            "state": request.form.get("state"),
            "city": request.form.get("city"),
            "zipcode": request.form.get("zipcode"),
            "address" : request.form.get("address"),
            "website": request.form.get("website"), # Current Website
            "document" : document,
            "ist_time" : current_time_ist,
            "invoice_number" : invoice_number,
            }
        

        response_order, response_user = Order.update_order(order_data), Login.user_order(request.form.get("customeremail"), paymentstatus, request.form.get("topic")) 
        # if response_order is success then send a confirmation mail for order and dashboard link directly for login
        # Also send link via mail to dashboard login along side email and password for attendee and speaker after registration 
        #  
        # update ordered webinar in history_purchased or history_pending

        return jsonify(response_order, response_user)


@app.route('/dashboard/<email>/<user_type>', methods =['GET'])
def dashboard(email, user_type):
    if user_type == "Speaker":
        
        dashboard_list,history = Speaker.speakerdashboard_data(email)
        return jsonify(dashboard_list,history)
    
    else:
        dashboard_list, history_pending, history_purchased = Order.find_order(email)
        """ 1. take email and search as customeremail in order_data
            2. if take topic, sessions from orderdata
            3. use topic to search topic,speaker, category, sessions url,date, time from webinar data
            4. display user history also whether paid or pending
        """ 
        
        return jsonify(dashboard_list, history_pending, history_purchased)

       
