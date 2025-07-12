from fastapi import FastAPI
from app.api.routes import interview
app = FastAPI(title="AI Mock Interview")

  
    
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
    
    