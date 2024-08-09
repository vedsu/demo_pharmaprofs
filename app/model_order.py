# Order Component
from app import mongo
from datetime import datetime, timedelta
import pytz
class Order():

    @staticmethod
    def update_order(order_data):

        try:
            mongo.db.order_data.insert_one(order_data)
            return ({"success": True, "message": "order placed successfully"}),201
        except Exception as e:
            return ({"success": False, "message": str(e)}), 403
        
    def find_order(customeremail):

        dashboard_list =[]
        try:
            orders = list(mongo.db.order_data.find({"customeremail":customeremail}))
            user_data = list(mongo.db.user_data.find({"email": customeremail}))
            if user_data:
                user = user_data[0]
                history_pending = user["history_pending"] 
                history_purchased = user["history_purchased"]
                # return user['email'], history_pending, history_purchased 
                
                for order in orders:
                    
                    live_url, recording_url, digitaldownload_url, transcript_url = None, None, None, None
                    topic = order["topic"]
                    customeremail = order["customeremail"]
                    paymentstatus = order["paymentstatus"]
                    sessionLive = order["sessionLive"] #True /False
                    sessionRecording = order["sessionRecording"] # True/ False
                    sessionDigitalDownload = order['sessionDigitalDownload'] # True or False
                    sessionTranscript = order["sessionTranscript"] # True or False
                    customername = order["customername"]
                    document = order["document"]

                    if paymentstatus == "purchased":
                        projection ={"_id":0}
                        webinar_data  = list(mongo.db.webinar_data.find({"topic":topic}, projection))
                        if webinar_data:
                            webinar = webinar_data[0]
                            # print("YES")
                            date = webinar["date"]
                            time = webinar["time"]
                            topic = webinar["topic"]
                            speaker = webinar["speaker"]
                            date_time = webinar["date_time"]
                            timeZone = webinar["timeZone"]
                            duration = webinar["duration"]
                            urlLive = webinar["urlLive"]
                            urlRecording = webinar["urlRecording"]
                            urlDigitalDownload = webinar["urlDigitalDownload"]
                            urlTranscript = webinar["urlTranscript"]
                            handle_live = handle_timezone(date_time, timeZone)
                            handle_other = handle_othertimezone(date_time, timeZone)
                            
                            if sessionLive == "True" and handle_live:
                                live_url =  urlLive
                            if sessionRecording == "True" and handle_other:
                                recording_url = urlRecording
                            if sessionDigitalDownload == "True" and handle_other:
                                digitaldownload_url = urlDigitalDownload
                            if sessionTranscript == "True" and handle_other:
                                transcript_url = urlTranscript
                            
                            dashboard_dict = {
                            "customername":customername ,
                            "webinar" : topic,
                            "speaker" : speaker ,
                            "date" : date,
                            "time" : time,
                            "timeZone" : timeZone,
                            "duration" : duration,
                            "live_url" : live_url,
                            "recording_url": recording_url,
                            "digitaldownload_url": digitaldownload_url,
                            "transcript_url" : transcript_url,
                            "document" : document
                            # "id": order ["id"],
                            # "orderdate": order["orderdate"],
                            # "webinardate": order["webinardate"],
                            # "session": order["session"], # Array
                            # "customername": order["customerName"],
                            # "billingemail": order["billingEmail"],
                            # "orderamount": order["orderamount"],
                            # "country" : order["country"],
                            # "state" : order["state"],
                            # "city" : order["city"],
                            # "zipcode" : order["zipcode"],
                            # "address": order["address"],
                            # "document": order["document"],
                            # "website" : order["website"]
                            }

                            dashboard_list.append(dashboard_dict)

                        
        except Exception as e:

                dashboard_list=[str(e)]

        return dashboard_list, history_pending, history_purchased


def handle_othertimezone(webinar_datetime_str,timeZone):
        # # Given webinar date and time strings
        # webinar_date_str = date_str
        # webinar_time_str = time_str
        # # Combine date and time strings into a datetime object
        # webinar_datetime_str = f"{webinar_date_str}T{webinar_time_str}:00.000Z"
        # webinar_datetime = datetime.strptime(webinar_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Given webinar date and time in ISO 8601 format
        webinar_datetime = datetime.strptime(webinar_datetime_str,  "%Y-%m-%dT%H:%M:%S.%fZ")



        # Time zones dictionary
        time_zones = {
        'PST': 'America/Los_Angeles',
        'EST': 'America/New_York',
        'IST': 'Asia/Kolkata',
        'UTC': 'UTC',
        'CST': 'America/Chicago'
        }
        
        webinar_tz = pytz.timezone(time_zones[timeZone])

        # Use only date, hours, and minutes
        webinar_datetime = webinar_tz.localize(webinar_datetime.replace(second=0, microsecond=0))
        webinar_datetime_utc =  webinar_datetime.astimezone(pytz.UTC) 
   
        # Current timeZone with specific timezone
        current_datetime_utc = datetime.now(pytz.UTC).replace(second=0, microsecond=0)

        time_difference = webinar_datetime_utc - current_datetime_utc
        # Check if the webinar is within the next 12 hours
        is_more_than_24_hours = timedelta(24) < time_difference < timedelta(hours=1440)

        return is_more_than_24_hours     



def handle_timezone(webinar_datetime_str,timeZone):
        # Given webinar date and time strings
        # webinar_date_str = date_str
        # webinar_time_str = time_str
        # # Combine date and time strings into a datetime object
        # webinar_datetime_str = f"{webinar_date_str}T{webinar_time_str}:00.000Z"
        # webinar_datetime = datetime.strptime(webinar_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Given webinar date and time in ISO 8601 format
        webinar_datetime = datetime.strptime(webinar_datetime_str,  "%Y-%m-%dT%H:%M:%S.%fZ")



        # Time zones dictionary
        time_zones = {
        'PST': 'America/Los_Angeles',
        'EST': 'America/New_York',
        'IST': 'Asia/Kolkata',
        'UTC': 'UTC',
        'CST': 'America/Chicago'
        }
        
        webinar_tz = pytz.timezone(time_zones[timeZone])

        # Use only date, hours, and minutes
        webinar_datetime = webinar_tz.localize(webinar_datetime.replace(second=0, microsecond=0))
        webinar_datetime_utc =  webinar_datetime.astimezone(pytz.UTC) 
   
        # Current timeZone with specific timezone
        current_datetime_utc = datetime.now(pytz.UTC).replace(second=0, microsecond=0)

        time_difference = webinar_datetime_utc - current_datetime_utc
        # Check if the webinar is within the next 12 hours
        is_less_than_12_hours = timedelta(0) < time_difference < timedelta(hours=48)

        return is_less_than_12_hours
