
# Create virtual environment
python -m venv presales_ai
source presales_ai/bin/activate  # or presales_ai\Scripts\activate on Windows

# Install dependencies
pip install openai langchain crewai streamlit plotly pandas numpy 
pip install python-dotenv chromadb requests beautifulsoup4
pip install azure-identity azure-mgmt-compute azure-mgmt-network
pip install boto3 google-cloud-compute
pip install docker kubernetes

