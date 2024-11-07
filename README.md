# CommunityAidAI

## Run
```sh
# Create and activate python environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Run in dev mode
fastapi dev --host 0.0.0.0 app/main.py
```