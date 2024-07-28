from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic

from src.database import get_databases, get_database_connection, post_database
from src.schemas import PostDatabaseSchema, QueryRequest, QueryResponse, LoginRequest
from src.services.query_service import QueryService
from src.services.llm_service import generate_sql_query
from src.utils.preprocessing import preprocess_query
from src.config.log_handler import logger

app = FastAPI()

security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sql-assistant-indol.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login(login_request: LoginRequest):
    try:
        logger.log_info(f"{login_request.username} {login_request.host} {login_request.password}")
        connection = get_database_connection(
            host=login_request.host,
            user=login_request.username,
            password=login_request.password,
            port=login_request.port,
            database=login_request.database
        )
        connection.close()
        return {"message": "Login successful"}

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid credentials: {e}"
        )

@app.get("/databases")
async def list_databases(host: str, user: str, password: str):
    try:
        databases = get_databases(
            host=host,
            user=user,
            password=password
            )
        return databases
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_data(
    request: QueryRequest,
    user: str, password: str,
    host: str
):
    try:
        connection = get_database_connection(
            host=host,
            user=user,
            password=password,
            database=request.database
        )
        query_service = QueryService(connection)

        generated_query = generate_sql_query(
            user_input=request.query,
            database=request.database,
            connection=connection,
        )

        processed_query: str = preprocess_query(generated_query)
        response = query_service.get_data(processed_query)

        try:
            post_database(
                PostDatabaseSchema(
                    user=user,
                    database=request.database,
                    user_query=request.query,
                    processed_query=processed_query,
                    response=response,
                    connection=connection
                )
            )
        except Exception:
            pass

        return QueryResponse(
            sql_query=processed_query,
            response=response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)