from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(_('about/'), views.about, name='about'),
    path(_('products/'), views.products, name='products'),
    path(_('products/<str:slug>/'), views.product_detail, name='product_detail'),
    path(_('certifications/'), views.certifications, name='certifications'),
    path(_('export/'), views.export, name='export'),
    path(_('contact/'), views.contact, name='contact'),
    path(_('branding/'), views.branding, name='branding'),
    path(_('blog/'), views.blog, name='blog'),
    path(_('blog/<str:slug>/'), views.blog_detail, name='blog_detail'),
    path(_('packaging/'), views.packaging, name='packaging'),
    path(_('quality-control/'), views.quality_control, name='quality_control'),
    path(_('manufacturing/'), views.manufacturing, name='manufacturing'),
    path(_('faq/'), views.faq, name='faq'),
    path('set-language/<str:language_code>/', views.set_language, name='set_language'),
]
