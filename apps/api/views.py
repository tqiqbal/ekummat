from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q
from .pagination import CustomPageNumberPagination

from apps.home.models import (
    Book, BookPDF, QuranChapterOld, HadithBook, 
    HadithBookMainChapter, HadithBookSubChapter, 
    HadithBookContent, HadithBookExcelFile
)
from .serializers import (
    BookSerializer, BookPDFSerializer, QuranChapterOldSerializer,
    QuranChapterOldListSerializer, HadithBookSerializer, HadithBookMainChapterSerializer,
    HadithBookSubChapterSerializer, HadithBookContentSerializer,
    HadithBookExcelFileSerializer
)

def etag_books(request, *args, **kwargs):
    latest = Book.objects.latest('updated_at')
    return f'"{latest.updated_at.timestamp()}"'

def etag_bookpdfs(request, *args, **kwargs):
    latest = BookPDF.objects.latest('updated_at')
    return f'"{latest.updated_at.timestamp()}"'

def etag_quran(request, *args, **kwargs):
    latest = QuranChapterOld.objects.latest('updated_at')
    return f'"{latest.updated_at.timestamp()}"'

def etag_hadith_books(request, *args, **kwargs):
    latest = HadithBook.objects.latest('updated_at')
    return f'"{latest.updated_at.timestamp()}"'

def etag_hadith_main_chapters(request, *args, **kwargs):
    latest = HadithBookMainChapter.objects.latest('updated_at')
    return f'"{latest.updated_at.timestamp()}"'

def etag_hadith_sub_chapters(request, *args, **kwargs):
    latest = HadithBookSubChapter.objects.latest('updated_at')
    return f'"{latest.updated_at.timestamp()}"'

def etag_hadith_content(request, *args, **kwargs):
    latest = HadithBookContent.objects.latest('updated_at')
    return f'"{latest.updated_at.timestamp()}"'


class APIRootView(APIView):
    """
    API root view providing links to all available endpoints
    """
    def get(self, request):
        return Response({
            'books': reverse('book-list', request=request, format=None),
            'book_pdfs': reverse('bookpdf-list', request=request, format=None),
            'quran_chapters': reverse('quranchapterold-list', request=request, format=None),
            'hadith_books': reverse('hadithbook-list', request=request, format=None),
            'hadith_main_chapters': reverse('hadithbookmainchapter-list', request=request, format=None),
            'hadith_sub_chapters': reverse('hadithbooksubchapter-list', request=request, format=None),
            'hadith_content': reverse('hadithbookcontent-list', request=request, format=None),
            'hadith_excel_files': reverse('hadithbookexcelfile-list', request=request, format=None),
            'search': reverse('api-search', request=request, format=None),
            'statistics': reverse('api-statistics', request=request, format=None),
        })

@method_decorator(condition(etag_func=etag_books), name='dispatch')
class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'id']
    ordering = ['title']

@method_decorator(condition(etag_func=etag_bookpdfs), name='dispatch')
class BookPDFViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Book PDFs
    """
    queryset = BookPDF.objects.select_related('book').all()
    serializer_class = BookPDFSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['book__category', 'book']
    search_fields = ['title', 'book__title']
    ordering_fields = ['title', 'id']
    ordering = ['title']

@method_decorator(condition(etag_func=etag_quran), name='dispatch')
class QuranChapterOldViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Quran Chapters
    """
    queryset = QuranChapterOld.objects.filter(is_visible=False)
    lookup_field = 'chapter_no'
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_visible']
    ordering_fields = ['chapter_no', 'created_at']
    ordering = ['chapter_no']

    def get_serializer_class(self):
        """
        Use different serializers for list and detail views
        """
        if self.action == 'list':
            return QuranChapterOldListSerializer
        return QuranChapterOldSerializer

@method_decorator(condition(etag_func=etag_hadith_books), name='dispatch')
class HadithBookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Hadith Books
    """
    queryset = HadithBook.objects.all()
    serializer_class = HadithBookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'id']
    ordering = ['title']

@method_decorator(condition(etag_func=etag_hadith_main_chapters), name='dispatch')
class HadithBookMainChapterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Hadith Book Main Chapters
    """
    queryset = HadithBookMainChapter.objects.select_related('hadithbook').all()
    serializer_class = HadithBookMainChapterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['hadithbook']
    search_fields = ['english_name', 'arabic_name']
    ordering_fields = ['chapter_no', 'english_name']
    ordering = ['chapter_no']

@method_decorator(condition(etag_func=etag_hadith_sub_chapters), name='dispatch')
class HadithBookSubChapterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Hadith Book Sub Chapters
    """
    queryset = HadithBookSubChapter.objects.select_related(
        'hadith_book_main_chapter__hadithbook'
    ).all()
    serializer_class = HadithBookSubChapterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['hadith_book_main_chapter', 'hadith_book_main_chapter__hadithbook']
    search_fields = ['sub_chapter_name']
    ordering_fields = ['id', 'sub_chapter_name']
    ordering = ['id']

@method_decorator(condition(etag_func=etag_hadith_content), name='dispatch')
class HadithBookContentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Hadith Book Content
    """
    queryset = HadithBookContent.objects.select_related(
        'hadith_book_sub_chapter__hadith_book_main_chapter__hadithbook'
    ).all()
    serializer_class = HadithBookContentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'hadith_book_sub_chapter', 
        'hadith_book_sub_chapter__hadith_book_main_chapter',
        'hadith_book_sub_chapter__hadith_book_main_chapter__hadithbook',
        'hadith_book_sub_chapter__hadith_book_main_chapter__chapter_no',
        'grade'
    ]
    search_fields = ['arabic_content', 'roman_urdu_content', 'hindi_content', 'reference_field']
    ordering_fields = ['sr_no', 'id']
    ordering = ['sr_no']

    @action(detail=False, methods=['get'])
    def by_grade(self, request):
        """
        Get hadith content filtered by grade
        """
        grade = request.query_params.get('grade', None)
        if grade:
            queryset = self.queryset.filter(grade=grade)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'Grade parameter is required'}, status=400)


class HadithBookExcelFileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Hadith Book Excel Files
    """
    queryset = HadithBookExcelFile.objects.select_related(
        'Hadithbook', 'hadith_book_main_chapter', 'Hadith_book_sub_chapter'
    ).all()
    serializer_class = HadithBookExcelFileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['Hadithbook', 'hadith_book_main_chapter', 'Hadith_book_sub_chapter']
    ordering_fields = ['id']
    ordering = ['id']


class SearchAPIView(APIView):
    """
    Global search across all content types
    """
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=400)
        
        results = {
            'books': [],
            'hadith_content': [],
            'quran_chapters': []
        }
        
        # Search in books
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:10]
        results['books'] = BookSerializer(books, many=True).data
        
        # Search in hadith content
        hadith_content = HadithBookContent.objects.filter(
            Q(arabic_content__icontains=query) | 
            Q(roman_urdu_content__icontains=query) | 
            Q(hindi_content__icontains=query) |
            Q(reference_field__icontains=query)
        )[:10]
        results['hadith_content'] = HadithBookContentSerializer(hadith_content, many=True).data
        
        # Search in Quran chapters
        quran_chapters = QuranChapterOld.objects.filter(
            Q(chapter_content__icontains=query) & Q(is_visible=True)
        )[:10]
        results['quran_chapters'] = QuranChapterOldSerializer(quran_chapters, many=True).data
        
        return Response(results)


class StatisticsAPIView(APIView):
    """
    Get statistics about the content
    """
    def get(self, request):
        stats = {
            'total_books': Book.objects.count(),
            'total_book_pdfs': BookPDF.objects.count(),
            'total_quran_chapters': QuranChapterOld.objects.filter(is_visible=True).count(),
            'total_hadith_books': HadithBook.objects.count(),
            'total_hadith_main_chapters': HadithBookMainChapter.objects.count(),
            'total_hadith_sub_chapters': HadithBookSubChapter.objects.count(),
            'total_hadith_content': HadithBookContent.objects.count(),
            'books_by_category': {},
            'hadith_by_grade': {},
        }
        
        # Books by category
        books_by_category = Book.objects.values('category').annotate(count=Count('id'))
        for item in books_by_category:
            stats['books_by_category'][item['category']] = item['count']
        
        # Hadith by grade
        hadith_by_grade = HadithBookContent.objects.values('grade').annotate(count=Count('id'))
        for item in hadith_by_grade:
            if item['grade']:
                stats['hadith_by_grade'][item['grade']] = item['count']
        
        return Response(stats) 