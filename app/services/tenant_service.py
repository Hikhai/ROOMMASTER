"""
Tenant Service - Business logic cho quản lý khách thuê
"""
from app import db
from app.models import Tenant, Room
from datetime import datetime
from sqlalchemy import or_


class TenantService:
    """Service xử lý logic nghiệp vụ liên quan đến khách thuê"""
    
    @staticmethod
    def get_all_tenants(page=1, per_page=10, search=None, status=None):
        """
        Lấy danh sách khách thuê với filter và phân trang
        
        Args:
            page: Trang hiện tại
            per_page: Số khách mỗi trang
            search: Từ khóa tìm kiếm
            status: Trạng thái (active/moved_out)
            
        Returns:
            Pagination object
        """
        query = Tenant.query
        
        # Áp dụng filter
        if search:
            query = query.filter(
                or_(
                    Tenant.full_name.ilike(f'%{search}%'),
                    Tenant.id_number.ilike(f'%{search}%'),
                    Tenant.phone.ilike(f'%{search}%')
                )
            )
        
        if status:
            query = query.filter(Tenant.status == status)
        
        # Sắp xếp và phân trang
        return query.order_by(Tenant.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def get_tenant_by_id(tenant_id):
        """Lấy khách thuê theo ID"""
        return Tenant.query.get_or_404(tenant_id)
    
    @staticmethod
    def create_tenant(data):
        """
        Tạo khách thuê mới
        
        Args:
            data: Dictionary chứa thông tin khách thuê
            
        Returns:
            Tenant object
        """
        try:
            # Parse dates
            move_in_date = datetime.strptime(data['move_in_date'], '%d/%m/%Y').date() \
                if data.get('move_in_date') else None
            
            move_out_date = datetime.strptime(data['move_out_date'], '%d/%m/%Y').date() \
                if data.get('move_out_date') else None
            
            date_of_birth = datetime.strptime(data['date_of_birth'], '%d/%m/%Y').date() \
                if data.get('date_of_birth') else None
            
            tenant = Tenant(
                room_id=data['room_id'],
                full_name=data['full_name'],
                id_number=data['id_number'],
                phone=data['phone'],
                email=data.get('email'),
                date_of_birth=date_of_birth,
                hometown=data.get('hometown'),
                move_in_date=move_in_date,
                move_out_date=move_out_date,
                deposit=data.get('deposit', 0),
                is_main_tenant=data.get('is_main_tenant', False),
                status=data.get('status', 'active'),
                notes=data.get('notes')
            )
            
            db.session.add(tenant)
            
            # Cập nhật trạng thái phòng nếu khách vào ở
            if tenant.status == 'active':
                room = Room.query.get(data['room_id'])
                if room:
                    room.status = 'occupied'
            
            db.session.commit()
            return tenant
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_tenant(tenant_id, data):
        """
        Cập nhật thông tin khách thuê
        
        Args:
            tenant_id: ID của khách thuê
            data: Dictionary chứa thông tin cần update
            
        Returns:
            Tenant object
        """
        try:
            tenant = Tenant.query.get_or_404(tenant_id)
            old_room_id = tenant.room_id
            old_status = tenant.status
            
            # Parse dates nếu có
            if 'move_in_date' in data and data['move_in_date']:
                data['move_in_date'] = datetime.strptime(data['move_in_date'], '%d/%m/%Y').date()
            
            if 'move_out_date' in data and data['move_out_date']:
                data['move_out_date'] = datetime.strptime(data['move_out_date'], '%d/%m/%Y').date()
            
            if 'date_of_birth' in data and data['date_of_birth']:
                data['date_of_birth'] = datetime.strptime(data['date_of_birth'], '%d/%m/%Y').date()
            
            # Cập nhật các trường
            for key, value in data.items():
                if hasattr(tenant, key) and key not in ['id', 'created_at']:
                    setattr(tenant, key, value)
            
            # Cập nhật trạng thái phòng nếu cần
            if old_status != tenant.status or old_room_id != tenant.room_id:
                # Phòng cũ
                if old_room_id:
                    old_room = Room.query.get(old_room_id)
                    if old_room:
                        # Kiểm tra còn khách nào đang ở không
                        remaining = Tenant.query.filter_by(
                            room_id=old_room_id, 
                            status='active'
                        ).count()
                        if remaining == 0:
                            old_room.status = 'available'
                
                # Phòng mới
                if tenant.status == 'active':
                    new_room = Room.query.get(tenant.room_id)
                    if new_room:
                        new_room.status = 'occupied'
            
            db.session.commit()
            return tenant
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def checkout_tenant(tenant_id, checkout_date=None):
        """
        Trả phòng cho khách thuê
        
        Args:
            tenant_id: ID của khách thuê
            checkout_date: Ngày trả phòng (mặc định hôm nay)
            
        Returns:
            Tenant object
        """
        tenant = Tenant.query.get_or_404(tenant_id)
        
        if not checkout_date:
            checkout_date = datetime.now().date()
        
        tenant.status = 'moved_out'
        tenant.move_out_date = checkout_date
        
        # Kiểm tra phòng còn khách nào không
        room = Room.query.get(tenant.room_id)
        if room:
            remaining = Tenant.query.filter_by(
                room_id=room.id,
                status='active'
            ).count()
            
            if remaining == 0:
                room.status = 'available'
        
        db.session.commit()
        return tenant
    
    @staticmethod
    def delete_tenant(tenant_id):
        """Xóa khách thuê"""
        tenant = Tenant.query.get_or_404(tenant_id)
        room_id = tenant.room_id
        
        try:
            db.session.delete(tenant)
            
            # Cập nhật trạng thái phòng nếu cần
            room = Room.query.get(room_id)
            if room:
                remaining = Tenant.query.filter_by(
                    room_id=room_id,
                    status='active'
                ).count()
                
                if remaining == 0:
                    room.status = 'available'
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_active_tenants():
        """Lấy danh sách khách đang thuê"""
        return Tenant.query.filter_by(status='active').all()
    
    @staticmethod
    def get_tenant_statistics():
        """Thống kê khách thuê"""
        total = Tenant.query.count()
        active = Tenant.query.filter_by(status='active').count()
        moved_out = Tenant.query.filter_by(status='moved_out').count()
        
        return {
            'total': total,
            'active': active,
            'moved_out': moved_out
        }
