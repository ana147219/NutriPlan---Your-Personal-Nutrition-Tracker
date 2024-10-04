from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from djangoProject1 import settings
from . import views

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path('', views.HomeView.as_view(), name="index"),
    path('login', views.LoginView.as_view(), name="login-page"),
    path('home', views.HomePageView.as_view(), name="home"),
    path('make_plan', views.MakePlanView.as_view(), name="make_plan"),
    path('get-food-list', views.MakePlanSearchView.as_view(), name="get-food-list"),
    path('signup', views.SignupView.as_view(), name="signup"),
    path('verify', views.VerifyView.as_view(), name="verify"),
    path('check_username/', views.CheckUsernameView.as_view(), name='check_username'),
    path('check_email/', views.CheckEmailView.as_view(), name='check_email'),
    path('save-plan', views.SavePlanView.as_view(), name="save-plan"),
    path('search_plan', views.SearchPlanView.as_view(), name="search_plan"),
    path('search_nutri', views.SearchNutriView.as_view(), name="search_nutri"),
    path('preview_plan', views.PlanPageView.as_view(), name="preview_plan"),
    path('nutriPage.html', views.NutriPageView.as_view(), name="nutriPage"),
    path('get-plan-list', views.SearchPlanSearchView.as_view(), name="get-plan-list"),
    path('rate-plan', views.RatePlanView.as_view(), name="rate-plan"),
    path('calendar-plan', views.CalendarPlanView.as_view(), name="calendar-plan"),
    path('date-food-timeline', views.CalendarTimelineView.as_view(), name="date-food-timeline"),
    path('begin-plan', views.BeginPlan.as_view(), name="begin-plan"),
    path('get-meal-info', views.MealView.as_view(), name="get-meal-info"),
    path('finish-meal', views.FinishMeal.as_view(), name="finish-meal"),
    path('give-up', views.GiveUp.as_view(), name='give-up'),
    path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('get-nutri-list', views.SearchNutriViewSearch.as_view(), name="get-nutri-list"),
    path('preview_nutri', views.NutriPageView.as_view(), name="preview_nutri"),
    path('rate-nutri', views.RateNutriView.as_view(), name="rate-nutri"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('delete-plan', views.DeletePlanView.as_view(), name='delete-plan'),
    path('change-data', views.ChangeDataView.as_view(), name="change-data"),
    path('nutritionist/<int:nutritionist_id>/order/', views.OrderView.as_view(), name='order_form'),
    path('download-plan', views.DownloadPlanView.as_view(), name='download-plan'),
    path('publish-plan', views.PublishPlanView.as_view(), name="publish-plan"),
    path('send-plan', views.SendPlanView.as_view(), name='send-plan'),
    path('get-notifications', views.NotificatonView.as_view(), name='get-notifications'),
    path('dismiss-form', views.DismissNotificationsView.as_view(), name='dismiss-form'),
    path('upload_profile_picture', views.UpdateProfilePictureView.as_view(), name='upload_profile_picture'),
    path('add_comment_nutri', views.AddCommentForNutriView.as_view(), name='add_comment_nutri'),
    path('add_comment_plan', views.AddCommentForPlanView.as_view(), name='add_comment_plan'),
    path('check-form', views.CheckForm.as_view(), name='check-form'),
    path('delete-form', views.DeleteForm.as_view(), name='delete-form'),
    path('resend-code-forgot-pass/', views.ResendCodeForgotPassView.as_view(), name='resend_code_forgot_pass'),
    path('resend-code-signup/', views.ResendCodeSignupView.as_view(), name='resend_code_signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = "NutriPlan Admin Settings"
admin.site.site_header = "NutriPlan Admin"
admin.site.site_title = "Site NutriPlan"
