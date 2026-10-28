# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django.views.generic import TemplateView
from apps.home import views

urlpatterns = [
    path('articles/', TemplateView.as_view(template_name='frontend/articles/index.html'), name='article_list'),
    path('articles/khel-ya-imtihaan/', TemplateView.as_view(template_name='frontend/articles/khel-ya-imtihaan.html'), name='article_khel_ya_imtihaan'),
    #Home page
    re_path(r'^mishkat-al-masabih/(?P<main_chp>\w+)/(?P<id_no>\d+)/$', views.t_hadith_content,name='t_hadith_content'),

    # Quran Start 
    path('',views.quran_list_chapter, name='quran_list_chapter'),
    path('<int:chapter_id>/',views.quran_get_chapter, name='quran_get_chapter'),
    # Quran  End 

    # mishkat Start
    path('mishkat-al-masabih/',views.hadith_mainchapter, name='mishkat-al-masabih'),
    re_path(r'^mishkat-al-masabih/(?P<main_chp>\w+)/$', views.hadith_subchapter,name='hadith_subchapter'),
    # re_path(r'^mishkat-al-masabih/(?P<main_chp>\w+)/(?P<sr_no>\d+)/$', views.hadith_content,name='hadith_content'),
    re_path(r'^mishkat-al-masabih/(?P<main_chp>\w+)/(?P<sub_chp_id>\d+)/(?P<sr_no>\d+)/$', views.hadith_content,name='hadith_content'),
    # mishkat End
    

    path('pdf_hadith_list',views.pdf_hadith_list, name='pdf_hadith_list'),
    path('pdf_dua_list',views.pdf_dua_list, name='pdf_dua_list'),
    path('pdf_quran_list',views.pdf_quran_list, name='pdf_quran_list'),
    
    # The Login page
    path('login', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
