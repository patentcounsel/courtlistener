from alert.citations.feeds import CitedByFeed
from alert.opinion_page.sitemap import opinion_sitemap_maker
from alert.opinion_page.views import (
    view_opinion, view_opinion_citations, view_authorities, view_docket,
    serve_static_file)
from django.conf.urls import patterns, url


mime_types = ('pdf', 'wpd', 'txt', 'doc', 'html', 'mp3', 'wav')
urlpatterns = patterns('',
    url(r'^opinion/(\d*)/(.*)/cited-by/$', view_opinion_citations,
        name='view_case_citations'),
    url(r'^opinion/(\d*)/(.*)/authorities/$', view_authorities,
        name='view_authorities'),
    url(r'^opinion/(\d*)/(.*)/$', view_opinion, name="view_case"),
    url(r'^docket/(\d*)/(.*)/$', view_docket, name="view_docket"),

    # Serve a static file
    (r'^(?P<file_path>(?:' + "|".join(mime_types) + ')/.*)$',
     serve_static_file),

    # Feeds
    (r'^feed/(?P<doc_id>.*)/cited-by/$', CitedByFeed()),

    # Sitemap
    (r'^sitemap-opinions\.xml', opinion_sitemap_maker),
)
