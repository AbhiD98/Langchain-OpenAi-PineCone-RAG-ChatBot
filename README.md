# Langchain Rag ChatBot

This script creates a Streamlit chatbot using PDF documents. It loads, splits, and embeds PDFs with OpenAI's embeddings into Pinecone. The app handles user queries, displaying responses interactively. It's designed for efficient Q&A despite hardware limits on running local models.

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AbhiD98/Langchain-Rag-ChatBot.git
   cd Langchain-Rag-ChatBot

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

3. **Set Up Credentials**  <br>
   Create a .env file in the root directory of the project. Add your own credentials for Pinecone and OpenAI APIs in the .env file:
   ```bash
   # Set up Pinecone Index Credentials
   export PINECONE_API_KEY=your_pinecone_api_key_here
   export PINECONE_ENV=us-east-1

   # Create Pinecone Index
   pinecone create abhi-alemeno \
       --dimension 1536 \
       --metric cosine \
       --cloud AWS \
       --region us-east-1


4. **Create PineCone Index**
   ```bash
   streamlit run main.py
  
5. **Run the Application**
   ```bash
   streamlit run main.py

Copy and paste this Markdown content into your `README.md` file. Replace the placeholders (`your_pinecone_api_key_here`, `your_pinecone_environment_here`, `your_openai_api_key_here`) with your actual API keys before using them. This format provides clear instructions for users to get started with your project while ensuring security practices are emphasized.
