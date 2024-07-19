from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
import logging

web = Flask(__name__)
web.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///real.db"
web.config['MAIL_SERVER'] = 'smtp.gmail.com'
web.config['MAIL_PORT'] = 465
web.config['MAIL_USERNAME'] = 'avni.jain2022@vitstudent.ac.in'
web.config['MAIL_PASSWORD'] = '$iA9z05cuI'
web.config['MAIL_USE_TLS'] = False
web.config['MAIL_USE_SSL'] = True
web.config['MAIL_DEBUG'] = True

mail = Mail(web)
db = SQLAlchemy(web)

class Real(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Resource_Name = db.Column(db.String(200), nullable=False)
    Task_Asigned = db.Column(db.String(200), nullable=False)
    Start_Date = db.Column(db.String(10))
    End_Date = db.Column(db.String(10))
    Status = db.Column(db.String(200), nullable=False)
    Phone = db.Column(db.Integer)
    Email = db.Column(db.String(50))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Resource_Name}"

@web.route("/", methods=["POST", "GET"])
def home():
    allreal = Real.query.all()
    return render_template('windex.html', allreal=allreal)

@web.route("/add", methods=["POST", "GET"])
def add():
    if request.method == 'POST':
        Resource_Name = request.form['Resource_Name']
        Task_Asigned = request.form['Task_Asigned']
        Start_Date = request.form['Start_Date']
        End_Date = request.form['End_Date']
        Status = request.form['Status']
        Phone = request.form['Phone']
        Email = request.form['Email']
        real = Real(Resource_Name=Resource_Name, Task_Asigned=Task_Asigned, Start_Date=Start_Date, End_Date=End_Date, Status=Status, Phone=Phone, Email=Email)
        db.session.add(real)
        db.session.commit()
        return redirect("/")
    return render_template('add.html')

@web.route('/edit/<int:sno>', methods=["POST", "GET"])
def edit(sno):
    if request.method == "POST":
        Resource_Name = request.form['Resource_Name']
        Task_Asigned = request.form['Task_Asigned']
        Start_Date = request.form['Start_Date']
        End_Date = request.form['End_Date']
        Status = request.form['Status']
        Phone = request.form['Phone']
        Email = request.form['Email']
        real = Real.query.filter_by(sno=sno).first()
        real.Resource_Name = Resource_Name
        real.Task_Asigned = Task_Asigned
        real.Start_Date = Start_Date
        real.End_Date = End_Date
        real.Status = Status
        real.Phone = Phone
        real.Email = Email
        db.session.add(real)
        db.session.commit()
        return redirect('/')
    real = Real.query.filter_by(sno=sno).first()
    return render_template('edit.html', real=real)

def send_emails():
    with web.app_context():
        dt = datetime.now()
        d = dt.strftime("%Y-%m-%d")
        overdue_records = Real.query.filter(Real.Status == "In Progress", Real.End_Date < d).all()
        
        for record in overdue_records:
            body = ("Dear " + record.Resource_Name + ",\n\n" +
                    "Your task '" + record.Task_Asigned + "' is overdue. " +
                    "Please take necessary action.\n\n" +
                    "Regards,\nTeam")
            
            msg = Message('Task Overdue Alert',
                          sender="avni.jain2022@vitstudent.ac.in",
                          recipients=[record.Email])
            msg.body = body
            
            try:
                mail.send(msg)
                print(f"Email sent successfully to {record.Email}")
            except Exception as e:
                print(f"Error sending email to {record.Email}: {e}")
                logging.error(f"Error sending email to {record.Email}: {e}")
        
        print("Completed sending emails")

scheduler = BackgroundScheduler()
scheduler.add_job(send_emails, 'interval', minutes=1)  # Schedule the job to run every minute for testing
scheduler.start()

if __name__ == "__main__":
    web.run(host="0.0.0.0",debug=True, port=8010)
