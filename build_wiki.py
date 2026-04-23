
"""
Build the complete HTML wiki for seniors-recipes.
Generates:
  wiki/index.html          — category grid index
  wiki/recipes/<id>.html   — one page per recipe
"""
import os, sys
sys.path.insert(0, "/sessions/relaxed-funny-mayer")
from recipes_data import RECIPES, CATEGORIES

WIKI = "/sessions/relaxed-funny-mayer/wiki"
RECIPES_DIR = f"{WIKI}/recipes"
os.makedirs(RECIPES_DIR, exist_ok=True)

# ── colour scheme per category ───────────────────────────────────────────────
CAT_COLORS = {
    "One-Pan Dinners":                          {"bg":"#FFF4EC","accent":"#E67E22","badge":"#F39C12"},
    "Minimal Cooking High-Protein & High-Fibre":{"bg":"#F0FBF4","accent":"#27AE60","badge":"#1E8449"},
    "Simple Tofu Recipes":                      {"bg":"#FDF3FF","accent":"#8E44AD","badge":"#9B59B6"},
    "No-Cook Healthy Snack Plates":             {"bg":"#EBF5FB","accent":"#2874A6","badge":"#3498DB"},
    "Quick Grocery-Hack Meals":                 {"bg":"#FDFAF0","accent":"#D4A017","badge":"#F1C40F"},
}

CATEGORY_ICONS = {
    "One-Pan Dinners": "🍳",
    "Minimal Cooking High-Protein & High-Fibre": "💪",
    "Simple Tofu Recipes": "🌿",
    "No-Cook Healthy Snack Plates": "🥗",
    "Quick Grocery-Hack Meals": "⚡",
}

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --font: 'Segoe UI', Arial, sans-serif;
  --text: #2C3E50;
  --muted: #7F8C8D;
  --border: #E8EAED;
  --radius: 12px;
  --shadow: 0 2px 12px rgba(0,0,0,.08);
}
body { font-family: var(--font); color: var(--text); background: #FAFAFA; min-height: 100vh; }
a { color: inherit; text-decoration: none; }
header {
  background: #2C3E50;
  color: white;
  padding: 28px 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}
header .logo { font-size: 2rem; }
header h1 { font-size: 1.6rem; font-weight: 700; letter-spacing: -.5px; }
header p { font-size: .9rem; opacity: .75; margin-top: 2px; }
nav.breadcrumb {
  background: white;
  border-bottom: 1px solid var(--border);
  padding: 12px 32px;
  font-size: .85rem;
  color: var(--muted);
}
nav.breadcrumb a { color: #2874A6; }
nav.breadcrumb a:hover { text-decoration: underline; }
.container { max-width: 1100px; margin: 0 auto; padding: 32px 24px; }
/* index */
.cat-section { margin-bottom: 48px; }
.cat-title {
  font-size: 1.25rem; font-weight: 700;
  margin-bottom: 18px;
  padding: 10px 18px;
  border-radius: var(--radius);
  display: flex; align-items: center; gap: 10px;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 18px;
}
.card {
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: transform .18s, box-shadow .18s;
  cursor: pointer;
}
.card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,.13); }
.card img { width: 100%; height: 150px; object-fit: cover; display: block; }
.card-body { padding: 14px 16px 16px; }
.card-body h3 { font-size: .95rem; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }
.card-body p { font-size: .8rem; color: var(--muted); line-height: 1.45; }
.badge {
  display: inline-block;
  font-size: .7rem; font-weight: 700;
  padding: 3px 9px;
  border-radius: 20px;
  margin-bottom: 8px;
  color: white;
}
/* recipe page */
.recipe-hero { position: relative; border-radius: var(--radius); overflow: hidden; margin-bottom: 32px; box-shadow: var(--shadow); }
.recipe-hero img { width: 100%; max-height: 380px; object-fit: cover; display: block; }
.recipe-hero .overlay {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 24px 28px;
  background: linear-gradient(transparent, rgba(0,0,0,.65));
  color: white;
}
.recipe-hero .overlay h1 { font-size: 1.8rem; font-weight: 800; }
.recipe-hero .overlay .cat { font-size: .85rem; opacity: .85; margin-top: 4px; }
.recipe-meta {
  display: flex; gap: 24px; flex-wrap: wrap;
  margin-bottom: 32px;
}
.meta-box {
  background: white;
  border-radius: var(--radius);
  padding: 16px 22px;
  box-shadow: var(--shadow);
  flex: 1;
  min-width: 120px;
  text-align: center;
}
.meta-box .num { font-size: 1.5rem; font-weight: 800; }
.meta-box .lbl { font-size: .75rem; color: var(--muted); margin-top: 2px; text-transform: uppercase; letter-spacing: .5px; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px; }
@media (max-width: 650px) { .two-col { grid-template-columns: 1fr; } .recipe-meta { gap: 12px; } }
.section-card {
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 24px;
}
.section-card h2 {
  font-size: 1.1rem; font-weight: 700;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--border);
  display: flex; align-items: center; gap: 8px;
}
.section-card ul, .section-card ol { padding-left: 22px; }
.section-card li { margin-bottom: 8px; font-size: .92rem; line-height: 1.55; }
.section-card ol li { padding-left: 4px; }
.nutrient-grid {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;
  margin-bottom: 32px;
}
@media (max-width: 600px) { .nutrient-grid { grid-template-columns: repeat(3, 1fr); } }
.nut-box {
  background: white;
  border-radius: var(--radius);
  padding: 16px 12px;
  text-align: center;
  box-shadow: var(--shadow);
}
.nut-box .val { font-size: 1.4rem; font-weight: 800; }
.nut-box .unit { font-size: .7rem; color: var(--muted); }
.nut-box .name { font-size: .72rem; color: var(--muted); margin-top: 3px; text-transform: uppercase; letter-spacing: .4px; }
.back-link {
  display: inline-flex; align-items: center; gap: 6px;
  color: #2874A6; font-size: .9rem; font-weight: 600;
  margin-bottom: 24px;
}
.back-link:hover { text-decoration: underline; }
footer {
  background: #2C3E50; color: rgba(255,255,255,.6);
  text-align: center; padding: 20px;
  font-size: .8rem; margin-top: 60px;
}
"""

HEAD = lambda title, extra_css="": f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Seniors Recipes</title>
<style>{CSS}{extra_css}</style>
</head>
<body>
<header>
  <span class="logo">🍽️</span>
  <div>
    <h1>Seniors Recipes</h1>
    <p>Simple · Healthy · One-person meals for ages 75+</p>
  </div>
</header>"""

FOOT = """<footer>
  <p>Seniors Recipes Wiki · Simple, healthy meals for ages 75+ · High protein · High fibre · Minimal processing</p>
</footer>
</body></html>"""

# ── index.html ───────────────────────────────────────────────────────────────
def build_index():
    html = HEAD("Home")
    html += '<nav class="breadcrumb">🏠 Home</nav>\n'
    html += '<div class="container">\n'
    html += f'<p style="font-size:.95rem;color:#555;margin-bottom:32px;">A collection of <strong>{len(RECIPES)} recipes</strong> organised into {len(CATEGORIES)} categories. Each recipe includes metric ingredients, step-by-step instructions, and nutrient estimates.</p>\n'

    for cat in CATEGORIES:
        cols = CAT_COLORS.get(cat, {"bg":"#F8F9FA","accent":"#555","badge":"#888"})
        icon = CATEGORY_ICONS.get(cat,"🍴")
        cat_recipes = [r for r in RECIPES if r["category"] == cat]
        html += f'<section class="cat-section">\n'
        html += f'<div class="cat-title" style="background:{cols["bg"]};color:{cols["accent"]}">'
        html += f'<span>{icon}</span><span>{cat}</span>'
        html += f'<span style="margin-left:auto;font-size:.8rem;color:{cols["muted"] if "muted" in cols else cols["accent"]}80">{len(cat_recipes)} recipes</span>'
        html += '</div>\n'
        html += '<div class="card-grid">\n'
        for r in cat_recipes:
            html += f'''<a href="recipes/{r["id"]}.html" class="card">
  <img src="images/{r["id"]}.jpg" alt="{r["title"]}" loading="lazy">
  <div class="card-body">
    <span class="badge" style="background:{cols["badge"]}">{cat[:18]}</span>
    <h3>{r["title"]}</h3>
    <p>{r["description"][:80]}{"…" if len(r["description"])>80 else ""}</p>
  </div>
</a>\n'''
        html += '</div>\n</section>\n'

    html += '</div>\n' + FOOT
    with open(f"{WIKI}/index.html", "w") as f:
        f.write(html)
    print("✓ index.html")

# ── recipe pages ─────────────────────────────────────────────────────────────
def build_recipe(r):
    cols  = CAT_COLORS.get(r["category"], {"bg":"#F8F9FA","accent":"#555","badge":"#888"})
    icon  = CATEGORY_ICONS.get(r["category"],"🍴")
    n     = r["nutrients"]

    html  = HEAD(r["title"])
    html += f'<nav class="breadcrumb"><a href="../index.html">🏠 Home</a> › {r["category"]} › {r["title"]}</nav>\n'
    html += '<div class="container">\n'
    html += f'<a href="../index.html" class="back-link">← Back to all recipes</a>\n'

    # Hero
    html += f'''<div class="recipe-hero">
  <img src="../images/{r["id"]}.jpg" alt="{r["title"]}">
  <div class="overlay">
    <h1>{r["title"]}</h1>
    <div class="cat">{icon} {r["category"]}</div>
  </div>
</div>\n'''

    # Meta boxes
    html += '<div class="recipe-meta">\n'
    for val, lbl in [
        (r["servings"], "Serving"),
        (f'{n["calories"]} kcal', "Energy"),
        (f'{n["protein_g"]} g', "Protein"),
        (f'{n["fibre_g"]} g', "Fibre"),
    ]:
        html += f'<div class="meta-box"><div class="num">{val}</div><div class="lbl">{lbl}</div></div>\n'
    html += '</div>\n'

    # Description
    html += f'<p style="font-size:1.02rem;line-height:1.65;margin-bottom:28px;color:#444;">{r["description"]}</p>\n'

    # Ingredients + Steps
    html += '<div class="two-col">\n'

    # Ingredients
    html += '<div class="section-card">\n'
    html += f'<h2>🛒 Ingredients <span style="font-size:.8rem;font-weight:400;color:#999">per serving</span></h2>\n<ul>\n'
    for ing in r["ingredients"]:
        html += f'<li>{ing}</li>\n'
    html += '</ul>\n</div>\n'

    # Steps
    html += '<div class="section-card">\n'
    html += '<h2>👨‍🍳 Instructions</h2>\n<ol>\n'
    for step in r["steps"]:
        html += f'<li>{step}</li>\n'
    html += '</ol>\n</div>\n'

    html += '</div>\n'  # end two-col

    # Nutrition
    html += '<div class="section-card" style="margin-bottom:32px;">\n'
    html += '<h2>📊 Estimated Nutrients <span style="font-size:.8rem;font-weight:400;color:#999">per serving</span></h2>\n'
    html += '<div class="nutrient-grid" style="margin-top:16px;margin-bottom:0;">\n'
    nut_colors = {
        "calories": cols["accent"],
        "protein_g": "#27AE60",
        "carbs_g": "#E67E22",
        "fat_g": "#8E44AD",
        "fibre_g": "#2874A6",
    }
    nut_names = {
        "calories": ("Calories","kcal"),
        "protein_g": ("Protein","g"),
        "carbs_g": ("Carbohydrates","g"),
        "fat_g": ("Total Fat","g"),
        "fibre_g": ("Dietary Fibre","g"),
    }
    for key, (name, unit) in nut_names.items():
        color = nut_colors.get(key, cols["accent"])
        html += f'''<div class="nut-box">
  <div class="val" style="color:{color}">{n[key]}</div>
  <div class="unit">{unit}</div>
  <div class="name">{name}</div>
</div>\n'''
    html += '</div>\n</div>\n'  # end nutrient section-card

    # Tip box
    tips = {
        "One-Pan Dinners": "💡 <strong>Tip:</strong> Line the baking tray with foil or baking paper for easy cleanup.",
        "Minimal Cooking High-Protein & High-Fibre": "💡 <strong>Tip:</strong> Keep canned beans and lentils in your pantry for a quick protein boost any day.",
        "Simple Tofu Recipes": "💡 <strong>Tip:</strong> Pat tofu dry before cooking to achieve a better texture and golden colour.",
        "No-Cook Healthy Snack Plates": "💡 <strong>Tip:</strong> Assemble on a large plate or board and eat straight away — no cooking needed.",
        "Quick Grocery-Hack Meals": "💡 <strong>Tip:</strong> Buy pre-cooked rotisserie chicken or deli meat to keep assembly time under 5 minutes.",
    }
    tip = tips.get(r["category"],"")
    if tip:
        html += f'<div style="background:{cols["bg"]};border-left:4px solid {cols["accent"]};padding:14px 18px;border-radius:0 8px 8px 0;margin-bottom:32px;font-size:.9rem;line-height:1.6;">{tip}</div>\n'

    # Related recipes (same category, up to 3)
    siblings = [x for x in RECIPES if x["category"] == r["category"] and x["id"] != r["id"]][:3]
    if siblings:
        html += '<div class="section-card">\n'
        html += f'<h2>🔗 More {r["category"]}</h2>\n'
        html += '<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:12px;">\n'
        for s in siblings:
            html += f'<a href="{s["id"]}.html" style="display:flex;align-items:center;gap:10px;background:#F8F9FA;border-radius:8px;padding:10px 14px;font-size:.88rem;font-weight:600;flex:1;min-width:160px;transition:background .15s;" onmouseover="this.style.background=\'#EEF\'" onmouseout="this.style.background=\'#F8F9FA\'">'
            html += f'<img src="../images/{s["id"]}.jpg" alt="" style="width:44px;height:44px;border-radius:6px;object-fit:cover;">'
            html += f'<span>{s["title"]}</span></a>\n'
        html += '</div>\n</div>\n'

    html += '</div>\n' + FOOT

    with open(f"{RECIPES_DIR}/{r['id']}.html","w") as f:
        f.write(html)

def main():
    build_index()
    for i, r in enumerate(RECIPES):
        build_recipe(r)
        print(f"  [{i+1}/{len(RECIPES)}] {r['id']}.html")
    print(f"\n✓ Wiki built: {len(RECIPES)+1} HTML files")

if __name__ == "__main__":
    main()
