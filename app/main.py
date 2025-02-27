from fastapi import FastAPI
from app.api.admin.admin_routes import router as admin_router
from app.api.signup.register_route import router as register_router
from app.api.signup.login_route import router as login_router


app = FastAPI()


app.include_router(admin_router)
app.include_router(register_router)
app.include_router(login_router)


# /users/{userid} -> should return user details
# /users/{userid}/platforms -> should return all platforms user integrated
# /users/{userid}/{platformid}/credentials -> /platforms/{platformid}/credentials?userid==id
# /platforms/{platformid} -> should return platform details
