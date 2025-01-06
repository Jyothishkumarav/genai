import json

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


def generate_des(feature):
    llm = ChatGroq(
        temperature=0,
        groq_api_key='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',
        model_name="llama-3.1-70b-versatile"
    )
    prompt_feature = PromptTemplate.from_template(
        """
        ### FEATURE DETAILS:
        {feature_description}
        ### INSTRUCTION:
        You are provided with details of a product feature.
        Your job is to return a detailed description of the feature documentation
        ###  (NO PREAMBLE):
        """
    )
    chain_feature = prompt_feature | llm
    res = chain_feature.invoke({"feature_description": str(feature)})
    print(res.content)

def generate_stock_data(feature):
    llm = ChatGroq(
        temperature=0,
        groq_api_key='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',
        model_name="llama-3.1-70b-versatile"
    )
    prompt_feature = PromptTemplate.from_template(
        """
        ### FEATURE DETAILS:
        {feature_description}
        ### INSTRUCTION:
        You are provided with details of a stock.
        Your job is to return a data in json format and don't mention json in response.
        don't use any preamble and response should be in a json format
        ###  (NO PREAMBLE):
        """
    )
    chain_feature = prompt_feature | llm
    res = chain_feature.invoke({"feature_description": str(feature)})
    response_string = res.content
    json_data = json.loads(response_string)
    json_string = json.dumps(json_data)
    return json_string
def generate_stock_valuation(feature):
    llm = ChatGroq(
        temperature=0,
        groq_api_key='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',
        model_name="llama-3.1-70b-versatile"
    )
    prompt_feature = PromptTemplate.from_template(
        """
        ### FEATURE DETAILS:
        {feature_description}
        ### INSTRUCTION:
        You are being stock analyst and you know to calculate the ideal stock price .You are provided with details of a stock and its ratio.
        Your job is determine and evaluate the stock price and determine it is fairly value d or not.
        explain it in details with calculation and also provide conclusions
        ###  (NO PREAMBLE):
        """
    )
    chain_feature = prompt_feature | llm
    res = chain_feature.invoke({"feature_description": str(feature)})
    response_string = res.content
    return response_string
if __name__ == "__main__":
    response = generate_stock_data('''    "Market Cap ₹ 40,680 Cr. Current Price ₹ 1,484 High / Low ₹ 1,929 / 1,283 Stock P/E 108 Book Value ₹ 62.6 Dividend Yield 0.46 % ROCE 26.6 % ROE 19.9 % Face Value ₹ 10.0 Add ratio to table Edit ratios"''')
    print(response)
    response = generate_stock_valuation(f'''{response}''')
    print(response)