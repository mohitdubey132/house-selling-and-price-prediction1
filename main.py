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
 
'''cur = conn.cursor()
cur.execute ("""
              ALTER TABLE BORKER
ADD CONSTRAINT BORKER_unique UNIQUE ( MOBILE_NO ,EMAIL_ID);        
  """)
conn.commit()
conn.close()
'''
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


''' registertion for new user '''
@app.route("/register" ,methods=["POST"])
def register_new():
    f1 = request.form.get("First_Name")
    l1 = request.form.get("Last_Name")
    email  = request.form.get("Email_Id")
    password = request.form.get("Password")
    mobile =  request.form.get("Mobile")
    
    if (f1 or l1 or email or password or mobile)=='':
        return render_template("login.html")

    f1 =f1 +" "+l1
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS,
                        host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    query_insert="""insert into customer (C_NAME,MOBILE_NO,EMAIL_ID,PASSWORD)
              values(%s,%s,%s,%s)  """
    record_to_insert = (f1,mobile,email,password)
    cur.execute(query_insert, record_to_insert)         
    
   # print("record store successfully")

    conn.commit()
    count = cur.rowcount

    conn.close()
   
    return render_template("login.html")




''' search request  routes '''
@app.route("/se", methods=["POST"])
def search():
    city = request.form.get("City")
    Price = request.form.get("Price")
    Balcony = request.form.get("Balcony")
    BHK =request.form.get("BHK")
    print("city",city,"Price",Price)
    return render_template("Agents.html")
@app.route("/login_customer" , methods=["POST"])
def login_customer():
    email = request.form.get("email")
    password= request.form.get("password")
    

    ''' 
   EXECUT EACH CERATE QUERY ONR BY ON USING 
    # CUSTOMER TABLE 
   '''