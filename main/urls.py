from django.urls import path
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap
from .views import (
    HomeView,
    CategoriesView,
    SearchView,
    CategoryItemsView,
    ItemView,
    LinkView,
    SubmitLinkView,
    ReportLinkWorkingView,
    ReportLinkBrokenView,
    ReportLinkSpamView,
    PrivacyPolicyView,
)
from .sitemaps import ItemSitemap, StaticViewSitemap

item_sitemap = ItemSitemap()
sitemaps = {
    "static": StaticViewSitemap,
    "items": item_sitemap,
}

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("search/", SearchView.as_view(), name="search"),
    path(
        "category/<slug:category_slug>/",
        CategoryItemsView.as_view(),
        name="category_items",
    ),
    path("item/<slug:item_slug>/", ItemView.as_view(), name="item"),
    path("link/<int:link_id>/", LinkView.as_view(), name="link"),
    path("link/", SubmitLinkView.as_view(), name="submit_link"),
    path(
        "link/working/<int:link_id>/",
        ReportLinkWorkingView.as_view(),
        name="report_link_working",
    ),
    path(
        "link/broken/<int:link_id>/",
        ReportLinkBrokenView.as_view(),
        name="report_link_broken",
    ),
    path(
        "link/spam/<int:link_id>/",
        ReportLinkSpamView.as_view(),
        name="report_link_spam",
    ),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy_policy"),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path(
        "sitemap.xml",
        cache_page(86400)(sitemaps_views.index),
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
    ),
    path(
        "sitemap-<section>.xml",
        cache_page(86400)(sitemaps_views.sitemap),
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),
]
