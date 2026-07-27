from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# ==================================================
# HTTP EXCEPTION HANDLER
# ==================================================

async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )


# ==================================================
# VALIDATION EXCEPTION HANDLER
# ==================================================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "status_code": 422,
            "message": "Validation Error",
            "errors": errors
        }
    )


# ==================================================
# REGISTER ALL EXCEPTION HANDLERS
# ==================================================

def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        HTTPException,
        http_exception_handler
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler
    )