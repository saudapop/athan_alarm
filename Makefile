install:
	sh init.sh

run:
	source ./athan-app-venv/bin/activate && cd client && npm run build && cd .. && python3 app.py