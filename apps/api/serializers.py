from rest_framework import serializers
from apps.home.models import (
    Book, BookPDF, QuranChapterOld, HadithBook, 
    HadithBookMainChapter, HadithBookSubChapter, 
    HadithBookContent, HadithBookExcelFile
)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'volumes', 'description', 'category', 'created_at', 'updated_at']


class BookPDFSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = BookPDF
        fields = ['id', 'book', 'book_id', 'title', 'total_pages', 'file_url', 'external_file_url', 'created_at', 'updated_at']


class QuranChapterOldListSerializer(serializers.ModelSerializer):
    """
    Serializer for Quran chapters list view (without content)
    """
    class Meta:
        model = QuranChapterOld
        fields = ['id', 'chapter_no', 'chapter_content', 'is_visible', 'created_at', 'updated_at']


class QuranChapterOldSerializer(serializers.ModelSerializer):
    """
    Serializer for Quran chapter detail view (with content)
    """
    class Meta:
        model = QuranChapterOld
        fields = ['id', 'chapter_no', 'chapter_content', 'is_visible', 'created_at', 'updated_at']


class HadithBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithBook
        fields = ['id', 'title', 'description', 'slug', 'created_at', 'updated_at']


class HadithBookMainChapterSerializer(serializers.ModelSerializer):
    hadithbook = HadithBookSerializer(read_only=True)
    hadithbook_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = HadithBookMainChapter
        fields = ['id', 'hadithbook', 'hadithbook_id', 'chapter_no', 'english_name', 'arabic_name', 'created_at', 'updated_at']


class HadithBookSubChapterSerializer(serializers.ModelSerializer):
    hadith_book_main_chapter = HadithBookMainChapterSerializer(read_only=True)
    hadith_book_main_chapter_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = HadithBookSubChapter
        fields = ['id', 'hadith_book_main_chapter', 'hadith_book_main_chapter_id', 'sub_chapter_name', 'created_at', 'updated_at']


class HadithBookContentSerializer(serializers.ModelSerializer):
    hadith_book_sub_chapter = HadithBookSubChapterSerializer(read_only=True)
    hadith_book_sub_chapter_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = HadithBookContent
        fields = [
            'id', 'hadith_book_sub_chapter', 'hadith_book_sub_chapter_id',
            'sr_no', 'arabic_content', 'roman_urdu_content', 
            'hindi_content', 'reference_field', 'grade', 'created_at', 'updated_at'
        ]


class HadithBookExcelFileSerializer(serializers.ModelSerializer):
    Hadithbook = HadithBookSerializer(read_only=True)
    hadith_book_main_chapter = HadithBookMainChapterSerializer(read_only=True)
    Hadith_book_sub_chapter = HadithBookSubChapterSerializer(read_only=True)
    
    class Meta:
        model = HadithBookExcelFile
        fields = [
            'id', 'file_url', 'Hadithbook', 'hadith_book_main_chapter', 
            'Hadith_book_sub_chapter'
        ] 