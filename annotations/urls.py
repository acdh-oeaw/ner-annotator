from django.conf.urls import url
from . import views

app_name = 'annotations'

urlpatterns = [
    url(r'^nersamples/$', views.NerSampleListView.as_view(), name='browse_nersamples'),
    url(r'^nersamples/todo$', views.NerSampleToDoListView.as_view(), name='browse_nersamples_todo'),
    url(r'^nersamples/upload$', views.UploadNerSamplesView.as_view(), name='upload_nersamples'),
    url(r'^nersample/detail/(?P<pk>[0-9]+)$', views.NerSampleDetailView.as_view(),
        name='nersample_detail'),
    url(r'^nersample/create/$', views.NerSampleCreate.as_view(),
        name='nersample_create'),
    url(r'^nersample/edit/(?P<pk>[0-9]+)$', views.NerSampleUpdate.as_view(),
        name='nersample_edit'),
    url(r'^nersample/delete/(?P<pk>[0-9]+)$', views.NerSampleDelete.as_view(),
        name='nersample_delete'),
]
