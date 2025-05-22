from langchain.llms import OpenAI

llm = OpenAI(temperature=0.2)  # or Granite LLM when deployed

def grade_answer(question, student_answer):
    prompt = f"Grade the answer: Q: {question} A: {student_answer}. Also, give brief feedback."
    return llm.predict(prompt)
