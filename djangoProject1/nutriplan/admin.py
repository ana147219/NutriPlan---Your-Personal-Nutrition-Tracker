"""
Tijana Gasic 0247/2021
"""

from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.http import request

from . import models
from .my_views.HomeView import DeletePlanView


class MyUserAdmin(UserAdmin):
    """
    Class that represents custom settings and fields for User in admin panel
    """
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')

    search_fields = ['^username']  # which field is used for search


    def get_search_results(self, request, queryset, search_term):
        """
        This function is used to filter the username that fully matches with the username in the search field.
        It returns queryset
        :param request:
        :param queryset:
        :param search_term:
        :return:
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term.strip():
            queryset = queryset.filter(username__exact=search_term)
        return queryset, use_distinct

    fieldsets_superuser = (
        (("BASIC INFO"), {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("email", "gender", "profile_picture")}),
        (("Permissions"),{"fields": ("is_active","is_staff","is_superuser","groups","user_permissions",),},),(("Important dates"), {"fields": ("last_login", "date_joined")}),)

    fieldsets_mod = (
        (("BASIC INFO"), {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("email", "gender", "profile_picture")}),
        (("Permissions"),{"fields": ("is_active","is_staff",),},),(("Important dates"), {"fields": ("last_login", "date_joined")}),)

    fieldsets_regular = (
        (("Personal info"), {"fields": ("email", "gender", "profile_picture")}),(("Permissions"),{"fields": ("is_active",),},),)
    fieldsets_see_admin = (
        (("BASIC ADMIN INFO"), {"fields": ("username","email", "profile_picture","is_staff","is_superuser",)}),)
    fieldsets_see_mod = (
        (("BASIC MODERATOR INFO"), {"fields": ("username","email", "profile_picture","is_staff")}),)
    fieldsets_basic_user_mod_view = ((("Permissions"),{"fields": ("is_active",),},),(("Important dates"), {"fields": ("last_login", "date_joined")}),)


    def has_change_permission(self, request, obj=None):
        """
        This function is used to check if a user has permission to edit certain users
        :param request:
        :param obj:
        :return: bool
        """
        if obj is not None and obj.is_superuser:
            if request.user.is_superuser and obj.pk == request.user.pk:
                return True
            else:
                return False

        elif obj is not None and obj.is_staff and not obj.is_superuser:
            if request.user.is_staff and not request.user.is_superuser and obj.pk == request.user.pk:
                return True
            elif request.user.is_superuser:
                return True
            elif request.user.is_staff and not request.user.is_superuser and obj.pk != request.user.pk:
                return False
            else:
                False
        else:
            True
        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        """
        This function is used to check if a user has permission to delete certain users
        :param request:
        :param obj:
        :return: bool
        """
        if obj is not None and obj.is_superuser and request.user.is_superuser:
            return False
        elif obj is not None and obj.is_staff and not request.user.is_superuser:
            return False
        else:
            return True



    def get_fieldsets(self, request, obj=None):
        """
        This function is used to create the fieldsets that the certain users can see
        on other users which depends on their status
        :param request:
        :param obj:
        :return: certain fieldsets
        """

        if obj:
            if request.user.is_superuser:
                return self.fieldsets_superuser

            elif not request.user.is_superuser and request.user.is_staff:

                if obj.pk == request.user.pk:
                    return self.fieldsets_mod
                elif not obj.is_superuser and obj.is_staff:
                    return self.fieldsets_see_mod
                elif obj.is_superuser:
                    return self.fieldsets_see_admin
                else:
                    return self.fieldsets_basic_user_mod_view
        else:
            return super().get_fieldsets(request, obj)






class NutriCommentAdmin(admin.ModelAdmin):
    """
    Class that represents custom settings and fields for comments for nutritionists
    """

    search_fields = ['^nutri__username']
    list_display = ('author','nutri','comment')

    def has_change_permission(self, request, obj=None):
        """
        this function is used to check if a user has permission to edit certain comments
        :param request:
        :param obj:
        :return: bool
        """
        if obj:return False



class PlanCommentAdmin(admin.ModelAdmin):
    """
    Class that represents custom settings and fields for comments for plans
    """

    search_fields = ['^plan__name']
    list_display = ('author','plan','comment')

    def has_change_permission(self, request, obj=None):
        """
        this function is used to check if a user has permission to edit certain comments
        :param request:
        :param obj:
        :return: bool
        """
        if obj:return False


class FoodAdmin(admin.ModelAdmin):


    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:

            return False





class PlanAdmin(admin.ModelAdmin):
    """
    Class that represents custom settings and fields for plans
    """

    search_fields = ['^name']
    list_display = ('id','name','owner','is_public')
    #list_filter = ('is_public',)


    def get_queryset(self, request):
        """
        this function is used to create the queryset for public plans
        :param request:
        :return: queryset
        """

        queryset = super().get_queryset(request)
        queryset = queryset.filter(is_public='True')
        return queryset

    def get_actions(self, request):
        """
        this function is used to create the custom delete actions for public plans
        :param request:
        :return: actions
        """
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        """
        This function is used to check if a user has permission to delete certain plans
        :param request:
        :param obj:
        :return: bool
        """
        if obj is not None and not obj.is_public:
            return False
        return super().has_delete_permission(request, obj)

    def custom_delete_action(self, request, queryset):
        """
        This function is used to call custom delete action that is defined in DeletePlanView
        :param request:
        :param queryset:
        :return: custom delete action
        """
        for plan in queryset:
            DeletePlanView().delete_plan(plan)



    custom_delete_action.short_description = "My Delete"

    action=[]
    actions = [custom_delete_action]

admin.site.register(models.NutriComment,NutriCommentAdmin)
admin.site.register(models.PlanComment,PlanCommentAdmin)
admin.site.register(models.MyUser, MyUserAdmin)

admin.site.register(models.Food,FoodAdmin)

admin.site.register(models.Plan,PlanAdmin)
admin.site.register(models.Tag)
admin.site.register(models.FormTags)



