.PHONY: setup run

setup:
	python -m venv venv
	venv\Scripts\pip.exe install -r requirements.txt
	ollama pull llama3
	(source venv/Scripts/activate && python -m app.main create-tables-in-db)
	@echo "______________________"
	@echo "Creating an admin user..."
	(source venv/Scripts/activate && python -m app.main create-an-api-key "admin" "hussein@admin.com")


run:
	@echo "Starting Ollama in background..."
	ollama run llama3 & # Run Ollama in the background

	@echo "Starting FastAPI API in background..."
	# (source activate) && command makes sure the venv is activated for this specific sub-shell
	(source venv/Scripts/activate && uvicorn app.main:api_app --reload) &

	@echo "Starting Streamlit app in background..."
	(source venv/Scripts/activate && streamlit run app/Home.py) &