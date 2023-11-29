import streamlit as st
import requests
from urllib.parse import quote

# Streamlit app layout
st.title("Financial Statements Search")

# Form
with st.form(key='search_form'):
    state = st.selectbox('State', ['VA'])  # Replace with actual state list
    locality = st.selectbox('Locality', ['City of Harrisonburg', 'County of Orange'])
    fiscal_year = st.selectbox('Fiscal Year', [2022])
    #datapoint = st.selectbox('Select Datapoint', ['total unassigned fund balance'])
    #datapoint = st.text_input('Datapoint')
    datapoint = st.text_input('Datapoint','total unassigned fund balance')
    submit_button = st.form_submit_button(label='Submit')

# Handling form submission
if submit_button:
    # Create JSON object from form data
    data = {
        'state': state,
        'locality': locality,
        'fiscal-year': fiscal_year,
        'datapoint': datapoint
    }

    # API endpoint
    url = 'https://financialstatementssearch.azurewebsites.net/api/httptriggersearchqueryhandler'

    # Post request to the API
    response = requests.post(url, json=data)
    
    # Check if the response is successful
    if response.status_code == 200:
        response_data = response.json()
        pdf_url = response_data.get('pdf-url')
        value = response_data.get('value')
        pages = response_data.get('pages')

        #encoded_pdf_url = quote(pdf_url, safe='')
        encoded_pdf_url = pdf_url.replace(' ', '%20')
        
        # Display the results
        # formatted_value = "${:,}".format(value)
        st.write(f"Value: {value}")
        st.write(f"Source: {encoded_pdf_url}")
        st.write(f"Pages: {pages}")
    else:
        st.error("Failed to fetch data from the API")

# Run the app: streamlit run app.py
