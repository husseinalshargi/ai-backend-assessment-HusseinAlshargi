setup:
	python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt

run:
	venv\Scripts\activate && uvicorn app.main:app --reload

test:
	venv\Scripts\activate && pytest
