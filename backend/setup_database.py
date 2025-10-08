#!/usr/bin/env python3
"""
Script để setup database schema cho TripEasy
Chạy script này để tạo tất cả tables cần thiết
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.database import Base, ca_cert_path
from app.models.models import Trip, TripMember, Activity, Expense, ExpenseCategory

def create_database_tables():
    """Tạo tất cả database tables"""
    try:
        print("🔧 Đang kết nối database...")
        print(f"Host: {settings.database_host}")
        print(f"Port: {settings.database_port}")
        print(f"Database: {settings.database_name}")
        
        # Tạo engine
        engine = create_engine(
            settings.database_url.replace("?ssl_ca=ca-cert.pem", f"?ssl_ca={ca_cert_path}"),
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={
                "ssl_disabled": False,
                "ssl_ca": ca_cert_path
            }
        )
        
        # Test connection
        print("🔍 Kiểm tra kết nối database...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            print(f"✅ Kết nối thành công: {result.fetchone()}")
        
        # Tạo tables
        print("🏗️ Đang tạo database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tạo tables thành công!")
        
        # Kiểm tra tables đã tạo
        print("📋 Kiểm tra tables đã tạo:")
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            for table in tables:
                print(f"  - {table[0]}")
        
        # Kiểm tra cấu trúc bảng trips
        print("🔍 Kiểm tra cấu trúc bảng trips:")
        with engine.connect() as conn:
            result = conn.execute(text("DESCRIBE trips"))
            columns = result.fetchall()
            for col in columns:
                print(f"  - {col[0]}: {col[1]} ({col[2]})")
                
        print("🎉 Setup database hoàn tất!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi setup database: {e}")
        return False

def check_database_status():
    """Kiểm tra trạng thái database"""
    try:
        from app.core.database import SessionLocal
        
        print("🔍 Kiểm tra trạng thái database...")
        db = SessionLocal()
        
        # Kiểm tra tables
        result = db.execute(text("SHOW TABLES")).fetchall()
        print(f"📋 Có {len(result)} tables trong database:")
        for table in result:
            print(f"  - {table[0]}")
            
        # Kiểm tra dữ liệu mẫu
        if any('trips' in str(table[0]) for table in result):
            trip_count = db.execute(text("SELECT COUNT(*) FROM trips")).fetchone()
            print(f"📊 Số lượng trips: {trip_count[0]}")
            
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra database: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TripEasy Database Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        success = check_database_status()
    else:
        success = create_database_tables()
    
    if success:
        print("✅ Hoàn tất!")
        sys.exit(0)
    else:
        print("❌ Có lỗi xảy ra!")
        sys.exit(1)
