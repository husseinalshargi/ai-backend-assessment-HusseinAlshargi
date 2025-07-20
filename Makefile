setup:
	python -m venv venv
	venv\Scripts\pip install -r requirements.txt
	ollama pull llama3

run:
	start /B cmd /C "ollama run llama3"
	venv\Scripts\python -m uvicorn app.main:api_app --reload

