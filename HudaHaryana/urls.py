
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from core.views import SignupView, UserAPIViewSet, EnquiryAPIViewSet, BookmarkAPIViewSet, MainEnquiryAPIViewSet, ContactsAPIViewSet, ImagesAPIViewSet, PropertiesAPIViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserAPIViewSet, basename='user')
router.register('enquiry', EnquiryAPIViewSet, basename='userprofile')
router.register('bookmark', BookmarkAPIViewSet, basename='bookmark')
router.register('main-enquiry', MainEnquiryAPIViewSet, basename='main-enquiry')
router.register('contact', ContactsAPIViewSet, basename='contact')
router.register('images', ImagesAPIViewSet, basename='images')
router.register('property', PropertiesAPIViewSet, basename='property')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/signup/', SignupView, name='signup'),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('blog/', include('blog.urls', namespace='blog')),

    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls), name='api'),

]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)