# Utilities
from app import mongo, mail, s3_client
from datetime import datetime, timedelta
# from app import mail
from flask import render_template_string
from flask_mail import Message
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO


class Utility():
    
    
    @staticmethod
    def generate_pdf(Webinar,customername, country, websiteUrl, customeremail, date_time_str, webinardate, comma_separated_keys, orderamount, invoice_number):
        # File and document details
        documentTitle = 'Invoice'
        title = 'Payment Details'
        subTitle = Webinar
        textLines = [
            
            f'Customer Name: {customername}',
            f'Country: {country}',
            f'Invoice Number: {invoice_number}',
            f'Registered Email: {customeremail}',
            f'Order Date: {date_time_str}',
            f'Webinar Date: {webinardate}',
            f'Webinar Session: {comma_separated_keys}',
            f'Order Amount: {orderamount}',
            f'Website URL: {websiteUrl}',
        ]
        thankYouNote = 'Thank you for your participation!'

        # Create PDF in memory
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Set the title of the document
        pdf.setTitle(documentTitle)

        # Create the title by setting its font and putting it on the canvas
        pdf.setFont('Helvetica-Bold', 36)
        pdf.drawCentredString(width / 2, height - 60, title)

        # Create the subtitle by setting its font, color, and putting it on the canvas
        pdf.setFillColorRGB(0, 0, 255)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(width / 2, height - 100, subTitle)

        # Draw a line below the subtitle
        pdf.line(40, height - 110, width - 40, height - 110)

        # Create multiline text using textline and for loop
        text = pdf.beginText(40, height - 140)
        text.setFont("Helvetica", 14)
        text.setFillColor(colors.black)
        for line in textLines:
            text.textLine(line)
            # Add space and line after each text line
            text.moveCursor(0, 20)  # Move cursor down for the next line

        pdf.drawText(text)

        # Add the thank you note at the bottom of the page
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(width / 2, 60, thankYouNote)

        # Save the PDF to the in-memory buffer
        pdf.save()
        buffer.seek(0)

        # Upload the PDF to S3
        bucket_name = "vedsubrandwebsite"
        object_key = f'websiteorder/{invoice_number}.pdf'
        s3_client.put_object(
            Body=buffer,
            Bucket=bucket_name,
            Key=object_key
        )

        # Generate S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
        return s3_url
    
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
        
         

      
