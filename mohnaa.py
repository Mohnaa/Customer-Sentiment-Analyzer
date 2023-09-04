import streamlit as st
import pandas as pd
import openai
import time

# Set up OpenAI API credentials
openai.api_key = "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"

# Generate personalized sentiments using OpenAI API
def generate_sentiment(customer_data):
    prompt = f"I Want you to act as sentiment analyser that will analyse the sentiment:\n"
    prompt += f"Generate sentiment value (Positive, Negative, Neutral) from following data:\n"
    prompt += f"Customer ID: {customer_data['customerid']}\n"
    prompt += f"Name: {customer_data['name']}\n"
    prompt += f"Chat: {customer_data['chat']}\n"
    prompt += f"Consider all the Above customer data and Generate the sentiment."



    # Try to make the API call, and if a rate limit error occurs, wait and retry after a brief delay
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=100,
                temperature=0.1,
                n=1,
                stop=None,
            )
            offer = response.choices[0].text.strip()
            return offer
        except openai.error.RateLimitError as e:
            st.error("Rate limit reached. Waiting for 20 seconds before retrying.")
            time.sleep(20)  # Wait for 20 seconds before retrying

# Function to load data from Excel file
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

def main():
    # Apply custom CSS style to the title and sidebar using HTML tags and inline CSS
    st.markdown("""
        <style>
            h1 {
                color: red;
                text-align: center;
                padding-top: 20px;
                padding-bottom: 20px;
                background-color: yellow; /* Set background color to yellow */
            }
            .sidebar .sidebar-content {
                background-color: yellow;
            }
            .fileinput-button label {
                background-color: red !important;
                color: white !important;
                border-color: red !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Upload and load data from Excel file
    st.sidebar.header("Upload Customer Data")

    # Apply custom style to the file uploader button
    st.markdown(
        """
        <style>
            .fileinput-button:before {
                content: "Upload a file";
                background-color: red;
                color: white;
                display: block;
                border-radius: 5px;
                padding: 8px 16px;
                cursor: pointer;
                # background-color: yellow;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    file = st.sidebar.file_uploader("", type=["xls", "xlsx"])

    if file is not None:
        df = load_data(file)

        # Display the loaded data
        st.header("Loaded Customer Data")
        st.dataframe(df)

        # Generate personalized offers and store them in a DataFrame
        offers_df = pd.DataFrame(columns=["customerid", "name", "chat", "Sentiment"])
        for index, row in df.iterrows():
            try:
                offer = generate_sentiment(row)
                offers_df.loc[len(offers_df)] = [row["customerid"], row["name"], row["chat"], offer]

            except Exception as e:
                st.error(f"Error generating sentiment for customer ID {row['customerid']}: {str(e)}")

        # Set the index of the DataFrame to start from 1
        offers_df.index = offers_df.index + 1

        # Display the generated Sentiment table in the UI
        st.header("Generated Sentiment")
        st.table(offers_df)

if __name__ == "__main__":
    # Display the title only once at the beginning
    st.markdown("<h1>Sentiment Analyzer</h1>", unsafe_allow_html=True)
    main()
