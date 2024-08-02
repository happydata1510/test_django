from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # 읽기 전용 요청(GET, HEAD, OPTIONS)은 항상 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 그 외의 요청은 관리자에게만 허용
        return request.user and request.user.is_staff
