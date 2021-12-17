from app import app, db
from app.models import *
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView


class CommonView(ModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True


class AuthenticatedView(ModelView):
    pass


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class UserRoleView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã quyền',
        'role_name': 'Tên quyền',
        'note': 'Ghi chú',
        'users': 'Người dùng'
    }
    column_searchable_list = ['role_name']
    column_filters = ['role_name']
    form_columns = ['role_name', 'users', 'note']


class UserView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã người dùng',
        'username': 'Tên người dùng',
        'password': 'Mật khẩu',
        'avatar': 'Ảnh đại diện',
        'email': 'Email',
        'active': 'Hoạt động',
        'joined_date': 'Ngày tham gia',
        'user_role_id': 'Mã quyền',
        'comments': 'Bình luận',

        'user_role': 'Quyền'
    }
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'active', 'joined_date', 'user_role_id']
    form_columns = ['username', 'password', 'avatar', 'email', 'active', 'joined_date', 'user_role']


class CustomerView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã khách hàng',
        'first_name': 'Tên',
        'last_name': 'Họ',
        'birthday': 'Ngày sinh',
        'gender': 'Giới tính',
        'identification_card': 'Số CMND',
        'nationality': 'Quốc tịch',
        'address': 'Địa chỉ',
        'phone_number': 'Số điện thoại',
        'note': 'Ghi chú',
        'comments': 'Bình luận',
        'rents': 'Phiếu thuê phòng',
        'book_rooms': 'Phiếu đặt phòng'
    }
    column_searchable_list = ['identification_card', 'phone_number', 'first_name', ]
    column_filters = ['first_name', 'last_name', 'birthday', 'gender', 'identification_card',
                      'nationality', 'address', 'phone_number']
    form_excluded_columns = ['comments', 'rents', 'book_rooms']


class BookRoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã đặt phòng',
        'check_in_date': 'Ngày nhận phòng',
        'check_out_date': 'Ngày trả phòng',
        'customer_id': 'Mã khách hàng',
        'note': 'Ghi chú',
        'rooms': 'Phòng',

        'customer': 'Khách hàng'
    }
    column_filters = ['check_in_date', 'check_out_date', 'customer_id']
    form_columns = ['check_in_date', 'check_out_date', 'customer', 'rooms', 'note']


class RentView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã thuê phòng',
        'check_in_date': 'Ngày nhận phòng',
        'check_out_date': 'Ngày trả phòng',
        'customer_id': 'Mã khách hàng',
        'note': 'Ghi chú',
        'bills': 'Hóa đơn thanh toán',
        'rooms': 'Phòng',

        'customer': 'Khách hàng',
    }
    column_filters = ['check_in_date', 'check_out_date', 'customer_id']
    form_columns = ['check_in_date', 'check_out_date', 'customer', 'rooms', 'note']


class BillView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã hóa đơn thanh toán',
        'rent_id': 'Mã phiếu thuê phòng',
        'total': 'Tổng tiền',
        'note': 'Ghi chú',

        'rent': 'Phiếu thuê phòng',
    }
    column_searchable_list = ['total']
    column_filters = ['total', 'rent_id']
    form_columns = ['rent_id', 'total', 'rent', 'note']


class KindOfRoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã loại phòng',
        'kind_of_room_name': 'Loại phòng',
        'price': 'Giá',
        'standard_number': 'Số lượng tiêu chuẩn',
        'maximum_number': 'Số lượng tối đa',
        'image': 'Hình ảnh',
        'note': 'Ghi chú',
        'rooms': 'Phòng'
    }
    column_searchable_list = ['kind_of_room_name', 'price']
    column_filters = ['kind_of_room_name', 'price', 'standard_number', 'maximum_number']
    form_columns = ['kind_of_room_name', 'price', 'standard_number', 'maximum_number', 'image', 'rooms', 'note']


class RoomStatusView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã tình trạng phòng',
        'room_status_name': 'Trạng thái phòng',
        'note': 'Ghi chú',
        'rooms': 'Phòng'
    }
    column_searchable_list = ['room_status_name']
    column_filters = ['room_status_name']
    form_columns = ['room_status_name', 'rooms', 'note']


class ImageView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã hình ảnh',
        'rank': 'Thứ tự ảnh',
        'link': 'Đường dẫn ảnh',
        'room_id': 'Mã phòng',
        'note': 'Ghi chú',

        'room': 'Phòng'
    }
    column_filters = ['room_id']
    form_columns = ['link', 'rank', 'room', 'note']


class RoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã phòng',
        'room_number': 'Số phòng',
        'description': 'Mô tả',
        'room_status_id': 'Mã trạng thái',
        'kind_of_room_id': 'Mã loại phòng',
        'note': 'Ghi chú',
        'comments': 'Bình luận',
        'images': 'Hình ảnh',

        'kind_of_room': 'Loại phòng',
        'rooms_status': 'Trạng thái phòng',
        'book_room_detail': 'Chi tiết đặt phòng',
        'rent_detail': 'Chi tiết thuê phòng',
        'book_rooms': 'Đặt phòng',
        'rents': 'Thuê phòng'
    }
    column_searchable_list = ['room_number']
    column_filters = ['room_number', 'kind_of_room_id', 'room_status_id']
    form_columns = ['room_number', 'description', 'rooms_status', 'kind_of_room', 'images', 'note']


class CommonCoefficientView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã hệ số chung',
        'check_in_deadline': 'Hạn ngày nhận phòng',
        'surcharge': 'Phần trăm phụ thu',
        'number_foreign_visitor': 'Hệ số khách nước ngoài'
    }
    can_delete = False
    column_filters = ['check_in_deadline', 'surcharge', 'number_foreign_visitor']


class CommentView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã bình luận',
        'user_id': 'Mã người dùng',
        'room_id': 'Mã phòng',
        'customer_id': 'Mã khách hàng',
        'created_date': 'Ngày tạo',
        'content': 'Nội dung',

        'user': 'Người dùng',
        'customer': 'Khách hàng',
        'room': 'Phòng'
    }
    column_filters = ['created_date', 'user_id', 'customer_id', 'room_id']


admin = Admin(app=app, name='Administrator', template_mode='bootstrap4',
              index_view=MyAdminIndexView(menu_icon_type='fa', menu_icon_value='fa-home'))

# user_management
admin.add_view(UserRoleView(UserRole,
                            db.session, menu_icon_type='fa', menu_icon_value='fa-key', name='Quyền người dùng',
                            category='Quản lý người dùng'))
admin.add_view(UserView(User,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-user', name='Người dùng',
                        category='Quản lý người dùng'))
admin.add_view(CustomerView(Customer,
                            db.session, menu_icon_type='fa', menu_icon_value='fa-users', name='Khách hàng',
                            category='Quản lý người dùng'))
admin.add_sub_category(name='user_management', parent_name='Quản lý người dùng')

# manage_votes
admin.add_view(BookRoomView(BookRoom,
                            db.session, menu_icon_type='fa', menu_icon_value='fa-address-book', name='Đặt phòng',
                            category='Quản lý phiếu'))
admin.add_view(RentView(Rent,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-check-circle', name='Thuê phòng',
                        category='Quản lý phiếu'))
admin.add_view(BillView(Bill,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-sticky-note', name='Hóa đơn thanh toán',
                        category='Quản lý phiếu'))
admin.add_sub_category(name='manage_votes ', parent_name='Quản lý phiếu')

# room_manager
admin.add_view(RoomStatusView(RoomStatus,
                              db.session, menu_icon_type='fa', menu_icon_value='fa-toggle-on', name='Trạng thái phòng',
                              category='Quản lý phòng'))
admin.add_view(ImageView(Image,
                         db.session, menu_icon_type='fa', menu_icon_value='fa-image', name='Hình ảnh phòng',
                         category='Quản lý phòng'))
admin.add_view(KindOfRoomView(KindOfRoom,
                              db.session, menu_icon_type='fa', menu_icon_value='fa-bars', name='Loại phòng',
                              category='Quản lý phòng'))
admin.add_view(RoomView(Room,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-hotel', name='Phòng',
                        category='Quản lý phòng'))
admin.add_sub_category(name='room_manager ', parent_name='Quản lý phòng')

# CommonCoefficient
admin.add_view(CommonCoefficientView(CommonCoefficient,
                                     db.session, menu_icon_type='fa', menu_icon_value='fa-calculator',
                                     name='Hệ số chung'))
# Comment
admin.add_view(CommentView(Comment,
                           db.session, menu_icon_type='fa', menu_icon_value='fa-comments', name='Bình luận'))


