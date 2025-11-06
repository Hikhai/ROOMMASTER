"""
Script Migration: Thêm unique constraint cho Invoice
Chạy file này để cập nhật database với constraint mới
"""
from app import create_app, db
from app.models import Invoice
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🔧 Bắt đầu migration database...")
    
    # Kiểm tra xem constraint đã tồn tại chưa
    inspector = db.inspect(db.engine)
    constraints = inspector.get_unique_constraints('invoices')
    
    constraint_exists = any(c['name'] == 'uq_room_month_year' for c in constraints)
    
    if constraint_exists:
        print("✅ Unique constraint 'uq_room_month_year' đã tồn tại!")
    else:
        print("📝 Đang thêm unique constraint...")
        
        # Kiểm tra xem có hóa đơn trùng lặp không
        duplicate_check = db.session.execute(text("""
            SELECT room_id, month, year, COUNT(*) as count
            FROM invoices
            GROUP BY room_id, month, year
            HAVING COUNT(*) > 1
        """)).fetchall()
        
        if duplicate_check:
            print("⚠️  CẢNH BÁO: Phát hiện hóa đơn trùng lặp:")
            for row in duplicate_check:
                print(f"   - Phòng {row.room_id}, Tháng {row.month}/{row.year}: {row.count} hóa đơn")
            
            print("\n❌ Không thể thêm unique constraint khi có dữ liệu trùng lặp!")
            print("💡 Vui lòng xóa các hóa đơn trùng lặp trước:")
            print("   1. Vào menu Hóa đơn")
            print("   2. Tìm và xóa các hóa đơn trùng (giữ lại 1 hóa đơn cho mỗi phòng/tháng)")
            print("   3. Chạy lại script này")
        else:
            try:
                # SQLite không hỗ trợ ADD CONSTRAINT, cần tạo lại bảng
                print("   Đang tạo lại bảng invoices với unique constraint...")
                
                # Bước 1: Tạo bảng mới với constraint
                db.session.execute(text("""
                    CREATE TABLE invoices_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room_id INTEGER NOT NULL,
                        created_by INTEGER,
                        month INTEGER NOT NULL,
                        year INTEGER NOT NULL,
                        room_price REAL DEFAULT 0,
                        electric_old REAL DEFAULT 0,
                        electric_new REAL DEFAULT 0,
                        electric_unit_price REAL DEFAULT 3500,
                        water_old REAL DEFAULT 0,
                        water_new REAL DEFAULT 0,
                        water_unit_price REAL DEFAULT 20000,
                        other_fees REAL DEFAULT 0,
                        total_amount REAL DEFAULT 0,
                        status VARCHAR(20) DEFAULT 'unpaid',
                        created_at DATETIME,
                        due_date DATETIME,
                        notes TEXT,
                        FOREIGN KEY (room_id) REFERENCES rooms(id),
                        FOREIGN KEY (created_by) REFERENCES users(id),
                        UNIQUE (room_id, month, year)
                    )
                """))
                
                # Bước 2: Copy dữ liệu từ bảng cũ sang bảng mới
                db.session.execute(text("""
                    INSERT INTO invoices_new 
                    SELECT * FROM invoices
                """))
                
                # Bước 3: Xóa bảng cũ
                db.session.execute(text("DROP TABLE invoices"))
                
                # Bước 4: Đổi tên bảng mới
                db.session.execute(text("ALTER TABLE invoices_new RENAME TO invoices"))
                
                db.session.commit()
                print("✅ Đã thêm unique constraint thành công!")
                print("✅ Từ giờ: MỖI PHÒNG - MỖI THÁNG - CHỈ MỘT HÓA ĐƠN")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Lỗi khi thêm constraint: {e}")
    
    print("\n📊 Thống kê hiện tại:")
    total_invoices = Invoice.query.count()
    print(f"   - Tổng số hóa đơn: {total_invoices}")
    
    # Đếm số phòng đã có hóa đơn
    unique_room_months = db.session.execute(text("""
        SELECT COUNT(DISTINCT CONCAT(room_id, '-', month, '-', year)) as count
        FROM invoices
    """)).scalar()
    print(f"   - Số phòng-tháng unique: {unique_room_months}")
    
    print("\n✅ Migration hoàn tất!")
