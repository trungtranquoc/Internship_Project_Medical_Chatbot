echo "Run Chatbot Service..."
cd chatbot || exit 1
source .venv/bin/activate || exit 1
python server.py