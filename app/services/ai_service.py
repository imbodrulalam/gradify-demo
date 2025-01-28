# return an example of a professional email

def generate_email():
    try:
        response = {
            "subject": "Welcome to our platform!",
            "body": "Hi there! We are excited to have you on board. You can now access all the features of our platform. If you have any questions, feel free to reach out to us. Enjoy!",
            "signature": "Best, The Team",
        }        
        return response
    except Exception as e:
        return f"Error generating email: {str(e)}"
