from django.conf.urls import patterns, url


urlpatterns = patterns(
    "moderna.views",
    url(r"^$", "index", name="home"),
)
