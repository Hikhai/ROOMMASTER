"""
Room Service - Business logic cho quản lý phòng
"""
from app import db
from app.models import Room, Tenant
from sqlalchemy import or_, and_


class RoomService:
    """Service xử lý logic nghiệp vụ liên quan đến phòng"""
    
    @staticmethod
    def get_all_rooms(page=1, per_page=10, search=None, status=None):
        """
        Lấy danh sách phòng với filter và phân trang
        
        Args:
            page: Trang hiện tại
            per_page: Số phòng mỗi trang
            search: Từ khóa tìm kiếm
            status: Trạng thái phòng
            
        Returns:
            Pagination object
        """
        query = Room.query
        
        # Áp dụng filter
        if search:
            query = query.filter(
                or_(
                    Room.room_number.ilike(f'%{search}%'),
                    Room.description.ilike(f'%{search}%')
                )
            )
        
        if status:
            query = query.filter(Room.status == status)
        
        # Sắp xếp và phân trang
        return query.order_by(Room.room_number).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def get_room_by_id(room_id):
        """Lấy phòng theo ID"""
        return Room.query.get_or_404(room_id)
    
    @staticmethod
    def get_room_by_number(room_number):
        """Lấy phòng theo số phòng"""
        return Room.query.filter_by(room_number=room_number).first()
    
    @staticmethod
    def create_room(data):
        """
        Tạo phòng mới
        
        Args:
            data: Dictionary chứa thông tin phòng
            
        Returns:
            Room object hoặc None nếu lỗi
        """
        try:
            room = Room(
                room_number=data['room_number'],
                floor=data.get('floor'),
                area=data.get('area'),
                price=data['price'],
                deposit=data.get('deposit', 0),
                status=data.get('status', 'available'),
                description=data.get('description')
            )
            db.session.add(room)
            db.session.commit()
            return room
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_room(room_id, data):
        """
        Cập nhật thông tin phòng
        
        Args:
            room_id: ID của phòng
            data: Dictionary chứa thông tin cần update
            
        Returns:
            True nếu thành công, False nếu thất bại
        """
        try:
            room = Room.query.get_or_404(room_id)
            
            # Cập nhật các trường
            for key, value in data.items():
                if hasattr(room, key):
                    setattr(room, key, value)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_room(room_id):
        """
        Xóa phòng
        
        Args:
            room_id: ID của phòng
            
        Returns:
            True nếu thành công
            
        Raises:
            ValueError: Nếu phòng đang có người thuê
        """
        room = Room.query.get_or_404(room_id)
        
        # Kiểm tra phòng có người thuê không
        if room.status == 'occupied':
            active_tenants = Tenant.query.filter_by(
                room_id=room_id, 
                status='active'
            ).count()
            if active_tenants > 0:
                raise ValueError('Không thể xóa phòng đang có người thuê')
        
        try:
            db.session.delete(room)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_available_rooms():
        """Lấy danh sách phòng trống"""
        return Room.query.filter_by(status='available').order_by(Room.room_number).all()
    
    @staticmethod
    def get_room_statistics():
        """
        Lấy thống kê về phòng
        
        Returns:
            Dictionary chứa thống kê
        """
        total_rooms = Room.query.count()
        occupied_rooms = Room.query.filter_by(status='occupied').count()
        available_rooms = Room.query.filter_by(status='available').count()
        maintenance_rooms = Room.query.filter_by(status='maintenance').count()
        
        return {
            'total': total_rooms,
            'occupied': occupied_rooms,
            'available': available_rooms,
            'maintenance': maintenance_rooms,
            'occupancy_rate': (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
        }
    
    @staticmethod
    def update_room_status(room_id, status):
        """
        Cập nhật trạng thái phòng
        
        Args:
            room_id: ID của phòng
            status: Trạng thái mới ('available', 'occupied', 'maintenance')
        """
        room = Room.query.get_or_404(room_id)
        room.status = status
        db.session.commit()
        return room
