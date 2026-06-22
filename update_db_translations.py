import os
import django
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinaigre_project.settings')
django.setup()

from core.models import Product

def run():
    print("Starting product translations database update...")
    
    # Mapping from old French name_en to new English name_en
    MAPPING = {
        "Vinaigre blond d’alcool": "Blond Alcohol Vinegar",
        "Vinaigre blond d'alcool": "Blond Alcohol Vinegar",
        "Vinaigre de vin rouge": "Red Wine Vinegar",
        "Vinaigre de vin blanc": "White Wine Vinegar",
        "Vinaigre aromatisé pomme": "Apple Aromatic Vinegar",
        "Vinaigre aromatisé citron": "Lemon Aromatic Vinegar",
        "Vinaigre de cidre": "Apple Cider Vinegar",
        "Vinaigre coloré": "Caramel Colored Vinegar",
        "Cornichon de citron": "Lemon Pickled Gherkins",
        "Pâte de piment fort": "Hot Pepper Paste",
        "Pâte de câpre": "Caper Paste",
    }
    
    updated_count = 0
    
    for product in Product.objects.all():
        old_name = product.name_en
        if old_name in MAPPING:
            new_name = MAPPING[old_name]
            new_slug = slugify(new_name)
            print(f"Updating Product ID {product.id}:")
            print(f"  Name: '{old_name}' -> '{new_name}'")
            print(f"  Slug: '{product.slug}' -> '{new_slug}'")
            
            product.name_en = new_name
            product.slug = new_slug
            product.save()
            updated_count += 1
        else:
            # Check for case-insensitive match or fuzzy match just in case
            matched = False
            for old_key, new_val in MAPPING.items():
                if old_name.lower().replace("'", "").replace("’", "") == old_key.lower().replace("'", "").replace("’", ""):
                    new_slug = slugify(new_val)
                    print(f"Updating Product ID {product.id} (Fuzzy Match):")
                    print(f"  Name: '{old_name}' -> '{new_val}'")
                    print(f"  Slug: '{product.slug}' -> '{new_slug}'")
                    product.name_en = new_val
                    product.slug = new_slug
                    product.save()
                    updated_count += 1
                    matched = True
                    break
            if not matched:
                print(f"Skipping Product ID {product.id}: '{old_name}' (No mapping found)")

    print(f"Database update completed. {updated_count} products updated successfully!")

if __name__ == '__main__':
    run()
