from fastapi import FastAPI
from product.funcs import router as pr_router
from account.funcs import router as ac_router
from product.funcs import router_cat

app = FastAPI()

app.include_router(pr_router)
app.include_router(ac_router)
app.include_router(router_cat)
