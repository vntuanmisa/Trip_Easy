from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .core.database import engine, Base
from .api import trips, members, activities, expenses
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

# Create FastAPI app
app = FastAPI(
    title="TripEasy API",
    description="API cho ứng dụng quản lý du lịch TripEasy",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Không tìm thấy tài nguyên"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Lỗi máy chủ nội bộ"}
    )

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "TripEasy API đang hoạt động",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        from .core.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Hệ thống hoạt động bình thường"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Hệ thống gặp sự cố"
        )

# Include routers
app.include_router(trips.router, prefix="/api/trips", tags=["Trips"])
app.include_router(members.router, prefix="/api/trips", tags=["Members"])
app.include_router(activities.router, prefix="/api/trips", tags=["Activities"])
app.include_router(expenses.router, prefix="/api/trips", tags=["Expenses"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)