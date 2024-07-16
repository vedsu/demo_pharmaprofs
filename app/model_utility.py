# Utilities
from app import mongo
from datetime import datetime, timedelta

class Utility():
    @staticmethod
    def subscribe(subscriber):
       current_datetime = datetime.now()
       try:
            mongo.db.subscriber_list.insert_one({"email":subscriber, "type":"subscriber", "date":current_datetime})
            return ({"success": True, "message": "subscribed successfully"}),201
       except Exception as e:
            return ({"success": False, "message": str(e)}), 403

    @staticmethod
    def unsubscribe(unsubscriber):
       current_datetime = datetime.now()
       try:
            mongo.db.subscriber_list.insert_one({"email":unsubscriber, "type":"unsubscriber", "date":current_datetime})
            return ({"success": True, "message": "unsubscribed successfully"}),201
       except Exception as e:
            return ({"success": False, "message": str(e)}), 403
         

      
