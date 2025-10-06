# TripEasy - Ứng Dụng Quản Lý Du Lịch

## 🚀 Tổng Quan
TripEasy là ứng dụng web quản lý du lịch toàn diện với thiết kế mobile-first, giúp người dùng và nhóm bạn/gia đình dễ dàng lên kế hoạch, theo dõi lịch trình, quản lý chi tiêu và tự động chia tiền sau chuyến đi.

## ✨ Tính Năng Chính
- 🗺️ Quản lý chuyến đi với tích hợp bản đồ
- 📅 Lịch trình hoạt động theo ngày
- 💰 Quản lý chi phí đa tiền tệ
- 👥 Quản lý thành viên với hệ số chia tiền tùy chỉnh
- 📊 Báo cáo và chia tiền thông minh
- 🌐 Hỗ trợ đa ngôn ngữ (Tiếng Việt & Tiếng Anh)

## 🛠️ Tech Stack
- **Backend**: Python (FastAPI)
- **Frontend**: React với TypeScript
- **Database**: MySQL (Aiven Cloud)
- **Deployment**: Vercel
- **Maps**: Google Maps API
- **UI**: Tailwind CSS + Shadcn/ui

## 📁 Cấu Trúc Dự Án
```
Trip_Easy/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core settings
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── vercel.json
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   ├── utils/          # Utilities
│   │   ├── i18n/           # Internationalization
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   └── vercel.json
├── database/               # Database scripts
│   └── schema.sql
└── docs/                   # Documentation
```

## 🚀 Hướng Dẫn Chạy Dự Án

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 📝 Git Workflow
1. `git add .`
2. `git commit -m "mô tả thay đổi"`
3. `git push`
4. Deploy chủ động lên Vercel
5. Mapping URL cố định

## 🌐 Deployment
- Frontend: https://tripeasy-frontend.vercel.app
- Backend API: https://tripeasy-backend.vercel.app

## 📄 License
MIT License
