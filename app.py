import streamlit as st
import pandas as pd

# Data storage (replace with database in a real app)
DATA_FILE = "maids_data.csv"

# Load data
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Location", "Skills"])

# Save data
def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# Main application
def main():
    st.title("Maid for Each Other")
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Menu", ["Home", "Register", "Search"])

    # Home page
    if menu == "Home":
        st.write("""
        Welcome to **Maid for Each Other**! 
        - Register as a maid to offer your services.
        - Search for maids based on location and skills.
        """)
    
    # Register page
    elif menu == "Register":
        st.header("Register as a Maid")
        with st.form("register_form"):
            name = st.text_input("Name")
            location = st.text_input("Location")
            skills = st.text_input("Skills (comma-separated)")
            submitted = st.form_submit_button("Register")
        
        if submitted:
            data = load_data()
            # new_entry = {"Name": name, "Location": location, "Skills": skills}
            # data = pd.concat(new_entry, ignore_index=True)
            new_entry = pd.DataFrame([{"Name": name, "Location": location, "Skills": skills}])
            data = pd.concat([data, new_entry], ignore_index=True)
            save_data(data)
            st.success(f"Successfully registered {name}!")

    # Search page
    elif menu == "Search":
        st.header("Search for a Maid")
        location_query = st.text_input("Enter location to search")
        skill_query = st.text_input("Enter required skill(s)")

        if st.button("Search"):
            data = load_data()
            if data.empty:
                st.warning("No maids found.")
            else:
                results = data
                if location_query:
                    results = results[results["Location"].str.contains(location_query, case=False, na=False)]
                if skill_query:
                    results = results[results["Skills"].str.contains(skill_query, case=False, na=False)]
                
                if results.empty:
                    st.warning("No maids match your search criteria.")
                else:
                    st.write("### Search Results")
                    st.dataframe(results)

# Run the app
if __name__ == "__main__":
    main()
