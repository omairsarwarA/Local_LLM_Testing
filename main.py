from llm_service import LocalLLM

llm = LocalLLM("gemma3:1b")
user_query = "write test script to test login module of ecommerce website"
print(user_query)
response = llm.ask(user_query)
print(response)