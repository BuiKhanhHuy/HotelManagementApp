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
        'id': 'M?? ng?????i d??ng',
        'username': 'T??n ng?????i d??ng',
        'password': 'M???t kh???u',
        'avatar': '???nh ?????i di???n',
        'email': 'Email',
        'active': 'Ho???t ?????ng',
        'joined_date': 'Ng??y tham gia',
        'comments': 'B??nh lu???n',
        'user_role': 'Quy???n'
    }
    column_list = ['username', 'password', 'avatar', 'email', 'active', 'joined_date', 'user_role']
    column_searchable_list = ['username', 'email', 'user_role']
    column_filters = ['username', 'email', 'active', 'joined_date', 'user_role']
    form_columns = ['username', 'password', 'avatar', 'email', 'active', 'joined_date', 'user_role']


class CustomerTypeView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? lo???i kh??ch h??ng',
        'customer_type_name': 'T??n lo???i kh??ch h??ng',
        'note': 'Ghi ch??',
        'customer': 'Kh??ch h??ng'
    }
    column_searchable_list = ['id', 'customer_type_name']
    column_filters = ['id', 'customer_type_name']
    form_columns = ['customer_type_name', 'note', 'customers']


class CustomerView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? kh??ch h??ng',
        'name': 'T??n',
        'gender': 'Gi???i t??nh',
        'identification_card': 'S??? CMND',
        'customer_type_id': 'M?? lo???i kh??ch h??ng',
        'customer_type': 'Lo???i kh??ch h??ng',
        'address': '?????a ch???',
        'phone_number': 'S??? ??i???n tho???i',
        'note': 'Ghi ch??',
    }
    column_searchable_list = ['identification_card', 'phone_number', 'name']
    column_filters = ['name', 'gender', 'identification_card',
                      'address', 'phone_number', 'customer_type_id']
    form_excluded_columns = ['rents', 'book_rooms']


class BookRoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? ?????t ph??ng',
        'booking_date': 'Ng??y ?????t ph??ng',
        'check_in_date': 'Ng??y nh???n ph??ng',
        'check_out_date': 'Ng??y tr??? ph??ng',
        'active': 'Ho???t ?????ng',
        'done': 'Ho??n th??nh',
        'note': 'Ghi ch??',
        'user': 'T??i kho???n ng?????i d??ng',

        'rooms': 'Ph??ng ?????t',
        'customer': 'Kh??ch h??ng'
    }
    column_list = ['booking_date', 'check_in_date', 'check_out_date', 'rooms', 'customer', 'user', 'active',
                   'done', 'note']
    column_filters = ['booking_date', 'check_in_date', 'check_out_date', 'active', 'done']
    form_columns = ['check_in_date', 'check_out_date', 'rooms', 'customer', 'user', 'active', 'done', 'note']


class RentView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? thu?? ph??ng',
        'check_in_date': 'Ng??y nh???n ph??ng',
        'check_out_date': 'Ng??y tr??? ph??ng',
        'active': 'Ho???t ?????ng',
        'note': 'Ghi ch??',
        'room_id': 'M?? ph??ng',
        'room': 'Ph??ng thu??',

        'customers': 'Kh??ch h??ng',
        'bill': 'H??a ????n thanh to??n'
    }
    column_list = ['check_in_date', 'check_out_date', 'customers', 'room', 'room_id', 'active', 'note']
    column_filters = ['check_in_date', 'check_out_date', 'room_id', 'active']
    form_columns = ['check_in_date', 'check_out_date', 'customers', 'room', 'active', 'note']
    pass


class BillView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? h??a ????n thanh to??n',
        'total': 'T???ng ti???n',
        'created_date': 'Ng??y l???p h??a ????n',
        'note': 'Ghi ch??',

        'rent': 'Phi???u thu?? ph??ng',
    }
    column_list = ['id', 'rent', 'total', 'created_date', 'note']
    column_searchable_list = ['id', 'total']
    column_filters = ['id', 'total', 'created_date']
    form_columns = ['rent', 'total', 'note']


class RoomStatusView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? t??nh tr???ng ph??ng',
        'room_status_name': 'T??n t??nh tr???ng ph??ng',
        'rooms': 'Ph??ng'
    }
    column_list = ['room_status_name', 'rooms']
    column_searchable_list = ['room_status_name']
    column_filters = ['room_status_name']
    form_columns = ['room_status_name', 'rooms']


class KindOfRoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? lo???i ph??ng',
        'kind_of_room_name': 'Lo???i ph??ng',
        'description': 'M?? t???',
        'images': 'H??nh ???nh',
        'note': 'Ghi ch??',
        'rooms': 'Ph??ng'
    }
    column_list = ['kind_of_room_name', 'description', 'rooms', 'images', 'note']
    column_searchable_list = ['kind_of_room_name']
    column_filters = ['kind_of_room_name']
    form_columns = ['kind_of_room_name', 'description', 'rooms', 'images', 'note']


class ImageView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? h??nh ???nh',
        'rank': 'Th??? t??? ???nh',
        'link': '???????ng d???n ???nh',
        'kind_of_room_id': 'M?? lo???i ph??ng',
        'note': 'Ghi ch??',

        'kind_of_room': 'Lo???i ph??ng'
    }
    column_list = ['link', 'rank', 'kind_of_room', 'kind_of_room_id', 'note']
    column_filters = ['kind_of_room_id']
    form_columns = ['link', 'rank', 'kind_of_room', 'note']


class RoomView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? ph??ng',
        'room_number': 'S??? ph??ng',
        'price': 'Gi??',
        'standard_number': 'S??? l?????ng ti??u chu???n',
        'maximum_number': 'S??? l?????ng t???i ??a',
        'description': 'M?? t???',
        'kind_of_room_id': 'M?? lo???i ph??ng',
        'room_status_id': 'M?? t??nh tr???ng',
        'image': 'H??nh ???nh',
        'note': 'Ghi ch??',
        'comments': 'B??nh lu???n',

        'kind_of_room': 'Lo???i ph??ng',
        'room_status': 'T??nh tr???ng ph??ng',
        'active': 'Ho???t ?????ng',
        'book_rooms': 'Phi???u ?????t ph??ng',
        'rents': 'Phi???u thu?? ph??ng',
        'book_rooms': '?????t ph??ng',
        'rents': 'Thu?? ph??ng'
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
        'id': 'M?? h??? s??? chung',
        'check_in_deadline': 'H???n ng??y nh???n ph??ng',
        'surcharge': 'Ph???n tr??m ph??? thu',
        'number_foreign_visitor': 'H??? s??? kh??ch n?????c ngo??i'
    }
    can_delete = False
    column_filters = ['check_in_deadline', 'surcharge', 'number_foreign_visitor']


class CommentView(CommonView, AuthenticatedView):
    column_labels = {
        'id': 'M?? b??nh lu???n',
        'user_id': 'M?? ng?????i d??ng',
        'room_id': 'M?? ph??ng',
        'created_date': 'Ng??y t???o',
        'content': 'N???i dung',

        'user': 'Ng?????i d??ng',
        'room': 'Ph??ng'
    }
    column_filters = ['created_date', 'user_id', 'room_id']


admin = Admin(app=app, name='TRANG QU???N TR???', template_mode='bootstrap4',
              index_view=MyAdminIndexView(menu_icon_type='fa', menu_icon_value='fa-tachometer', name='Th???ng k??'))

# user_management
admin.add_view(UserView(User,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-user', name='Ng?????i d??ng',
                        category='Qu???n l?? ng?????i d??ng'))
admin.add_view(CustomerView(Customer,
                            db.session, menu_icon_type='fa', menu_icon_value='fa-users', name='Kh??ch h??ng',
                            category='Qu???n l?? ng?????i d??ng'))
admin.add_view(CustomerTypeView(CustomerType,
                                db.session, menu_icon_type='fa', menu_icon_value='fa-id-badge', name='Lo???i kh??ch h??ng',
                                category='Qu???n l?? ng?????i d??ng'))
admin.add_sub_category(name='user_management', parent_name='Qu???n l?? ng?????i d??ng')

# manage_votes
admin.add_view(BookRoomView(BookRoom,
                            db.session, menu_icon_type='fa', menu_icon_value='fa-check-square', name='Phi???u ?????t ph??ng',
                            category='Qu???n l?? phi???u'))
admin.add_view(RentView(Rent,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-shopping-basket', name='Phi???u thu?? ph??ng',
                        category='Qu???n l?? phi???u'))
admin.add_view(BillView(Bill,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-credit-card', name='H??a ????n thanh to??n',
                        category='Qu???n l?? phi???u'))
admin.add_sub_category(name='manage_votes ', parent_name='Qu???n l?? phi???u')

# room_manager
admin.add_view(ImageView(Image,
                         db.session, menu_icon_type='fa', menu_icon_value='fa-image', name='H??nh ???nh ph??ng',
                         category='Qu???n l?? ph??ng'))
admin.add_view(RoomStatusView(RoomStatus,
                              db.session, menu_icon_type='fa', menu_icon_value='fa-bars', name='T??nh tr???ng ph??ng',
                              category='Qu???n l?? ph??ng'))
admin.add_view(KindOfRoomView(KindOfRoom,
                              db.session, menu_icon_type='fa', menu_icon_value='fa-bars', name='Lo???i ph??ng',
                              category='Qu???n l?? ph??ng'))
admin.add_view(RoomView(Room,
                        db.session, menu_icon_type='fa', menu_icon_value='fa-hotel', name='Ph??ng',
                        category='Qu???n l?? ph??ng'))
admin.add_sub_category(name='room_manager ', parent_name='Qu???n l?? ph??ng')

# CommonCoefficient
admin.add_view(CommonCoefficientView(CommonCoefficient,
                                     db.session, menu_icon_type='fa', menu_icon_value='fa-calculator',
                                     name='H??? s??? chung'))
# Comment
admin.add_view(CommentView(Comment,
                           db.session, menu_icon_type='fa', menu_icon_value='fa-comments', name='B??nh lu???n'))
