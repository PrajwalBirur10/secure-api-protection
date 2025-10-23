from fastapi import FastAPI

app=FastAPI()

@app.get("/health")
def health_check():
	return {"status": "OK"}

@app.get("/books")
def get_books():
	return [{"title": "Zero Trust APIs"}, {"title": "App & API Protection"}]
