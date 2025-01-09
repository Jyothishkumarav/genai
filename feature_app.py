import streamlit as st
from uuid import uuid4
from feature_controller import FeatureController  # Import the controller class
from feature_dto import FeatureDTO  # Import DTO class if not already done
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Initialize FeatureController (which in turn uses FeatureService)
controller = FeatureController()

# Function to generate descriptions or test cases using AI
def generate_description(features):
    llm = ChatGroq(
        temperature=0,
        groq_api_key='gsk_Q',
        model_name="llama-3.1-70b-versatile"
    )
    prompt_feature = PromptTemplate.from_template(
        """
        ### FEATURE DETAILS:
        {feature_description}
        ### INSTRUCTION:
        You are provided with details of a product feature.
        Your job is to return a detailed description of the feature documentation.
        """
    )
    chain_feature = prompt_feature | llm
    res = chain_feature.invoke({"feature_description": str(features)})
    return res.content

def generate_test_cases(features):
    llm = ChatGroq(
        temperature=0,
        groq_api_key='gQ',
        model_name="llama-3.1-70b-versatile"
    )
    prompt_test_case = PromptTemplate.from_template(
        """
        ### FEATURE DETAILS:
        {feature_description}
        ### INSTRUCTION:
        Based on the provided feature details, generate detailed test cases in a tabular form including functional and regression tests.
        """
    )
    chain_feature = prompt_test_case | llm
    res = chain_feature.invoke({"feature_description": str(features)})
    return res.content


# Streamlit UI
st.title("Product Feature Manager")

# Pages for navigation
page = st.sidebar.selectbox("Select Page", ["Add Feature", "Search Feature", "Update Document Status", "Generate Test Cases"])

# Add feature page
if page == "Add Feature":
    st.header("Add New Product Feature")
    with st.form(key="feature_form"):
        feature_desc = st.text_area("Feature Description")
        new_tags = st.text_input("Enter New Tags (comma-separated)")
        all_tags = controller.get_all_tags()
        selected_tags = st.multiselect("Select Existing Tags", all_tags)
        link = st.text_input("Product Document Link")

        # Merge new tags entered by user with the selected ones
        if new_tags:
            selected_tags += [tag.strip() for tag in new_tags.split(",") if tag.strip()]

        submit_button = st.form_submit_button(label="Add Feature")

    if submit_button:
        feature_dto = FeatureDTO(description=feature_desc, tags=selected_tags, link=link, status="active")
        controller.add_feature(feature_dto)
        st.success("Feature added successfully!")

# Search feature page
if page == "Search Feature":
    st.header("Search Product Features")
    search_query = st.text_input("Search by Query")
    search_tags = st.multiselect("Filter by Tags (optional)", controller.get_all_tags())
    num_docs = st.number_input("Number of Documents to Search", min_value=1, max_value=100, value=10)
    search_button = st.button("Search")

    if search_button:
        query_text = search_query if search_query else ""

        if search_tags:
            results = controller.search_features(query_text, search_tags, n_results=num_docs)
        else:
            results = controller.search_features(query_text, n_results=num_docs)

        if results:
            features_combined = ""
            with st.expander("Relevant Documents", expanded=False):
                # To store all the descriptions
                for i, result in enumerate(results):  # Iterate over filtered results
                    st.write(f"Feature {i + 1}: {result}")
                    features_combined += f"\nFeature {i + 1}: {result}"

            # Call AI description generation for all features combined
            if features_combined:
                with st.spinner('Generating AI  documentation...'):
                    generated_desc = generate_description(features_combined)
                    st.write(f"AI-Generated Description for All Features: {generated_desc}")
        else:
            st.write("No matching features found.")

# Update document status page
if page == "Update Document Status":
    st.header("Update Document Status")

    search_query = st.text_input("Search by Query for Document")
    search_button = st.button("Search for Document IDs")

    if search_button:
        results = controller.search_features(search_query)
        if results:
            doc_ids = [doc_id for sublist in results['ids'] for doc_id in sublist]
            documents = results['documents'][0]
            st.session_state['search_results'] = {'doc_ids': doc_ids, 'documents': documents}
        else:
            st.write("No matching documents found.")

    if 'search_results' in st.session_state:
        doc_ids = st.session_state['search_results']['doc_ids']
        if doc_ids:
            selected_doc_id = st.selectbox("Select Document to Update", doc_ids)

            if selected_doc_id:
                st.session_state['selected_doc_id'] = selected_doc_id
                index = doc_ids.index(selected_doc_id)

                if index < len(st.session_state['search_results']['documents']):
                    doc_content = st.session_state['search_results']['documents'][index]
                    st.session_state['document_content'] = doc_content

    if 'document_content' in st.session_state:
        st.text_area("Document Content", st.session_state['document_content'], height=150)

        update_button = st.button("Mark as Inactive")
        if update_button:
            controller.update_feature_status(st.session_state['selected_doc_id'], "inactive")
            st.success(f"Document {st.session_state['selected_doc_id']} marked as inactive!")
if page == "Generate Test Cases":
    st.header("Generate Test Cases for Features")

    search_query = st.text_input("Search by Query")
    search_tags = st.multiselect("Filter by Tags (optional)", controller.get_all_tags())
    num_docs = st.number_input("Number of Documents to Fetch", min_value=1, max_value=100, value=10)
    search_button = st.button("Generate Test Cases")

    if search_button:
        query_text = search_query if search_query else ""

        if search_tags:
            results = controller.search_features(query_text, search_tags, n_results=num_docs)
        else:
            results = controller.search_features(query_text, n_results=num_docs)

        if results:
            features_combined = ""
            with st.expander("Relevant Documents..", expanded=False):
                  # To store all the descriptions
                for i, result in enumerate(results):  # Iterate over filtered results
                    st.write(f"Feature {i + 1}\n: {result}")
                    features_combined += f"\nFeature {i + 1}\n: {result}"

            # Call AI test case generation for all features combined
            if features_combined:
                with st.spinner('generating test cases with AI'):
                    generated_test_cases = generate_test_cases(features_combined)
                    st.write(f"AI-Generated Test Cases for Selected Features: {generated_test_cases}")
        else:
            st.write("No matching features found.")
