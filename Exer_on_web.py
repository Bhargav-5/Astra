import streamlit as st
import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql2024",
    database="astra"

)
mycursor = mydb.cursor()
print("Connection Established. . . .")
def check_credentials(username, password):
    # Implementing logic to verify username and password against a database
    global dati
    mycursor.execute("select * from signup_details")
    result = mycursor.fetchall()
    found = False
    for row in result:
        if username == row[0] and password == row[1]:
            found = True
            dati = str(datetime.datetime.now())
            sql = "insert into login_details(username,password,date_time_details) values(%s,%s,%s)"
            val = (username, password, dati)
            mycursor.execute(sql,val)
            mydb.commit()
            break
    return found  

def signup_user(username, password, email, phnum):
    sql = "insert into signup_details(username,password,email,phn_num) values(%s,%s,%s,%s)"
    val = (username,password,email,phnum)
    mycursor.execute(sql,val)
    mydb.commit()
    st.success("Signed-Up Succesfully")


st.set_page_config(
    page_title="AI Fitness Trainer",
)


auth_option = st.selectbox("Choose an option", ("Login", "Sign Up"))

if auth_option == "Login":
    login_container = st.container()
    with login_container:
        st.header("Login")
        username_input = st.text_input("Username", key="login-username")
        password_input = st.text_input("Password", type="password", key="login-password")
        login_button = st.button("Login")

        # Login logic
        if login_button:
            if check_credentials(username_input, password_input):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username_input  
                st.session_state["password"] = password_input
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

else:
    signup_container = st.container()
    with signup_container:
        st.header("Sign Up")
        signup_username_input = st.text_input("Username", key="signup-username")
        signup_password_input = st.text_input("Password", type="password", key="signup-password")
        signup_confirm_password_input = st.text_input("Confirm Password", type="password", key="signup-confirm-password")
        signup_email_input = st.text_input("Email", key="signup-email")
        signup_number_input = st.text_input("Phone Number", key="signup-number")
        signup_button = st.button("Sign Up")

        # Signup logic
        if signup_button:
            if signup_password_input == signup_confirm_password_input:
                signup_user(signup_username_input, signup_confirm_password_input, signup_email_input,signup_number_input)  # Replace with your implementation
                st.success("Sign up successful! Please log in.")
            else:
                st.error("Passwords do not match")


if "logged_in" in st.session_state:
    st.write(f"Welcome, {st.session_state['username']}!")
    option = st.sidebar.selectbox("Options",("Exercises","Dashboard",))
    if option == "Dashboard":
        st.title("Your Performance")
        sql = "select * from exercise_logs where username=%s"
        val = (st.session_state['username'],)
        mycursor.execute(sql,val)
        res = mycursor.fetchall()
        for row in res:
            st.write(row)

    exer_option = st.selectbox("Choose an exercise", ("---None---","Pushups", "Squats"))
    if exer_option == "Pushups":
        from Pushup_classes import Live_Pushups
        push = Live_Pushups()
        push.livePushups()
        sql_insert = "insert into exercise_logs(username,date_time,exercise_name,reps_made) values(%s,%s,%s,%s)"
        val_insert = (st.session_state['username'],st.session_state['password'],exer_option,str(int(push.cnt)))
        mycursor.execute(sql_insert,val_insert)
        mydb.commit()
        
        
    elif exer_option == "Squats":
        from Squats_classes import Squats_Live
        sqt = Squats_Live()
        sqt.liveSquats()
        sql_insert = "insert into exercise_logs(username,date_time,exercise_name,reps_made) values(%s,%s,%s,%s)"
        val_insert = (st.session_state['username'],st.session_state['password'],exer_option,str(int(sqt.squat_ctr)))
        mycursor.execute(sql_insert,val_insert)
        mydb.commit()
    else:
        st.write("***** No Exercise Chosen *****")
        
    