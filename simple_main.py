from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/")
def api_v1():
    return {"API": "v1", "status": "working"}

@app.get("/api/v1/test/{id}")
def test(id: str):
    return {"id": id, "test": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
