#1. IMPORT SECTION

import streamlit as st  # ui banane ke liye
import pandas as pd    # data handle karne ke liye
import database       #  sq lite operations(crud)
import auth           # login authentication

#2. DATABASE INITIALIZATION

database.init_db() #  init_b -> database aur employee table create karta ha agar exit nhi karta

#3.  PAGE CONFIGURATION.

st.set_page_config(page_title="Employee Management System", layout="wide")  # page title aur layout set karta hai.

#4. SESSION STATE(LOGIN CONTROL)

if "auth" not in st.session_state:  # st.session_state -> tempory memory maintain karta ha.
    st.session_state.auth=False    # agar true hua to login hogaya

#5. # LOGIN AUTHENTICATION

if not st.session_state.auth:
    auth.login()   # login()-> username/password verify karta ha.
    st.stop()      # st.stop-> login hone tak app app ko stop karte ha.

# --- CUSTOM CSS FOR BLUE HEADER + CARDS ---

#6. CSS STYLING KAR RAHE HA

# st.markdown-> custom html /css apply karne ke liye

st.markdown("""   
    <style>
  .main-header {
        background: #1e88e5;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
  .metric-card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        color: #262730!important;
        border: 1px solid #e0e0e0;
    }
   .metric-card h3 {
        color: #1e88e5!important;
        margin: 5px 0;
        font-size: 24px;
    }
   .metric-card b {
        color: #262730!important;
        font-size: 14px;
    }
    div[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# --- BLUE HEADER ---

#7. HEADER (ST.MARKDOWN())-> blue title me show hoga

st.markdown('<div class="main-header"><h2>Employee Management System</h2></div>', unsafe_allow_html=True)

# --- LOGOUT ---

#8. SIDEBAR LOGOUT

if st.sidebar.button("Logout"): #st.sidebar.button-> side bar me button banta ha
    st.session_state.auth = False
    st.rerun()  # app referesh karta ha

#9.  FECH DATA

df=database.fetch()  #-> database se data laata hai

# --- TOP METRIC CARDS ---

#10. columns
# len(df)-> rows count karta ha
col1, col2, col3, col4 = st.columns(4)  #st.columns(4)-> screen divide karta ha
with col1:
    st.markdown(f'''
    <div class="metric-card">
        👥<br>
        <b>Total Employees</b><br>
        <h3>{len(df)}</h3>  
    </div>
    ''', unsafe_allow_html=True)

with col2:
#12. AVERAGE SALARY

    avg_sal = df['salary'].mean() if not df.empty else 0  # mean()->average nikalta ha
    st.markdown(f'''
    <div class="metric-card">
        💰<br>
        <b>Average Salary</b><br>
        <h3>₹{avg_sal:,.0f}</h3>
    </div>
    ''', unsafe_allow_html=True)

with col3:
#13. FILTER MALE/FEMALE

    male_count = len(df[df['gender'] == 'Male'])  #df[df['gender'] == 'Male'])  -> condition apply karta ha
    st.markdown(f'''
    <div class="metric-card">
        👨<br>
        <b>Male Employees</b><br>
        <h3>{male_count}</h3>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    female_count = len(df[df['gender'] == 'Female'])
    st.markdown(f'''
    <div class="metric-card">
        👩<br>
        <b>Female Employees</b><br>
        <h3>{female_count}</h3>
    </div>
    ''', unsafe_allow_html=True)

# --- LEFT FORM + RIGHT TABLE LAYOUT ---
left_col, right_col = st.columns([1, 3])

# --- LEFT SIDE FORM ---
with left_col:
    st.subheader("Add Employee")

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    if st.session_state.edit_id:
        emp_data = df[df['id'] == st.session_state.edit_id].iloc[0]
        btn_text = "Save Changes"
    else:
        emp_data = pd.Series({'id':'', 'name':'', 'phone':'', 'role':'Web Developer', 'gender':'Male', 'salary':0})
        btn_text = "Add Employee"

    roles_list = ["Web Developer", "Data Scientist", "DevOps Engineer", "Technical Writer", "Network Engineer", "Business Analyst", "IT Consultant", "Cloud Architect"]

#14. ST.FORM()

    with st.form("employee_form", clear_on_submit=True):    # st.form -> input group create karta ha
        id=st.text_input("Id", value=emp_data['id'], disabled=st.session_state.edit_id is not None)  #st.text_input -> text input
        name=st.text_input("Name", value=emp_data['name'])
        phone=st.text_input("Phone", value=emp_data['phone'])
        role=st.selectbox("Role", roles_list, index=roles_list.index(emp_data['role']) if emp_data['role'] in roles_list else 0)
          # st.selectbox() -> droupdown ke liye use hota ha
       
        gender=st.selectbox("Gender", ["Male", "Female"], index=["Male", "Female"].index(emp_data['gender']) if emp_data['gender'] in ["Male", "Female"] else 0)
        
        # st.number_input() -> number input ke liye use hota ha
        salary=st.number_input("Salary", value=float(emp_data['salary']))

               #st.form_submit_button() -> submit button ke liye use hota ha
        submit = st.form_submit_button(btn_text, use_container_width=True, type="primary")

        if submit:
            if st.session_state.edit_id:
                database.update((id, name, phone, role, gender, salary)) #database.update()->employee edit karta ha
                st.success("Updated!")
                st.session_state.edit_id = None
            else:
                if id in df['id'].values:
                    st.error("ID exists!")
                else:
                    database.insert((id, name, phone, role, gender, salary))  #database.inser-> create ya employee add karta ha
                    st.success("Added!")
            st.rerun()
                    
            
                   

    st.markdown("---")
    st.write("**Update / Delete Employee**")

    # Sirf 1 baar selectbox hai ab, unique key ke saath
    selected_id = st.selectbox("Select ID", df['id'].values if not df.empty else [], key="select_emp")

    col_upd, col_del, col_new = st.columns(3)
    with col_upd:
        if st.button("Load for Update", use_container_width=True, key="load_btn"):
            if selected_id:
                st.session_state.edit_id = selected_id
                st.rerun()

    with col_del:
        if st.button("Delete Employee", use_container_width=True, type="primary", key="del_btn"):
            if selected_id:
                database.delete(selected_id)   #database.delete -> employee remove karta ha
                st.success(f"Deleted {selected_id}")
                st.session_state.edit_id = None
                st.rerun()

    with col_new:
        if st.button("New Employee", use_container_width=True, key="new_btn"):
            st.session_state.edit_id = None
            st.rerun()

# --- RIGHT SIDE TABLE + CHARTS ---

# SEARCH SYSTEM(SEARCH KAREGA)

with right_col:
    search_term = st.text_input("🔍 Search by Name, ID, or Role", placeholder="Type to search...", key="search_box")

    df_display = df.copy()
    if search_term:
        df_display = df_display[
            df_display['name'].str.contains(search_term, case=False, na=False) |  # str.contains -> search filter karta ha
            df_display['id'].str.contains(search_term, case=False, na=False) |
            df_display['role'].str.contains(search_term, case=False, na=False)
        ]
    df_display = df_display[df_display['id'].astype(str).str.strip()!= '']

    btn_col1, btn_col2, btn_col3 = st.columns([1,1,4])
    with btn_col1:
        if st.button("Show All", key="show_all"):
            st.rerun()
    with btn_col2:

        #st.download_button -> csv download karta ha.
        st.download_button("Export CSV", df.to_csv(index=False), "employees.csv", key="export_csv")

                                     # df.to_csv ->data convert karta hai.
                                    
# TABLE DISPLAY

    st.dataframe(    # st.dataframe -> interactive tabe banata hai.
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": "ID",
            "name": "Name",
            "phone": "Phone",
            "role": "Role",
            "gender": "Gender",
            "salary": st.column_config.NumberColumn("Salary", format="₹%d")
        }
    )

     # CHARTS

    if not df.empty:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.subheader("Employees by Role")
            role_count = df['role'].value_counts()
            st.bar_chart(role_count)   # st.bar_chart -> for bar chart-> role analysis.
        with chart_col2:
            st.subheader("Salary Analysis")
            st.line_chart(df.set_index('id')['salary'])  #  st.line_chart() ->line chart ->(salary analysis)
              
              
