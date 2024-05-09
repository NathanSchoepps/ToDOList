from fastapi import FastAPI

import routers.ToDOList
import routers.Auth

app = FastAPI(
    title="ToDOList",
    docs_url="/",
)


app.include_router(routers.ToDOList.router)
app.include_router(routers.Auth.router)
