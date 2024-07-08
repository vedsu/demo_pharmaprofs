# Webinar Component

from app import mongo

class Webinar():

    @staticmethod
    def data_webinar(w_id, website):
        
        webinar_info = None
        try: 
            
            webinar_data = list(mongo.db.webinar_data.find({"$and":[{"webinar_url":w_id}, {"website":website}]}))
            webinar = webinar_data[0]
               
            webinar_data_dict ={
            
                    "id":webinar ["id"],

                    "topic":webinar ["topic"],
                    "industry":webinar ["industry"],
                    "speaker":webinar ["speaker"],
                    "date":webinar ["date_time"],
                    "time":webinar ["time"],
                    "timeZone":webinar["timeZone"],
                    "duration":webinar["duration"],
                    "category":webinar["category"],
                    
                    "sessionLive":webinar ["sessionLive"],
                    "priceLive":webinar ["priceLive"],
                    "urlLive":webinar ["urlLive"],
                    
                    "sessionRecording":webinar ["sessionRecording"],
                    "priceRecording":webinar ["priceRecording"],
                    "urlRecording":webinar ["urlRecording"],

                    "sessionDigitalDownload":webinar ["sessionDigitalDownload"],
                    "priceDigitalDownload":webinar ["priceDigitalDownload"],
                    "urlDigitalDownload":webinar ["urlDigitalDownload"],
                    
                    "sessionTranscript":webinar ["sessionTranscript"],
                    "priceTranscript":webinar ["priceTranscript"],
                    "urlTranscript":webinar ["urlTranscript"],

                    "status":webinar ["status"],
                    "webinar_url": webinar ["webinar_url"],
                    "description":webinar ["description"],

                    }
            webinar_info = webinar_data_dict
        except Exception as e:
            webinar_info = None
        
        return webinar_info
    
    @staticmethod
    def view_webinar():
        webinar_list = []
        try:
            webinar_data = list(mongo.db.webinar_data.find({"status":"Active"}))
            for webinar in webinar_data:
                webinar_dict = {

                "id":webinar["id"],

                "topic":webinar["topic"],
                "industry":webinar["industry"],
                "speaker":webinar["speaker"],
                "website":webinar["website"],
                "date":webinar["date_time"],
                "time":webinar["time"],
                "timeZone":webinar["timeZone"],
                "duration":webinar["duration"],
                "category":webinar["category"],
                
                "sessionLive":webinar["sessionLive"],
                "priceLive":webinar["priceLive"],
                "urlLive":webinar["urlLive"],
                
                "sessionRecording":webinar["sessionRecording"],
                "priceRecording":webinar["priceRecording"],
                "urlRecording":webinar["urlRecording"],

                "sessionDigitalDownload":webinar["sessionDigitalDownload"],
                "priceDigitalDownload":webinar["priceDigitalDownload"],
                "urlDigitalDownload":webinar["urlDigitalDownload"],
                
                "sessionTranscript":webinar["sessionTranscript"],
                "priceTranscript":webinar["priceTranscript"],
                "urlTranscript":webinar["urlTranscript"],

                "status":webinar["status"],
                "webinar_url": webinar["webinar_url"],
                "description":webinar["description"],
                    
                    }
                webinar_list.append(webinar_dict)
        except Exception as e:
            webinar_list = []
        return webinar_list


