# -*- encoding:utf-8 -*-
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated

from users.models import User


class IsProfileOwner(IsAuthenticated):
    """
    Restrict edit to owners only
    """
    def has_object_permission(self, request, view, obj=None):
        # in edit request restrict permission to profile owner only
        if (request.method in ['PUT', 'PATCH']) and obj is not None:
            model = obj.__class__.__name__

            user_id = obj.id

            # in case of social link view
            if model == 'SocialLink':
                user_id = obj.user.id

            return request.user.id == user_id
        else:
            return True

    def has_permission(self, request, view):
        """ applies to social-link-list """
        if request.method == 'POST':
            user = User.objects.only('id', 'username').get(username=request.user.username)
            return request.user.id == user.id

        return True


class IsNotAuthenticated(IsAuthenticated):
    """
    Restrict access only to unauthenticated users.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return False
        else:
            return True


class IsSuperUser(IsAuthenticated):
    def has_permission(self, request, view, obj=None):
        return request.user and request.user.is_authenticated() and request.user.is_superuser


class BasePermissionSet(BasePermission):
    """
        This Object apply a set of permission for each Viewset Method
        via  {method}_perms  attribute.

        retrieve_perms : GET
        update_perms : PATCH
        destroy_perms : DELETE
    """
    default_perms = [AllowAny, ]

    def get_perm_set(self, request, view):
        perm = "{}_perms".format(view.action)
        permset = getattr(self, perm)

        if not isinstance(permset, (list, tuple)):
            raise RuntimeError("Invalid permission definition.")

        if permset is None:
            return [permission() for permission in self.default_perms]
        else:
            return [permission() for permission in permset]

    def has_permission(self, request, view):
        # DEBUG print view.action, " view in has permission"
        if view.action:
            for permission in self.get_perm_set(request, view):
                if not permission.has_permission(request, self):
                    return False
            return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # DEBUG print view.action, " view in has permission object"
        if view.action:
            for permission in self.get_perm_set(request, view):
                if not permission.has_object_permission(request, self, obj):
                    return False
            return True
        else:
            return True








