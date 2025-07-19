setup:
	python -m venv venv
	venv\Scripts\pip install -r requirements.txt
	ollama pull llama3

start-ollama:
	start /B cmd /C "ollama run llama3"

run:
	venv\Scripts\python -m uvicorn app.main:app --reload

