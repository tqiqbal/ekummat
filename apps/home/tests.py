from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase
from django.urls import resolve, reverse

from .templatetags.utils import file_url


class RelatedList(list):
    def all(self):
        return self


class ReadingExperienceTests(SimpleTestCase):
    """Public pages retain their content, translations, and established links."""

    def setUp(self):
        self.factory = RequestFactory()
        self.chapter = {
            'id': 1,
            'name_simple': 'Al-Fatihah',
            'name_complex': 'Al-Fātiĥah',
            'name_arabic': 'الفاتحة',
            'revelation_place': 'makkah',
            'verses_count': 7,
            'translated_name': {'name': 'The Opener'},
        }
        self.quran_html = '<h2>Al-Fatihah</h2><p>Original Roman Urdu Tafseer.</p><p dir="rtl">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</p>'
        self.main_chapter = SimpleNamespace(english_name='Faith', arabic_name='الإيمان', chapter_no=1, get_absolute_url='/mishkat-al-masabih/Faith/')
        self.subchapter = SimpleNamespace(id=2, sub_chapter_name='The meaning of faith', hadith_book_main_chapter=self.main_chapter)
        self.hadith = SimpleNamespace(
            id=7, sr_no=3, roman_urdu_content='Original Roman Urdu content.',
            hindi_content='मूल हिंदी पाठ', arabic_content='النص العربي',
            reference_field='Original reference 123', grade='Sahih',
            hadith_book_sub_chapter=self.subchapter,
            get_absolute_url='/mishkat-al-masabih/Faith/7/',
        )
        self.subchapter.hadithbookcontent_set = RelatedList([self.hadith])

    def test_home_retains_every_surah_link_and_search_metadata(self):
        chapters = [dict(self.chapter, id=number, name_simple=f'Surah {number}') for number in range(1, 115)]
        chapters[0] = self.chapter
        with patch('apps.home.views.requests.request', return_value=Mock(json=lambda: {'chapters': chapters})):
            response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-chapter-card', count=114)
        for number in range(1, 115):
            self.assertContains(response, f'href="/{number}/"')
        self.assertContains(response, 'data-chapter-search')
        self.assertContains(response, 'data-expand-chapters')
        self.assertContains(response, 'data-place="makkah"')
        self.assertContains(response, 'href="/articles/"')

    def test_quran_reader_preserves_html_and_boundary_navigation(self):
        for chapter_id in (1, 114):
            chapter = dict(self.chapter, id=chapter_id)
            with patch('apps.home.views.requests.request', return_value=Mock(json=lambda: {'chapter': chapter})), patch('apps.home.views.QuranChapterOld.objects.filter') as query:
                query.return_value.first.return_value = SimpleNamespace(chapter_content=self.quran_html)
                response = self.client.get(f'/{chapter_id}/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.quran_html, html=False)
            self.assertContains(response, 'data-save-reading')
            self.assertContains(response, 'data-font-change')
            self.assertContains(response, 'data-reading-theme')
            self.assertNotContains(response, 'href="/0/"')
            self.assertNotContains(response, 'href="/115/"')
            self.assertContains(response, 'href="/2/"' if chapter_id == 1 else 'href="/113/"')

    def test_quran_without_content_has_a_library_link(self):
        with patch('apps.home.views.requests.request', return_value=Mock(json=lambda: {'chapter': self.chapter})), patch('apps.home.views.QuranChapterOld.objects.filter') as query:
            query.return_value.first.return_value = None
            response = self.client.get('/1/')
        self.assertContains(response, 'Tafseer is not available yet')
        self.assertContains(response, 'href="/pdf_quran_list"')

    def test_hadith_both_existing_urls_keep_all_languages_and_reference(self):
        for path in ('/mishkat-al-masabih/Faith/7/', '/mishkat-al-masabih/Faith/2/3/'):
            with patch('apps.home.views.HadithBookContent.objects.filter') as query:
                query.return_value.first.return_value = self.hadith
                response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            for value in (self.hadith.roman_urdu_content, self.hadith.hindi_content, self.hadith.arabic_content, self.hadith.reference_field):
                self.assertContains(response, value)
            self.assertContains(response, 'data-language-tab', count=3)
            self.assertContains(response, 'data-language-panel', count=3)
            self.assertContains(response, self.hadith.get_absolute_url)

    def test_hadith_chapter_includes_all_entries(self):
        html = render_to_string('frontend/hadees_subchapter.html', {'hadith_sub_chapter': [self.subchapter]}, request=self.factory.get('/mishkat-al-masabih/Faith/'))
        self.assertIn(self.subchapter.sub_chapter_name, html)
        self.assertIn(self.hadith.roman_urdu_content, html)
        self.assertIn(self.hadith.reference_field, html)
        self.assertIn('data-hadith', html)

    def test_hadith_index_keeps_chapter_links(self):
        html = render_to_string('frontend/hadees_mainchapter.html', {'hadith_main_chapter_list': [self.main_chapter]}, request=self.factory.get('/mishkat-al-masabih/'))
        self.assertIn(self.main_chapter.get_absolute_url, html)
        self.assertIn(self.main_chapter.arabic_name, html)

    def test_pdf_library_retains_external_and_uploaded_file_urls(self):
        external = SimpleNamespace(title='External PDF', external_file_url='https://example.org/original.pdf', file_url=None)
        uploaded = SimpleNamespace(title='Uploaded PDF', external_file_url='', file_url=SimpleNamespace(url='/media/book/original.pdf'))
        book = SimpleNamespace(title='Original book title', volumes='2', bookpdf_set=RelatedList([external, uploaded]))
        for path in ('/pdf_quran_list', '/pdf_hadith_list', '/pdf_dua_list'):
            html = render_to_string('frontend/pdf_book_list.html', {'book_list': [book], 'category': 'dua' if 'dua' in path else ''}, request=self.factory.get(path))
            self.assertIn(external.external_file_url, html)
            self.assertIn(uploaded.file_url.url, html)
            self.assertIn(book.title, html)
            self.assertIn('rel="noopener noreferrer"', html)

    def test_file_url_supports_missing_files_without_raising(self):
        self.assertEqual(file_url(SimpleNamespace(external_file_url='', file_url=None)), '')
        self.assertEqual(file_url(SimpleNamespace(external_file_url='https://example.org/book.pdf', file_url=None)), 'https://example.org/book.pdf')

    def test_article_routes_and_reference_content_are_preserved(self):
        response = self.client.get(reverse('article_khel_ya_imtihaan'))
        self.assertEqual(response.status_code, 200)
        for text in ('Jab Maut Khud Zibah Ki Jayegi', 'Zeenat Ka Dhoka', 'Khel Ka Guman', 'Azmaish Ka Tarazu', 'Ṣaḥīḥ al-Bukhārī 6548', 'ٱلَّذِى خَلَقَ'):
            self.assertContains(response, text)
        self.assertContains(response, 'data-reader')
        self.assertContains(response, 'href="/articles/"')
        self.assertEqual(self.client.get('/articles/').status_code, 200)
        self.assertEqual(self.client.get('/articles/missing/').status_code, 404)

    def test_existing_route_names_are_unchanged(self):
        for path, name in (('/', 'quran_list_chapter'), ('/18/', 'quran_get_chapter'), ('/mishkat-al-masabih/', 'mishkat-al-masabih'), ('/pdf_quran_list', 'pdf_quran_list'), ('/pdf_hadith_list', 'pdf_hadith_list'), ('/pdf_dua_list', 'pdf_dua_list')):
            self.assertEqual(resolve(path).url_name, name)
