import streamlit as st
import time


def show_progress():

    status = st.empty()

    progress = st.progress(0)

    steps = [

        ("Calculating Process Data...", 30)
      
    ]

    for message, value in steps:

        status.info(message)

        progress.progress(value)

        time.sleep(0.3)

    status.success(
        "Audit Generated Successfully!"
    )

    time.sleep(0.5)

    status.empty()

    progress.empty()
