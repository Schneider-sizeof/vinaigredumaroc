import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinaigre_project.settings')
django.setup()

from core.models import SiteSettings, Certification, PackagingFormat, Category, Product, BlogPost

def populate():
    print("Initializing Vinaigre du Maroc B2B Database population...")

    # 1. Site Settings
    settings, created = SiteSettings.objects.get_or_create(
        id=1,
        defaults={
            'site_name': 'Vinaigre du Maroc',
            'phone': '+212 5 35 12 34 56',
            'email': 'export@vinaigredemaroc.com',
            'address': 'Quartier Industriel Bensouda, Fès 30000, Morocco',
            'facebook_url': 'https://facebook.com/vinaigredemaroc',
            'instagram_url': 'https://instagram.com/vinaigredemaroc',
            'linkedin_url': 'https://linkedin.com/company/vinaigredemaroc',
        }
    )
    if created:
        print("[OK] Created Site Settings")
    else:
        print("[OK] Site Settings already exists")

    # 2. Certifications
    certs_data = [
        {
            'code': 'BRCGS',
            'name': 'BRC Global Standard',
            'icon': '🛡️',
            'theme_color': '#581825',
            'subtitle_en': 'BRC Global Standard for Food Safety (Grade A)',
            'subtitle_fr': 'Norme Mondiale BRC pour la Sécurité des Aliments (Grade A)',
            'subtitle_ar': 'معيار BRC العالمي لسلامة الأغذية (الفئة أ)',
            'subtitle_es': 'Norma Mundial BRC para la Inocuidad de los Alimentos (Grado A)',
            'subtitle_it': 'Standard Globale BRC per la Sicurezza Alimentare (Grado A)',
            'description_en': 'GFSI-recognized standard showing premium safety controls across the manufacturing facility.',
            'description_fr': 'Norme reconnue par la GFSI démontrant des contrôles de sécurité optimaux dans l\'usine.',
            'description_ar': 'معيار معترف به من GFSI يوضح ضوابط السلامة المتميزة عبر منشأة التصنيع.',
            'description_es': 'Norma reconocida por la GFSI que demuestra controles de seguridad óptimos en la planta.',
            'description_it': 'Standard riconosciuto GFSI che attesta i massimi controlli di sicurezza nello stabilimento.',
        },
        {
            'code': 'IFS',
            'name': 'IFS Food Standard',
            'icon': '🏅',
            'theme_color': '#0b3c2a',
            'subtitle_en': 'IFS Food Certification',
            'subtitle_fr': 'Certification IFS Food',
            'subtitle_ar': 'شهادة الأغذية IFS',
            'subtitle_es': 'Certificación IFS Food',
            'subtitle_it': 'Certificazione IFS Food',
            'description_en': 'Audited manufacturing operations ensuring high biological processing safety and product consistency.',
            'description_fr': 'Opérations de fabrication auditées assurant une sécurité de traitement biologique élevée.',
            'description_ar': 'عمليات تصنيع خاضعة للرقابة تضمن سلامة معالجة بيولوجية عالية واتساق المنتج.',
            'description_es': 'Operaciones de fabricación auditadas que garantizan una alta seguridad de procesamiento biológico.',
            'description_it': 'Operazioni di produzione verificate che garantiscono elevata sicurezza biologica.',
        },
        {
            'code': 'HALAL',
            'name': 'Halal Certified',
            'icon': '🕌',
            'theme_color': '#1e4620',
            'subtitle_en': '100% Halal Food Production',
            'subtitle_fr': 'Production Alimentaire 100% Halal',
            'subtitle_ar': 'إنتاج غذائي حلال 100%',
            'subtitle_es': 'Producción Alimentaria 100% Halal',
            'subtitle_it': 'Produzione Alimentare 100% Halal',
            'description_en': 'Religious and physical-chemical audits proving zero cross-contamination and pure, lawful foods.',
            'description_fr': 'Audits prouvant l\'absence de contamination croisée et des aliments purs et conformes.',
            'description_ar': 'تدقيق شرعي وتقني يثبت خلو المنتجات من أي تلوث متقاطع وموافقتها للشريعة.',
            'description_es': 'Auditorías que demuestran la ausencia de contaminación cruzada y alimentos puros.',
            'description_it': 'Verifiche che attestano l\'assenza di contaminazione incrociata e alimenti conformi.',
        },
        {
            'code': 'KOSHER',
            'name': 'Kosher Certified',
            'icon': '✡️',
            'theme_color': '#0d3b66',
            'subtitle_en': 'Kosher Food Compliance',
            'subtitle_fr': 'Conformité Alimentaire Casher',
            'subtitle_ar': 'شهادة كوشر للأغذية',
            'subtitle_es': 'Conformidad Alimentaria Kosher',
            'subtitle_it': 'Conformità Alimentare Kosher',
            'description_en': 'Full biological raw source traceability under strict rabbinate supervision.',
            'description_fr': 'Traçabilité complète des sources biologiques sous la supervision stricte du rabbinat.',
            'description_ar': 'تتبع كامل للمصادر البيولوجية الخام تحت إشراف حاخامي صارم.',
            'description_es': 'Trazabilidad completa de fuentes biológicas bajo estricta supervisión rabínica.',
            'description_it': 'Tracciabilità totale delle fonti biologiche sotto la stretta supervisione del rabbinato.',
        },
        {
            'code': 'FDA',
            'name': 'FDA Registered',
            'icon': '🇺🇸',
            'theme_color': '#333333',
            'subtitle_en': 'US FDA Registered Facility',
            'subtitle_fr': 'Établissement Enregistré auprès de la FDA US',
            'subtitle_ar': 'منشأة مسجلة لدى هيئة الغذاء والدواء الأمريكية (FDA)',
            'subtitle_es': 'Establecimiento Registrado en la FDA de EE.UU.',
            'subtitle_it': 'Stabilimento Registrato presso la FDA degli Stati Uniti',
            'description_en': 'Continuous compliance with US food safety, enabling clean clearances at US ports of entry.',
            'description_fr': 'Conformité continue avec la sécurité alimentaire américaine, facilitant le dédouanement aux ports.',
            'description_ar': 'الالتزام المستمر بسلامة الأغذية الأمريكية ، مما يتيح التخليص السهل في الموانئ.',
            'description_es': 'Cumplimiento continuo de la inocuidad alimentaria de EE.UU., facilitando el despacho aduanero.',
            'description_it': 'Conformità costante alle norme di sicurezza degli Stati Uniti per un facile sdoganamento.',
        }
    ]

    for cert in certs_data:
        obj, created = Certification.objects.get_or_create(code=cert['code'], defaults=cert)
        if created:
            print(f"[OK] Created Certification: {cert['code']}")

    # 3. Packaging Formats
    pkgs_data = [
        {'name': '200ml Glass', 'volume': '200ml', 'material_en': 'Glass', 'material_fr': 'Verre', 'material_ar': 'زجاج', 'material_es': 'Vidrio', 'material_it': 'Vetro', 'carton_specs_en': '12 bottles/box', 'pallet_specs_en': '120 boxes/pallet'},
        {'name': '300ml Glass', 'volume': '300ml', 'material_en': 'Glass', 'material_fr': 'Verre', 'material_ar': 'زجاج', 'material_es': 'Vidrio', 'material_it': 'Vetro', 'carton_specs_en': '12 bottles/box', 'pallet_specs_en': '108 boxes/pallet'},
        {'name': '500ml Glass', 'volume': '500ml', 'material_en': 'Glass', 'material_fr': 'Verre', 'material_ar': 'زجاج', 'material_es': 'Vidrio', 'material_it': 'Vetro', 'carton_specs_en': '12 bottles/box', 'pallet_specs_en': '84 boxes/pallet'},
        {'name': '200ml PET', 'volume': '200ml', 'material_en': 'PET', 'material_fr': 'PET', 'material_ar': 'بلاستيك PET', 'material_es': 'PET', 'material_it': 'PET', 'carton_specs_en': '24 bottles/box', 'pallet_specs_en': '96 boxes/pallet'},
        {'name': '2L PET', 'volume': '2L', 'material_en': 'PET', 'material_fr': 'PET', 'material_ar': 'بلاستيك PET', 'material_es': 'PET', 'material_it': 'PET', 'carton_specs_en': '6 jugs/box', 'pallet_specs_en': '60 boxes/pallet'},
        {'name': '5L PET', 'volume': '5L', 'material_en': 'PET', 'material_fr': 'PET', 'material_ar': 'بلاستيك PET', 'material_es': 'PET', 'material_it': 'PET', 'carton_specs_en': '4 jugs/box', 'pallet_specs_en': '48 boxes/pallet'},
        {'name': '1000L IBC', 'volume': '1000L', 'material_en': 'HDPE Tank on Galvanized Pallet', 'material_fr': 'Citerne PEHD sur Palette Galvanisée', 'material_ar': 'خزان PEHD على لوح مجلفن', 'material_es': 'Tanque PEHD en Palet Galvanizado', 'material_it': 'Cisterna PEHD su Pallet Zincato', 'carton_specs_en': '1 IBC Tank', 'pallet_specs_en': '1 Tank/Pallet slot'},
    ]

    for pkg in pkgs_data:
        obj, created = PackagingFormat.objects.get_or_create(name=pkg['name'], defaults=pkg)
        if created:
            print(f"[OK] Created Packaging Format: {pkg['name']}")

    # 4. Categories
    vinegars_cat, created = Category.objects.get_or_create(
        slug='vinegars',
        defaults={
            'name_en': 'Vinegars',
            'name_fr': 'Vinaigres',
            'name_ar': 'أنواع الخل',
            'name_es': 'Vinagres',
            'name_it': 'Aceti',
            'description_en': 'Premium biological fermented vinegars made from selected ciders, red and white wines, and alcohols.',
            'description_fr': 'Vinaigres fermentés biologiques de qualité supérieure élaborés à partir de cidres et de vins sélectionnés.',
            'description_ar': 'خل مخمر بيولوجي ممتاز مصنوع من التفاح المحضر والخمور المنتقاة.',
            'description_es': 'Vinagres fermentados biológicos premium elaborados a partir de sidras y vinos seleccionados.',
            'description_it': 'Pregiati aceti fermentati biologicamente a partire da sidro e vini selezionati.',
        }
    )
    if created:
        print("[OK] Created Category: Vinegars")

    sauces_cat, created = Category.objects.get_or_create(
        slug='sauces-condiments',
        defaults={
            'name_en': 'Sauces & Condiments',
            'name_fr': 'Sauces & Condiments',
            'name_ar': 'الصلصات والتوابل',
            'name_es': 'Salsas y Condimentos',
            'name_it': 'Salse e Condimenti',
            'description_en': 'Authentic Moroccan export hot sauces, capers pastes, and preserved specialties.',
            'description_fr': 'Sauces piquantes d\'exportation marocaines authentiques et spécialités de condiments.',
            'description_ar': 'صلصات حارة مغربية أصلية للتصدير ومعاجين الكبار والتوابل Preserved.',
            'description_es': 'Salsas picantes de exportación marroquíes auténticas y especialidades de condimentos.',
            'description_it': 'Salse piccanti d\'esportazione marocchine autentiche e specialità sottaceto.',
        }
    )
    if created:
        print("[OK] Created Category: Sauces & Condiments")

    # 5. Products (11 products)
    all_packaging = list(PackagingFormat.objects.all())
    all_certs = list(Certification.objects.all())

    products_data = [
        # --- VINEGARS ---
        {
            'category': vinegars_cat,
            'name_en': 'Blond Alcohol Vinegar',
            'name_fr': 'Vinaigre blond d’alcool',
            'name_ar': 'خل الكحول الأشقر',
            'name_es': 'Vinagre rubio de alcohol',
            'name_it': 'Aceto biondo di alcool',
            'acidity': '6%',
            'is_premium': True,
            'is_featured': True,
            'short_description_en': 'Crystal clear, high-purity blonde alcohol vinegar for pickling and culinary preservation.',
            'short_description_fr': 'Vinaigre d\'alcool blond d\'une grande pureté pour les marinades et la conservation.',
            'short_description_ar': 'خل كحولي أشقر نقي للغاية مثالي للتخليل وحفظ الأغذية.',
            'short_description_es': 'Vinagre rubio de alcohol de alta pureza para encurtidos y conservación.',
            'short_description_it': 'Aceto biondo di alcool ad elevata purezza per sottaceti e conservazione.',
            'description_en': 'Manufactured using advanced continuous biological fermentation. Possesses clean acidity and clarity, serving bulk food packers and retail supermarket brands alike.',
            'ingredients_en': 'Diluted agricultural alcohol vinegar, coloring caramel.',
            'usage_ideas_en': 'Pickling cucumbers, commercial salad dressings, institutional food preparation.',
        },
        {
            'category': vinegars_cat,
            'name_en': 'Red Wine Vinegar',
            'name_fr': 'Vinaigre de vin rouge',
            'name_ar': 'خل النبيذ الأحمر',
            'name_es': 'Vinagre de vino tinto',
            'name_it': 'Aceto di vino rosso',
            'acidity': '6%',
            'is_premium': True,
            'is_featured': True,
            'short_description_en': 'Rich, deep red wine vinegar, fermented from selected Moroccan grapes.',
            'short_description_fr': 'Vinaigre de vin rouge riche et profond, fermenté à partir de raisins marocains sélectionnés.',
            'short_description_ar': 'خل نبيذ أحمر غني وداكن، مخمر من العنب المغربي الفاخر.',
            'short_description_es': 'Vinagre de vino tinto rico y profundo, fermentado de uvas marroquíes.',
            'short_description_it': 'Aceto di vino rosso ricco e profondo, fermentato da uve marocchine selezionate.',
            'description_en': 'Slowly acetified to keep the natural grape bouquet. Adds a premium, robust acidic body to gourmet dressings and Mediterranean marinades.',
            'ingredients_en': 'Red wine vinegar, antioxidant (sulfites).',
            'usage_ideas_en': 'Vinaigrettes, red meat marinades, gourmet sauce reductions.',
        },
        {
            'category': vinegars_cat,
            'name_en': 'White Wine Vinegar',
            'name_fr': 'Vinaigre de vin blanc',
            'name_ar': 'خل النبيذ الأبيض',
            'name_es': 'Vinagre de vino blanco',
            'name_it': 'Aceto di vino bianco',
            'acidity': '6%',
            'is_premium': False,
            'is_featured': False,
            'short_description_en': 'Crisp, delicate white wine vinegar with subtle floral highlights.',
            'short_description_fr': 'Vinaigre de vin blanc frais et délicat avec de subtils reflets floraux.',
            'short_description_ar': 'خل نبيذ أبيض منعش ولطيف مع إيحاءات زهرية خفيفة.',
            'short_description_es': 'Vinagre de vino blanco crujiente y delicado con sutiles toques florales.',
            'short_description_it': 'Aceto di vino bianco fresco e delicato con sfumature floreali.',
            'description_en': 'Fermented from clean white wines. Clear and bright body with a subtle fruity balance, optimized for fish, seafood sauces, and high-end retail dressing brands.',
            'ingredients_en': 'White wine vinegar, antioxidant (sulfites).',
            'usage_ideas_en': 'Hollandaise sauce, fish seasonings, pickling white vegetables.',
        },
        {
            'category': vinegars_cat,
            'name_en': 'Apple Aromatic Vinegar',
            'name_fr': 'Vinaigre aromatisé pomme',
            'name_ar': 'خل بنكهة التفاح',
            'name_es': 'Vinagre aromatizado manzana',
            'name_it': 'Aceto aromatizzato alla mela',
            'acidity': '6%',
            'is_premium': False,
            'is_featured': False,
            'short_description_en': 'Premium vinegar infused with sweet, crisp apple extracts.',
            'short_description_fr': 'Vinaigre de qualité supérieure infusé d\'extraits de pommes douces et fraîches.',
            'short_description_ar': 'خل ممتاز غني بمستخلصات التفاح الحلوة والمنعشة.',
            'short_description_es': 'Vinagre premium infusionado con extractos de manzana dulce.',
            'short_description_it': 'Pregiato aceto infuso con estratti di mele dolci e fresche.',
            'description_en': 'Features a harmonious balance between intense acidity and natural apple sweetness. Ideal for light summer dressings and retail packaging catalogs.',
            'ingredients_en': 'White vinegar, natural apple flavoring, caramel coloring.',
            'usage_ideas_en': 'Summer salads, white meat marinades, fruit pickles.',
        },
        {
            'category': vinegars_cat,
            'name_en': 'Lemon Aromatic Vinegar',
            'name_fr': 'Vinaigre aromatisé citron',
            'name_ar': 'خل بنكهة الليمون',
            'name_es': 'Vinagre aromatizado limón',
            'name_it': 'Aceto aromatizzato al limone',
            'acidity': '6%',
            'is_premium': False,
            'is_featured': False,
            'short_description_en': 'Bright, zesty lemon-infused white vinegar, adding fresh citrus acidity.',
            'short_description_fr': 'Vinaigre blanc frais infusé au citron, apportant une acidité citrique vive.',
            'short_description_ar': 'خل أبيض منعش بنكهة الليمون، يضفي حموضة حمضيات حيوية.',
            'short_description_es': 'Vinagre blanco infusionado con limón, aportando acidez cítrica fresca.',
            'short_description_it': 'Aceto bianco infuso con limone, per una fresca nota di acidità agrumata.',
            'description_en': 'Combines standard 6% biological acidity with fresh lemon peel oils. Excellent choice for seafood packing, retail table condiments, and gourmet marinades.',
            'ingredients_en': 'White vinegar, natural lemon essential oils.',
            'usage_ideas_en': 'Fish dressings, chicken seasoning, fresh green salads.',
        },
        {
            'category': vinegars_cat,
            'name_en': 'Apple Cider Vinegar',
            'name_fr': 'Vinaigre de cidre',
            'name_ar': 'خل التفاح الطبيعي',
            'name_es': 'Vinagre de sidra de manzana',
            'name_it': 'Aceto di sidro di mela',
            'acidity': '5%',
            'is_premium': True,
            'is_featured': True,
            'short_description_en': 'Unfiltered, biologically fermented apple cider vinegar, rich in active cultures.',
            'short_description_fr': 'Vinaigre de cidre de pomme non filtré, riche en cultures actives.',
            'short_description_ar': 'خل تفاح طبيعي غير مصفى، غني بالخمائر النشطة ومثالي للصحة.',
            'short_description_es': 'Vinagre de sidra de manzana sin filtrar, rico en cultivos activos.',
            'short_description_it': 'Aceto di sidro di mele non filtrato, ricco di colture attive.',
            'description_en': 'Naturally fermented from local Moroccan apples. Fully raw to keep active mother structures. High demand in US/EU organic retail markets.',
            'ingredients_en': 'Raw fermented apple cider vinegar.',
            'usage_ideas_en': 'Health tonics, zesty salad dressings, organic cosmetics.',
        },
        {
            'category': vinegars_cat,
            'name_en': 'Caramel Colored Vinegar',
            'name_fr': 'Vinaigre coloré',
            'name_ar': 'الخل الملون',
            'name_es': 'Vinagre coloreado',
            'name_it': 'Aceto colorato',
            'acidity': '6%',
            'is_premium': False,
            'is_featured': False,
            'short_description_en': 'Caramel colored white vinegar, optimized for general retail uses.',
            'short_description_fr': 'Vinaigre blanc coloré au caramel, optimisé pour les usages généraux.',
            'short_description_ar': 'خل أبيض ملون بالكاراميل، مصمم للاستخدامات التجارية العامة.',
            'short_description_es': 'Vinagre blanco coloreado con caramelo, optimizado para uso general.',
            'short_description_it': 'Aceto bianco colorato con caramello, ideale per usi commerciali generali.',
            'description_en': 'Designed specifically for private label supermarket grids. High clarity, uniform coloration, and strict acidity levels serve standard B2B buyers.',
            'ingredients_en': 'Diluted white vinegar, food-grade caramel color.',
            'usage_ideas_en': 'Table condiment, pickling, general seasoning.',
        },
        # --- SAUCES & CONDIMENTS ---
        {
            'category': sauces_cat,
            'name_en': 'Hot Sauce',
            'name_fr': 'Sauce Piquante',
            'name_ar': 'صلصة حارة',
            'name_es': 'Salsa Picante',
            'name_it': 'Salsa Piccante',
            'acidity': '3%',
            'is_premium': True,
            'is_featured': True,
            'short_description_en': 'Fiery, export-grade hot pepper sauce, aged with natural vinegar.',
            'short_description_fr': 'Sauce piquante de qualité d\'exportation, vieillie au vinaigre naturel.',
            'short_description_ar': 'صلصة حارة قوية للتصدير، معتقة بالخل الطبيعي.',
            'short_description_es': 'Salsa picante de exportación, madurada con vinagre natural.',
            'short_description_it': 'Salsa piccante d\'esportazione, invecchiata con aceto naturale.',
            'description_en': 'Crafted using handpicked red hot chilies, biological vinegar, and sea salt. Delivers clean, intense heat for international wholesale and retail restaurant distribution.',
            'ingredients_en': 'Aged red hot peppers, vinegar, salt, stabilizers.',
            'usage_ideas_en': 'Chicken wings, marinades, tabletop dining condiment.',
        },
        {
            'category': sauces_cat,
            'name_en': 'Lemon Pickled Gherkins',
            'name_fr': 'Cornichon de citron',
            'name_ar': 'مخلل خيار بالليمون',
            'name_es': 'Pepinillos con limón',
            'name_it': 'Cetriolini al limone',
            'acidity': '4%',
            'is_premium': True,
            'is_featured': False,
            'short_description_en': 'Zesty pickled baby cucumbers infused with natural Moroccan lemon.',
            'short_description_fr': 'Petits cornichons croquants infusés au citron marocain naturel.',
            'short_description_ar': 'مخلل خيار صغير مقرمش غني بنكهة الليمون المغربي الطبيعي.',
            'short_description_es': 'Pepinillos crujientes infusionados con limón marroquí natural.',
            'short_description_it': 'Cetriolini croccanti infusi con limone marocchino naturale.',
            'description_en': 'Handpicked baby cucumbers pickled in clear vinegar brine and zesty lemon rings. Extremely popular specialty condiment for European and Middle Eastern food tables.',
            'ingredients_en': 'Baby cucumbers, vinegar, water, lemon rings, salt, natural spices.',
            'usage_ideas_en': 'Gourmet plates, burger dressings, traditional side dishes.',
        },
        {
            'category': sauces_cat,
            'name_en': 'Hot Pepper Paste',
            'name_fr': 'Pâte de piment fort',
            'name_ar': 'معجون الفلفل الحار',
            'name_es': 'Pasta de chile picante',
            'name_it': 'Pasta di peperoncino piccante',
            'acidity': '2.5%',
            'is_premium': False,
            'is_featured': False,
            'short_description_en': 'Thick, robust red hot pepper paste, perfect for culinary compounding.',
            'short_description_fr': 'Pâte de piment rouge épaisse et robuste, parfaite pour les préparations culinaires.',
            'short_description_ar': 'معجون فلفل حار أحمر كثيف ومميز، مثالي للاستخدامات الصناعية والطهي.',
            'short_description_es': 'Pasta de chile rojo espesa y robusta, perfecta para la cocina.',
            'short_description_it': 'Pasta di peperoncino rosso densa e robusta, ideale in cucina.',
            'description_en': 'Ground sun-dried chilies blended with sea salt and vinegar. Serves bulk food companies, sauce manufacturers, and retail supermarket lines.',
            'ingredients_en': 'Red hot chilies, salt, vinegar, acidity regulators.',
            'usage_ideas_en': 'Industrial base for sauces, meat marinades, restaurant compounding.',
        },
        {
            'category': sauces_cat,
            'name_en': 'Caper Paste',
            'name_fr': 'Pâte de câpre',
            'name_ar': 'معجون الكبار',
            'name_es': 'Pasta de alcaparras',
            'name_it': 'Paté di capperi',
            'acidity': '3%',
            'is_premium': True,
            'is_featured': True,
            'short_description_en': 'Premium savory caper tapenade paste, packed with Mediterranean umami.',
            'short_description_fr': 'Pâte de câpres savoureuse et de qualité supérieure, riche en saveurs.',
            'short_description_ar': 'معجون كبار مالح فاخر، غني بنكهة أومامي البحر الأبيض المتوسط.',
            'short_description_es': 'Pasta de alcaparras premium y sabrosa, rica en sabores.',
            'short_description_it': 'Paté di capperi pregiato e saporito, ricco di sapore mediterraneo.',
            'description_en': 'Finely ground salted Moroccan capers blended with vinegar and vegetable oil. A gourmet umami spread optimized for B2B export contracts.',
            'ingredients_en': 'Moroccan capers, sunflower oil, vinegar, spices.',
            'usage_ideas_en': 'Gourmet spreads, seafood sauces, salad dressings.',
        }
    ]


    PRODUCT_TRANSLATIONS = {
        "Blond Alcohol Vinegar": {
            "description_fr": "Fabriqué par fermentation biologique continue avancée. Possède une acidité nette et une grande clarté, idéal pour les conditionneurs de produits alimentaires en vrac et les marques de supermarchés.",
            "ingredients_fr": "Vinaigre d'alcool agricole dilué, colorant caramel.",
            "usage_ideas_fr": "Cornichons au vinaigre, vinaigrettes commerciales, préparation de repas collectifs.",
            "description_ar": "صُنع باستخدام تخمير حيوي مستمر متطور. يتميز بحموضة ونقاء تام، ليلبي متطلبات معبئي الأغذية بالجملة والعلامات التجارية للتجزئة على حد سواء.",
            "ingredients_ar": "خل كحولي زراعي مخفف، ملون كراميل.",
            "usage_ideas_ar": "تخليل الخيار، تتبيلات السلطات التجارية، تحضير الأغذية للمؤسسات.",
            "description_es": "Fabricado mediante fermentación biológica continua avanzada. Posee una acidez limpia y claridad, sirviendo tanto a envasadores de alimentos a granel como a marcas de supermercados.",
            "ingredients_es": "Vinagre de alcohol agrícola diluido, colorante caramelo.",
            "usage_ideas_es": "Encurtido de pepinillos, aderezos comerciales para ensaladas, preparación institucional de alimentos.",
            "description_it": "Prodotto con fermentazione biologica continua avanzata. Ha un'acidità pulita e un'ottima limpidezza, ideale per confezionatori di alimenti sfusi e marchi di supermercati.",
            "ingredients_it": "Aceto di alcool agricolo diluito, colorante caramello.",
            "usage_ideas_it": "Sottaceti, condimenti commerciali per insalata, preparazione di cibi per mense."
        },
        "Red Wine Vinegar": {
            "description_fr": "Acétifié lentement pour conserver le bouquet naturel du raisin. Apporte une touche acide robuste et raffinée aux vinaigrettes gourmandes et marinades méditerranéennes.",
            "ingredients_fr": "Vinaigre de vin rouge, antioxydant (sulfites).",
            "usage_ideas_fr": "Vinaigrettes, marinades pour viandes rouges, réductions de sauces gourmandes.",
            "description_ar": "خل نبيذ أحمر معتق ببطء للحفاظ على نكهة العنب الطبيعية. يضفي قواماً حمضياً قوياً ومميزاً للتتبيلات الراقية واللحوم المتوسطية.",
            "ingredients_ar": "خل نبيذ أحمر، مضاد للأكسدة (كبريتات).",
            "usage_ideas_ar": "الصلصات الحمضية، تتبيل اللحوم الحمراء، تقليل الصلصات الفاخرة.",
            "description_es": "Acetificado lentamente para conservar el bouquet natural de la uva. Aporta un cuerpo ácido robusto y premium a los aderezos gourmet y marinados mediterráneos.",
            "ingredients_es": "Vinagre de vino tinto, antioxidante (sulfitos).",
            "usage_ideas_es": "Vinagretas, adobos para carne roja, reducciones de salsa gourmet.",
            "description_it": "Acetificato lentamente per conservare il bouquet naturale dell'uva. Aggiunge un corpo acido robusto e di alta qualità a condimenti gourmet e marinate mediterranee.",
            "ingredients_it": "Aceto di vino rosso, antiossidante (solfiti).",
            "usage_ideas_it": "Vinaigrette, marinate per carni rosse, riduzioni di salse gourmet."
        },
        "White Wine Vinegar": {
            "description_fr": "Fermenté à partir de vins blancs de qualité. Corps clair et brillant avec un équilibre fruité subtil, optimisé pour les poissons, les sauces de fruits de mer et les vinaigrettes de luxe.",
            "ingredients_fr": "Vinaigre de vin blanc, antioxydant (sulfites).",
            "usage_ideas_fr": "Sauce hollandaise, assaisonnements pour poissons, conservation des légumes blancs.",
            "description_ar": "مخمر من أنقى أنواع النبيذ الأبيض. قوام صاف ومشرق مع توازن فاكهي لطيف، مثالي للأسماك، وصلصات المأكولات البحرية، وتتبيلات التجزئة الراقية.",
            "ingredients_ar": "خل نبيذ أبيض، مضاد للأكسدة (كبريتات).",
            "usage_ideas_ar": "صلصة الهولنديز، تتبيل الأسماك، تخليل الخضروات البيضاء.",
            "description_es": "Fermentado a partir de vinos blancos limpios. Cuerpo claro y brillante con un sutil equilibrio frutal, optimizado para pescados, salsas de mariscos y aderezos premium de supermercado.",
            "ingredients_es": "Vinagre de vino blanco, antioxidante (sulfitos).",
            "usage_ideas_es": "Salsa holandesa, condimentos para pescado, encurtido de verduras blancas.",
            "description_it": "Fermentato da vini bianchi selezionati. Corpo limpido e brillante con un delicato equilibrio fruttato, ideale per pesce, sughi di mare e marchi di condimenti di fascia alta.",
            "ingredients_it": "Aceto di vino bianco, antiossidante (solfiti).",
            "usage_ideas_it": "Salsa olandese, condimenti per pesce, conservazione di ortaggi bianchi."
        },
        "Apple Aromatic Vinegar": {
            "description_fr": "Présente un équilibre harmonieux entre l'acidité intense et la douceur naturelle de la pomme. Idéal pour les vinaigrettes légères d'été et les catalogues de vente au détail.",
            "ingredients_fr": "Vinaigre blanc, arôme naturel de pomme, colorant caramel.",
            "usage_ideas_fr": "Salades d'été, marinades de viande blanche, pickles de fruits.",
            "description_ar": "يتميز بتوازن متناغم بين الحموضة القوية وحلاوة التفاح الطبيعية. مثالي لتتبيلات الصيف الخفيفة وكتالوجات التعبئة والتجزئة.",
            "ingredients_ar": "خل أبيض، نكهة تفاح طبيعية، ملون كراميل.",
            "usage_ideas_ar": "سلطات الصيف، تتبيل اللحوم البيضاء، مخللات الفاكهة.",
            "description_es": "Presenta un equilibrio armonioso entre la acidez intensa y el dulzor natural de la manzana. Ideal para aderezos ligeros de verano y catálogos de venta al por menor.",
            "ingredients_es": "Vinagre blanco, aroma natural de manzana, colorante caramelo.",
            "usage_ideas_es": "Ensaladas de verano, marinados de carne blanca, encurtido de frutas.",
            "description_it": "Presenta un equilibrio armonioso tra acidità intensa e la dolcezza naturale della mela. Ideale per condimenti estivi leggeri e cataloghi di vendita al dettaglio.",
            "ingredients_it": "Aceto bianco, aroma naturale di mela, colorante caramello.",
            "usage_ideas_it": "Insalate estive, marinate per carni bianche, sottaceti di frutta."
        },
        "Lemon Aromatic Vinegar": {
            "description_fr": "Associe une acidité biologique standard de 6 % à des huiles d'écorce de citron fraîches. Excellent pour le conditionnement des fruits de mer, les condiments de table et les marinades gourmandes.",
            "ingredients_fr": "Vinaigre blanc, huiles essentielles de citron naturelles.",
            "usage_ideas_fr": "Vinaigrettes pour poissons, assaisonnement de poulet, salades vertes fraîches.",
            "description_ar": "يجمع بين حموضة حيوية بنسبة 6% وزيوت قشر الليمون الطازجة. خيار ممتاز لتعبئة المأكولات البحرية، وتتبيلات المائدة للتجزئة، وتتبيلات الطهي الفاخرة.",
            "ingredients_ar": "خل أبيض، زيوت ليمون أساسية طبيعية.",
            "usage_ideas_ar": "صلصات الأسماك، تتبيل الدجاج، السلطات الخضراء الطازجة.",
            "description_es": "Combina una acidez biológica estándar del 6% con aceites frescos de cáscara de limón. Excelente opción para el envasado de mariscos, condimentos de mesa y marinados gourmet.",
            "ingredients_es": "Vinagre blanco, aceites esenciales de limón naturales.",
            "usage_ideas_es": "Aderezos de pescado, sazón para pollo, ensaladas verdes frescas.",
            "description_it": "Combina la tipica acidità biologica al 6% con oli essenziali di scorza di limone. Ottima scelta per il confezionamento di frutti di mare, condimenti da tavola e marinate gourmet.",
            "ingredients_it": "Aceto bianco, oli essenziali naturali di limone.",
            "usage_ideas_it": "Condimenti per pesce, condimento per pollo, insalate verdi fresche."
        },
        "Apple Cider Vinegar": {
            "description_fr": "Fermenté naturellement à partir de pommes marocaines locales. Totalement brut pour préserver la 'mère de vinaigre' active. Très demandé sur les marchés biologiques américains et européens.",
            "ingredients_fr": "Vinaigre de cidre de pomme brut fermenté.",
            "usage_ideas_fr": "Toniques de santé, vinaigrettes relevées, cosmétiques biologiques.",
            "description_ar": "مخمر طبيعياً من التفاح المغربي المحلي. خام وغير مصفى للحفاظ على 'أم الخل' النشطة. طلب مرتفع في أسواق العضوية الأمريكية والأوروبية.",
            "ingredients_ar": "خل تفاح خام مخمر.",
            "usage_ideas_ar": "منشطات الصحة، تتبيلات السلطات الحيوية، مستحضرات التجميل العضوية.",
            "description_es": "Fermentado naturalmente a partir de manzanas marroquíes locales. Totalmente crudo para mantener activas las estructuras de la madre. Alta demanda en mercados orgánicos de EE. UU. y la UE.",
            "ingredients_es": "Vinagre de sidra de manzana fermentado crudo.",
            "usage_ideas_es": "Tónicos de salud, aderezos picantes para ensalada, cosmética orgánica.",
            "description_it": "Fermentato naturalmente da mele marocchine locali. Completamente grezzo per mantenere attiva la 'madre' del condimento. Alta richiesta nei mercati biologici di Stati Uniti ed Europa.",
            "ingredients_it": "Aceto di sidro di mele grezzo fermentato.",
            "usage_ideas_it": "Bevande salutari, condimenti saporiti per insalata, biologici."
        },
        "Caramel Colored Vinegar": {
            "description_fr": "Conçu spécifiquement pour les réseaux de supermarchés sous marque de distributeur. Clarté élevée, coloration uniforme et niveaux d'acidité stricts pour répondre aux exigences des acheteurs B2B.",
            "ingredients_fr": "Vinaigre blanc dilué, colorant caramel de qualité alimentaire.",
            "usage_ideas_fr": "Condiment de table, conserves au vinaigre, assaisonnement général.",
            "description_ar": "مصمم خصيصاً لشبكات السوبرماركت والعلامات التجارية الخاصة. يتميز بنقاء عالي، وتلوين موحد، ومستويات حموضة دقيقة تخدم المشترين الصناعيين.",
            "ingredients_ar": "خل أبيض مخفف، لون كراميل غذائي.",
            "usage_ideas_ar": "تتبيلة مائدة، تخليل، بهارات عامة.",
            "description_es": "Diseñado específicamente para supermercados bajo marca blanca. Alta claridad, coloración uniforme y niveles estrictos de acidez para compradores B2B.",
            "ingredients_es": "Vinagre blanco diluido, colorante caramelo de calidad alimentaria.",
            "usage_ideas_es": "Condimento de mesa, encurtidos, condimento general.",
            "description_it": "Sviluppato specificamente per le catene di supermercati con marchio privato. Elevata limpidezza, colorazione uniforme e livelli rigorosi di acidità per soddisfare i compratori B2B.",
            "ingredients_it": "Aceto bianco diluito, colorante caramello alimentare.",
            "usage_ideas_it": "Condimento da tavola, conservazione, condimento generale."
        },
        "Hot Sauce": {
            "description_fr": "Préparée avec des piments rouges sélectionnés à la main, du vinaigre biologique et du sel marin. Offre un piquant propre et intense pour la vente en gros et la restauration internationale.",
            "ingredients_fr": "Piments rouges vieillis, vinaigre, sel, stabilisants.",
            "usage_ideas_fr": "Ailes de poulet, marinades, condiment pour tables de restaurant.",
            "description_ar": "مُعد باستخدام فلفل أحمر حار منتقى يدوياً، وخل حيوي، وملح بحري. يضفي حرارة نقية وقوية تناسب أسواق الجملة الدولية ومطاعم التجزئة.",
            "ingredients_ar": "فلفل أحمر حار معتق، خل، ملح، مواد مثبتة.",
            "usage_ideas_ar": "أجنحة الدجاج، التتبيلات، صلصة مائدة للمطاعم.",
            "description_es": "Elaborada con chiles rojos seleccionados a mano, vinagre biológico y sal marina. Ofrece un picante limpio e intenso para distribución mayorista y restauración internacional.",
            "ingredients_es": "Chiles rojos madurados, vinagre, sal, estabilizantes.",
            "usage_ideas_es": "Alitas de pollo, adobos, condimento de mesa para restaurantes.",
            "description_it": "Elaborata con peperoncini rossi selezionati a mano, aceto biologico e sale marino. Offre un calore pulito e intenso per l'ingrosso internazionale e la ristorazione.",
            "ingredients_it": "Peperoncini rossi invecchiati, aceto, sale, stabilizzanti.",
            "usage_ideas_it": "Ali di pollo, marinate, condimento da tavola per ristoranti."
        },
        "Lemon Pickled Gherkins": {
            "description_fr": "Jeunes cornichons croquants marinés dans une saumure de vinaigre claire et des tranches de citron marocain. Condiment spécial très apprécié sur les tables d'Europe et du Moyen-Orient.",
            "ingredients_fr": "Petits cornichons, vinaigre, eau, tranches de citron, sel, épices naturelles.",
            "usage_ideas_fr": "Plats gourmets, garnitures de burgers, plats d'accompagnement traditionnels.",
            "description_ar": "خيار صغير مقرمش منتقى يدوياً مخلل في محلول خل نقي مع شرائح ليمون مغربي منعشة. مقبلات خاصة مشهورة جداً للمائدة الأوروبية والشرق أوسطية.",
            "ingredients_ar": "خيار صغير، خل، ماء، شرائح ليمون، ملح، توابل طبيعية.",
            "usage_ideas_ar": "أطباق فاخرة، تزيين البرجر، الأطباق الجانبية التقليدية.",
            "description_es": "Pepinillos pequeños seleccionados a mano en salmuera de vinagre claro y rodajas de limón marroquí fresco. Condimento de especialidad muy popular en las mesas europeas y de Medio Oriente.",
            "ingredients_es": "Pepinillos pequeños, vinagre, agua, rodajas de limón, sal, especias naturales.",
            "usage_ideas_es": "Platos gourmet, aderezos para hamburguesas, acompañamientos tradicionales.",
            "description_it": "Cetriolini novelli selezionati a mano marinati in salamoia di aceto e fette di limone marocchino. Condimento speciale estremamente popolare per le tavole europee e mediorientali.",
            "ingredients_it": "Cetriolini novelli, aceto, acqua, fette di limone, sale, spezie naturali.",
            "usage_ideas_it": "Piatti gourmet, farcitura di burger, contorni tradizionali."
        },
        "Hot Pepper Paste": {
            "description_fr": "Piments séchés au soleil moulus et mélangés à du sel marin et du vinaigre. Destinée aux industriels de l'agroalimentaire, aux fabricants de sauces et aux supermarchés.",
            "ingredients_fr": "Piments rouges forts, sel, vinaigre, régulateurs d'acidité.",
            "usage_ideas_fr": "Base industrielle pour sauces, marinades de viande, préparations de restauration.",
            "description_ar": "فلفل حار مجفف تحت أشعة الشمس ومطحون مع ملح البحر والخل. يخدم شركات الأغذية الكبرى، مصنعي الصلصات، وخطوط السوبرماركت للتجزئة.",
            "ingredients_ar": "فلفل أحمر حار، ملح، خل، منظمات الحموضة.",
            "usage_ideas_ar": "قاعدة صناعية للصلصات، تتبيل اللحوم، تحضير مطاعم.",
            "description_es": "Chiles secados al sol triturados y mezclados con sal marina y vinagre. Sirve a empresas de alimentos a granel, fabricantes de salsas y líneas de supermercado.",
            "ingredients_es": "Chiles rojos picantes, sal, vinagre, reguladores de acidez.",
            "usage_ideas_es": "Base industrial para salsas, marinados de carne, aderezos de restaurante.",
            "description_it": "Peperoncini essiccati al sole macinati e mescolati con sale marino e aceto. Ideale per aziende alimentari all'ingrosso, produttori di salse e supermercati.",
            "ingredients_it": "Peperoncini rossi piccanti, sale, aceto, regolatori di acidità.",
            "usage_ideas_it": "Peperoncini macinati, sale, aceto, regolatori di acidità."
        },
        "Caper Paste": {
            "description_fr": "Câpres marocaines salées et finement broyées, mélangées à du vinaigre et de l'huile végétale. Une tapenade gourmande riche en umami, optimisée pour les contrats d'exportation B2B.",
            "ingredients_fr": "Câpres marocaines, huile de tournesol, vinaigre, épices.",
            "usage_ideas_fr": "Tartinades gourmandes, sauces pour fruits de mer, vinaigrettes.",
            "description_ar": "كبار مغربي مالح مطحون ناعماً ومخلوط بالخل والزيت النباتي. معجون أومامي فاخر مصمم خصيصاً لعقود التصدير الصناعية.",
            "ingredients_ar": "كبار مغربي، زيت عباد الشمس، خل، توابل.",
            "usage_ideas_ar": "مدهونات فاخرة، صلصات المأكولات البحرية، تتبيلات السلطة.",
            "description_es": "Alcaparras marroquíes saladas finamente trituradas mezcladas con vinagre y aceite vegetal. Un paté gourmet de umami optimizado para contratos de distribución B2B.",
            "ingredients_es": "Alcaparras marroquíes, aceite de girasol, vinagre, especias.",
            "usage_ideas_es": "Pastas gourmet para untar, salsas de mariscos, aderezos para ensaladas.",
            "description_it": "Capperi marocchini salati finemente macinati e mescolati con aceto e olio vegetale. Un paté gourmet ricco di umami, ideale per i contratti di esportazione B2B.",
            "ingredients_it": "Capperi marocchini, olio di girasole, aceto, spezie.",
            "usage_ideas_it": "Creme gourmet da spalmare, salse per frutti di mare, condimenti per insalata."
        }
    }


    for prod in products_data:
        # Merge translation fields
        name_en = prod['name_en']
        if name_en in PRODUCT_TRANSLATIONS:
            prod.update(PRODUCT_TRANSLATIONS[name_en])

        obj, created = Product.objects.get_or_create(

            name_en=prod['name_en'],
            defaults={
                'category': prod['category'],
                'name_fr': prod.get('name_fr', ''),
                'name_ar': prod.get('name_ar', ''),
                'name_es': prod.get('name_es', ''),
                'name_it': prod.get('name_it', ''),
                'acidity': prod.get('acidity', '6%'),
                'is_premium': prod.get('is_premium', False),
                'is_featured': prod.get('is_featured', False),
                'short_description_en': prod.get('short_description_en', ''),
                'short_description_fr': prod.get('short_description_fr', ''),
                'short_description_ar': prod.get('short_description_ar', ''),
                'short_description_es': prod.get('short_description_es', ''),
                'short_description_it': prod.get('short_description_it', ''),
                'description_en': prod.get('description_en', ''),
                'description_fr': prod.get('description_fr', ''),
                'description_ar': prod.get('description_ar', ''),
                'description_es': prod.get('description_es', ''),
                'description_it': prod.get('description_it', ''),
                'ingredients_en': prod.get('ingredients_en', ''),
                'ingredients_fr': prod.get('ingredients_fr', ''),
                'ingredients_ar': prod.get('ingredients_ar', ''),
                'ingredients_es': prod.get('ingredients_es', ''),
                'ingredients_it': prod.get('ingredients_it', ''),
                'usage_ideas_en': prod.get('usage_ideas_en', ''),
                'usage_ideas_fr': prod.get('usage_ideas_fr', ''),
                'usage_ideas_ar': prod.get('usage_ideas_ar', ''),
                'usage_ideas_es': prod.get('usage_ideas_es', ''),
                'usage_ideas_it': prod.get('usage_ideas_it', ''),
            }
        )
        if created:
            # Associate packaging and certifications
            obj.packaging_formats.set(all_packaging)
            obj.certifications.set(all_certs)
            obj.save()
            print(f"[OK] Created Product: {prod['name_en']}")

    # 6. Blog Posts
    posts_data = [
        {
            'title_en': 'How Mixed-Container Shipping Saves B2B Import Logistics Cost',
            'title_fr': 'Comment l\'expédition par conteneurs mixtes réduit les coûts logistiques B2B',
            'title_ar': 'كيف يوفر الشحن بالحاويات المشتركة تكاليف اللوجستيات B2B',
            'title_es': 'Cómo el envío de contenedores mixtos ahorra costos logísticos B2B',
            'title_it': 'Come le spedizioni in container misti riducono i costi logistici B2B',
            'excerpt_en': 'Discover how combining vinegars, hot sauces, and caper pastes in a single FCL mixed container load optimizes shipping rates.',
            'excerpt_fr': 'Découvrez comment combiner vinaigres, sauces piquantes et pâtes de câpres dans un seul conteneur mixte FCL optimise les coûts.',
            'excerpt_ar': 'اكتشف كيف يؤدي دمج الخل والصلصات الحارة ومعجون الكبار في حاوية FCL واحدة إلى تحسين أسعار الشحن.',
            'excerpt_es': 'Descubra cómo combinar vinagres, salsas picantes y pastas de alcaparras en un solo contenedor mixto FCL optimiza los costos.',
            'excerpt_it': 'Scopri come combinare aceti, salse piccanti e paté di capperi in un unico container FCL ottimizza le tariffe.',
            'content_en': 'Mixed container load shipping is the ultimate strategy for international B2B food buyers. By shipping multiple product categories (such as biological wine vinegars, retail PET white vinegars, hot chili sauces, and gourmet tapenade pastes) in a single FCL pallet shipment, commercial brokers minimize inventory storage costs, maximize local distribution turns, and benefit from unified customs clearances at European, UK, and USA ports.',
            'is_published': True,
        },
        {
            'title_en': 'Acidity Standards in Industrial Vinegar Production: BRC vs FDA',
            'title_fr': 'Normes d\'acidité dans la production industrielle de vinaigre : BRC vs FDA',
            'title_ar': 'معايير الحموضة في إنتاج الخل الصناعي: BRC مقابل FDA',
            'title_es': 'Normas de acidez en la producción industrial de vinagre: BRC vs FDA',
            'title_it': 'Standard di acidità nella produzione industriale di aceto: BRC vs FDA',
            'excerpt_en': 'An in-depth chemical and regulatory review of commercial acidity thresholds required by European IFS and US FDA import systems.',
            'excerpt_fr': 'Une revue chimique et réglementaire approfondie des seuils d\'acidité requis par les systèmes d\'importation européens.',
            'excerpt_ar': 'مراجعة كيميائية وتنظيمية متعمقة لعتبات الحموضة التجارية المطلوبة بموجب أنظمة الاستيراد.',
            'excerpt_es': 'Una revisión química y regulatoria de los umbrales de acidez comercial requeridos por los sistemas de importación.',
            'excerpt_it': 'Un\'analisi chimica e normativa approfondita sulle soglie di acidità commerciali richieste per l\'importazione.',
            'content_en': 'Biological vinegars require exact acetic acid concentrations. Our laboratories perform automated titrations to calibrate constant 6% and 8% profiles. This post reviews how safety frameworks like the British Retail Consortium (BRC GS) and the United States Food and Drug Administration (FDA) verify biological acidity, plant sanitation, and stainless fermentation tanks to secure clean food clearances.',
            'is_published': True,
        }
    ]

    for post in posts_data:
        obj, created = BlogPost.objects.get_or_create(
            title_en=post['title_en'],
            defaults={
                'title_fr': post.get('title_fr', ''),
                'title_ar': post.get('title_ar', ''),
                'title_es': post.get('title_es', ''),
                'title_it': post.get('title_it', ''),
                'excerpt_en': post.get('excerpt_en', ''),
                'excerpt_fr': post.get('excerpt_fr', ''),
                'excerpt_ar': post.get('excerpt_ar', ''),
                'excerpt_es': post.get('excerpt_es', ''),
                'excerpt_it': post.get('excerpt_it', ''),
                'content_en': post.get('content_en', ''),
                'is_published': post.get('is_published', True),
            }
        )
        if created:
            print(f"[OK] Created Blog Post: {post['title_en']}")

    print("[OK] Database population finished successfully!")

if __name__ == '__main__':
    populate()
