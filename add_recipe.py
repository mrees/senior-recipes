
#!/usr/bin/env python3
"""
add_recipe.py — Update skill for seniors-recipes wiki
======================================================
Usage:
  python3 add_recipe.py

This script prompts you for a new recipe, generates an illustrative
image, creates a recipe HTML page, and rebuilds the index.

After running, commit and push to GitHub:
  git add .
  git commit -m "Add recipe: <name>"
  git push

The GitHub Actions workflow will then deploy the updated wiki automatically.
"""

import os, sys, textwrap

# ── make sure we can import from the wiki directory ──────────────────────────
WIKI_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WIKI_DIR)
sys.path.insert(0, os.path.dirname(WIKI_DIR))   # parent, for generate_images if needed

RECIPES_DATA = os.path.join(WIKI_DIR, "recipes_data.py")

def slugify(text):
    import re
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def prompt(label, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"\n{label}{suffix}: ").strip()
    return val if val else default

def prompt_list(label):
    print(f"\n{label} (enter one per line, blank line to finish):")
    items = []
    while True:
        line = input("  > ").strip()
        if not line:
            break
        items.append(line)
    return items

def prompt_int(label, default):
    raw = input(f"\n{label} [{default}]: ").strip()
    try:
        return int(raw)
    except:
        return default

# ── categories ───────────────────────────────────────────────────────────────
CATEGORIES = [
    "One-Pan Dinners",
    "Minimal Cooking High-Protein & High-Fibre",
    "Simple Tofu Recipes",
    "No-Cook Healthy Snack Plates",
    "Quick Grocery-Hack Meals",
]

def pick_category():
    print("\nCategory:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"  {i}. {c}")
    print(f"  {len(CATEGORIES)+1}. New category (type name)")
    choice = input("  Choose [1–{}]: ".format(len(CATEGORIES)+1)).strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(CATEGORIES):
            return CATEGORIES[idx]
    except:
        pass
    return input("  New category name: ").strip()

# ── generate a simple illustrative image ─────────────────────────────────────
def make_placeholder_image(recipe_id, title, category):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("  [!] Pillow not installed. Skipping image generation.")
        return

    CAT_COLORS = {
        "One-Pan Dinners":                           ("#E67E22","#FFF4EC"),
        "Minimal Cooking High-Protein & High-Fibre": ("#27AE60","#F0FBF4"),
        "Simple Tofu Recipes":                       ("#8E44AD","#FDF3FF"),
        "No-Cook Healthy Snack Plates":              ("#2874A6","#EBF5FB"),
        "Quick Grocery-Hack Meals":                  ("#D4A017","#FDFAF0"),
    }
    accent, bg_hex = CAT_COLORS.get(category, ("#555555","#F8F8F8"))

    def hex_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2],16) for i in (0,2,4))

    W, H = 800, 480
    img = Image.new("RGB", (W, H), hex_rgb(bg_hex))
    d = ImageDraw.Draw(img)

    # Gradient
    c1 = hex_rgb(bg_hex)
    c2 = tuple(max(0, x-30) for x in c1)
    for y in range(H):
        t = y / H
        row = tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))
        d.line([(0,y),(W,y)], fill=row)

    # Decorative plate
    ac = hex_rgb(accent)
    ac_light = tuple(min(255, int(x*1.4)) for x in ac)
    d.ellipse([200, 80, 600, 400], fill=(255,255,255,200))
    d.ellipse([220, 95, 580, 385], fill=ac_light)

    # Label strip
    d.rectangle([0, H-90, W, H], fill=ac)

    try:
        font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    except:
        font_b = font = ImageFont.load_default()

    # Wrap title
    lines = textwrap.wrap(title, width=36)
    y_start = H - 80 + (80 - len(lines)*36)//2
    for line in lines:
        d.text((W//2, y_start), line, font=font_b, fill="white", anchor="mm")
        y_start += 36

    d.text((W//2, 58), category, font=font, fill=ac, anchor="mm")

    out = os.path.join(WIKI_DIR, "images", f"{recipe_id}.jpg")
    img.save(out, "JPEG", quality=90)
    print(f"  ✓ Image saved: images/{recipe_id}.jpg")

# ── append to recipes_data.py ────────────────────────────────────────────────
RECIPE_TEMPLATE = """
    {{
        "id": "{id}",
        "title": "{title}",
        "category": "{category}",
        "description": "{description}",
        "servings": {servings},
        "ingredients": {ingredients},
        "steps": {steps},
        "nutrients": {nutrients},
    }},
"""

def append_recipe_to_data(recipe):
    """Append new recipe dict to recipes_data.py"""
    import ast, re
    with open(RECIPES_DATA, "r") as f:
        src = f.read()

    # Find the closing bracket of the RECIPES list
    # We insert before the last ] in the file
    idx = src.rfind("]")
    if idx == -1:
        print("  [!] Could not find RECIPES list end. Please add recipe manually.")
        return

    # Build the entry string
    entry = (
        "\n    {\n"
        f'        "id": {repr(recipe["id"])},\n'
        f'        "title": {repr(recipe["title"])},\n'
        f'        "category": {repr(recipe["category"])},\n'
        f'        "description": {repr(recipe["description"])},\n'
        f'        "servings": {recipe["servings"]},\n'
        f'        "ingredients": {repr(recipe["ingredients"])},\n'
        f'        "steps": {repr(recipe["steps"])},\n'
        f'        "nutrients": {repr(recipe["nutrients"])},\n'
        "    },\n"
    )

    new_src = src[:idx] + entry + src[idx:]
    with open(RECIPES_DATA, "w") as f:
        f.write(new_src)
    print(f"  ✓ Recipe appended to recipes_data.py")

# ── generate the HTML page ───────────────────────────────────────────────────
def build_recipe_page(recipe):
    """Import build_wiki and generate the recipe page."""
    # Temporarily patch recipes_data to include our new recipe
    try:
        import importlib
        sys.path.insert(0, WIKI_DIR)
        import recipes_data as rd
        importlib.reload(rd)

        # Also reload build_wiki
        build_wiki_path = os.path.join(WIKI_DIR, "..", "build_wiki.py")
        if not os.path.exists(build_wiki_path):
            build_wiki_path = os.path.join(WIKI_DIR, "build_wiki.py")

        import importlib.util
        spec = importlib.util.spec_from_file_location("build_wiki",
            os.path.join(os.path.dirname(WIKI_DIR), "build_wiki.py"))
        bw = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bw)

        # Find the new recipe in the freshly loaded data
        r = next((x for x in bw.RECIPES if x["id"] == recipe["id"]), None)
        if r:
            bw.build_recipe(r)
            print(f"  ✓ Recipe page: recipes/{recipe['id']}.html")
        else:
            print("  [!] Recipe not found in reloaded data. Run build_wiki.py manually.")

        # Rebuild index
        bw.build_index()
        print("  ✓ index.html rebuilt")

    except Exception as e:
        print(f"  [!] Could not auto-build HTML: {e}")
        print("       Run:  python3 build_wiki.py")

# ── main ─────────────────────────────────────────────────────────────────────
def main():
    print("\n╔══════════════════════════════════════════╗")
    print("║   Seniors Recipes — Add New Recipe       ║")
    print("╚══════════════════════════════════════════╝")

    title    = prompt("Recipe title")
    if not title:
        print("Title is required. Exiting."); return

    rid      = prompt("Recipe ID (slug)", slugify(title))
    category = pick_category()
    desc     = prompt("One-line description")
    servings = prompt_int("Servings per recipe", 1)

    print("\nIngredients (metric quantities):")
    ingredients = prompt_list("Enter ingredients")

    print("\nInstructions:")
    steps = prompt_list("Enter steps")

    print("\nEstimated nutrients per serving:")
    calories   = prompt_int("  Calories (kcal)", 400)
    protein    = prompt_int("  Protein (g)", 20)
    carbs      = prompt_int("  Carbohydrates (g)", 40)
    fat        = prompt_int("  Total Fat (g)", 15)
    fibre      = prompt_int("  Dietary Fibre (g)", 5)

    recipe = {
        "id": rid,
        "title": title,
        "category": category,
        "description": desc,
        "servings": servings,
        "ingredients": ingredients,
        "steps": steps,
        "nutrients": {
            "calories": calories,
            "protein_g": protein,
            "carbs_g": carbs,
            "fat_g": fat,
            "fibre_g": fibre,
        },
    }

    print(f"\n── Summary ──────────────────────────")
    print(f"  Title   : {title}")
    print(f"  ID      : {rid}")
    print(f"  Category: {category}")
    print(f"  Servings: {servings}")
    print(f"  Ingredients: {len(ingredients)}")
    print(f"  Steps   : {len(steps)}")
    confirm = input("\nProceed? [Y/n]: ").strip().lower()
    if confirm == 'n':
        print("Cancelled."); return

    print("\nBuilding…")
    make_placeholder_image(rid, title, category)
    append_recipe_to_data(recipe)
    build_recipe_page(recipe)

    print(f"""
✅ Done! New recipe added: {title}

Next steps:
  1. Optionally replace images/{rid}.jpg with your own photo.
  2. Commit and push:
       cd /path/to/senior-recipes
       git add .
       git commit -m "Add recipe: {title}"
       git push
  3. GitHub Pages will deploy automatically in ~30 seconds.
""")

if __name__ == "__main__":
    main()
