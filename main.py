from flask import Flask ,render_template, request, session, redirect,jsonify,flash
from flask_cors import cross_origin
from flask_session import Session
import smtplib
import random
import psycopg2
import db
import BangalorePricePrediction as tm
import os 
import datetime
from werkzeug.utils import secure_filename   
UPLOAD_FOLDER ='D:\\modules\\static\\uploads_home'
ALLOWED_EXTENSIONS= {'jpg','jpeg'}
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
Session(app)
 
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


@app.route("/")
def index():
    Property =db.get_property()
    return render_template("index.html" ,propertys= Property ) 
@app.route("/2")
def index2():
    Property =db.get_property()
    return render_template("index.html" ,propertys= Property ) 
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

@app.route("/login_2")    
def login_2():
    return render_template("login_broker.html")

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
    db.create_customers(f1,mobile,email,password)    
    return render_template("login.html")




''' search request  routes '''
@app.route("/search", methods=["POST"])
def search():
    Area_type = request.form.get("Area_type")
    Price = request.form.get("Price")
    Balcony = request.form.get("Balcony")
    BHK =request.form.get("BHK")
    print("city","Price",Price)

    Property =db.get_property_2(Area_type,Price,Balcony,BHK)
    return render_template("index.html" ,propertys= Property )
    



@app.route("/login_customer" , methods=["POST"])
def login_customer():
    email = request.form.get("email")
    password= request.form.get("password")
    email = email.replace("'","")
    email = email.lower()
    password = password.replace(";","")
    try:
        records,count =db.login(email,password)  
        print ("login successful no error in that") 
        flag = 'no'
        if count != 1:
            flag = 'y'
            print ("count==",count,email,'   ',password)
            return render_template("login.html",alart = flag)
        # print("record store successfully")       
    
        #maessage= "there is an problem "+ str(e)            try to remove problems 
       #SSSS return   maessage
    
         #conn.close()
       # ''' retriving user infomation  '''
        id = 0
        for record in records:
            id = record[0] 
            print(id)
            name= record[1]
            mobile = record[2]
            email = record[3]
        session["c_id"] = id
        session["name"] = name
        results = db.find_appointment(str(id))
        print(results)
        print ("find_appointment  successful no error in that")
        return render_template("customer_dashboard.html",c_name=name,Mobile=mobile,Email=email,appointments=results)
    except Exception as e:
        message= str(e)
        return render_template("error.html",error= message)
    ''' 
   EXECUT EACH CERATE QUERY ONR BY ON USING 
    # CUSTOMER TABLE 
   '''
#--------------------------------------------------------------------------------
       #broker loging 
@app.route("/login_broker" , methods=["POST"])
def login_broker():
    email = request.form.get("email")
    password= request.form.get("password")
    email = email.replace("'","")
    email = email.lower()
    password = password.replace(";","")
    try:
        records,count =db.login_bro(email,password)  
        print ("login successful no error in that route loging broker") 
        flag = 'no'
        if count != 1:
            flag = 'y'
            print ("count==",count,email,'   ',password)
            return render_template("login_broker.html",alart = flag)
        # print("record store successfully")       
    
        #maessage= "there is an problem "+ str(e)            try to remove problems 
       #SSSS return   maessage
    
         #conn.close()
       # ''' retriving user infomation  '''
        id = 0
        for record in records:
            id = record[0] 
            print(id)
            name= record[1]
            mobile = record[2]
            email = record[3]
        session["c_id"] = id
        print(session["c_id"],"by login ")
        session["name"] = name
        session['email'] = email
        results = db.find_appointment_brokers(str(id))
        print ("find_appointment  successful no error in that broker")
        return render_template("broker_dash.html",c_name=name,Mobile=mobile,Email=email,appointments=results)
    except Exception as e:
        message= str(e)
        return render_template("error.html",error= message)

''' registertion for new user '''
@app.route("/register_broker" ,methods=["POST"])
def register_new_broker():
    f1 = request.form.get("First_Name")
    l1 = request.form.get("Last_Name")
    email  = request.form.get("Email_Id")
    password = request.form.get("Password")
    mobile =  request.form.get("Mobile")
    address = request.form.get("Address")
    if (f1 or l1 or email or password or mobile)=='':
        return render_template("login.html")

    f1 =f1 +" "+l1
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS,
                            host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        query_insert="""insert into borker (b_NAME,MOBILE_NO,EMAIL_ID,PASSWORD,ADDRESS)
                values(%s,%s,%s,%s,%s)  """
        record_to_insert = (f1,mobile,email,password,address)
        cur.execute(query_insert, record_to_insert)                     
        # print("record store successfully")       
    except Exception as e:
        maessage= "there is an problem "+ str(e)
        return   maessage
    finally :
         conn.commit()
         count = cur.rowcount
         conn.close()    
    return render_template("login_broker.html")

#---------------------------------------------------------------------------------------
    #logout user
@app.route("/log_out")
def logout():
    session["name"] = None
    session["c_id"] = None
    
    return redirect("/")
#----------------------------------------------------------------------------------------
    #delete  appointment  
@app.route("/delete/<string:id>",methods=['POST','GET'])
def delete_app(id):
    db.delete_appointments(id)
    return redirect("/login_customer2")
#---------------------------------------------------------------------------------------
    #reschedule
@app.route("/reschedule/<string:id> ",methods=['POST','GET'])
def reschedule_app(id):
    #if db.reschedule_appointments(id):
    pass
    return redirect("/index.html")   
#--------------------------------------------------------------------------------------
   # Book_appointment 
@app.route("/book_appointment/<string:p_id>/<string:b_id>",methods=['POST','GET'])
def book_appointment_customer(p_id,b_id):
    print(p_id,"getting property id",b_id)
    if "c_id" in session:
        user_id = session["c_id"]
    else :
        return redirect("/login")
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
    NextDay_Date =NextDay_Date.strftime ('%d-%m-%Y')
    print (NextDay_Date)
    try:
        db.create_appointment(user_id,b_id,p_id,NextDay_Date)
        flash('Your appointment is booked ',)
        return redirect(url_for('/2'))
    except :
        Property =db.get_property()
        return render_template("index.html" ,propertys= Property )

#--------------------------------------------------------------------------------------
@app.route("/add_proprtry",methods=['POST'])
def add_proprtrys():
    if request.method=="POST":
       print('add propety link working')
       try:
            print(session["c_id"],"by login  again")
            #print(type(session["C_id"]))
            if "c_id" in session:
                user_id = session["c_id"]
                print(user_id,"session access susseefully")

            Sqft = float(request.form.get('sqft'))
            print(Sqft)
            Bhk=   int(request.form.get('bhk'))
            print(Bhk)
            Address = str(request.form.get('address'))
            print(Address)
            Balcony = int(request.form.get('balconny'))
            print(Balcony)
            Bath = int(request.form.get('bath'))
            print(Bath)
            Date = str(request.form.get('date'))
            print(Date)
            Price= float(request.form.get('price'))
            print(Price)
            Area_type=str(request.form.get('Area_type'))
            print(Area_type)
            if (Sqft or Bhk or Address or Balcony or Bath or Date or Price or user_id)== None:
                    return render_template("login_dash.html")
            else:
                print("all parameters have vales")
            try:
                db.add_proprtry(Sqft,Bhk,Address,Balcony,Bath,Date,Price,Area_type,user_id)  
            except Exception as e:
                message= str(e)
                print("message",maessage)
            return render_template("error.html",error= message)   
       except:
        print("not working")
    return redirect("/login_broker_2")
#--------------------------------------------------------------------------------------
   #  here start the data science part

@app.route("/pridict_home")
def home_pridict():
    return ("/home.html")

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': tm.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_area_names', methods=['GET'])
def get_area_names():
    response = jsonify({
        'area': tm.get_area_values()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_availability_names', methods=['GET'])
def get_availability_names():
    response = jsonify({
        'availability': tm.get_availability_values()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/pridict_home1")
@cross_origin()
def home1():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
#@cross_origin()
def predict():
    if request.method == "POST":
        sqft = float(request.form['sqft'])
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        loc = request.form.get('loc')
        area = request.form.get('area')
        availability = request.form.get('avail')

        prediction = round(float(tm.predict_house_price(loc, area, availability, sqft, bhk, bath)), 2)
        prediction /=10
        return render_template('home.html', prediction_text="The house price is Rs. {} lakhs".format(prediction))

    return render_template("home.html")

   #
def allowed_file(filename):
     return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload_image', methods=['GET', 'POST']) 
def upload_file():
     if request.method == 'POST': 
        # check if the post request has the file part
        print(type(request.files)) 
        if (request.files== None):
            print("nono nothing here")

        if 'file1' not in request.files: 
            #flash('No file part')
            print("error point 1") 
            return  "there is no files" 
        file = request.files['file1'] 
        # if user does not select file, browser also 
        # submit an empty part without filename 
        if file.filename == '': 
            flash('No selected file')
            print("error point 2")
            return redirect('/broker_dash.html') 
        if file and allowed_file(file.filename):
             filename = secure_filename(file.filename) 
             create_filename=filename.split('.')

             print(type(file.filename))
             print(filename)
             print("error in saving of image")
             file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename)) 
             print("error point 3")
             return redirect(url_for('uploaded_file', filename=filename)) 
     return   """<!doctype html> <title>Upload new File</title> <h1>Upload new File</h1> <form method=post enctype=multipart/form-data> <input type=file > <input type=submit value=Upload> </form>  """          
#-----------------------------------------------------------------------------------------------------------#
     # redirect urls
@app.route("/login_broker_2" )
def login_broker_2():
    if "c_id" in session:
        user_id = session["c_id"]
    else:
        return render_template("login_broker.html")
    
    try:
        records,count =db.login_broker_2(user_id)  
        print ("login successful no error in that route loging broker") 
        flag = 'no'
        if count != 1:
            flag = 'y'
            print ("count==",count,email,'   ',password)
            return render_template("login_broker.html",alart = flag)
        id = 0
        for record in records:
            id = record[0] 
            print(id)
            name= record[1]
            mobile = record[2]
            email = record[3]
        results = db.find_appointment_brokers(str(id))    
        print ("find_appointment  successful no error in that broker")
        return render_template("broker_dash.html",c_name=name,Mobile=mobile,Email=email,appointments=results)
    except Exception as e:
        message= str(e)
        return render_template("error.html",error= message)
     #redirect customer2
@app.route("/login_customer2")
def login_customer2():
    if "c_id" in session:
        user_id = session["c_id"]
    else:
        return render_template("login_customer.html")
    
    try:
        records,count =db.login_customer_2(user_id)  
        print ("login successful no error in that route loging broker") 
        flag = 'no'
        if count != 1:
            flag = 'y'
            print ("count==",count,email,'   ',password)
            return render_template("login_customer.html",alart = flag)
        id = 0
        for record in records:
            id = record[0] 
            print(id)
            name= record[1]
            mobile = record[2]
            email = record[3]
        results = db.find_appointment(str(user_id))    
        print ("find_appointment  successful no error in that broker")
        return render_template("customer_dashboard.html",c_name=name,Mobile=mobile,Email=email,appointments=results)
    except Exception as e:
        message= str(e)
        return render_template("error.html",error= message)

#-----------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=False)
#allowed_file(filename): return '.' in filename and \ filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS @app.route('/', methods=['GET', 'POST']) def upload_file(): if request.method == 'POST': # check if the post request has the file part if 'file' not in request.files: flash('No file part') return redirect(request.url) file = request.files['file'] # if user does not select file, browser also # submit an empty part without filename if file.filename == '': flash('No selected file') return redirect(request.url) if file and allowed_file(file.filename): filename = secure_filename(file.filename) file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) return redirect(url_for('uploaded_file', filename=filename)) return ''' <!doctype html> <title>Upload new File</title> <h1>Upload new File</h1> <form method=post enctype=multipart/form-data> <input type=file name=file> <input type=submit value=Upload> </form> '''