import psycopg2
#  data base coonection 
def connect_db():
      DB_NAME = "Ghardekho"
      DB_USER = "postgres"
      DB_PASS = "github@0"
      DB_HOST = "localhost"
      DB_PORT = "5432"
      conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS,
                           host=DB_HOST, port=DB_PORT)
      print("Database connected successfully")
      cur = conn.cursor()
      return cur,conn
#---------------------------------------------------------------------------------#
def create_customers(f1,mobile,email,password):
            try: 
                  f1,mobile,email,password= f1,mobile,email,password
                  cur,conn = connect_db()
                  query_insert="""insert into customer (C_NAME,MOBILE_NO,EMAIL_ID,PASSWORD)
                              values(%s,%s,%s,%s)  """
                  record_to_insert = (f1,mobile,email,password)
                  cur.execute(query_insert, record_to_insert)                     
                     # print("record store successfully")       
            except Exception as e:
               maessage= "there is an problem "+ str(e)
               return   maessage
            finally :
                  conn.commit()
                  count = cur.rowcount
                  conn.close()


# --------------------------------------------------------------------------------#
def login(email,password):
      try: 
         email,password=email,password
         cur,conn = connect_db()
         query_To_login="select * from customer where email_id = %s and password =%s "
         cur.execute(query_To_login,(email,password,))
         records = cur.fetchall()
         count = cur.rowcount
         return records,count 
      finally:
         conn.commit()
         count= cur.rowcount
         conn.close()
#--------------------------#------------------------$------------------------------#
def login_bro(email,password):
      try: 
         email,password=email,password
         cur,conn = connect_db()
         query_To_login="select * from borker where email_id = %s and password =%s "
         cur.execute(query_To_login,(email,password,))
         records = cur.fetchall()
         count = cur.rowcount
         return records,count 
      finally:
         conn.commit()
         count= cur.rowcount
         conn.close()

#----------------------------------------------------------------------------------#
         #appointment method  
def find_appointment(id):
   try: 
         id=id 
         cur,conn = connect_db()
         print('@1',id)
         appointment ="""select a.a_date , b.b_name, b.mobile_no, p.address from appointment a inner join borker b 
                                       on a.b_id=b.b_id 
                                       inner join property p
                                       on a.p_id= p.p_id
                                       where a.c_id = %s
                                       """
         print("id value # importants  ",id)
         cur.execute(appointment,(id,))
         print('@2')
         results = cur.fetchall()
         return results

   finally:
      conn.commit()
      conn.close()
#-----------------------------------------------------------------------------------#
        #delete appointments 
def delete_appointments(id):
   try:
      cur,conn= connect_db()
      delete_appointment =""" delete from appointment where app_id=%s
                           """
      cur.execute(delete_appointment,(id,))
      message = "recorde deleted successfully"
      return maessage
   except Exception as e:
               maessage= "there is an problem "+ str(e)
               return   maessage

   finally:
      conn.commit()
      conn.close()
                                 

'''
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
create table customer(
                C_ID Serial primary key,
                C_NAME VARCHAR(50),
                MOBILE_NO CHAR(10),
                EMAIL_ID VARCHAR(50),
                PASSWORD VARCHAR(10)
             )   
              ALTER TABLE customer
ADD CONSTRAINT customer_unique UNIQUE ( MOBILE_NO ,EMAIL_ID); 
             create table BORKER(
                B_ID Serial primary key,
                B_NAME VARCHAR(50) NOT NULL,
                MOBILE_NO CHAR(10) NOT NULL,
                EMAIL_ID VARCHAR(50) NOT NULL,
                PASSWORD VARCHAR(10) NOT NULL,
                ADDRESS TEXT
             );  
             ALTER TABLE BORKER
ADD CONSTRAINT BORKER_unique UNIQUE ( MOBILE_NO ,EMAIL_ID);    
              create table PROPERTY(
                P_ID SERIAL PRIMARY KEY,
                TOTAL_SQFT NUMERIC NOT NULL,
                PRICE   INTEGER,
                AREA VARCHAR(50) NOT NULL,
                ADDRESS VARCHAR(50) NOT NULL,
                SIZE SMALLINT,
                BALCONY SMALLINT,
                AVAILABILITY DATE NOT NULL,
                BATH SMALLINT NOT NULL,
                B_ID INTEGER REFERENCES BORKER(B_ID) ON DELETE SET NULL,  
             );
            '''
'''server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('connectusjecmohit132@gmail.com','owjsnkodweasxjcc' )
'''