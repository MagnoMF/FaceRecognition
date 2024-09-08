from fastapi import FastAPI
from api.user import router
from db.init_db import init_db
import uvicorn

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8080, debug=False)