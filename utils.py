from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import os

def demo_function():
    print("This is a demo function.")
    
    
def generate_questions_from_techstack(tech_stacks):

    # Generate questions ONCE
    model = ChatOllama(model="llama3.2", temperature=0.7)
    tech_stack_list = tech_stacks.split(",")

    all_questions = []
    for techstack in tech_stack_list:
        template = """
        You are interviewer, you are expected to generate 3 interview questions on {blank_stack} tech stack.
        Simply return the questions in a comma separated format without any extra text, in the below format. Example: 
        What is Python?, Explain Django?, How does Streamlit work?
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        result = chain.invoke({"blank_stack": techstack})
        questions = result.content
        all_questions.extend([q.strip() for q in questions.split(",")])

        #print("\n\nQuestions:\n", all_questions)  # Debug
    return all_questions

def save_all_conversation_to_file(string_data):
    current_dir=os.getcwd()
    full_path=os.path.join(current_dir,"candidate_response/candidate_response.txt") #This is another way to get the path
    #full_path = "candidate_response/candidate_response.txt"
    #print("Debug 9: ", full_path) #Debugging line to check the path
    file =  open(full_path, "a", encoding="utf-8") #utf-8 encoding to support special characters, it's not necessary.
    file.write(string_data + "\n")
    file.close()



# For quick testing only
if __name__ == "__main__":
    #generate_questions_from_techstack("Python, Django")
    save_all_conversation_to_file("Agent: What is Python?")