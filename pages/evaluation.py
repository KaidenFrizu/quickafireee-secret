import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="osu!Quickfire Registration",
    page_icon=":fire:", initial_sidebar_state="collapsed")

# HACK: This is to get rid of the sidebar
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

with open("EVALUATION_HEADER.md", encoding="utf-8") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

with st.form("evaluation_form", clear_on_submit=True):
    # Parse our CSV file
    # TODO: Get this from a more reliable datasource, maybe google sheets?
    df = pd.read_csv("evaluation.csv")
    # Sample only 10 questions
    df = df.sample(10)
    # Get the questions, their choices and their correct answers
    questions = df["question"].tolist()
    # This is comma separated, so we need to split it
    choices = df["choices"].tolist()
    correct_answers = df["correct answer"].tolist()
    user_quiz_answers = []

    # Enumarate the questions and choices
    for question, choice in zip(questions, choices):
        # Convert choices into a list
        choice = choice.split(",")
        # Ask the user the question
        user_answer = st.radio(question, choice)
        # Append the user's answer to the list
        user_quiz_answers.append(user_answer)

    # Check if the user's answers are correct
    if st.form_submit_button("Submit"):
        evaluated_correct_answers = 0
        # Enumarate the user's answers and the correct answers
        for user_answer, correct_answer in zip(user_quiz_answers, correct_answers):
            # If the users' correct answer is the same as the correct answer, pass them
            if user_answer == correct_answer:
                evaluated_correct_answers += 1

        # If the user got all the answers correct, pass them
        if evaluated_correct_answers == len(correct_answers):
            st.success("You passed the evaluation! You can now register for the tournament.")
            switch_page("register")
        else:
            st.error("You got some answers wrong. Try again!.")
