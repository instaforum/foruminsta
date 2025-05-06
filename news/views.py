
import datetime
from time import timezone
import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator
import requests
import logging
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import NewsArticle, NewsSource
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import NewsArticle, NewsSource
from .forms import NewsArticleForm

import requests




logger = logging.getLogger(__name__)



def collect_news(request):
    source_name = request.GET.get('source')  # Récupération de la source depuis les paramètres GET
    articles = NewsArticle.objects.filter(is_active=True)
    
    if source_name:
        source = get_object_or_404(NewsSource, name=source_name)
        articles = articles.filter(source=source)  # Filtrage par source

    articles = articles.order_by('-published_at')
    
    paginator = Paginator(articles, 50)  # 20 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Récupération des sources distinctes
    sources = NewsSource.objects.all().order_by('name')

    context = {
        'articles': page_obj,
        'error': None if articles.exists() else "Aucun article trouvé.",
        'last_updated': articles.first().created_at if articles.exists() else None,
        'sources_count': articles.values('source').distinct().count(),
        'sources': sources
    }
    
    return render(request, 'news/news.html', context)

def create_news(request):
    if not request.user.is_moderator:
        return HttpResponse('Unauthorized', status=401)

    # Get or create the "Moderation" source
    moderation_source, created = NewsSource.objects.get_or_create(name='Insta')

    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            news_article = form.save(commit=False)
            news_article.source = moderation_source
            news_article.published_at = timezone.now()
            news_article.save()
            return redirect('home')
    else:
        form = NewsArticleForm()
    
    return render(request, 'news/create_news.html', {'form': form})

