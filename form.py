import streamlit as st
from utils import demo_function, generate_questions_from_techstack, save_all_conversation_to_file


print("New Instance #######################################################################") #For debugging purpose

# Dictionary to hold form values
form_values = {
    "name": None,
    "email": None,
    "country_code": None,
    "phone": None,
    "experience": None,
    "desired_positions": None,
    "current_location": None,
    "tech_stack": None
}

#Callback function 
def go_to_next_stage():
    st.session_state.page = "result"
    save_all_conversation_to_file("\n\n\n--- New Interview Session Started ---\n")
    #print("Debug-7: State changed successfully..... ") #Debug line 
    save_all_conversation_to_file(st.session_state.submitted_data) #Saving candidate info to file
    st.session_state.all_questions = generate_questions_from_techstack(st.session_state.tech_stack)


def question_display_with_history(questions: list):

    # Initialize session state
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display chat history FIRST
    for role, msg in st.session_state.history:
        with st.chat_message(role):
            st.write(msg)


    # If there are still questions left
    if st.session_state.q_index < len(questions):
        current_question = questions[st.session_state.q_index]

        # Show current question once
        if not st.session_state.history or st.session_state.history[-1][1] != current_question:
            st.session_state.history.append(("assistant", current_question))
            with st.chat_message("assistant"):
                st.write(current_question)
                

        # Wait for user input - MOVED TO THE END
        user_input = st.chat_input("Your answer...")
        if user_input:
            st.session_state.history.append(("user", user_input))
            st.session_state.q_index += 1
            st.rerun()
    else:
        # Show completion message
        if not st.session_state.history or st.session_state.history[-1][1] != "✅ All questions answered. Thank you!":
            #st.session_state.history.append(("assistant", "✅ All questions answered. Thank you!"))
            with st.chat_message("assistant"):
                st.write(f"All questions answered ✅. Thank you {st.session_state.name} ! :blue[TalentScout] team will evaluate your responses and reach out to you soon.") #Bring this line to end

                #Storing all conversation to file
                for role, msg in st.session_state.history:
                    save_all_conversation_to_file(f"\n{role.capitalize()}: {msg}")
                        



# session_state.page = "form" is the form page.
# session_state.page = "result" is the interview page.
if "page" not in st.session_state:
    st.session_state.page = "form"

if st.session_state.page == "form":
    st.title(":blue[TalentScout] Interview Form")
    st.markdown("Please fill out the form below to proceed to the interview. All fields are mandatory.")

    # Create a form
    with st.form(key='candidate_info_form'):
        form_values["name"] = st.text_input("Full name")
        form_values["email"] = st.text_input("Email address")
        form_values["country_code"] = st.selectbox("Country code", ["+91", "+1", "+44", "+61", "+81", "+49", "+33", "+86"])
        form_values["phone"] = st.text_input("Phone number (e.g., 1234567890)")
        form_values["experience"] = st.slider("Years of experience", 0, 30, 2)
        form_values["desired_positions"] = st.text_input("Desired positions")
        form_values["current_location"] = st.text_input("Current location")
        form_values["tech_stack"] = st.text_input("Tech stack (Simply put coma separated values e.g.: Python, Django, Streamlit, ...)")

        st.write("")  # Empty line for better spacing
        st.write(":red[Please ensure all fields are filled correctly before submitting the form. You won't be able to edit the information after submission.]")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button: 
            #print("Debug 1: ", form_values) #Debugging 1
            
            if not all(form_values.values()):  #Put 'all' keyword before deployment
                st.error("Please fill in all the fields.")
            else:
                #Saving form data from session state
                st.session_state.name = form_values["name"]
                st.session_state.email = form_values["email"]
                st.session_state.country_code = form_values["country_code"]
                st.session_state.phone = form_values["phone"]
                st.session_state.experience = form_values["experience"]
                st.session_state.desired_positions = form_values["desired_positions"]
                st.session_state.current_location = form_values["current_location"]
                st.session_state.tech_stack = form_values["tech_stack"]

                st.session_state.submitted_data = f"Name: {st.session_state.name} \nEmail: {st.session_state.email} \nCountry Code: {st.session_state.country_code} \nPhone: {st.session_state.phone} \nExperience: {st.session_state.experience} years \nDesired Positions: {st.session_state.desired_positions} \nCurrent Location: {st.session_state.current_location} \nTech Stack: {st.session_state.tech_stack}"
                #st.session_state.chat_history = ""  # Initialize chat history

                st.success("Form submitted successfully!")
                #st.write(f"Thankyou {form_values['name']}! \nYour Email ID is {form_values['email']}. \nWe will reach out to you soon.")
                st.balloons()
                st.markdown("After you click the :blue[Proceed to Interview] button below, wait few seconds for the app to load.")
                proceed_button = st.form_submit_button(label="Proceed to Interview", on_click=go_to_next_stage) 

                # print("Debug 2:")
                # demo_function()
                    

# Page 2: Result and Interview Page... State - 'result'
if st.session_state.page == "result":

    # Chat page starts here

    st.title("Welcome to the :blue[Interview App]!")
    st.markdown("#### **Your Submitted Information:**")

    # Display the data passed from the form #Debug purpose
    #submitted_data = f"Name: {st.session_state.name} \nEmail: {st.session_state.email} \nCountry Code: {st.session_state.country_code} \nPhone: {st.session_state.phone} \nExperience: {st.session_state.experience} years \nDesired Positions: {st.session_state.desired_positions} \nCurrent Location: {st.session_state.current_location} \nTech Stack: {st.session_state.tech_stack}"

    st.code(st.session_state.submitted_data)

    #To display all questions while maintaining chat history
    question_display_with_history(st.session_state.all_questions)
    

    # Below line is for testing purpose only.
    #question_display_with_history(['What is Python?', 'How does Pandas handle missing data?', 'What are the best practices for caching with Redis and Flask?', "What is Django's ORM system", 'How do you implement authentication and authorization in a Django project', "What are the benefits of using Django's built-in caching framework?"])


    

    




            
