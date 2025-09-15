from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.deps import get_db
from backend.app.models.user import User


app = FastAPI(title='Crypto screener API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде - конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM users")
    users = result.fetchall()
    return {"users": [dict(row) for row in users]}