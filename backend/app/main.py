from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .core.database import engine, Base
from .api import trips, members, activities, expenses
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables & ensure required columns exist (idempotent)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

    # Ensure required columns exist on trips (production DB may be legacy)
    ensure_trip_columns_sql = [
        # Using IF NOT EXISTS keeps this idempotent on MySQL 8+
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS description TEXT",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS start_date DATETIME NOT NULL",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS end_date DATETIME NOT NULL",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS currency ENUM('VND','USD','EUR','JPY','KRW','THB') DEFAULT 'VND'",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS child_factor DECIMAL(3,2) DEFAULT 0.5",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS rounding_rule INT DEFAULT 1000",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS invite_code VARCHAR(10)",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE trips ADD COLUMN IF NOT EXISTS updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        # Basic indexes if missing (ignore errors if exist)
        "CREATE INDEX IF NOT EXISTS idx_invite_code ON trips(invite_code)",
    ]
    with engine.begin() as conn:
        for stmt in ensure_trip_columns_sql:
            try:
                conn.execute(text(stmt))
            except Exception as sub_e:
                # Some MySQL variants may not support IF NOT EXISTS on certain clauses; ignore if already exists
                logger.warning(f"Schema ensure step ignored/failed: {stmt} -> {sub_e}")
    logger.info("Schema ensure: trips columns verified")
except Exception as e:
    logger.error(f"Error creating/ensuring database tables: {e}")
    # Continue anyway, tables might already exist

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
    allow_origins=settings.cors_origins_list + ["https://tripeasy-frontend.vercel.app"],
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
        # Test basic database connection without querying specific tables
        from .core.database import SessionLocal
        from sqlalchemy import text
        
        db = SessionLocal()
        result = db.execute(text("SELECT 1 as test")).fetchone()
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "test_result": result[0] if result else None,
            "message": "Hệ thống hoạt động bình thường"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Hệ thống gặp sự cố: {str(e)}"
        )

@app.get("/db-info")
async def database_info():
    """Kiểm tra thông tin database và tables"""
    try:
        from .core.database import SessionLocal
        from sqlalchemy import text
        
        db = SessionLocal()
        
        # Check if trips table exists
        result = db.execute(text("SHOW TABLES LIKE 'trips'")).fetchone()
        trips_exists = result is not None
        
        tables_info = {}
        if trips_exists:
            # Get trips table structure
            columns = db.execute(text("DESCRIBE trips")).fetchall()
            tables_info["trips"] = [{"name": col[0], "type": col[1], "null": col[2], "key": col[3]} for col in columns]
        
        db.close()
        return {
            "database": "connected",
            "trips_table_exists": trips_exists,
            "tables_info": tables_info
        }
    except Exception as e:
        logger.error(f"Database info check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Không thể lấy thông tin database: {str(e)}"
        )

# Include routers
app.include_router(trips.router, prefix="/api/trips", tags=["Trips"])
app.include_router(members.router, prefix="/api/trips", tags=["Members"])
app.include_router(activities.router, prefix="/api/trips", tags=["Activities"])
app.include_router(expenses.router, prefix="/api/trips", tags=["Expenses"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)