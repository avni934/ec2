# importing libraries 
from flask import Flask 
from flask_mail import Mail, Message 

app = Flask(__name__) 
mail = Mail(app) # instantiate the mail class 

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'avni.jain2022@vitstudent.ac.in' # apni gmail id daal dena
app.config['MAIL_PASSWORD'] = '$iA9z05cuI' # mail id ka password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

# message object mapped to a particular URL ‘/’ 
@app.route("/") 
def index(): 
    msg = Message( 
				'Hello', 
				sender ='avni.jain2022@vitstudent.ac.in', # apni mail id
				recipients =['rudrathakur@gmail.com']  # jisko mail bhejni hai
			) 
    msg.body = 'hi' # content mail mein kya bhejna hai 
    mail.send(msg) 
    return 'Sent'

if __name__ == '__main__': 
    app.run(debug = True) 

