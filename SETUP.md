# TripEasy - Hướng Dẫn Setup và Chạy Dự Án

## 🚀 Yêu Cầu Hệ Thống
- Node.js >= 16.x
- Python >= 3.8
- MySQL Database (Aiven Cloud đã được cấu hình)
- Git

## 📦 Cài Đặt

### 1. Clone Repository
```bash
git clone https://github.com/your-username/Trip_Easy.git
cd Trip_Easy
```

### 2. Setup Backend

#### Cài đặt dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Cấu hình Environment Variables
```bash
# Tạo file .env từ template
cp env.example .env

# Chỉnh sửa file .env với thông tin thực tế
DATABASE_HOST=tripeasy-tripeasy.l.aivencloud.com
DATABASE_PORT=26083
DATABASE_USER=avnadmin
DATABASE_PASSWORD=REDACTED
DATABASE_NAME=tripeasy
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
CORS_ORIGINS=http://localhost:3000,https://tripeasy-frontend.vercel.app
```

#### Khởi tạo Database
```bash
# Chạy script SQL để tạo tables
# Kết nối đến MySQL và chạy file database/schema.sql
mysql -h tripeasy-tripeasy.l.aivencloud.com -P 26083 -u avnadmin -p --ssl-ca=backend/app/core/ca-cert.pem tripeasy < database/schema.sql
```

#### Chạy Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 3. Setup Frontend

#### Cài đặt dependencies
```bash
cd frontend
npm install
```

#### Cấu hình Environment Variables
```bash
# Tạo file .env từ template
cp env.example .env

# Chỉnh sửa file .env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
REACT_APP_APP_NAME=TripEasy
REACT_APP_VERSION=1.0.0
```

#### Chạy Frontend
```bash
cd frontend
npm start
```

Frontend sẽ chạy tại: http://localhost:3000

## 🔧 Development

### Backend Development
```bash
cd backend
# Chạy với auto-reload
uvicorn app.main:app --reload

# Chạy tests (khi có)
pytest

# Format code
black app/
isort app/
```

### Frontend Development
```bash
cd frontend
# Chạy development server
npm start

# Build production
npm run build

# Run tests
npm test

# Linting
npm run lint
```

## 📱 Tính Năng Chính

### ✅ Đã Hoàn Thành
- [x] Cấu trúc dự án Backend (FastAPI) và Frontend (React)
- [x] Kết nối MySQL Database với SSL
- [x] API CRUD đầy đủ cho Trips, Members, Activities, Expenses
- [x] Thuật toán chia tiền thông minh
- [x] Giao diện mobile-first với Tailwind CSS
- [x] Hỗ trợ đa ngôn ngữ (Tiếng Việt & Tiếng Anh)
- [x] Git workflow và deployment setup
- [x] Cấu hình Vercel deployment

### 🚧 Đang Phát Triển
- [ ] Tích hợp Google Maps
- [ ] Quản lý thành viên chi tiết
- [ ] Quản lý hoạt động với map
- [ ] Quản lý chi phí với filters
- [ ] Báo cáo và biểu đồ
- [ ] PWA features
- [ ] Offline mode

### 🔮 Tính Năng Tương Lai
- [ ] OCR cho hóa đơn
- [ ] Push notifications
- [ ] Export PDF/CSV
- [ ] Social sharing
- [ ] Multi-currency real-time rates

## 🚀 Deployment

### Backend (Vercel)
```bash
cd backend
vercel --prod
```

### Frontend (Vercel)
```bash
cd frontend
npm run build
vercel --prod
```

### Environment Variables trên Vercel
Cấu hình các biến môi trường trên Vercel Dashboard theo hướng dẫn trong `DEPLOYMENT.md`

## 📊 Database Schema

Xem chi tiết schema trong file `database/schema.sql`:
- `trips` - Thông tin chuyến đi
- `trip_members` - Thành viên chuyến đi
- `activities` - Hoạt động trong chuyến đi
- `expenses` - Chi phí
- `expense_categories` - Danh mục chi phí tùy chỉnh

## 🔐 Bảo Mật

- SSL kết nối database
- Environment variables cho thông tin nhạy cảm
- CORS configuration
- Input validation
- SQL injection prevention

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Test connection
python -c "from backend.app.core.database import engine; print(engine.execute('SELECT 1').scalar())"
```

### Frontend Build Issues
```bash
# Clear cache và rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

### CORS Issues
Kiểm tra `CORS_ORIGINS` trong backend config

## 📞 Hỗ Trợ

- GitHub Issues: [Create Issue](https://github.com/your-username/Trip_Easy/issues)
- Documentation: Xem các file `.md` trong dự án
- API Docs: http://localhost:8000/docs (khi chạy local)

## 📄 License
MIT License - Xem file LICENSE để biết thêm chi tiết.
