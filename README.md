# Ai-automation-pipeline
LLM + FastAPI + Docker + Logging + basic CI &amp; tests

ai-automation-pipeline/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplikasi FastAPI utama
│   ├── models/
│   │   ├── __init__.py
│   │   └── llm_model.py        # Logika load model & inference
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── requests.py         # Model Pydantic untuk request/response
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging_setup.py    # Konfigurasi logging async
│   └── config/
│       ├── __init__.py
│       └── settings.py         # Konfigurasi environment variables
│
├── tests/                      # Unit dan integration tests
├── logs/                       # Direktori penyimpanan log files
├── model_weights/              # Penyimpanan model fine-tuned (opsional)
├── requirements.txt            # Dependencies
├── Dockerfile                  # Konfigurasi containerization
├── docker-compose.yml          # Orchestration multi-container
├── .env.example                # Template environment variables
├── .gitignore
├── README.md                   # Dokumentasi lengkap
└── .github/workflows/
    └── ci-cd.yml              # Pipeline CI/CD
