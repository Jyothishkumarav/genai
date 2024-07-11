from langchain_community.llms import Ollama
llm = Ollama(model="llama3")
response = llm.invoke("Being a software quality engineer create test cases for Login functionlity on web site include negative scenarios , can you give it in a tabular form")
print(response)
