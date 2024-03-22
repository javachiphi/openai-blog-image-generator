import streamlit as st

def display_pdf_selector():
    if 'pdf_metadata' in st.session_state and st.session_state['pdf_metadata']:
        pdf_id = st.radio(
            'Select a PDF to interact with:',
            options=list(st.session_state['pdf_metadata'].keys()),
            format_func=lambda x: st.session_state['pdf_metadata'][x]
        )
        return pdf_id
    else:
        st.write("No PDFs uploaded yet.")
        return None