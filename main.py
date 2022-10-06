from flask import Flask ,render_template, request
import smtplib
import random
import psycopg2
#  add email
'''server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('connectusjecmohit132@gmail.com','owjsnkodweasxjcc' )
'''
DB_NAME = "Ghardekho"
DB_USER = "postgres"
DB_PASS = "github@0"
DB_HOST = "localhost"
DB_PORT = "5432"
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS,
                        host=DB_HOST, port=DB_PORT)
print("Database connected successfully")
 
cur = conn.cursor()
cur.execute ("""
              CREATE TABLE APPOINTMENT(
                APP_ID SERIAL PRIMARY KEY,
                C_ID INTEGER REFERENCES CUSTOMER(C_ID),
                B_ID INTEGER REFERENCES BORKER(B_ID),
                P_ID INTEGER REFERENCES PROPERTY(P_ID),
                A_DATE  DATE NOT NULL
                )            
  """)
conn.commit()
conn.close()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/pass" ,methods=["POST"])
def start():
    num = random.random()
    name =request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    message=name+'this'+password+' is a message genrated'+email+' using python'+' youer  one time password is' +str(num)
    server.sendmail('mohit132@gmail.com', email,message)
    return render_template("pass2.html",email=email,password=password)
 

# Routes for home, about, etc
@app.route("/login")    
def login():
    return render_template("login.html")

@app.route("/Home") 
def home():
    return render_template("index.html")   

@app.route("/About_us")
def about():
    return render_template("AboutUs.html")

''' search request  routes '''
@app.route("/se", methods=["POST"])
def search():
    city = request.form.get("City")
    Price = request.form.get("Price")
    Balcony = request.form.get("Balcony")
    BHK =request.form.get("BHK")
    print("city",city,"Price",Price)
    return render_template("Agents.html")


    ''' 
   EXECUT EACH CERATE QUERY ONR BY ON USING 
    # CUSTOMER TABLE 
   '''