from django.conf.urls import patterns, url

urlpatterns = patterns(
    'mozillians.humans',
    url(r'^humans.txt$', 'views.humans', name='humans')
)
