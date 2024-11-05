from rest_framework.permissions import BasePermission

class IsCompanyAdmin(BasePermission):
    '''
    Allows access only to Company admin users
    '''
    def has_permission(self, request, view):
        user_role = request.user.role
        is_true = (user_role == 'company_admin')
        return bool(is_true and request.user.is_authenticated)


class IsSuperAdmin(BasePermission):
    '''
    Allows access only to super users
    '''
    def has_permission(self, request, view):
        user_role = request.user.role
        is_true = (user_role == 'super_admin')
        return bool(is_true and request.user.is_authenticated)


class IsUser(BasePermission):
    '''
    Allows access to regular users
    '''
    def has_permission(self, request, view):
        user_role = request.user.role
        is_true = (user_role == 'user')
        return bool(is_true and request.user.is_authenticated)


class IsStaff(BasePermission):
    '''
    Allows access to staff members?
    '''
    def has_permission(self, request, view):
        user_role = request.user.role
        is_true = (user_role == 'staff')
        return bool(is_true and request.user.is_authenticated)
    