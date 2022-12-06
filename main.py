import uvicorn
from fastapi import FastAPI
from data_accessors.elastic_search import MainDataAccessor

from api.welcome import router as hello_world
from api.developer_api import router as developer
from api.model_train import router as train_model
import config


app = FastAPI()
app.router.include_router(hello_world)
app.router.include_router(developer)
app.router.include_router(train_model)

@app.on_event("startup")
async def on_startup():
    """Execute code once on startup"""

    config.client = MainDataAccessor()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=4003,
        workers=5,
        ssl_keyfile=None,
        ssl_certfile=None,
        debug=True,
    )
