-- TripEasy Database Schema
-- Tạo database và các bảng cho ứng dụng quản lý du lịch

-- Tạo database
CREATE DATABASE IF NOT EXISTS tripeasy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tripeasy;

-- Bảng trips (Chuyến đi)
CREATE TABLE trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    destination VARCHAR(255) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    currency ENUM('VND', 'USD', 'EUR', 'JPY', 'KRW', 'THB') DEFAULT 'VND',
    child_factor DECIMAL(3,2) DEFAULT 0.5,
    rounding_rule INT DEFAULT 1000,
    invite_code VARCHAR(10) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_invite_code (invite_code),
    INDEX idx_dates (start_date, end_date)
);

-- Bảng trip_members (Thành viên chuyến đi)
CREATE TABLE trip_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    factor DECIMAL(3,2) DEFAULT 1.0,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    INDEX idx_trip_id (trip_id),
    INDEX idx_email (email),
    UNIQUE KEY unique_name_per_trip (trip_id, name),
    UNIQUE KEY unique_email_per_trip (trip_id, email)
);

-- Bảng activities (Hoạt động)
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    date DATETIME NOT NULL,
    location VARCHAR(500),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    INDEX idx_trip_date (trip_id, date),
    INDEX idx_location (latitude, longitude)
);

-- Bảng expenses (Chi phí)
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    activity_id INT,
    paid_by INT NOT NULL,
    description VARCHAR(500) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency ENUM('VND', 'USD', 'EUR', 'JPY', 'KRW', 'THB') NOT NULL,
    exchange_rate DECIMAL(10,4) DEFAULT 1.0,
    category ENUM('food', 'transport', 'accommodation', 'entertainment', 'shopping', 'other') DEFAULT 'other',
    is_shared BOOLEAN DEFAULT TRUE,
    date DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE SET NULL,
    FOREIGN KEY (paid_by) REFERENCES trip_members(id) ON DELETE CASCADE,
    INDEX idx_trip_date (trip_id, date),
    INDEX idx_paid_by (paid_by),
    INDEX idx_category (category),
    INDEX idx_shared (is_shared)
);

-- Bảng expense_categories (Danh mục chi phí tùy chỉnh)
CREATE TABLE expense_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    color VARCHAR(7) DEFAULT '#6B7280',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    INDEX idx_trip_id (trip_id),
    UNIQUE KEY unique_category_per_trip (trip_id, name)
);

-- Tạo các indexes bổ sung để tối ưu performance
CREATE INDEX idx_expenses_amount ON expenses(amount);
CREATE INDEX idx_expenses_exchange_rate ON expenses(exchange_rate);
CREATE INDEX idx_members_factor ON trip_members(factor);

-- Thêm dữ liệu mẫu (optional)
-- INSERT INTO trips (name, description, destination, start_date, end_date, currency, invite_code) 
-- VALUES ('Chuyến đi Đà Lạt', 'Chuyến du lịch cuối tuần tại Đà Lạt', 'Đà Lạt, Lâm Đồng', '2025-10-15 08:00:00', '2025-10-17 18:00:00', 'VND', 'DALAT001');

-- Tạo user cho ứng dụng (nếu cần)
-- CREATE USER 'tripeasy_user'@'%' IDENTIFIED BY 'secure_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON tripeasy.* TO 'tripeasy_user'@'%';
-- FLUSH PRIVILEGES;

-- Views để thống kê nhanh
CREATE VIEW trip_statistics AS
SELECT 
    t.id,
    t.name,
    t.destination,
    COUNT(DISTINCT tm.id) as member_count,
    COUNT(DISTINCT a.id) as activity_count,
    COUNT(DISTINCT e.id) as expense_count,
    COALESCE(SUM(e.amount * e.exchange_rate), 0) as total_expenses,
    COALESCE(SUM(CASE WHEN e.is_shared = TRUE THEN e.amount * e.exchange_rate ELSE 0 END), 0) as total_shared_expenses
FROM trips t
LEFT JOIN trip_members tm ON t.id = tm.trip_id
LEFT JOIN activities a ON t.id = a.trip_id
LEFT JOIN expenses e ON t.id = e.trip_id
GROUP BY t.id, t.name, t.destination;

-- Trigger để tự động cập nhật updated_at
DELIMITER //
CREATE TRIGGER update_trip_timestamp 
    BEFORE UPDATE ON trips 
    FOR EACH ROW 
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER update_activity_timestamp 
    BEFORE UPDATE ON activities 
    FOR EACH ROW 
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER update_expense_timestamp 
    BEFORE UPDATE ON expenses 
    FOR EACH ROW 
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//
DELIMITER ;

-- Thêm constraints để đảm bảo tính toàn vẹn dữ liệu
ALTER TABLE trips ADD CONSTRAINT chk_trip_dates CHECK (end_date > start_date);
ALTER TABLE trip_members ADD CONSTRAINT chk_member_factor CHECK (factor >= 0 AND factor <= 5);
ALTER TABLE expenses ADD CONSTRAINT chk_expense_amount CHECK (amount > 0);
ALTER TABLE expenses ADD CONSTRAINT chk_exchange_rate CHECK (exchange_rate > 0);

-- Tạo stored procedure để tính toán nhanh số dư thành viên
DELIMITER //
CREATE PROCEDURE CalculateMemberBalance(IN p_trip_id INT, IN p_member_id INT)
BEGIN
    DECLARE v_total_paid DECIMAL(15,2) DEFAULT 0;
    DECLARE v_total_owed DECIMAL(15,2) DEFAULT 0;
    DECLARE v_member_factor DECIMAL(3,2);
    DECLARE v_total_shared DECIMAL(15,2);
    DECLARE v_total_factor DECIMAL(8,2);
    
    -- Lấy hệ số của thành viên
    SELECT factor INTO v_member_factor 
    FROM trip_members 
    WHERE id = p_member_id AND trip_id = p_trip_id;
    
    -- Tính tổng tiền đã trả
    SELECT COALESCE(SUM(amount * exchange_rate), 0) INTO v_total_paid
    FROM expenses 
    WHERE trip_id = p_trip_id AND paid_by = p_member_id AND is_shared = TRUE;
    
    -- Tính tổng chi phí chung
    SELECT COALESCE(SUM(amount * exchange_rate), 0) INTO v_total_shared
    FROM expenses 
    WHERE trip_id = p_trip_id AND is_shared = TRUE;
    
    -- Tính tổng hệ số
    SELECT COALESCE(SUM(factor), 0) INTO v_total_factor
    FROM trip_members 
    WHERE trip_id = p_trip_id;
    
    -- Tính số tiền phải trả
    IF v_total_factor > 0 THEN
        SET v_total_owed = (v_total_shared / v_total_factor) * v_member_factor;
    END IF;
    
    -- Trả về kết quả
    SELECT 
        p_member_id as member_id,
        v_total_paid as total_paid,
        v_total_owed as total_owed,
        (v_total_paid - v_total_owed) as balance;
END//
DELIMITER ;
