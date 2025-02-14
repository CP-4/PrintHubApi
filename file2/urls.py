from django.urls import path
from . import views


urlpatterns = [
    path('files/', views.ListDocumentView.as_view(), name="files-all"),
    path('files/<int:pk>/', views.DocumentDetailView.as_view(), name="files-detail"),
    # path('files/<int:pk>', views.GetDocumentView.as_view(), name="file-get"),
    path('files/upload/', views.UploadDocumentView.as_view(), name="file-upload"),
    path('files/printmytray', views.PrintFiles.as_view(), name="print-my-tray"),
    path('files/pickup', views.PickUpFiles.as_view(), name="print-my-tray"),


    path('shops/', views.ListShopView.as_view(), name="shops-all"),
    path('shops/<int:pk>/', views.ShopDetailView.as_view(), name="shops-detail"),
    path('shops/getshopfromuser/', views.ShopDetailFromUserView.as_view(), name="shops-detail-form-user"),
    path('shop/register', views.CreateShopView.as_view(), name="shop-register"),
    path('shop/getprintjobs', views.GetPrintJobs.as_view(), name="get-print-jobs"),
    path('shop/getdeliveryjobs', views.GetDeliveryJobs.as_view(), name="get-delivery-jobs"),
    path('shop/setprintjobstatus/', views.SetPrintJobStatus.as_view(), name="set-print-status"),
    path('shop/testprintjobdone/', views.TestUpdatePrintStatusDone.as_view(), name="test-update-printstatus"),
	path('shop/printjobdone/<int:pk>', views.UpdatePrintStatusDone.as_view(), name="file-update-printstatus"),


    path('auth/login/', views.LoginView.as_view(), name="auth-login"),
    path('auth/register/', views.RegisterUsersView.as_view(), name="auth-register"),


    path('urlanalytics/trigger', views.UrlAnalyticsView.as_view(), name="uranal-trigger"),


    path('studymaterial/print', views.GuestStudentView.as_view(), name="gueststudent"),


    path('profile/update', views.UpdateStudentView.as_view(), name="update-student"),
]
