# from langchain_community.llms import ollama 
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.schema.output_parser import StrOutputParser
# from langchain.schema import AIMessage, HumanMessage
# import json
# import re
# from fuzzywuzzy import fuzz

# load_dotenv()

# # Initialize the model
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# # Set up initial messages and instructions for the bot
# messages = [
#     HumanMessage(content="You are IqBot, a highly intelligent AI. You can answer all kinds of questions from A to Z, ranging from general knowledge to specific queries. Provide detailed and helpful responses to any inquiry."),
#     MessagesPlaceholder("chat_history")
# ]

# # Define the prompt template
# prompt_template = ChatPromptTemplate.from_messages(messages)

# # Initialize chat history
# chat_history = []

# # Load custom datasets
# def load_datasets():
#     datasets = {}
#     try:
#         with open("./datasets/GarudaAerospace.json", "r") as f:
#             datasets["GarudaAerospace"] = json.load(f)
#         with open("./datasets/IqTechMax.json", "r") as f:
#             datasets["IqTechMax"] = json.load(f)
#     except FileNotFoundError as e:
#         print(f"Error loading datasets: {e}")
#     return datasets

# custom_datasets = load_datasets()

# # Function to find the best match in a dataset
# def find_best_match(query, dataset_name):
#     if dataset_name not in custom_datasets:
#         print(f"No data found for dataset: {dataset_name}")
#         return None

#     data = custom_datasets[dataset_name]
#     best_match = None
#     best_similarity = 0

#     for item in data:
#         if "prompt" in item and "completion" in item:
#             if query.lower() == item["prompt"].lower():
#                 return item["completion"]
#             similarity = fuzz.partial_ratio(query.lower(), item["prompt"].lower())
#             if similarity > best_similarity and similarity > 80:
#                 best_match = item["completion"]
#                 best_similarity = similarity

#     return best_match

# # Function to determine the relevant dataset
# def determine_relevant_dataset(query):
#     if re.search(r'\b(garuda|aerospace|drone|agnishwar)\b', query, re.IGNORECASE):
#         return "GarudaAerospace"
#     elif re.search(r'\b(iq techmax|techmax|services|products|iq)\b', query, re.IGNORECASE):
#         return "IqTechMax"
#     return None

# # Main chat function
# def chat(query):
#     response = None
#     relevant_dataset = determine_relevant_dataset(query)

#     if relevant_dataset:
#         response = find_best_match(query, relevant_dataset)

#     if not response:
#         chat_history.append(HumanMessage(content=query))
#         chain = prompt_template | model | StrOutputParser()
#         result = chain.invoke({"chat_history": chat_history})
#         response = result
#         chat_history.append(AIMessage(content=response))

#     return response


from langchain_community.llms import ollama 
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import AIMessage, HumanMessage
import json
import re
from fuzzywuzzy import fuzz

load_dotenv()

# Initialize the model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Set up initial messages and instructions for the bot
messages = [
    HumanMessage(content="You are IqBot, a highly intelligent AI. You can answer all kinds of questions from A to Z, ranging from general knowledge to specific queries. Provide detailed and helpful responses to any inquiry."),
    MessagesPlaceholder("chat_history")
]

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages(messages)

# Initialize chat history
chat_history = []

# Load custom datasets
def load_datasets():
    datasets = {}
    try:
        with open("./datasets/GarudaAerospace.json", "r") as f:
            datasets["GarudaAerospace"] = json.load(f)
        with open("./datasets/IqTechMax.json", "r") as f:
            datasets["IqTechMax"] = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading datasets: {e}")
    return datasets

custom_datasets = load_datasets()

# Function to find the best match in a dataset
def find_best_match(query, dataset_name):
    if dataset_name not in custom_datasets:
        print(f"No data found for dataset: {dataset_name}")
        return None

    data = custom_datasets[dataset_name]
    best_match = None
    best_similarity = 0

    for item in data:
        if "prompt" in item and "completion" in item:
            if query.lower() == item["prompt"].lower():
                return item["completion"]
            similarity = fuzz.partial_ratio(query.lower(), item["prompt"].lower())
            if similarity > best_similarity and similarity > 80:
                best_match = item["completion"]
                best_similarity = similarity

    return best_match

# Function to determine the relevant dataset
def determine_relevant_dataset(query):
    if re.search(r'\b(garuda|aerospace|drone|agnishwar)\b', query, re.IGNORECASE):
        return "GarudaAerospace"
    elif re.search(r'\b(iq techmax|techmax|services|products|iq)\b', query, re.IGNORECASE):
        return "IqTechMax"
    return None

# Identity-related responses
identity_responses = [
    "I am IqBot, a virtual AI assistant developed by Iq TechMax. How can I assist you?",
    "I was created by Iq TechMax to help with various queries. My name is IqBot.",
    "I am IqBot, your friendly virtual assistant from Iq TechMax. How can I assist you today?",
    "I was built by the talented team at Iq TechMax. I am IqBot, your AI assistant.",
    "I am IqBot, an AI assistant developed by Iq TechMax. I can assist you with a wide range of topics.",
    "I am IqBot, an AI developed by Iq TechMax to help you with your questions. What can I help you with today?"
]

# Check if the query is identity-related
def is_identity_query(query):
    identity_keywords = [
        "who are you", "who developed you", "who built you", "what is your name",
        "who created you", "tell me about yourself", "what can you do", "who are you?","what is the relation between you and iqtechmax"
    ]
    for keyword in identity_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', query, re.IGNORECASE):
            return True
    return False

# Main chat function
def chat(query):
    response = None

    # If the query is related to identity, provide predefined response
    if is_identity_query(query):
        response = identity_responses[0]  # You can choose a different response from the list
    
    # Otherwise, find relevant dataset and try to match
    if not response:
        relevant_dataset = determine_relevant_dataset(query)

        if relevant_dataset:
            response = find_best_match(query, relevant_dataset)

    # If no response found, use the model to generate an answer
    if not response:
        chat_history.append(HumanMessage(content=query))
        chain = prompt_template | model | StrOutputParser()
        result = chain.invoke({"chat_history": chat_history})
        response = result
        chat_history.append(AIMessage(content=response))

    return response
