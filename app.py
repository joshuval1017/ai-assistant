import os
import streamlit as st
import google.generativeai as genai

# Main function for the virtual assistant
def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyDpC7TYNKopgZdG4Bdc2jxdWUoxjRA_2c0'
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Virtual Assistant")

    # User input for command or query
    user_input = st.text_input(
        "Ask me anything (e.g., 'Set a reminder for 3 PM', 'What's the weather?', 'Play a song')"
    )

    # Button to submit query
    if st.button("Submit"):
        if user_input.strip():
            # Create a prompt for generating the assistant's response
            prompt = f"""
            You are an AI assistant similar to Siri, Alexa, and Cortana. Based on the following user query, generate a helpful response:

            "{user_input}"

            Please answer concisely and appropriately for the request (e.g., setting reminders, providing information, offering recommendations, or suggesting actions).
            """

            try:
                # Use the Gemini generative model to generate a response
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                assistant_response = response.text

                # Store the generated response in the session state
                st.session_state.assistant_response = assistant_response
                st.session_state.copy_status = "Copy Response to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't process your request. Please try again later.")
        else:
            st.warning("Please provide a valid command or question.")

    # Check if the assistant's response is in session state
    if 'assistant_response' in st.session_state:
        st.subheader("Assistant Response:")
        response_text_area = st.text_area(
            "Generated Response:", 
            st.session_state.assistant_response, 
            height=200, 
            key="response_content"
        )

        # Button to copy response to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Response to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var responseContent = document.querySelector('#response_content');
                    var range = document.createRange();
                    range.selectNode(responseContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
