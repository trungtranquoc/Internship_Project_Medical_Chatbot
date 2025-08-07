echo "Running Frontend Service..."
cd frontend || exit 1
source .venv/bin/activate || exit 1
chainlit run app.py --port 8000