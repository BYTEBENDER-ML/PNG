from langchain_community.llms import OpenAI

llm = OpenAI(temperature=0.2)
response = llm.predict("What is the capital of France?")
print(response)