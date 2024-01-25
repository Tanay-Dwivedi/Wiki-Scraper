import streamlit as st

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "London", "Paris", "Madrid"],
        "correct_option": "Paris",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Mars", "Jupiter", "Venus", "Saturn"],
        "correct_option": "Mars",
    },
]


def display_question(question_data, question_index):
    st.write(f"**Question {question_index}:** {question_data['question']}")
    selected_option = st.radio(
        f"Select an option for question {question_index}:",
        question_data["options"],
        key=f"question_{question_index}",
    )
    return selected_option == question_data["correct_option"], selected_option


st.title("Simple Quiz App")

score = 0
user_answers = {}

with st.form(key="quiz_form"):
    for i, question in enumerate(questions, start=1):
        st.write(f"### Question {i}")
        is_correct, selected_option = display_question(question, i)
        user_answers[f"Question {i}"] = {
            "Option Marked": selected_option,
            "Correct Option": question["correct_option"],
            "Status": "Correct" if is_correct else "Wrong",
        }

    submit_button = st.form_submit_button(label="Submit Quiz")

if submit_button:
    st.write("## Results:")
    for question_num, answer_info in user_answers.items():
        st.write(f"### {question_num}:")
        st.write(f"**Option Marked** - {answer_info['Option Marked']}")
        st.write(f"**Correct Option** - {answer_info['Correct Option']}")
        st.write(f"**Status** - {answer_info['Status']}")
        st.markdown("""-----""")

    score = sum(
        answer_info["Status"] == "Correct" for answer_info in user_answers.values()
    )
    st.write(f"### Your final score: {score}/{len(questions)}")
