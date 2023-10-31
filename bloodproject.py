# from openpyxl import load_workbook
import streamlit as st
# from twilio.rest import Client
import pandas as pd
import time
import sqlite3
# account_sid = 'ACea0e5c4ddb76a56f084758045b3b78b6'
# auth_token = 'ae2291601e317634771dcb2e5b827ef7'
connection = sqlite3.connect('bloodbase.db')
cursor = connection.cursor()



key0 = 0
flag = 1
flag0 = 0
id0 = ''
pass0 = ''

blood_list = ['A+','B+','AB+','O+','A-','B-','AB-','O-']
cities = ["Mumbai","Pune","Nagpur","Thane","Nashik","Aurangabad","Solapur","Amravati",
          "Kolhapur","Navi Mumbai","Akola","Sangli","Jalgaon","Latur","Dhule","Ahmednagar",
          "Ichalkaranji","Chandrapur","Parbhani","Jalna","Bhusawal","Nanded","Wardha","Yavatmal",
          "Satara","Beed","Osmanabad","Nandurbar","Gondia","Washim","Hinganghat","Buldana",
          "Ambajogai","Yawal","Udgir","Shrirampur","Anjangaon","Manmad","Uran","Pandharpur",
          "Wai","Sillod","Wardha","Malkapur","Wani",]


st.sidebar.subheader('WELCOME')
operation = st.sidebar.radio("Select", ["Add Donor", "Recipient",'About/Contact Us','Admin Panel'])
       
def login(id0,pass0):
    if id0 == 'SAADTEST' and pass0 == 'GENU':
        return 1
    else:
        return 2

def write_to_file(name,blood,number,city):
    # Insert data into the "users" table
    cursor.execute("INSERT INTO blooddatabase (name,blood,number,city) VALUES (?, ?, ?, ?)", (name, blood, number, city))
    connection.commit()

x,y,q,w,e,r,a,b = st.columns(8)
login = a.button('LogIn')
admin = b.button('Report')


rows = cursor.fetchall()

###################################################################        
if operation == 'Add Donor':
    st.header('Donor Registration Form')

    with st.form('form' , clear_on_submit=True):
        name = st.text_input('Enter Your Full Name')
        name = name.upper()
        col1,col2 = st.columns(2)
        number0 = col1.text_input('Enter Your Phone Number(IN)',max_chars=10)
        number = '+91 '+ number0
        blood = col2.selectbox('Select Blood Group', blood_list)
        city = st.selectbox('Select City' , cities)
        checkbox = st.checkbox('I Acknowledge that I dont have any Blood Related Disease',value=True)
        sub_button = st.form_submit_button('Submit')
    if checkbox:
        if sub_button:
             if name == '' or number == '':
                 error3 = st.error('Fill ALL THE FIELDS')
                 time.sleep(3)
                 error3.empty()
             elif len(number)!=14:
                 error4 = st.error('Invalid Number')
                 time.sleep(3)
                 error4.empty()
                 
             else:
                    cursor.execute("SELECT * FROM blooddatabase WHERE number = ?", (number,))
                    existing_row = cursor.fetchone()
                    if existing_row:
                         warn0 = st.error('USER ALREDY EXIST !!!') 
                         time.sleep(2)
                         warn0.empty()
                         flag0 = 1     
                    else:
                        write_to_file(name,blood,number,city)
                        sucs = st.success('Form Submitted')
                        time.sleep(5)
                        sucs.empty()
    else:
        error0 = st.error('Please Acknowledge the Checkbox else You are not Eligible as a Donor')
        time.sleep(3)
        error0.empty()

###################################################################
elif operation == 'Recipient':
    
    st.warning('App is Under Construction in this section')
    data1 = []
    data2 = []
    # data3 = []
    st.header('Find Donor')
    with st.form('form2'):
        col1,col2 = st.columns(2)
        # number = col1.text_input('Enter Your Phone Number',value= '+91 ')
        blood = col1.selectbox('Select Blood Group', blood_list)
        city0 = col2.selectbox('Select City' , cities)
        sub_button = st.form_submit_button('Find')
    
    

    if sub_button:
    # Query the database to fetch data based on city and blood type
        cursor.execute("SELECT name, number, blood FROM blooddatabase WHERE city = ? AND blood = ?", (city0, blood,))
        result = cursor.fetchall()
        for row in result:
            name, number, blood = row
            data1.append({
                'Name': name,
                'Phone': number,
                'Blood Group': blood
                })
        cursor.execute("SELECT name, number, blood,city FROM blooddatabase WHERE city != ? AND blood = ?", (city0,blood,))
        result2 = cursor.fetchall()
        for row in result2:
            name, number, blood,city = row
            data2.append({
                'Name': name,
                'Phone': number,
                'Blood Group': blood,
                'City': city0
            })

    if data1:
        st.subheader(f'Available Donors for {blood}/O+ in {city0}')
        st.table(pd.DataFrame(data1))
    else:
        if sub_button:
            st.write(f'Not Any {blood} Donor Available in {city0}')
    if data2:        
        st.subheader(f'Available Donors for {blood}/O+ Across Maharashtra')
        st.table(pd.DataFrame(data2))
    else:
        if sub_button:
            st.write(f'Not Any {blood} Donor Available in Maharashtra Right now')
         
        
###################################################################

elif operation == 'Admin Panel':
    st.success("Thank You For Visiting (under Construction)")
    st.header('Admin Panel')
    # df = pd.read_excel(path)
    user_credentials = {
        'saad': 'saad',
        'genu': 'genu',
    }
    with st.form('form5',clear_on_submit=True):
        col1,col2 = st.columns(2)
        username = col1.text_input('Username')
        password = col2.text_input('Password', type='password')
        login_button = st.form_submit_button('Login')
    def authenticate_user(username, password):
        if username in user_credentials and user_credentials[username] == password:
            return True
        else:
            return False
    key1 = 0
    if login_button:
        if authenticate_user(username, password):
            st.success('Logged in successfully!')
            key1 = 1
        else:
            error = st.error('Authentication failed. Please check your credentials.')       
            time.sleep(2)
            error.empty()
        if key1 == 1:
                st.subheader('All Donors !')
                # st.table(df)
                logout = st.button('logout')
                if logout:
                    st.epmty()
        else:
            st.error('You must log in to access this content.')

###################################################################

elif operation == 'About/Contact Us':
    st.header('Contact Us')
    st.subheader("Reach us at saadfoundation@gmail.com")
    a1,b1 = st.columns(2)
    a1.text_input('Enter Your Name')
    b1.text_input('Enter Your Mail-id')
    st.text_area('Write a Message',max_chars=200)
    # st.link('dss.com')
connection.commit()
connection.close()

# if about:
    # operation = 0
#     st.empty()
#     st.write('Welcome')
    # page()

