import streamlit as st
from uuid import uuid4
from chromadb_orchestartor import ChromaDBManager
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Initialize ChromaDB client
client = ChromaDBManager("chroma_db_test1")  # Use a persistent directory

# Function to generate descriptions or test cases using AI
def generate_description(features):
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
        Your job is to return a detailed description of the feature documentation.
        """
    )
    chain_feature = prompt_feature | llm
    res = chain_feature.invoke({"feature_description": str(features)})
    return res.content

# Helper function to get unique tags from the database
def get_all_tags():
    return client.get_all_tags()

# Streamlit UI
st.title("Product Feature Manager")

# Pages for navigation
page = st.sidebar.selectbox("Select Page", ["Add Feature", "Search Feature", "Update Document Status"])

# Add feature page
if page == "Add Feature":
    st.header("Add New Product Feature")
    with st.form(key="feature_form"):
        feature_desc = st.text_area("Feature Description")
        new_tags = st.text_input("Enter New Tags (comma-separated)")
        all_tags = get_all_tags()
        selected_tags = st.multiselect("Select Existing Tags", all_tags)
        link = st.text_input("Product Document Link")

        # Merge new tags entered by user with the selected ones
        if new_tags:
            selected_tags += [tag.strip() for tag in new_tags.split(",") if tag.strip()]

        submit_button = st.form_submit_button(label="Add Feature")

    if submit_button:
        client.add_feature(feature_desc, selected_tags, link)
        st.success("Feature added successfully!")

# Search feature page
if page == "Search Feature":
    st.header("Search Product Features")
    search_query = st.text_input("Search by Query")
    search_tags = st.multiselect("Filter by Tags (optional)", get_all_tags())
    search_button = st.button("Search")

    if search_button:
        query_text = search_query if search_query else ""

        if search_tags:
            results = client.search_features(query_text, search_tags)
        else:
            results = client.search_features(query_text)

        if results:
            st.write("Search Results:")
            features_combined = ""  # To store all the descriptions

            for i, result in enumerate(results):  # Iterate over filtered results
                for res in result:
                    st.write(f"Feature {i + 1}: {res}")
                    features_combined += f"\nFeature {i + 1}: {res}"

            # Call AI description generation for all features combined
            if features_combined:
                generated_desc = generate_description(features_combined)
                st.write(f"AI-Generated Description for All Features: {generated_desc}")
        else:
            st.write("No matching features found.")

# Update document status page
if page == "Update Document Status":

    # Update document status page
    st.header("Update Document Status")

    # Search and retrieve document IDs
    search_query = st.text_input("Search by Query for Document")
    search_button = st.button("Search for Document IDs")

    # Ensure search results are persisted in the session state
    if search_button:
        # Fetch and store the search results in session state
        results = client.search_features(search_query)

        if results:
            # Flatten and store results in session state
            doc_ids = [doc_id for sublist in results['ids'] for doc_id in sublist]
            documents = results['documents'][0]

            # Log the length of doc_ids and documents
            # st.write(f"Number of Document IDs: {len(doc_ids)}")
            # st.write(f"Number of Documents: {len(documents)}")

            st.session_state['search_results'] = {
                'doc_ids': doc_ids,
                'documents': documents
            }
        else:
            st.write("No matching documents found.")

    # Display search results if available in session state
    if 'search_results' in st.session_state:
        # Extract document IDs from the session state
        doc_ids = st.session_state['search_results']['doc_ids']

        if doc_ids:
            # Allow user to select a document ID
            selected_doc_id = st.selectbox("Select Document to Update", doc_ids)

            # Store the selected document ID in session state after selection
            if selected_doc_id:
                st.session_state['selected_doc_id'] = selected_doc_id

                try:
                    # Retrieve the index of the selected document ID
                    index = doc_ids.index(selected_doc_id)

                    # Log the selected index and corresponding document content length
                    # st.write(f"Selected Index: {index}")
                    # st.write(
                    #     f"Document Content at Index {index}: {st.session_state['search_results']['documents'][index]}")

                    # Ensure the index is valid for the document content list
                    if index < len(st.session_state['search_results']['documents']):
                        doc_content = st.session_state['search_results']['documents'][index]
                        st.session_state['document_content'] = doc_content
                    else:
                        st.error(f"Error: Document content not found for the selected document ID.")
                except ValueError:
                    st.error(f"Error: Selected document ID not found in the results.")
                except IndexError:
                    st.error(f"Error: Invalid index when accessing document content.")
        else:
            st.write("No document IDs found in search results.")

    # Display the document content if available in the session state
    if 'document_content' in st.session_state:
        st.text_area("Document Content", st.session_state['document_content'], height=150)

        # Provide a button to mark the document as inactive
        update_button = st.button("Mark as Inactive")
        if update_button:
            client.update_document_status(st.session_state['selected_doc_id'], "active")
            st.success(f"Document {st.session_state['selected_doc_id']} marked as inactive!")

            # Optionally clear session state for the document after the update
            del st.session_state['document_content']
            del st.session_state['selected_doc_id']



