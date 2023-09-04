import streamlit as st
import mysql.connector
import openai

# Set up OpenAI API credentials
openai.api_key = "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"

# Function to establish a connection to the MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="temp"
    )

# Function to insert sentiment data into the MySQL database
def insert_sentiment_into_db(connection, customer_id, name, chat, sentiment):
    query = "INSERT INTO users (customer_id, name, chat, sentiment) VALUES (%s, %s, %s, %s)"
    values = (customer_id, name, chat, sentiment)
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        st.success("Sentiment data inserted into the database.")
    except Exception as e:
        connection.rollback()  # Rollback the transaction if there's an error
        st.error(f"Error inserting sentiment data: {str(e)}")
    finally:
        cursor.close()

# Generate personalized sentiments using OpenAI API
def generate_sentiment(name, chat):
    prompt = f"I want you to act as a sentiment analyzer that will analyze the sentiment:\n"
    prompt += f"Generate sentiment value (Positive, Negative, Neutral) from following data:\n"
    prompt += f"Name: {name}\n"
    prompt += f"Chat: {chat}\n"
    prompt += f"Consider all the above customer data and generate the sentiment."

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            temperature=0.1,
            n=1,
            stop=None,
        )
        sentiment = response.choices[0].text.strip()
        return sentiment
    except openai.error.OpenAIError as e:
        return f"Error: {e}"

def main():
    st.title("Sentiment Analyzer")

    # Collecting customer information
    name = st.text_input("Enter customer name:")
    chat = st.text_area("Enter customer chat:")
    
    if st.button("Generate Sentiment"):
        # Generate sentiment using OpenAI API
        sentiment = generate_sentiment(name, chat)

        # Connect to MySQL database
        mysql_connection = connect_to_mysql()

        # Insert sentiment data into the MySQL database
        try:
            customer_id = len(name)  # Just a simple example of generating an ID
            insert_sentiment_into_db(mysql_connection, customer_id, name, chat, sentiment)
        except Exception as e:
            st.error(f"Error inserting sentiment data: {str(e)}")

        # Close the MySQL connection
        mysql_connection.close()

        # Display the generated sentiment
        st.write(f"Generated Sentiment: {sentiment}")

if __name__ == "__main__":
    main()
