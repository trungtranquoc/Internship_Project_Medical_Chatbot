echo "Running Backend Service..."
cd backend || exit 1
source .venv/bin/activate || exit 1
python app.py