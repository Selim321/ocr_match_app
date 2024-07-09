import streamlit as st
from matcher import check_match

# Initialize the session state for alternate names
if 'alternate_names' not in st.session_state:
    st.session_state.alternate_names = ['']  # Initialize with one alternate name field

# Function to add a new alternate name
def add_alternate_name():
    st.session_state.alternate_names.append('')

# Function to remove an alternate name
def remove_alternate_name(index):
    st.session_state.alternate_names.pop(index)

# Title of the app
st.title("Product Name Matcher")

# Input fields for scanned name and product name
scanned_name = st.text_input("Scanned Name")
product_name = st.text_input("Product Name")

# Alternate names section
st.header("Alternate Names")
for i, alt_name in enumerate(st.session_state.alternate_names):
    st.text_input(f"Alternate Name {i+1}", value=alt_name, key=f'alt_name_{i}')
    st.button(f"Remove Alternate Name {i+1}", on_click=remove_alternate_name, args=(i,))

# Button to add more alternate names
if st.button("Add Alternate Name"):
    add_alternate_name()
    st.experimental_rerun()  # Rerun the script to update the UI immediately

# Button to test match
if st.button("Test Match"):
    alt_names = [st.session_state[f'alt_name_{i}'] for i in range(len(st.session_state.alternate_names))]
    match, matches = check_match(scanned_name, product_name, alt_names, threshold=0.5, n=2)
    if match:
        st.success("Match found!")
        st.write("Matched Words:", matches)
    else:
        st.error("No match found.")