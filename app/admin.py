from app import app, db, dao
from app.models import *
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import request, redirect, url_for


class CommonView(ModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True


class AuthenticatedView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated \
               and current_user.user_role == UserRole.ADMIN:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_admin', next=request.url))


class MyAdminIndexView(AdminIndexView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        if request.method.__eq__('POST'):
            month_year = request.form.get('month_year')
            if month_year.__ne__(''):
                year = datetime.strptime(month_year, "%Y-%m").year
                month = datetime.strptime(month_year, "%Y-%m").month

                month_revenue_stats = dao.month_revenue_stats(year, month)
                month_density_stats = dao.month_density_stats(year, month)

                return self.render('admin/index.html',
                                   month_revenue_stats=month_revenue_stats[0],
                                   total_revenue=month_revenue_stats[1],
                                   month_density_stats=month_density_stats[0],
                                   total_density=month_density_stats[1],
                                   year=year, month=month)
        month_revenue_stats = dao.month_revenue_stats()
        month_density_stats = dao.month_density_stats()
        return self.render('admin/index.html',
                           month_revenue_stats=month_revenue_stats[0],
                           total_revenue=month_revenue_stats[1],
                           month_density_stats=month_density_stats[0],
                           total_density=month_density_stats[1])

    def is_accessible(self):
        if current_user.is_authenticated \
               and current_user.user_role == UserRole.ADMIN:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_admin', next=request.url))


class UserView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã người dùng',
        'username': 'Tên người dùng',
        'password': 'Mật khẩu',
        'avatar': 'Ảnh đại diện',
        'email': 'Email',
        'active': 'Hoạt động',
        'joined_date': 'Ngày tham gia',
        'comments': 'Bình luận',
        'user_role': 'Quyền'
    }
    column_list = ['username', 'password', 'avatar', 'email', 'active', 'joined_date', 'user_role']
    column_searchable_list = ['username', 'email', 'user_role']
    column_filters = ['username', 'email', 'active', 'joined_date', 'user_role']
    form_columns = ['username', 'password', 'avatar', 'email', 'active', 'joined_date', 'user_role']


class CustomerTypeView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã loại khách hàng',
        'customer_type_name': 'Tên loại khách hàng',
        'note': 'Ghi chú',
        'customer': 'Khách hàng'
    }
    column_searchable_list = ['id', 'customer_type_name']
    column_filters = ['id', 'customer_type_name']
    form_columns = ['customer_type_name', 'note', 'customers']


class CustomerView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã khách hàng',
        'name': 'Tên',
        'gender': 'Giới tính',
        'identification_card': 'Số CMND',
        'customer_type_id': 'Mã loại khách hàng',
        'customer_type': 'Loại khách hàng',
        'address': 'Địa chỉ',
        'phone_number': 'Số điện thoại',
        'note': 'Ghi chú',
    }
    column_searchable_list = ['identification_card', 'phone_number', 'name']
    column_filters = ['name', 'gender', 'identification_card',
                      'address', 'phone_number', 'customer_type_id']
    form_excluded_columns = ['rents', 'book_rooms']


class BookRoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã đặt phòng',
        'booking_date': 'Ngày đặt phòng',
        'check_in_date': 'Ngày nhận phòng',
        'check_out_date': 'Ngày trả phòng',
        'active': 'Hoạt động',
        'done': 'Hoàn thành',
        'note': 'Ghi chú',
        'user': 'Tài khoản người dùng',

        'rooms': 'Phòng đặt',
        'customer': 'Khách hàng'
    }
    column_list = ['booking_date', 'check_in_date', 'check_out_date', 'rooms', 'customer', 'user', 'active',
                   'done', 'note']
    column_filters = ['booking_date', 'check_in_date', 'check_out_date', 'active', 'done']
    form_columns = ['check_in_date', 'check_out_date', 'rooms', 'customer', 'user', 'active', 'done', 'note']


class RentView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã thuê phòng',
        'check_in_date': 'Ngày nhận phòng',
        'check_out_date': 'Ngày trả phòng',
        'active': 'Hoạt động',
        'note': 'Ghi chú',
        'room_id': 'Mã phòng',
        'room': 'Phòng thuê',

        'customers': 'Khách hàng',
        'bill': 'Hóa đơn thanh toán'
    }
    column_list = ['check_in_date', 'check_out_date', 'customers', 'room', 'room_id', 'active', 'note']
    column_filters = ['check_in_date', 'check_out_date', 'room_id', 'active']
    form_columns = ['check_in_date', 'check_out_date', 'customers', 'room', 'active', 'note']
    pass


class BillView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã hóa đơn thanh toán',
        'total': 'Tổng tiền',
        'created_date': 'Ngày lập hóa đơn',
        'note': 'Ghi chú',

        'rent': 'Phiếu thuê phòng',
    }
    column_list = ['id', 'rent', 'total', 'created_date', 'note']
    column_searchable_list = ['id', 'total']
    column_filters = ['id', 'total', 'created_date']
    form_columns = ['rent', 'total', 'note']


class RoomStatusView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã tình trạng phòng',
        'room_status_name': 'Tên tình trạng phòng',
        'rooms': 'Phòng'
    }
    column_list = ['room_status_name', 'rooms']
    column_searchable_list = ['room_status_name']
    column_filters = ['room_status_name']
    form_columns = ['room_status_name', 'rooms']


class KindOfRoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã loại phòng',
        'kind_of_room_name': 'Loại phòng',
        'description': 'Mô tả',
        'images': 'Hình ảnh',
        'note': 'Ghi chú',
        'rooms': 'Phòng'
    }
    column_list = ['kind_of_room_name', 'description', 'rooms', 'images', 'note']
    column_searchable_list = ['kind_of_room_name']
    column_filters = ['kind_of_room_name']
    form_columns = ['kind_of_room_name', 'description', 'rooms', 'images', 'note']


class ImageView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã hình ảnh',
        'rank': 'Thứ tự ảnh',
        'link': 'Đường dẫn ảnh',
        'kind_of_room_id': 'Mã loại phòng',
        'note': 'Ghi chú',

        'kind_of_room': 'Loại phòng'
    }
    column_list = ['link', 'rank', 'kind_of_room', 'kind_of_room_id', 'note']
    column_filters = ['kind_of_room_id']
    form_columns = ['link', 'rank', 'kind_of_room', 'note']


class RoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'Mã phòng',
        'room_number': 'Số phòng',
        'price': 'Giá',
        'standard_number': 'Số lượng tiêu chuẩn',
        'maximum_number': 'Số lượng tối đa',
        'description': 'Mô tả',
        'kind_of_room_id': 'Mã loại phòng',
        'room_status_id': 'Mã tình trạng',
        'image': 'Hình ảnh',
        'note': 'Ghi chú',
        'comments': 'Bình luận',

        'kind_of_room': 'Loại phòng',
        'room_status': 'Tình trạng phòng',
        'active': 'Hoạt động',
        'book_rooms': 'Phiếu đặt phòng',
        'rents': 'Phiếu thuê phòng',
        'book_rooms': 'Đặt phòng',
        'rents': 'Thuê phòng'
    }
    column_list = ['room_number', 'price', 'standard_number', 'maximum_number', 'description', 'kind_of_room',
                   'room_status',
                   'kind_of_room_id', 'active', 'image', 'note']
    column_searchable_list = ['room_number', 'price']
    column_filters = ['room_number', 'kind_of_room_id', 'room_status_id', 'price', 'standard_number', 'maximum_number',
                      'active']
    form_columns = ['room_number', 'price', 'standard_number', 'maximum_number',
                    'description', 'active', 'kind_of_room', 'room_status', 'image', 'note']


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
        'created_date': 'Ngày tạo',
        'content': 'Nội dung',

        'user': 'Người dùng',
        'room': 'Phòng'
    }
    column_filters = ['created_date', 'user_id', 'room_id']


admin = Admin(app=app, name='TRANG QUẢN TRỊ', template_mode='bootstrap4',
              index_view=MyAdminIndexView(menu_icon_type='fa', menu_icon_value='fa-tachometer', name='Thống kê'))

# user_management
admin.add_view(UserView(User,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-user', name='Người dùng',
                        category='Quản lý người dùng'))
admin.add_view(CustomerView(Customer,
                            db.session, menu_icon_type='fa', menu_icon_value='fa-users', name='Khách hàng',
                            category='Quản lý người dùng'))
admin.add_view(CustomerTypeView(CustomerType,
                                db.session, menu_icon_type='fa', menu_icon_value='fa-id-badge', name='Loại khách hàng',
                                category='Quản lý người dùng'))
admin.add_sub_category(name='user_management', parent_name='Quản lý người dùng')

# manage_votes
admin.add_view(BookRoomView(BookRoom,
                            db.session, menu_icon_type='fa', menu_icon_value='fa-check-square', name='Phiếu đặt phòng',
                            category='Quản lý phiếu'))
admin.add_view(RentView(Rent,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-shopping-basket', name='Phiếu thuê phòng',
                        category='Quản lý phiếu'))
admin.add_view(BillView(Bill,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-credit-card', name='Hóa đơn thanh toán',
                        category='Quản lý phiếu'))
admin.add_sub_category(name='manage_votes ', parent_name='Quản lý phiếu')

# room_manager
admin.add_view(ImageView(Image,
                         db.session, menu_icon_type='fa', menu_icon_value='fa-image', name='Hình ảnh phòng',
                         category='Quản lý phòng'))
admin.add_view(RoomStatusView(RoomStatus,
                              db.session, menu_icon_type='fa', menu_icon_value='fa-bars', name='Tình trạng phòng',
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
