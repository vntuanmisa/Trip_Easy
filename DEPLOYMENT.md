# TripEasy - Git Workflow và Deployment Checklist

## 📋 Checklist Commit & Deploy

### Trước khi Commit
- [ ] Kiểm tra code không có lỗi syntax
- [ ] Test các tính năng mới
- [ ] Cập nhật documentation nếu cần
- [ ] Đảm bảo không commit thông tin nhạy cảm (passwords, API keys)
- [ ] Kiểm tra file .env không được commit

### Git Workflow
```bash
# 1. Kiểm tra trạng thái
git status

# 2. Thêm tất cả thay đổi
git add .

# 3. Commit với message mô tả rõ ràng
git commit -m "feat: thêm tính năng quản lý chuyến đi"

# 4. Push lên repository
git push origin main
```

### Commit Message Convention
- `feat:` - Tính năng mới
- `fix:` - Sửa lỗi
- `docs:` - Cập nhật documentation
- `style:` - Thay đổi formatting, không ảnh hưởng logic
- `refactor:` - Refactor code
- `test:` - Thêm hoặc sửa tests
- `chore:` - Cập nhật build tools, dependencies

### Deployment trên Vercel

#### Backend Deployment
1. **Cấu hình Environment Variables trên Vercel (không ghi giá trị thật vào repo):**
   ```
   DATABASE_HOST=<set-on-vercel-dashboard>
   DATABASE_PORT=<set-on-vercel-dashboard>
   DATABASE_USER=<set-on-vercel-dashboard>
   DATABASE_PASSWORD=<set-on-vercel-dashboard>
   DATABASE_NAME=<set-on-vercel-dashboard>
   SECRET_KEY=<set-on-vercel-dashboard>
   GOOGLE_MAPS_API_KEY=<set-on-vercel-dashboard>
   CORS_ORIGINS=<your-frontend-domain>,http://localhost:3000
   ```

2. **Deploy Backend:**
   ```bash
   cd backend
   vercel --prod
   ```

3. **Mapping URL cố định:**
   - Vào Vercel Dashboard
   - Settings > Domains
   - Thêm custom domain: `tripeasy-backend.vercel.app`

#### Frontend Deployment
1. **Cấu hình Environment Variables:**
   ```
   REACT_APP_API_URL=https://tripeasy-backend.vercel.app
   REACT_APP_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
   ```

2. **Deploy Frontend:**
   ```bash
   cd frontend
   npm run build
   vercel --prod
   ```

3. **Mapping URL cố định:**
   - Custom domain: `tripeasy-frontend.vercel.app`

### Checklist Sau Deploy
- [ ] Kiểm tra backend API hoạt động: `https://tripeasy-backend.vercel.app/health`
- [ ] Kiểm tra frontend load được: `https://tripeasy-frontend.vercel.app`
- [ ] Test kết nối giữa frontend và backend
- [ ] Kiểm tra database connection
- [ ] Test các tính năng chính

### Troubleshooting

#### Lỗi Database Connection
```python
# Kiểm tra trong backend/app/core/database.py
# Đảm bảo SSL certificate được tạo đúng
# Kiểm tra environment variables
```

#### Lỗi CORS
```python
# Cập nhật CORS_ORIGINS trong backend/app/core/config.py
# Thêm domain frontend vào danh sách allowed origins
```

#### Build Error Frontend
```bash
# Xóa node_modules và rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Monitoring & Maintenance
- Kiểm tra logs trên Vercel Dashboard
- Monitor database performance
- Backup database định kỳ
- Cập nhật dependencies thường xuyên

### URLs Chính Thức
- **Frontend**: https://tripeasy-frontend.vercel.app
- **Backend API**: https://tripeasy-backend.vercel.app
- **API Docs**: https://tripeasy-backend.vercel.app/docs
- **Health Check**: https://tripeasy-backend.vercel.app/health
