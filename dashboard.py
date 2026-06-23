import streamlit as st

def cards(df):

    c1,c2=st.columns(2)

    with c1:

        st.metric(
            "Employees",
            len(df)
        )

    with c2:

        if len(df):

            st.metric(
                "Avg Salary",
                f"₹{df.salary.mean():,.0f}"
            )