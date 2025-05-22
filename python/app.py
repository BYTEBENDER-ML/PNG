import streamlit as st
from grading_model import grade_answer
from recommender import recommend_topic
import pandas as pd

# Title of the app
st.title("Smart Learning Assistant")
st.markdown("Helping students learn smarter, not harder 💡")

# Section: Input question and answer
st.subheader("📘 Practice Question")
question = st.text_input("Enter your question:")
student_answer = st.text_area("Your Answer:")

if st.button("Submit Answer"):
    if question.strip() and student_answer.strip():
        result = grade_answer(question, student_answer)
        st.success("✅ Feedback:")
        st.write(result)
    else:
        st.warning("Please provide both a question and your answer.")

# Divider
st.markdown("---")

# Section: Learning suggestions
st.subheader("📊 Personalized Learning Suggestions")

# Simulated performance data
performance_data = pd.DataFrame({
    'topic': ['Algebra', 'Geometry', 'Trigonometry'],
    'score': [40, 70, 45]  # Let's say scores out of 100
})

suggestions = recommend_topic(performance_data)

if suggestions:
    st.write("You may want to review the following topics:")
    for topic in suggestions:
        st.markdown(f"- {topic}")
else:
    st.write("Great job! You're doing well across all topics.")