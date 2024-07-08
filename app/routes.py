
from app import app
from app import mongo
from flask import request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.model_login import Login
from app.model_webinar import Webinar
from app.model_speaker import Speaker
from app.model_order import Order
import string
import random
from app import s3_client, s3_resource


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
    
@app.route('/order', methods = ['POST'])
def order():
    paymentstatus = None
    session = []
    id = len(list(mongo.db.order_data.find({})))+1
    if request.method in 'POST':
        
        customeremail = request.form.get('customeremail')
        paymentstatus = request.form.get("paymentstatus")
        if paymentstatus == "purchased":
            N= 3
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
            bucket_name = "vedsubrandwebsite"
            object_key = customeremail.split('@')[0]+"_"+res
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/order/{object_key}.pdf"
            invoice = request.files.get("invoice")
            s3_client.put_object(
                Body = invoice,
                Bucket = bucket_name,
                Key = f'order/{object_key}.pdf'
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
            "document" : document
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

       
