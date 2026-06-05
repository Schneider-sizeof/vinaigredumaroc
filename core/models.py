from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Certification(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="e.g. HALAL, KOSHER, IFS, BRC, FDA")
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, default='🏅')
    
    # Multilingual descriptions
    description_en = models.TextField(blank=True, default='')
    description_fr = models.TextField(blank=True, default='')
    description_ar = models.TextField(blank=True, default='')
    description_es = models.TextField(blank=True, default='')
    description_it = models.TextField(blank=True, default='')
    
    subtitle_en = models.CharField(max_length=150, blank=True, default='')
    subtitle_fr = models.CharField(max_length=150, blank=True, default='')
    subtitle_ar = models.CharField(max_length=150, blank=True, default='')
    subtitle_es = models.CharField(max_length=150, blank=True, default='')
    subtitle_it = models.CharField(max_length=150, blank=True, default='')
    
    theme_color = models.CharField(max_length=20, default='#0b3c2a')

    class Meta:
        ordering = ['code']
        verbose_name = _('Certification')
        verbose_name_plural = _('Certifications')

    def __str__(self):
        return self.code


class PackagingFormat(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. 200ml, 300ml, 500ml, 2L, 5L, 200ml PET, 1000L IBC")
    volume = models.CharField(max_length=50, help_text="Volume or capacity")
    material_en = models.CharField(max_length=100, default='Glass')
    material_fr = models.CharField(max_length=100, default='Verre')
    material_ar = models.CharField(max_length=100, default='زجاج')
    material_es = models.CharField(max_length=100, default='Vidrio')
    material_it = models.CharField(max_length=100, default='Vetro')
    
    # B2B logistics details
    carton_specs_en = models.CharField(max_length=150, blank=True, default='')
    carton_specs_fr = models.CharField(max_length=150, blank=True, default='')
    carton_specs_ar = models.CharField(max_length=150, blank=True, default='')
    carton_specs_es = models.CharField(max_length=150, blank=True, default='')
    carton_specs_it = models.CharField(max_length=150, blank=True, default='')

    pallet_specs_en = models.CharField(max_length=150, blank=True, default='')
    pallet_specs_fr = models.CharField(max_length=150, blank=True, default='')
    pallet_specs_ar = models.CharField(max_length=150, blank=True, default='')
    pallet_specs_es = models.CharField(max_length=150, blank=True, default='')
    pallet_specs_it = models.CharField(max_length=150, blank=True, default='')

    class Meta:
        ordering = ['id']
        verbose_name = _('Packaging Format')
        verbose_name_plural = _('Packaging Formats')

    def __str__(self):
        return self.name


class Category(models.Model):
    name_en = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200, blank=True, default='')
    name_ar = models.CharField(max_length=200, blank=True, default='')
    name_es = models.CharField(max_length=200, blank=True, default='')
    name_it = models.CharField(max_length=200, blank=True, default='')
    
    slug = models.SlugField(unique=True, blank=True)
    slug_fr = models.SlugField(unique=True, blank=True, null=True, max_length=260)
    slug_ar = models.SlugField(unique=True, blank=True, null=True, max_length=260, allow_unicode=True)
    slug_es = models.SlugField(unique=True, blank=True, null=True, max_length=260)
    slug_it = models.SlugField(unique=True, blank=True, null=True, max_length=260)

    description_en = models.TextField(blank=True, default='')
    description_fr = models.TextField(blank=True, default='')
    description_ar = models.TextField(blank=True, default='')
    description_es = models.TextField(blank=True, default='')
    description_it = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text=_("Upload category thumbnail picture"))

    class Meta:
        ordering = ['id']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        if self.name_fr and not self.slug_fr:
            self.slug_fr = slugify(self.name_fr) or f"{self.slug}-fr"
        if self.name_es and not self.slug_es:
            self.slug_es = slugify(self.name_es) or f"{self.slug}-es"
        if self.name_it and not self.slug_it:
            self.slug_it = slugify(self.name_it) or f"{self.slug}-it"
        if self.name_ar and not self.slug_ar:
            self.slug_ar = slugify(self.name_ar, allow_unicode=True) or f"{self.slug}-ar"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_en


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    name_en = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200, blank=True, default='')
    name_ar = models.CharField(max_length=200, blank=True, default='')
    name_es = models.CharField(max_length=200, blank=True, default='')
    name_it = models.CharField(max_length=200, blank=True, default='')
    
    slug = models.SlugField(unique=True, blank=True)
    slug_fr = models.SlugField(unique=True, blank=True, null=True, max_length=260)
    slug_ar = models.SlugField(unique=True, blank=True, null=True, max_length=260, allow_unicode=True)
    slug_es = models.SlugField(unique=True, blank=True, null=True, max_length=260)
    slug_it = models.SlugField(unique=True, blank=True, null=True, max_length=260)

    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True,
                              help_text=_('Upload a product image (JPEG, PNG, WebP).'),
                              verbose_name=_('Product Image'))


    short_description_en = models.CharField(max_length=350, blank=True, default='')
    short_description_fr = models.CharField(max_length=350, blank=True, default='')
    short_description_ar = models.CharField(max_length=350, blank=True, default='')
    short_description_es = models.CharField(max_length=350, blank=True, default='')
    short_description_it = models.CharField(max_length=350, blank=True, default='')

    description_en = models.TextField(blank=True, default='')
    description_fr = models.TextField(blank=True, default='')
    description_ar = models.TextField(blank=True, default='')
    description_es = models.TextField(blank=True, default='')
    description_it = models.TextField(blank=True, default='')

    ingredients_en = models.TextField(blank=True, default='', help_text="Comma separated or plain text ingredients list")
    ingredients_fr = models.TextField(blank=True, default='')
    ingredients_ar = models.TextField(blank=True, default='')
    ingredients_es = models.TextField(blank=True, default='')
    ingredients_it = models.TextField(blank=True, default='')

    usage_ideas_en = models.TextField(blank=True, default='')
    usage_ideas_fr = models.TextField(blank=True, default='')
    usage_ideas_ar = models.TextField(blank=True, default='')
    usage_ideas_es = models.TextField(blank=True, default='')
    usage_ideas_it = models.TextField(blank=True, default='')

    # Technical/B2B specs
    acidity = models.CharField(max_length=50, blank=True, default='6%', help_text="e.g. 6%, 8%")
    shelf_life_en = models.CharField(max_length=100, default='24 Months')
    shelf_life_fr = models.CharField(max_length=100, default='24 Mois')
    shelf_life_ar = models.CharField(max_length=100, default='24 شهراً')
    shelf_life_es = models.CharField(max_length=100, default='24 Meses')
    shelf_life_it = models.CharField(max_length=100, default='24 Mesi')

    storage_conditions_en = models.CharField(max_length=200, default='Store in a cool, dry place away from direct sunlight.')
    storage_conditions_fr = models.CharField(max_length=200, default='Conserver dans un endroit frais et sec, à l\'abri de la lumière directe.')
    storage_conditions_ar = models.CharField(max_length=200, default='يُحفظ في مكان بارد وجاف بعيداً عن أشعة الشمس المباشرة.')
    storage_conditions_es = models.CharField(max_length=200, default='Almacenar en un lugar fresco y seco, lejos de la luz solar directa.')
    storage_conditions_it = models.CharField(max_length=200, default='Conservare in luogo fresco e asciutto, lontano dalla luce solare diretta.')

    origin_en = models.CharField(max_length=100, default='Morocco')
    origin_fr = models.CharField(max_length=100, default='Maroc')
    origin_ar = models.CharField(max_length=100, default='المغرب')
    origin_es = models.CharField(max_length=100, default='Marruecos')
    origin_it = models.CharField(max_length=100, default='Marocco')

    packaging_formats = models.ManyToManyField(PackagingFormat, blank=True, related_name='products')
    certifications = models.ManyToManyField(Certification, blank=True, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        if self.name_fr and not self.slug_fr:
            self.slug_fr = slugify(self.name_fr) or f"{self.slug}-fr"
        if self.name_es and not self.slug_es:
            self.slug_es = slugify(self.name_es) or f"{self.slug}-es"
        if self.name_it and not self.slug_it:
            self.slug_it = slugify(self.name_it) or f"{self.slug}-it"
        if self.name_ar and not self.slug_ar:
            self.slug_ar = slugify(self.name_ar, allow_unicode=True) or f"{self.slug}-ar"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_en


class B2BInquiry(models.Model):
    company_name = models.CharField(max_length=200)
    country = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    requested_products = models.CharField(max_length=400, help_text="Products of interest")
    packaging_format = models.CharField(max_length=200, help_text="Formats requested e.g. 5L, 1000L IBC")
    quantity = models.CharField(max_length=150, help_text="e.g. 1 FCL, 10 Pallets, 5000 Liters")
    custom_message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('B2B Inquiry')
        verbose_name_plural = _('B2B Inquiries')

    def __str__(self):
        return f"Inquiry from {self.company_name} ({self.country})"


class BlogPost(models.Model):
    title_en = models.CharField(max_length=250)
    title_fr = models.CharField(max_length=250, blank=True)
    title_ar = models.CharField(max_length=250, blank=True)
    title_es = models.CharField(max_length=250, blank=True)
    title_it = models.CharField(max_length=250, blank=True)

    slug = models.SlugField(unique=True, blank=True, max_length=260)
    slug_fr = models.SlugField(unique=True, blank=True, null=True, max_length=260)
    slug_ar = models.SlugField(unique=True, blank=True, null=True, max_length=260, allow_unicode=True)
    slug_es = models.SlugField(unique=True, blank=True, null=True, max_length=260)
    slug_it = models.SlugField(unique=True, blank=True, null=True, max_length=260)

    excerpt_en = models.TextField(max_length=400, blank=True)
    excerpt_fr = models.TextField(max_length=400, blank=True)
    excerpt_ar = models.TextField(max_length=400, blank=True)
    excerpt_es = models.TextField(max_length=400, blank=True)
    excerpt_it = models.TextField(max_length=400, blank=True)

    content_en = models.TextField()
    content_fr = models.TextField(blank=True)
    content_ar = models.TextField(blank=True)
    content_es = models.TextField(blank=True)
    content_it = models.TextField(blank=True)

    author_en = models.CharField(max_length=100, default='Vinaigre du Maroc')
    author_fr = models.CharField(max_length=100, default='Vinaigre du Maroc')
    author_ar = models.CharField(max_length=100, default='خل المغرب')
    author_es = models.CharField(max_length=100, default='Vinagre de Marruecos')
    author_it = models.CharField(max_length=100, default='Aceto del Marocco')

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        if self.title_fr and not self.slug_fr:
            self.slug_fr = slugify(self.title_fr) or f"{self.slug}-fr"
        if self.title_es and not self.slug_es:
            self.slug_es = slugify(self.title_es) or f"{self.slug}-es"
        if self.title_it and not self.slug_it:
            self.slug_it = slugify(self.title_it) or f"{self.slug}-it"
        if self.title_ar and not self.slug_ar:
            self.slug_ar = slugify(self.title_ar, allow_unicode=True) or f"{self.slug}-ar"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_en


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='Vinaigre du Maroc')
    phone = models.CharField(max_length=50, default='+212 5 35 12 34 56')
    email = models.EmailField(default='export@vinaigredemaroc.com')
    address = models.TextField(default='Quartier Industriel Bensouda, Fès 30000, Morocco')
    facebook_url = models.URLField(blank=True, default='https://facebook.com')
    instagram_url = models.URLField(blank=True, default='https://instagram.com')
    linkedin_url = models.URLField(blank=True, default='https://linkedin.com')
    google_analytics_id = models.CharField(max_length=50, blank=True, help_text='e.g. G-XXXXXXXXXX')

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return self.site_name


HERO_PAGE_CHOICES = [
    ('home',           'Homepage'),
    ('about',          'About Us'),
    ('products',       'Products'),
    ('certifications', 'Certifications'),
    ('blog',           'Blog'),
    ('branding',       'Branding / Private Label'),
    ('contact',        'Contact'),
    ('export',         'Export'),
    ('packaging',      'Packaging'),
]


class HeroMedia(models.Model):
    page = models.CharField(max_length=50, choices=HERO_PAGE_CHOICES, unique=True,
                            help_text='Which page this hero background is for.')
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')], default='image')
    image = models.ImageField(upload_to='backgrounds/', blank=True, null=True,
                              help_text='Upload a hero background image (JPEG, PNG, WebP).')
    video = models.FileField(upload_to='backgrounds/videos/', blank=True, null=True,
                             help_text='Upload a hero background video (MP4, WebM). Used only when media type is Video.')

    class Meta:
        verbose_name = _('Hero Background')
        verbose_name_plural = _('Hero Backgrounds')
        ordering = ['page']

    def __str__(self):
        return f"Hero — {self.get_page_display()}"

