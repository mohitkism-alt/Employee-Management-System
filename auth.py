import streamlit as st

def login():

    st.title(
        "Employee Login"
    )

    u=st.text_input(
        "Username"
    )

    p=st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if(
            u=="admin"
            and
            p=="123"
        ):

            st.session_state.auth=True

            st.rerun()

        else:

            st.error(
                "Invalid"
            )