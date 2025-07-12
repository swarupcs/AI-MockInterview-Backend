## Folder Structure

backend/
├── app/
│   ├── main.py                   # Entry point: FastAPI app + routers
│   ├── core/                     # Core config & global utilities
│   │   ├── config.py             # Env settings & constants
│   │   └── security.py           # JWT/Auth utils
│   ├── db/
│   │   ├── database.py           # DB engine, session creation
│   │   └── models/               # SQLAlchemy models
│   │       └── interview.py
│   ├── api/
│   │   ├── deps.py               # Route dependencies (get_user, get_db, etc.)
│   │   ├── routes/
│   │   │   ├── interview.py      # Interview routes
│   │   │   └── auth.py           # (Optional) Auth routes
│   ├── schemas/                  # Pydantic models
│   │   └── interview.py
│   ├── services/                 # Business logic / external integrations
│   │   └── interview_ai.py
│   ├── utils/                    # Common helpers, logging, etc.
│   └── tests/                    # Unit and integration tests
│       └── test_interview.py
├── requirements.txt
├── .env                          # Environment variables
└── alembic/                      # (Optional) Alembic for DB migrations




## Run FastAPI Server
```
uvicorn app.main:app --reload



## Activate venv
```
venv\Scripts\activate
```

## Install Dependencies
```
pip install -r requirements.txt
```

## Required Packages
- fastapi
- uvicorn 
- openai 
- python-dotenv
- requests
- pydantic