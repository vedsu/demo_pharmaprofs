# Speaker Component
from app import mongo
import pytz
from datetime import datetime, timedelta

class Speaker():

    @staticmethod
    def data_speaker(s_id):
        
        speaker_info = None  
        try:
            speaker_data = list(mongo.db.speaker_data.find({"id":s_id}))
            speaker = speaker_data[0]
            speaker_dict={
                "id": speaker ["id"],
                "name": speaker ["name"],
                "email":speaker ["email"],
                "industry": speaker ["industry"],
                "status": speaker ["status"],
                "bio": speaker ["bio"],
                "contact" :speaker ["contact"],
                "photo": speaker["photo"],
                "history": speaker["history"]
            }
            
            speaker_info = speaker_dict
        except Exception as e:
            speaker_info = None 
            
        
        return speaker_info
    
    
    @staticmethod
    def view_speaker():

        speaker_list =[]

        try:
            speaker_data = list(mongo.db.speaker_data.find({}))
            for speaker in speaker_data:
                speaker_dict ={
                "id":speaker["id"],
                "name":speaker["name"],
                "email":speaker["email"],
                "contact": speaker["contact"],
                "industry":speaker["industry"],
                "status":speaker["status"],
                "bio":speaker["bio"],
                "photo": speaker["photo"]
                }
                speaker_list.append(speaker_dict)
        except Exception as e:
            speaker_list =[ ]

        return speaker_list
    
    @staticmethod
    def speakerdashboard_data(email):
        dashboard_list = [] 
        try:
            speaker_data = list(mongo.db.speaker_data.find({"email":email}))
            speaker = speaker_data[0]
            history =  speaker["history"]
            name = speaker["name"]
            for topic in history:
                
                webinar_data  = list(mongo.db.webinar_data.find({"topic":topic}))
                if webinar_data:
                    # dashboard_list.append(topic)
                    webinar = webinar_data[0]
                

                    if webinar["speaker"] == name:
                            date =  webinar["date_time"] 
                            timezone = webinar["timeZone"]
                            urlreturn = handle_timezone(date, timezone)
                            
                            if urlreturn is True:
                                urlLive = webinar["urlLive"]
                            
                            else:
                                urlLive = ""
                            
                            
                            webinar_dict ={
                                
                                "webinar": topic,
                                "date": webinar["date"],
                                "time": webinar["time"],
                                "timezone" : timezone,
                                "duration": webinar["duration"],
                                "urlLive": urlLive,
                                "website": webinar["website"]
                            
                            }

                            dashboard_list.append(webinar_dict)

        except Exception as e:
            dashboard_list = [str(e)]

        return dashboard_list,history


def handle_timezone(webinar_datetime_str,timeZone):

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




            

