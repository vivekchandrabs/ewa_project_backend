Here’s the README in markdown format:

# ChatBot Order System

This project is a Django-based chatbot platform that allows users to interact with a conversational AI to place orders. The chatbot is powered by OpenAI's language models and utilizes a FAISS vector store for efficient similarity searches within the chat database.

## Features

- **Interactive Chatbot**: Enables users to place orders through natural conversation.
- **Order Management**: Users can view and confirm their orders through the chatbot.
- **Database**: Uses SQLite as the database for efficient local storage.
- **FAISS Vector Store**: Facilitates quick retrieval of similar queries and responses, enhancing chatbot responsiveness.
- **Integration with OpenAI API**: Leverages OpenAI’s language model for dynamic conversations and order management.

---

## Requirements

Before running this project, ensure you have the following installed:

- Python 3.7+
- Django
- FAISS
- An API key for OpenAI

You can find all required packages in the `requirements.txt` file.

---

## Installation

1. **Clone the Repository**

   ```bash
   cd chatbot-order-system
   ```

2. **Install Dependencies**

   Run the following command to install all required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Environment Variables**

   Create a `.env` file in the root directory and add your OpenAI API key:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Ensure that `.env` is located in the root of your project directory.

4. **Run Migrations**

   Initialize the database by running Django migrations:

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**

   Once everything is set up, start the Django development server:

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` in your browser to interact with the chatbot.

---

## Project Structure

The key components of the project include:

- **Database**: SQLite for easy local storage and management of order and user data.
- **Language Processing**: OpenAI’s language models to interpret and process user inputs.
- **Vector Store**: FAISS, which allows the chatbot to search through previous interactions efficiently, improving contextual response generation.

---

## How It Works

The chatbot order system allows users to interact with an AI-based chatbot to place an order. Here's an overview of the workflow:

1. **User Interaction**: A user initiates a conversation with the chatbot.
2. **Order Placement**: Through natural language, users specify their order preferences and requirements.
3. **Chat Context Management**: The chatbot, using the FAISS vector store, recalls relevant past interactions and responses, enabling a coherent flow in extended conversations.
4. **Order Confirmation**: After gathering all necessary details, the chatbot confirms the order and provides a summary to the user.

---

## Important Notes

- **Environment Variables**: Remember to populate your `.env` file with your OpenAI API key before running the project.
- **FAISS Compatibility**: Ensure your Python environment supports FAISS. Some installations may require system-level dependencies.
- **Development Only**: This setup is configured for development use. For production deployment, consider using a more robust database (e.g., PostgreSQL) and implementing additional security measures.
