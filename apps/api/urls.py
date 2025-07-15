from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    APIRootView, BookViewSet, BookPDFViewSet, QuranChapterOldViewSet,
    HadithBookViewSet, HadithBookMainChapterViewSet,
    HadithBookSubChapterViewSet, HadithBookContentViewSet,
    HadithBookExcelFileViewSet, SearchAPIView, StatisticsAPIView
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'book-pdfs', BookPDFViewSet)
router.register(r'quran-chapters', QuranChapterOldViewSet)
router.register(r'hadith-books', HadithBookViewSet)
router.register(r'hadith-main-chapters', HadithBookMainChapterViewSet)
router.register(r'hadith-sub-chapters', HadithBookSubChapterViewSet)
router.register(r'hadith-content', HadithBookContentViewSet)
router.register(r'hadith-excel-files', HadithBookExcelFileViewSet)

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('', include(router.urls)),
    path('search/', SearchAPIView.as_view(), name='api-search'),
    path('statistics/', StatisticsAPIView.as_view(), name='api-statistics'),
] 