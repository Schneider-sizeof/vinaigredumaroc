from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import translation
from django.urls import reverse
from django.utils.translation import override as lang_override
from django.db.models import Q
from .models import Category, Product, PackagingFormat, Certification, BlogPost, B2BInquiry
from .forms import B2BInquiryForm

def home(request):
    featured_products = Product.objects.filter(is_featured=True).order_by('id')[:3]
    categories = Category.objects.all()[:4]
    certs = Certification.objects.all()[:5]
    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'certifications': certs,
    })

def about(request):
    return render(request, 'core/about.html')

def products(request):
    category_slug = request.GET.get('category', '')
    categories = Category.objects.all()
    
    if category_slug:
        # Resolve category in any language slug
        category = get_object_or_404(
            Category, 
            Q(slug=category_slug) | Q(slug_fr=category_slug) | Q(slug_ar=category_slug) | Q(slug_es=category_slug) | Q(slug_it=category_slug)
        )
        product_list = Product.objects.filter(category=category)
        active_category = category
    else:
        product_list = Product.objects.all()
        active_category = None

    return render(request, 'core/products.html', {
        'products': product_list,
        'categories': categories,
        'active_category': active_category,
    })

def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        Q(slug=slug) | Q(slug_fr=slug) | Q(slug_ar=slug) | Q(slug_es=slug) | Q(slug_it=slug)
    )
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    
    # Handle inline inquiry form for this specific product
    if request.method == 'POST':
        form = B2BInquiryForm(request.POST)
        if request.POST.get('website'):  # Anti-spam honeypot
            messages.success(request, _('Your inquiry has been sent successfully!'))
            return redirect('product_detail', slug=slug)

        if form.is_valid():
            form.save()
            messages.success(request, _('Your B2B inquiry has been sent successfully. Our export team will contact you shortly.'))
            return redirect('product_detail', slug=slug)
        else:
            messages.error(request, _('There was an error in your submission. Please check the fields below.'))
    else:
        # Prepopulate products of interest
        form = B2BInquiryForm(initial={'requested_products': product.name_en})

    return render(request, 'core/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'form': form,
    })

def packaging(request):
    formats = PackagingFormat.objects.all()
    return render(request, 'core/packaging.html', {'formats': formats})

def certifications(request):
    certs = Certification.objects.all()
    return render(request, 'core/certifications.html', {'certifications': certs})

def export(request):
    return render(request, 'core/export.html')

def quality_control(request):
    return render(request, 'core/quality_control.html')

def manufacturing(request):
    return render(request, 'core/manufacturing.html')

def contact(request):
    if request.method == 'POST':
        form = B2BInquiryForm(request.POST)
        if request.POST.get('website'):  # Anti-spam honeypot
            messages.success(request, _('Your message has been sent successfully!'))
            return redirect('contact')

        if form.is_valid():
            form.save()
            messages.success(request, _('Your B2B inquiry has been sent successfully! Our export team will contact you shortly.'))
            return redirect('contact')
        else:
            messages.error(request, _('There was an error in your submission. Please check the fields below.'))
    else:
        form = B2BInquiryForm()
    return render(request, 'core/contact.html', {'form': form})

def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'core/blog.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost,
        Q(slug=slug) | Q(slug_fr=slug) | Q(slug_ar=slug) | Q(slug_es=slug) | Q(slug_it=slug),
        is_published=True
    )
    related_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]
    return render(request, 'core/blog_detail.html', {
        'post': post,
        'related_posts': related_posts,
    })

def branding(request):
    return render(request, 'core/branding.html')

def faq(request):
    return render(request, 'core/faq.html')

def set_language(request, language_code):
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    translation.activate(language_code)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    return response

def sitemap_xml(request):
    import datetime
    from django.conf import settings as django_settings
    products_list = Product.objects.all()
    categories_list = Category.objects.all()
    posts = BlogPost.objects.filter(is_published=True)
    base_url = django_settings.SITE_URL
    languages = [code for code, name in django_settings.LANGUAGES]
    
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    urls = []
    
    # 1. Static Pages
    static_names = ['home', 'products', 'certifications', 'export', 'contact', 'branding', 'blog']
    for name in static_names:
        page_urls = {}
        for lang in languages:
            with lang_override(lang):
                page_urls[lang] = base_url + reverse(name)
        urls.append({
            'loc': page_urls['en'],
            'changefreq': 'weekly' if name == 'home' else 'monthly',
            'priority': '1.0' if name == 'home' else '0.9' if name == 'products' else '0.7',
            'lastmod': current_date,
            'links': [{'lang': lang, 'href': href} for lang, href in page_urls.items()]
        })

    # 2. Category Pages
    for category in categories_list:
        page_urls = {}
        for lang in languages:
            slug = getattr(category, f'slug_{lang}', None) or getattr(category, 'slug_en', None) or category.slug
            with lang_override(lang):
                page_urls[lang] = base_url + reverse('products') + f"?category={slug}"
        urls.append({
            'loc': page_urls['en'],
            'changefreq': 'monthly',
            'priority': '0.8',
            'lastmod': current_date,
            'links': [{'lang': lang, 'href': href} for lang, href in page_urls.items()]
        })
        
    # 3. Product Pages
    for prod in products_list:
        page_urls = {}
        for lang in languages:
            slug = getattr(prod, f'slug_{lang}', None) or getattr(prod, 'slug_en', None) or prod.slug
            with lang_override(lang):
                page_urls[lang] = base_url + reverse('product_detail', kwargs={'slug': slug})
        urls.append({
            'loc': page_urls['en'],
            'changefreq': 'monthly',
            'priority': '0.8',
            'lastmod': current_date,
            'links': [{'lang': lang, 'href': href} for lang, href in page_urls.items()]
        })
        
    # 4. Blog Posts
    for post in posts:
        page_urls = {}
        for lang in languages:
            slug = getattr(post, f'slug_{lang}', None) or getattr(post, 'slug_en', None) or post.slug
            with lang_override(lang):
                page_urls[lang] = base_url + reverse('blog_detail', kwargs={'slug': slug})
        urls.append({
            'loc': page_urls['en'],
            'changefreq': 'monthly',
            'priority': '0.6',
            'lastmod': current_date,
            'links': [{'lang': lang, 'href': href} for lang, href in page_urls.items()]
        })
        
    return render(request, 'core/sitemap.xml', {
        'urls': urls,
    }, content_type='application/xml')

def robots_txt(request):
    from django.conf import settings as django_settings
    base_url = django_settings.SITE_URL
    is_staging = getattr(django_settings, 'ROBOTS_DISALLOW_ALL', False)
    return render(request, 'core/robots.txt', {
        'base_url': base_url,
        'is_staging': is_staging,
    }, content_type='text/plain')
