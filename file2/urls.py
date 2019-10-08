from django.urls import path
from . import views


urlpatterns = [
    path('files/', views.ListDocumentView.as_view(), name="files-all"),
    path('files/<int:pk>/', views.DocumentDetailView.as_view(), name="files-detail"),
    # path('files/<int:pk>', views.GetDocumentView.as_view(), name="file-get"),
    path('files/upload/', views.UploadDocumentView.as_view(), name="file-upload"),
	path('shop/printjobdone/<int:pk>', views.UpdatePrintStatusDone.as_view(), name="file-update-printstatus"),
    path('files/printmytray', views.PrintFiles.as_view(), name="print-my-tray"),
    path('files/pickup', views.PickUpFiles.as_view(), name="print-my-tray"),


    path('shop/getprintjobs', views.GetPrintJobs.as_view(), name="get-print-jobs"),
    path('shop/getdeliveryjobs', views.GetDeliveryJobs.as_view(), name="get-delivery-jobs"),
    path('shop/setprintjobstatus/', views.SetPrintJobStatus.as_view(), name="set-print-status"),
    path('shop/testprintjobdone/', views.TestUpdatePrintStatusDone.as_view(), name="test-update-printstatus"),

    
    path('auth/login/', views.LoginView.as_view(), name="auth-login"),
    path('auth/register/', views.RegisterUsersView.as_view(), name="auth-register"),


]
