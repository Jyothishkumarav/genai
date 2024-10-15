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

generate_des('''Feed Slot Logic:
Identify boost-eligible jobs: Select jobs eligible for boosting based on current logic (Cumulative Fulfilment lagging with respect to run-rate until evaluation).

Calculate Boost Slot Net Score: Add a configurable boost score to the Organic score of eligible jobs based on SKU

Super Premium: +0.5 (Backend config)

Premium: +0.4 (Backend config)

Classic: +0.3 (Backend config)

Bulk: X * Custom SKU score (X = TBD, Backend config)

Jobs not eligible for boosting will retain their original Organic Net Score as the Boost Slot Net Score.

Unified Boost Category: Merge Super Premium, Premium, and Classic boost categories into one unified boost slot. Jobs with higher demand will receive a stronger boost through the increased boost score (as per SKU boost score).

Organic Slot Placement: Select the top-ranked organic job (not placed yet) based on Organic Slot Score and place it in an organic slot.

Boost Slot Placement: From remaining jobs, remove already placed jobs and select the top job by Boost Slot Net Score to fill the boost slots.

Implement deduplication logic across both Organic and Boost slots, based on Job Title * Sub-department * Company (Unique ID).

If a job with the same Unique ID is already placed in any slot above, move the duplicate job to the bottom of the list (above throttled jobs).''')