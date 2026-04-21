"""
generate_product_catalog.py
Generates a 500-record product catalogue JSON file for the Semantic Search exercise.
Descriptions are rich prose so ELSER's semantic matching visibly outperforms BM25.

Usage:
    python3 generate_product_catalog.py
Output:
    product-catalog.json  (same directory)
"""

import json, random, pathlib

random.seed(42)

CATEGORIES = {
    "footwear": [
        ("TrailMax Hiking Boot",
         "Waterproof full-grain leather hiking boot featuring a Vibram Megagrip outsole for exceptional traction on wet and dry surfaces. "
         "The asymmetric lacing system locks the heel securely, reducing fatigue on technical descents. "
         "A Gore-Tex Extended Comfort membrane keeps feet dry in stream crossings while remaining breathable during long climbs. "
         "Reinforced toe cap and heel counter protect against rock strikes. Ideal for multi-day alpine treks."),
        ("CloudStride Running Shoe",
         "Ultra-lightweight road running shoe built around a dual-density foam midsole that delivers responsive cushioning without sacrificing energy return. "
         "The engineered mesh upper wraps the midfoot for a sock-like fit, and the flared heel geometry promotes a natural heel-to-toe transition. "
         "Reflective details on the collar ensure visibility during pre-dawn or evening runs. "
         "Suitable for neutral to mild overpronators logging 30–60 miles per week."),
        ("Summit Approach Shoe",
         "Versatile approach shoe bridging the gap between hiking boot and climbing slipper. "
         "A sticky rubber rand extends up the toe for edging on rock, while the lugged outsole handles loose trail with confidence. "
         "The low-cut collar keeps the shoe light and packable. Internal heel webbing acts as a heel hook when scrambling. "
         "Popular with alpinists, via ferrata enthusiasts, and canyon hikers."),
        ("ArcticPace Insulated Boot",
         "Heavily insulated winter boot rated to -40 °C with a removable 10 mm Thinsulate liner that can be dried separately. "
         "The rubber shell is 100 % waterproof and resistant to fuel and oil, making it suitable for polar expeditions and industrial cold-storage environments. "
         "An EVA midsole provides thermal break between foot and frozen ground. "
         "Steel shank maintains structure when kicking steps in hard snow."),
        ("Mesa Trail Runner",
         "Purpose-built desert trail runner with an open-cell foam collar that drains water quickly after creek crossings. "
         "The gaiter attachment ring at the heel accommodates optional gaiters to keep sand and debris out. "
         "A rock plate between the midsole layers shields the forefoot on rocky singletrack without adding perceptible rigidity. "
         "Available in wide widths for runners with broader forefoot profiles."),
    ],
    "apparel": [
        ("Merino Base Layer Top",
         "190 gsm 100 % Merino wool long-sleeve base layer that regulates body temperature across a wide range of activity levels. "
         "Merino's natural crimp creates millions of tiny air pockets that trap heat when stationary and wick moisture when active. "
         "The fabric is naturally odour-resistant, allowing multi-day wear without laundering on expedition. "
         "Flatlock seams eliminate chafing under a harness or pack straps."),
        ("Hardshell Storm Jacket",
         "3-layer Gore-Tex Pro hardshell designed for sustained exposure to wind and precipitation in mountainous terrain. "
         "The helmet-compatible hood adjusts with one hand and features a laminated brim that holds shape in high winds. "
         "Pit-zip vents dump heat rapidly during aerobic ascents. "
         "All seams are fully taped and the YKK AquaGuard zips are rated to 15 minutes of sustained rain ingress testing. "
         "Packs into its own chest pocket."),
        ("Fleece Midlayer Pullover",
         "100 gsm grid-fleece midlayer with an open-face grid construction that increases breathability by 40 % compared to flat fleece. "
         "Offset shoulder seams prevent pressure points under pack straps. "
         "The half-zip collar opens for ventilation and closes high to warm the neck without a balaclava. "
         "Trim fit designed to layer under a shell without bunching."),
        ("Lightweight Down Vest",
         "Ethically sourced 800-fill-power down vest with a recycled ripstop nylon shell treated with a fluorine-free DWR finish. "
         "Internal baffles prevent cold spots and maintain loft across the torso without restricting arm movement. "
         "Packs into its own left-hand pocket for easy stowage in a day pack. "
         "Designed for belay stations, camp mornings, and urban commutes in cool weather."),
        ("Sun-Protective Hiking Shirt",
         "UPF 50+ nylon-elastane shirt with four-way stretch for unrestricted movement on trail and scrambles. "
         "The vented back panel with laser-cut perforations increases airflow to the high-sweat zone between the shoulder blades. "
         "Roll-up sleeve tabs convert the long-sleeve to a short-sleeve in seconds. "
         "Chest pocket with a key clip doubles as a phone pocket. Wrinkle-resistant for travel days."),
    ],
    "electronics": [
        ("GPS Multisport Watch",
         "Multi-band GNSS watch acquiring satellite fixes 3× faster than single-band equivalents in urban canyons and dense canopy. "
         "Built-in topographic maps cover 170 countries with automatic rerouting when off-trail. "
         "Tracks pace, heart rate, SpO2, and body battery energy reserve. "
         "Solar charging lens extends battery life to 46 days in smartwatch mode. "
         "Rated to 10 ATM for open-water swimming and watersports."),
        ("Action Camera 4K",
         "Ruggedised 4K/120fps action camera with a wide dynamic range sensor that retains highlight detail in high-contrast alpine lighting. "
         "HyperSmooth 6.0 electronic image stabilisation eliminates shake on mountain bike descents and ski runs. "
         "Waterproof to 10 m without a case. Voice commands allow hands-free operation with gloves. "
         "TimeWarp hyperlapse captures long hikes as short cinematic sequences."),
        ("Solar Power Bank",
         "26,800 mAh dual-panel solar power bank with a 20 W USB-C PD port for fast-charging laptops in the field. "
         "The monocrystalline panels charge the internal battery at 1 W per hour in direct noon sun, serving as a top-up source between resupply points. "
         "An integrated LED flashlight with SOS strobe doubles as an emergency signalling device. "
         "Rugged TPU shell is drop-rated to 1.5 m and water-resistant to IPX6."),
        ("Personal Locator Beacon",
         "406 MHz PLB with integrated GPS that transmits your precise coordinates to the COSPAS-SARSAT search-and-rescue satellite network when activated. "
         "Battery life of 7 years in standby, with a guaranteed 24-hour transmit time after activation. "
         "Registration is free and requires only an online form. "
         "No subscription required — unlike satellite communicators, the emergency channel is free to use globally. "
         "Approved for use in 209 countries."),
        ("Satellite Communicator",
         "Two-way satellite messenger with 100 % global Iridium coverage for text messaging, weather forecasts, and track sharing outside cellular range. "
         "The SOS button connects to the GEOS 24/7 emergency response centre within 60 seconds. "
         "Groups of up to 10 users can share real-time location on the companion app without a data plan. "
         "Rechargeable lithium battery provides 100 hours of 10-minute tracking intervals."),
    ],
    "camping": [
        ("3-Season Backpacking Tent",
         "Freestanding double-wall tent with a semi-geodesic pole architecture that sheds wind loads up to 60 mph. "
         "The inner mesh body maximises ventilation on warm nights while the footprint-integrated fly seals out rain and condensation. "
         "Two vestibules provide 12 square feet of gear storage to keep boots and packs dry. "
         "Colour-coded poles and clips allow solo set-up in under five minutes even in fading light."),
        ("Down Sleeping Bag -10 °C",
         "750-fill-power hydrophobic down sleeping bag rated to -10 °C using the EN 13537 standard. "
         "The hydrophobic treatment maintains 95 % of loft after soaking, critical in humid or wet conditions. "
         "A trapezoidal footbox prevents compressed down at the feet — the most common source of heat loss. "
         "Snag-free draft collar and internal draft tube seal the full-length zip against cold ingress."),
        ("Titanium Cookset",
         "Ultralight 3-piece titanium cookset — 900 ml pot, 550 ml cup, and lid that doubles as a frying pan. "
         "Titanium's superior strength-to-weight ratio results in a combined weight of 148 g without compromising durability. "
         "The hard-anodised interior resists scratching from metal utensils and cleans easily even without soap. "
         "Foldable handles with silicone grip inserts provide control at altitude where fine motor skills can be impaired."),
        ("Hammock with Straps",
         "Lightweight 190T ripstop nylon hammock rated to 200 kg with a continuous-loop suspension system using 1-inch polyester tree straps rated to 800 kg. "
         "The asymmetric lay allows a flat sleeping position without back strain during longer naps or overnight use. "
         "Integrated bug net zips from inside to keep insects out. Sets up between trees 3–5 m apart. Weighs 680 g complete."),
        ("Water Filter Straw",
         "Hollow-fibre membrane filter removing 99.9999 % of bacteria, 99.9 % of protozoa, and 99.999 % of microplastics down to 0.2 microns. "
         "Flow rate of 1 litre per minute with no pumping — gravity and suction do the work. "
         "Backflushes in seconds by blowing through the mouthpiece. "
         "Filter lifespan of 4,000 litres, verified by US EPA independent testing. Weighs 57 g."),
    ],
    "nutrition": [
        ("Endurance Gel 40 g",
         "Isotonic energy gel containing 25 g of fast-acting carbohydrates from a 2:1 maltodextrin-fructose ratio, optimising absorption across dual intestinal transporters. "
         "200 mg of sodium replaces electrolytes lost in high-sweat conditions. "
         "Caffeine-free formulation allows use at any point during a race without disrupting sleep strategy in multi-stage events. "
         "No water required — the isotonic formula is absorbed without additional fluid."),
        ("Protein Recovery Bar",
         "Post-exercise recovery bar with 20 g of whey protein isolate, 40 g of carbohydrates, and 500 mg of leucine to initiate muscle protein synthesis. "
         "Sweetened only with dates and honey — no artificial sweeteners or sugar alcohols that cause GI distress at altitude. "
         "Made in a gluten-free facility. "
         "The 2:1 carbohydrate-to-protein ratio matches research-backed recommendations for glycogen resynthesis within the 30-minute anabolic window."),
        ("Freeze-Dried Meal 550 kcal",
         "Backpacking meal freeze-dried at peak nutritional value, retaining 97 % of vitamins compared to conventional dehydration methods. "
         "Rehydrates in 8–10 minutes with boiling water directly in the pouch. "
         "550 kcal per serving supports a 3-hour sustained activity output. "
         "Flavours developed with professional alpinists and tested at 6,000 m elevation where taste perception is diminished. "
         "Packaging is recyclable through specialist soft-plastics programmes."),
        ("Electrolyte Tablets",
         "Effervescent electrolyte tablet with a complete spectrum of sodium (300 mg), potassium (100 mg), magnesium (25 mg), and calcium (50 mg) per tablet. "
         "Lightly flavoured with natural citrus — avoids the cloying sweetness that discourages hydration in heat. "
         "Dissolves in 500 ml of water within 90 seconds. "
         "Clinically tested formulation used by national triathlon and marathon squads. Tube of 20 tablets."),
        ("Trail Mix Energy Blend",
         "2:1:1 carbohydrate-fat-protein trail mix blending roasted cashews, dark chocolate chips, dried mango, and pumpkin seeds. "
         "Caloric density of 5.8 kcal per gram — more efficient than most gels for sustained low-to-moderate intensity efforts. "
         "Resealable zip-lock pouch keeps contents fresh in humid conditions. "
         "No added sulphites or preservatives. Suitable for vegan and gluten-free diets."),
    ],
    "accessories": [
        ("Trekking Poles — Collapsible",
         "Three-section collapsible trekking poles with a FlickLock Pro mechanism that sets in one snap and releases with a thumb press — even with gloves. "
         "The carbon fibre shaft absorbs trail vibration more effectively than aluminium, reducing cumulative arm fatigue on long descents. "
         "Interchangeable baskets cover summer trail, mud, and snow conditions without tools. "
         "Ergonomic cork grip wicks sweat and moulds to hand shape over time."),
        ("Climbing Harness — Sport",
         "Sport and gym climbing harness with four pressure-moulded foam waistbelt and leg loop panels that remain comfortable during extended hangdog sessions. "
         "The Wireframe technology reduces weight to 290 g without compromising the rigidity needed for precise clipping movements. "
         "Dual-density belay loop passes CE testing at 15 kN. "
         "Tall back-rise geometry prevents the harness from riding up during overhanging moves."),
        ("Avalanche Safety Pack",
         "Airbag-integrated backpack with a 35 L main compartment and a single-hand-pull airbag handle compatible with both right and left hands. "
         "The 150-litre airbag volume inflates in 3 seconds using a compressed air cylinder rated to 50 deployments. "
         "Ventilated back panel with aluminium framesheet transfers load to the hips during resort and backcountry carry. "
         "External attachment points for shovel, probe, and skis."),
        ("Bouldering Crash Pad",
         "4-fold crash pad with a 10 cm closed-cell foam core covered by a 5 cm open-cell foam landing layer. "
         "The layered construction prevents slab-through on falls from heights above 4 m. "
         "Carpet-fabric hinge covers the fold crease to eliminate the gap that can catch ankles. "
         "Shoulder straps and hip belt allow carrying the 8 kg pad on approach hikes up to 60 minutes."),
        ("Headlamp 700 lm",
         "700-lumen rechargeable headlamp with a proximity sensor that auto-dims when your hand or face approaches within 30 cm — preventing accidental blinding of companions. "
         "Red light mode preserves night vision during navigation. "
         "IPX8 waterproof to 1 m for use in heavy rain and river crossings. "
         "A single USB-C charge delivers full-brightness run time of 2 hours or economy-mode run time of 200 hours."),
    ],
}

BRAND_PREFIXES = [
    "Apex", "Summit", "Ridge", "Peak", "Granite", "Cascade", "Ember",
    "Nordic", "Terra", "Velo", "Arc", "Crest", "Foehn", "Boreal", "Cirque",
]

ADJECTIVES = [
    "Pro", "Elite", "Ultra", "Sport", "Lite", "Plus", "Max", "Evo",
    "Series 2", "Series 3", "V2", "V3", "X", "XL", "SE",
]

def vary_title(base_title: str) -> str:
    """Produce a brand-variant title so all 500 records feel distinct."""
    prefix = random.choice(BRAND_PREFIXES)
    suffix = random.choice(ADJECTIVES)
    return f"{prefix} {base_title} {suffix}"

def vary_description(base_desc: str) -> str:
    """Minor lexical variation so descriptions are not identical across records."""
    swaps = [
        ("exceptional", "outstanding"), ("ensuring", "providing"),
        ("suitable", "ideal"), ("popular", "favoured"),
        ("features", "incorporates"), ("provides", "delivers"),
        ("reduces", "minimises"), ("requires", "needs"),
        ("available", "offered"), ("designed", "engineered"),
        ("allows", "enables"), ("prevents", "avoids"),
        ("combining", "blending"), ("lightweight", "low-weight"),
    ]
    for a, b in random.sample(swaps, k=3):
        base_desc = base_desc.replace(a, b, 1)
    return base_desc

records = []
idx = 1

for category, products in CATEGORIES.items():
    # 6 categories × 84 = 504, trimmed to 500
    target = 84
    base_pool = products * (target // len(products) + 1)  # repeat to fill quota

    for i in range(target):
        base_title, base_desc = base_pool[i % len(products)]
        # Every 5th record: keep original title/desc so search demos have exact matches
        if i % 5 == 0:
            title, desc = base_title, base_desc
        else:
            title = vary_title(base_title)
            desc = vary_description(base_desc)

        records.append({
            "id": f"prod-{idx:04d}",
            "title": title,
            "description": desc,
            "category": category,
        })
        idx += 1

# Trim or pad to exactly 500
records = records[:500]

out_path = pathlib.Path(__file__).parent / "product-catalog.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"Written {len(records)} records to {out_path}")
