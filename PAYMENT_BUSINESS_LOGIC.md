# NGHIỆP VỤ THANH TOÁN HÓA ĐƠN - TÀI LIỆU CHI TIẾT

---

## MỤC LỤC

1. [Tổng quan](#1-tổng-quan)
2. [Các phương thức thanh toán](#2-các-phương-thức-thanh-toán)
3. [Validation và quy tắc](#3-validation-và-quy-tắc)
4. [Trạng thái hóa đơn](#4-trạng-thái-hóa-đơn)
5. [Công nợ và quá hạn](#5-công-nợ-và-quá-hạn)
6. [Báo cáo và thống kê](#6-báo-cáo-và-thống-kê)
7. [Xử lý trường hợp đặc biệt](#7-xử-lý-trường-hợp-đặc-biệt)

---

## 1. TỔNG QUAN

### 1.1. Quy trình thanh toán cơ bản

```
Tạo hóa đơn → Ghi nhận thanh toán → Cập nhật trạng thái → Hoàn tất
```

### 1.2. Model dữ liệu

**Invoice (Hóa đơn)**
- `total_amount`: Tổng tiền hóa đơn
- `status`: Trạng thái (unpaid, partial, paid)
- `due_date`: Hạn thanh toán
- `payment_date`: Ngày thanh toán đủ

**Payment (Thanh toán)**
- `amount`: Số tiền thanh toán
- `payment_method`: Phương thức (cash, bank_transfer)
- `payment_date`: Ngày thanh toán
- `notes`: Ghi chú

### 1.3. Quan hệ

- 1 hóa đơn có thể có nhiều lần thanh toán (1-N)
- Tổng các thanh toán = `paid_amount`
- Còn nợ = `total_amount - paid_amount`

---

## 2. CÁC PHƯƠNG THỨC THANH TOÁN

### 2.1. Thanh toán TOÀN BỘ (Phổ biến nhất - 70%)

**Đặc điểm:**
- Khách trả đủ 100% hóa đơn trong 1 lần
- Đơn giản, dễ quản lý
- Trạng thái chuyển từ `unpaid` → `paid`

**Ví dụ:**
```
Hóa đơn: 3.355.000đ
Khách trả: 3.355.000đ
→ Status: paid
→ payment_date: được set tự động
```

**Code logic:**
```python
if paid_amount >= total_amount:
    status = 'paid'
    payment_date = datetime.utcnow()
```

### 2.2. Thanh toán TỪNG PHẦN (Partial Payment - 20%)

**Đặc điểm:**
- Khách trả dần, mỗi lần 1 phần
- 1 hóa đơn có nhiều record Payment
- Trạng thái `partial` cho đến khi trả đủ

**Ví dụ:**
```
Hóa đơn: 3.355.000đ

Lần 1: 1.000.000đ → Status: partial, Còn nợ: 2.355.000đ
Lần 2: 1.000.000đ → Status: partial, Còn nợ: 1.355.000đ
Lần 3: 1.355.000đ → Status: paid, Còn nợ: 0đ
```

**Lưu ý quan trọng:**
- ✅ ĐÚNG: 1 Invoice, 3 Payments
- ❌ SAI: 3 Invoices riêng biệt

### 2.3. Thanh toán CHUYỂN KHOẢN

**Quy trình:**
1. Chủ nhà gửi thông tin CK cho khách
2. Khách chuyển khoản + gửi bill
3. Chủ nhà check bank → Xác nhận
4. Ghi nhận thanh toán trong hệ thống

**Thông tin cần ghi:**
- `payment_method`: bank_transfer
- `notes`: Mã GD, ngân hàng
- Có thể đính kèm ảnh bill

### 2.4. Thanh toán TRƯỚC HẠN

**Lợi ích:**
- Chủ nhà thu tiền sớm
- Khách không bị quên
- Có thể giảm giá ưu đãi

**Xử lý:**
- Tạo hóa đơn bình thường
- Cho phép thanh toán ngay
- `payment_date` ghi thời điểm thực tế

---

## 3. VALIDATION VÀ QUY TẮC

### 3.1. Validation 1: Số tiền > 0

```python
if amount <= 0:
    flash('❌ Số tiền thanh toán phải lớn hơn 0!', 'danger')
    return redirect(...)
```

**Lý do:** Tránh ghi nhận thanh toán không hợp lệ

### 3.2. Validation 2: Số tiền ≤ Còn nợ

```python
remaining = invoice.remaining_amount
if amount > remaining:
    flash(f'❌ Số tiền thanh toán ({amount:,.0f}đ) '
          f'lớn hơn số tiền còn nợ ({remaining:,.0f}đ)!', 'danger')
    return redirect(...)
```

**Lý do:**
- Tránh trả thừa
- Tránh lỗi ghi sổ
- Nếu thực sự trả thừa → Xử lý riêng (hoàn tiền)

### 3.3. Validation 3: Không thanh toán hóa đơn đã đủ

```python
if invoice.status == 'paid' and invoice.remaining_amount == 0:
    flash('⚠️ Hóa đơn này đã được thanh toán đầy đủ!', 'warning')
    return redirect(...)
```

**Lý do:** Tránh duplicate payment

### 3.4. Validation 4: Phương thức hợp lệ

```python
valid_methods = ['cash', 'bank_transfer']
if payment_method not in valid_methods:
    flash('❌ Phương thức thanh toán không hợp lệ!', 'danger')
    return redirect(...)
```

---

## 4. TRẠNG THÁI HÓA ĐƠN

### 4.1. Các trạng thái

| Trạng thái | Điều kiện | Badge |
|-----------|-----------|-------|
| `unpaid` | `paid_amount == 0` | 🔴 Chưa thanh toán |
| `partial` | `0 < paid_amount < total_amount` | 🟡 Thanh toán 1 phần |
| `paid` | `paid_amount >= total_amount` | 🟢 Đã thanh toán |

### 4.2. Logic tự động cập nhật trạng thái

```python
def update_status(self):
    """Tự động cập nhật trạng thái dựa trên số tiền đã trả"""
    paid = self.paid_amount
    
    if paid == 0:
        self.status = 'unpaid'
        self.payment_date = None
    elif paid >= self.total_amount:
        self.status = 'paid'
        # Chỉ set payment_date lần đầu tiên
        if self.payment_date is None:
            self.payment_date = datetime.utcnow()
    else:
        self.status = 'partial'
        self.payment_date = None
```

### 4.3. Thuộc tính tính toán (Properties)

```python
@property
def paid_amount(self):
    """Tổng đã trả = SUM(payments.amount)"""
    return sum(p.amount for p in self.payments)

@property
def remaining_amount(self):
    """Còn nợ = Tổng - Đã trả"""
    return max(0, self.total_amount - self.paid_amount)
```

---

## 5. CÔNG NỢ VÀ QUÁ HẠN

### 5.1. Tính số ngày quá hạn

```python
@property
def days_overdue(self):
    """Tính số ngày quá hạn"""
    if self.status == 'paid':
        return 0
    if not self.due_date:
        return 0
    
    now = datetime.utcnow()
    if now > self.due_date:
        delta = now - self.due_date
        return delta.days
    return 0
```

### 5.2. Phân loại mức độ nợ

| Mức độ | Ngày quá hạn | Màu | Hành động |
|--------|--------------|-----|-----------|
| `ok` | 0 | - | Không có |
| `warning` | 1-5 ngày | 🟡 Vàng | Nhắc nhở nhẹ |
| `danger` | 5-10 ngày | 🟠 Cam | Gọi điện đôn đốc |
| `critical` | > 10 ngày | 🔴 Đỏ đậm | Cắt dịch vụ / Buộc chuyển đi |

```python
@property
def overdue_level(self):
    """Phân loại mức độ nợ"""
    days = self.days_overdue
    
    if days == 0:
        return 'ok'
    elif days <= 5:
        return 'warning'
    elif days <= 10:
        return 'danger'
    else:
        return 'critical'
```

### 5.3. Badge HTML

```python
@property
def overdue_badge(self):
    """Badge HTML cho UI"""
    days = self.days_overdue
    
    if days == 0:
        return ''
    elif days <= 5:
        return f'<span class="badge bg-warning">Quá hạn {days} ngày</span>'
    elif days <= 10:
        return f'<span class="badge bg-danger">Nợ {days} ngày</span>'
    else:
        return f'<span class="badge bg-dark">Nợ xấu {days} ngày</span>'
```

---

## 6. BÁO CÁO VÀ THỐNG KÊ

### 6.1. Tổng hợp thu tiền (Collection Summary)

```python
PaymentService.get_collection_summary(month=2, year=2024)
```

**Kết quả:**
```python
{
    'total_receivable': 50_000_000,      # Tổng phải thu
    'total_collected': 40_000_000,       # Đã thu
    'total_uncollected': 10_000_000,     # Chưa thu
    'collection_rate': 80.0,             # Tỷ lệ thu 80%
    'invoice_count': 30                  # 30 hóa đơn
}
```

### 6.2. Báo cáo công nợ (Debt Report)

```python
PaymentService.get_debt_report(month=2, year=2024)
```

**Kết quả:**
```python
{
    'total_invoices': 30,
    'paid_count': 20,                    # Đã thanh toán đủ
    'partial_count': 7,                  # Trả 1 phần
    'unpaid_count': 3,                   # Chưa trả
    
    'overdue_warning_count': 3,          # Nợ 1-5 ngày
    'overdue_warning_amount': 5_000_000,
    
    'overdue_danger_count': 2,           # Nợ 5-10 ngày
    'overdue_danger_amount': 4_000_000,
    
    'overdue_critical_count': 1,         # Nợ xấu > 10 ngày
    'overdue_critical_amount': 3_000_000,
}
```

### 6.3. Dashboard công nợ

**URL:** `/reports/overdue`

**Hiển thị:**
- Tổng quan thu tiền (4 cards)
- Công nợ theo mức độ (3 categories)
- Danh sách chi tiết từng loại
- Thao tác nhanh (Thu tiền, Xem chi tiết)

---

## 7. XỬ LÝ TRƯỜNG HỢP ĐẶC BIỆT

### 7.1. Khách chuyển đi giữa tháng

**Tình huống:** Khách chuyển đi ngày 5/2

**Cách xử lý:**

**Phương án A (Đơn giản - Khuyến nghị):**
```
1. KHÔNG tạo hóa đơn tháng 2
2. Tính phí theo ngày: 5 × (2.500.000 / 30) = 416.667đ
3. Thu tiền mặt riêng, không vào hệ thống
4. Hoàn tiền cọc
```

**Phương án B (Chi tiết):**
```
1. Tạo hóa đơn tháng 2
2. Giảm giá phòng: 416.667đ (5 ngày)
3. Điện/nước: Tính theo số thực tế
4. Ghi chú: "Chuyển đi 5/2, chỉ ở 5 ngày"
```

### 7.2. Sửa hóa đơn đã tạo

**Quy tắc:**
- ✅ Cho phép sửa khi: `status != 'paid'`
- ❌ Không cho sửa khi: `status == 'paid'`

**Cảnh báo quan trọng:**

```python
# Khi sửa số điện/nước mới của tháng 1
# → Phải cập nhật số cũ của tháng 2

if next_invoice:
    flash('⚠️ Bạn cần kiểm tra hóa đơn tháng sau!', 'warning')
```

**UI hiển thị:**
```html
<div class="alert alert-warning">
    Phòng này đã có hóa đơn tháng sau.
    Nếu thay đổi số điện/nước, hãy cập nhật hóa đơn tháng sau!
</div>
```

### 7.3. Thu thừa tiền

**Tình huống:** Hóa đơn 3.355.000đ, khách chuyển 3.500.000đ

**Cách xử lý:**

**Phương án A: Hoàn lại ngay**
```
1. Ghi nhận thanh toán: 3.355.000đ
2. Chuyển khoản lại: 145.000đ
3. Ghi chú: "Hoàn thừa 145k"
```

**Phương án B: Trừ vào tháng sau**
```
1. Lưu ý khách đã trả trước 145k
2. Tháng sau giảm giá: -145.000đ
3. Ghi chú: "Trừ tiền thừa tháng trước"
```

### 7.4. Giảm giá / Ưu đãi

**Cách thực hiện:**

**Trong quá trình tạo hóa đơn:**
```
1. Tạo hóa đơn bình thường: 3.355.000đ
2. Thêm "Phí khác": -335.500đ (giảm 10%)
3. Ghi chú: "Giảm giá 10% khách lâu năm"
4. Tổng: 3.019.500đ
```

**Hoặc giảm tiền phòng trực tiếp:**
```
1. Tiền phòng: 2.500.000đ → 2.250.000đ
2. Ghi chú: "Giảm 10% khách cũ"
```

### 7.5. Hóa đơn bổ sung

**Tình huống:** Điều hòa hỏng giữa tháng, sửa 500k

**Cách xử lý:**

```python
# Sửa hóa đơn hiện tại
invoice.other_fees += 500_000
invoice.notes += ' + Sửa điều hòa 500k'
invoice.calculate_total()
db.session.commit()
```

**Kết quả:**
```
Tổng cũ: 3.355.000đ
Tổng mới: 3.855.000đ
Nếu đã trả 3.355.000đ → Còn nợ thêm 500.000đ
```

---

## PHỤ LỤC: QUICK REFERENCE

### Flash Messages mẫu

```python
# Success
flash('✅ Đã ghi nhận thanh toán 1.000.000đ!', 'success')

# Warning
flash('⚠️ Số tiền vượt quá số tiền còn nợ!', 'warning')

# Danger
flash('❌ Số tiền phải lớn hơn 0!', 'danger')

# Info
flash('💡 Hóa đơn còn nợ 2.355.000đ', 'info')
```

### JavaScript Validation

```javascript
// Real-time validation
amountInput.addEventListener('input', function() {
    const amount = parseFloat(this.value) || 0;
    const remaining = parseFloat('{{ invoice.remaining_amount }}');
    
    if (amount > remaining) {
        showAlert('danger', 'Số tiền vượt quá còn nợ!');
        submitBtn.disabled = true;
    } else {
        submitBtn.disabled = false;
    }
});

// Confirmation cho partial payment
form.addEventListener('submit', function(e) {
    if (amount < remaining) {
        const confirmed = confirm(
            `Thanh toán ${amount}đ, còn nợ ${remaining - amount}đ. Tiếp tục?`
        );
        if (!confirmed) e.preventDefault();
    }
});
```

### SQL Queries hữu ích

```sql
-- Tổng thu trong tháng
SELECT SUM(amount) FROM payments 
WHERE MONTH(payment_date) = 2 AND YEAR(payment_date) = 2024;

-- Hóa đơn quá hạn
SELECT * FROM invoices 
WHERE status != 'paid' AND due_date < NOW()
ORDER BY due_date;

-- Khách nợ nhiều nhất
SELECT room_id, SUM(remaining_amount) as debt
FROM invoices WHERE status != 'paid'
GROUP BY room_id ORDER BY debt DESC;
```

---

**Tài liệu này được tạo ngày:** 08/11/2024  
**Phiên bản:** 1.0  
**Tác giả:** GitHub Copilot  
**Hệ thống:** RoomMaster - Quản lý nhà trọ
