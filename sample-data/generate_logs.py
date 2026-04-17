#!/usr/bin/env python3
"""
Generate a realistic Apache combined-format access log with ~2M lines covering Apr 1-17, 2026.
Includes an embedded APT-style attack scenario from 185.220.101.x (Tor exit node range).
"""

import gzip
import random
import os
import sys
from datetime import datetime, timedelta, timezone

# Fixed seed for reproducibility
random.seed(42)

OUTPUT_PATH = "/Users/ryanburnhamelastic/Documents/Github/customer-architect-panel/sample-data/apache_access.log.gz"
OLD_LOG_PATH = "/Users/ryanburnhamelastic/Documents/Github/customer-architect-panel/sample-data/apache_access.log"

TARGET_LINES = 2_000_000
PROGRESS_INTERVAL = 200_000

# Apache Combined Log Format:
# IP - USER [DD/Mon/YYYY:HH:MM:SS +0000] "METHOD PATH HTTP/1.1" STATUS BYTES "REFERER" "USER_AGENT"

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# --- User Agents ---
DESKTOP_UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]
MOBILE_UAS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
]
BOT_UAS = [
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
]

# The attacker's UA — slightly outdated Chrome, subtle tell
ATTACKER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Safari/537.36"

ALL_UAS = (
    [(ua, 0.55) for ua in DESKTOP_UAS] +
    [(ua, 0.30) for ua in MOBILE_UAS] +
    [(ua, 0.15) for ua in BOT_UAS]
)

def pick_ua():
    r = random.random()
    if r < 0.55:
        return random.choice(DESKTOP_UAS)
    elif r < 0.85:
        return random.choice(MOBILE_UAS)
    else:
        return random.choice(BOT_UAS)

# --- IP ranges ---
PRIVATE_RANGES = [
    (192, 0, 2),    # TEST-NET-1
    (203, 0, 113),  # TEST-NET-3
    (198, 51, 100), # TEST-NET-2
]
GLOBAL_PREFIXES = [
    (1, 2, 3), (5, 10, 20), (8, 8, 8), (23, 45, 67), (31, 13, 80),
    (45, 33, 21), (52, 1, 100), (66, 102, 7), (74, 125, 200), (80, 58, 61),
    (93, 184, 216), (104, 16, 124), (108, 162, 234), (151, 101, 65), (172, 217, 14),
    (185, 89, 10), (194, 168, 1), (199, 59, 150), (204, 79, 197), (208, 67, 222),
    (210, 130, 5), (216, 58, 194), (217, 0, 17), (37, 48, 234), (46, 182, 10),
]

def random_ip():
    r = random.random()
    if r < 0.15:
        base = random.choice(PRIVATE_RANGES)
        return f"{base[0]}.{base[1]}.{base[2]}.{random.randint(1,254)}"
    else:
        base = random.choice(GLOBAL_PREFIXES)
        return f"{base[0]}.{base[1]}.{base[2]}.{random.randint(1,254)}"

# --- URLs ---
PRODUCT_IDS = [str(random.randint(1000, 9999)) for _ in range(200)]
PRODUCT_SLUGS = [
    "wireless-headphones", "running-shoes", "coffee-maker", "laptop-stand",
    "yoga-mat", "smart-watch", "desk-lamp", "water-bottle", "backpack",
    "keyboard", "webcam", "monitor", "gaming-chair", "notebook", "pen-set"
]
CATEGORIES = ["electronics", "clothing", "sports", "home", "books", "toys", "beauty", "automotive"]
STREAM_IDS = [str(random.randint(100, 9999)) for _ in range(100)]
STREAM_NAMES = [
    "goes-east-full", "goes-west-conus", "goes-16-mesoscale", "goes-18-band2",
    "abi-channel-13", "fulldisk-visible", "night-microphysics", "fire-temperature"
]
API_RESOURCE = ["users", "products", "orders", "recommendations", "inventory", "reviews"]
SEARCH_TERMS = [
    "headphones", "shoes+size+10", "laptop+stand", "coffee+beans", "yoga+blocks",
    "smart+home", "gaming+mouse", "4k+monitor", "running+gear", "winter+jacket"
]

def random_url():
    r = random.random()
    if r < 0.20:
        # Products
        slug = random.choice(PRODUCT_SLUGS)
        pid = random.choice(PRODUCT_IDS)
        sub = random.random()
        if sub < 0.4:
            return f"/products/{slug}-{pid}"
        elif sub < 0.6:
            return f"/products/{random.choice(CATEGORIES)}"
        elif sub < 0.8:
            return f"/products/{slug}-{pid}/reviews"
        else:
            return f"/products/featured"
    elif r < 0.35:
        # Streaming
        sub = random.random()
        if sub < 0.5:
            return f"/streaming/{random.choice(STREAM_NAMES)}"
        elif sub < 0.7:
            return f"/streaming/live/{random.choice(STREAM_IDS)}"
        elif sub < 0.85:
            return f"/streaming/archive/{random.choice(STREAM_IDS)}/latest.jpg"
        else:
            return f"/streaming/metadata/{random.choice(STREAM_IDS)}"
    elif r < 0.50:
        # API
        sub = random.random()
        res = random.choice(API_RESOURCE)
        if sub < 0.3:
            return f"/api/v1/{res}"
        elif sub < 0.5:
            pid = random.randint(1, 50000)
            return f"/api/v1/{res}/{pid}"
        elif sub < 0.65:
            return f"/api/v1/{res}?page={random.randint(1,20)}&limit={random.choice([10,20,50])}"
        elif sub < 0.75:
            return "/api/v1/auth/login"
        elif sub < 0.85:
            return "/api/v1/auth/refresh"
        else:
            return f"/api/v1/recommendations?user_id={random.randint(1,100000)}"
    elif r < 0.60:
        # Search
        q = random.choice(SEARCH_TERMS)
        return f"/search?q={q}&page={random.randint(1,5)}"
    elif r < 0.70:
        # Account
        sub = random.random()
        if sub < 0.4:
            return "/account/profile"
        elif sub < 0.6:
            return "/account/orders"
        elif sub < 0.8:
            return "/account/settings"
        else:
            return "/account/wishlist"
    elif r < 0.82:
        # Images/static
        sub = random.random()
        if sub < 0.5:
            slug = random.choice(PRODUCT_SLUGS)
            return f"/images/products/{slug}-{random.randint(1,9)}.jpg"
        elif sub < 0.7:
            return f"/images/banners/{random.choice(['hero', 'sale', 'new-arrivals', 'featured'])}.jpg"
        else:
            return f"/static/css/main.{random.randint(100,999)}.css"
    elif r < 0.92:
        # Home / misc
        pages = ["/", "/about", "/contact", "/faq", "/shipping", "/returns", "/privacy", "/terms"]
        return random.choice(pages)
    else:
        # CDN/assets
        return f"/assets/js/bundle.{random.randint(100,999)}.js"

def random_method_for_url(url):
    if "login" in url or "checkout" in url or "account/update" in url:
        return "POST" if random.random() < 0.6 else "GET"
    if random.random() < 0.97:
        return "GET"
    return "POST"

def random_status(url, method):
    r = random.random()
    if "login" in url and method == "POST":
        # login endpoint — mostly 200, some 401
        if r < 0.85:
            return 200
        elif r < 0.97:
            return 401
        else:
            return 429
    if r < 0.82:
        return 200
    elif r < 0.87:
        return 304
    elif r < 0.92:
        return 301
    elif r < 0.96:
        return 404
    elif r < 0.985:
        return 400
    elif r < 0.995:
        return 500
    else:
        return 503

def random_bytes(status, url):
    if status in (304, 301):
        return random.randint(0, 512)
    if "images" in url or ".jpg" in url:
        return random.randint(20000, 500000)
    if ".css" in url or ".js" in url:
        return random.randint(5000, 200000)
    if "/api/v1/" in url:
        return random.randint(200, 50000)
    if status == 404:
        return random.randint(200, 2000)
    if status == 500:
        return random.randint(500, 5000)
    return random.randint(1000, 80000)

def random_referer(url):
    if random.random() < 0.55:
        return "-"
    bases = ["https://goes-viewer.example.com", "https://www.google.com", "https://www.bing.com",
             "https://goes-viewer.example.com/products", "https://goes-viewer.example.com/search"]
    return random.choice(bases)

def format_log_line(ip, dt, method, url, status, nbytes, referer, ua):
    ts = dt.strftime(f"%d/%b/%Y:%H:%M:%S +0000")
    return f'{ip} - - [{ts}] "{method} {url} HTTP/1.1" {status} {nbytes} "{referer}" "{ua}"\n'

# --- Traffic volume by hour (relative weights) ---
# Higher 8:0-22:0, peaks around 12:0 and 19:0-20:0
HOUR_WEIGHTS = [
    0.3, 0.2, 0.15, 0.12, 0.10, 0.12,   # 0-5
    0.25, 0.50, 0.80, 1.0, 1.10, 1.20, # 6-11
    1.40, 1.30, 1.20, 1.15, 1.20, 1.25, # 12-17
    1.35, 1.50, 1.40, 1.20, 0.90, 0.55, # 18-23
]
HOUR_WEIGHT_TOTAL = sum(HOUR_WEIGHTS)
# Normalized cumulative for sampling
HOUR_CUM = []
cumulative = 0
for w in HOUR_WEIGHTS:
    cumulative += w / HOUR_WEIGHT_TOTAL
    HOUR_CUM.append(cumulative)

def sample_hour():
    r = random.random()
    for i, c in enumerate(HOUR_CUM):
        if r <= c:
            return i
    return 23

# Weekend factor
def day_factor(dt):
    dow = dt.weekday()  # 0=Mon, 6=Sun
    if dow >= 5:
        return 0.75
    return 1.0

# --- Build attack events ---
# These will be inserted into the event stream sorted by time

UTC = timezone.utc

def dt(year, month, day, hour, minute, second):
    return datetime(year, month, day, hour, minute, second, tzinfo=UTC)

attack_events = []

# Apr 1-3: Quiet recon from 185.220.101.47
recon_ip = "185.220.101.47"
recon_entries = [
    (dt(2026,4,1,14,22,11), "GET", "/robots.txt", 200, 1247),
    (dt(2026,4,1,14,22,45), "GET", "/sitemap.xml", 200, 8432),
    (dt(2026,4,1,14,23,18), "GET", "/", 200, 42310),
    (dt(2026,4,1,14,35,2), "GET", "/products/wireless-headphones-1234", 200, 35820),
    (dt(2026,4,1,14,36,55), "GET", "/products/coffee-maker-5678", 200, 34110),
    (dt(2026,4,2,10,11,33), "GET", "/about", 200, 18900),
    (dt(2026,4,2,10,12,8), "GET", "/products/electronics", 200, 52340),
    (dt(2026,4,2,10,15,44), "GET", "/search?q=headphones&page=1", 200, 28730),
    (dt(2026,4,3,16,44,21), "GET", "/products/featured", 200, 47220),
    (dt(2026,4,3,16,45,9), "GET", "/streaming/goes-east-full", 200, 3210),
]
for ts, method, url, status, nbytes in recon_entries:
    attack_events.append((ts, recon_ip, method, url, status, nbytes))

# Apr 4-7: Vulnerability scanning — same IP
vuln_scan = [
    (dt(2026,4,4,22,15,33), "GET", "/admin", 404, 1247),
    (dt(2026,4,4,22,15,48), "GET", "/wp-admin", 404, 1247),
    (dt(2026,4,4,22,16,2), "GET", "/wp-admin/", 404, 1247),
    (dt(2026,4,4,22,16,19), "GET", "/phpmyadmin", 404, 1247),
    (dt(2026,4,4,22,16,44), "GET", "/.env", 404, 1247),
    (dt(2026,4,4,22,17,1), "GET", "/.git/config", 404, 1247),
    (dt(2026,4,5,1,44,22), "GET", "/admin.php", 404, 1247),
    (dt(2026,4,5,1,44,39), "GET", "/config.php", 404, 1247),
    (dt(2026,4,5,1,44,56), "GET", "/wp-login.php", 404, 1247),
    (dt(2026,4,5,1,45,14), "GET", "/xmlrpc.php", 404, 1247),
    (dt(2026,4,5,1,45,31), "GET", "/.htaccess", 404, 1247),
    (dt(2026,4,5,1,45,50), "GET", "/backup.sql", 404, 1247),
    (dt(2026,4,6,3,22,17), "GET", "/administrator", 404, 1247),
    (dt(2026,4,6,3,22,34), "GET", "/api/swagger.json", 404, 1247),
    (dt(2026,4,6,3,22,52), "GET", "/api/v1/docs", 200, 14320),
    (dt(2026,4,6,3,23,10), "GET", "/server-status", 403, 1024),
    (dt(2026,4,7,23,55,12), "GET", "/cgi-bin/test.cgi", 404, 1247),
    (dt(2026,4,7,23,55,29), "GET", "/console", 404, 1247),
    (dt(2026,4,7,23,55,47), "GET", "/actuator/health", 404, 1247),
    (dt(2026,4,7,23,56,5), "GET", "/actuator/env", 404, 1247),
]
for ts, method, url, status, nbytes in vuln_scan:
    attack_events.append((ts, recon_ip, method, url, status, nbytes))

# Apr 8-13: Slow credential stuffing — rotating IPs in 185.220.101.x/24, 2:0-4:0 UTC
# Bursts of 2-3 with 30-90s gaps
stuffing_schedule = [
    # (day, base_hour, base_min, base_sec, last_octet)
    # Apr 8
    (8,  2, 11,  7, 12),
    (8,  2, 11, 44, 12),
    (8,  2, 12, 18, 12),
    (8,  3, 2, 33, 73),
    (8,  3, 3, 5, 73),
    # Apr 9
    (9,  2, 33, 14, 201),
    (9,  2, 33, 57, 201),
    (9,  2, 34, 44, 201),
    (9,  3, 15, 29, 88),
    (9,  3, 15, 59, 88),
    # Apr 10
    (10, 2, 44, 3, 134),
    (10, 2, 44, 37, 134),
    (10, 3, 22, 12, 55),
    (10, 3, 22, 48, 55),
    (10, 3, 23, 19, 55),
    # Apr 11
    (11, 2, 17, 52, 166),
    (11, 2, 18, 24, 166),
    (11, 3, 8, 41, 99),
    (11, 3, 9, 14, 99),
    # Apr 12
    (12, 2, 55, 31, 47),
    (12, 2, 56, 3, 47),
    (12, 2, 56, 39, 47),
    (12, 3, 41, 17, 182),
    (12, 3, 41, 50, 182),
    # Apr 13
    (13, 2, 28, 8, 117),
    (13, 2, 28, 44, 117),
    (13, 3, 55, 22, 203),
    (13, 3, 55, 55, 203),
    (13, 3, 56, 31, 203),
]
for day, hour, minute, second, octet in stuffing_schedule:
    ts = dt(2026, 4, day, hour, minute, second)
    ip = f"185.220.101.{octet}"
    attack_events.append((ts, ip, "POST", "/api/v1/auth/login", 401, 512))

# Apr 14, 2:47:33 — Successful login
attack_events.append((dt(2026,4,14,2,47,33), "185.220.101.47", "POST", "/api/v1/auth/login", 200, 512))

# Apr 14 2:48 - 3:19 — Exfiltration session
exfil = [
    (dt(2026,4,14,2,48,12), "GET", "/api/v1/users?limit=10000", 200, 2194302),
    (dt(2026,4,14,2,52,44), "GET", "/api/v1/orders?export=true&start=2024-1-1", 200, 5431808),
    (dt(2026,4,14,2,59,17), "GET", "/api/v1/products?export=csv&include_pricing=true", 200, 3817472),
    (dt(2026,4,14,3,4,55), "GET", "/api/v1/users/export/bulk", 403, 256),
    (dt(2026,4,14,3,5,22), "GET", "/api/v1/payments/transactions?export=true", 403, 256),
    (dt(2026,4,14,3,6,11), "GET", "/api/v1/orders?page=1", 200, 819200),
    (dt(2026,4,14,3,8,33), "GET", "/api/v1/orders?page=2", 200, 819200),
    (dt(2026,4,14,3,10,55), "GET", "/api/v1/orders?page=3", 200, 819200),
    (dt(2026,4,14,3,13,17), "GET", "/api/v1/orders?page=4", 200, 819200),
    (dt(2026,4,14,3,15,39), "GET", "/api/v1/orders?page=5", 200, 819200),
    (dt(2026,4,14,3,17,1), "GET", "/search?q=%27+OR+%271%27%3D%271", 200, 28340),
    (dt(2026,4,14,3,19,44), "GET", "/api/v1/orders?page=6", 200, 614400),
]
for ts, method, url, status, nbytes in exfil:
    attack_events.append((ts, "185.220.101.47", method, url, status, nbytes))

# Apr 15-17: Quiet check-ins
quiet_checkins = [
    (dt(2026,4,15,9,14,22), "GET", "/", 200, 42310),
    (dt(2026,4,15,21,33,45), "GET", "/api/v1/auth/refresh", 200, 512),
    (dt(2026,4,16,8,55,12), "GET", "/products/featured", 200, 47220),
    (dt(2026,4,17,11,22,9), "GET", "/", 200, 42310),
    (dt(2026,4,17,14,44,33), "GET", "/streaming/goes-east-full", 200, 3210),
]
for ts, method, url, status, nbytes in quiet_checkins:
    attack_events.append((ts, recon_ip, method, url, status, nbytes))

# Sort attack events by timestamp
attack_events.sort(key=lambda x: x[0])

# Convert attack events to a dict keyed by approximate timestamp for merging
# We'll use a pointer-based merge approach

print(f"Total attack events to embed: {len(attack_events)}")

# --- Generate normal traffic timestamps for each day ---
# We need ~2M total lines across 17 days. Subtract attack events (~100).
# Distribute lines by day, weighted by day_factor and total hourly traffic.

START_DATE = datetime(2026, 4, 1, tzinfo=UTC)
NUM_DAYS = 17

# Lines per day (weighted by weekend factor)
lines_normal = TARGET_LINES - len(attack_events)
day_factors = []
for d in range(NUM_DAYS):
    day = START_DATE + timedelta(days=d)
    day_factors.append(day_factor(day))
total_factor = sum(day_factors)
lines_per_day = [int(lines_normal * f / total_factor) for f in day_factors]
# Fix rounding
lines_per_day[-1] += lines_normal - sum(lines_per_day)

print(f"Lines per day (sample): {lines_per_day[:5]}...")
print(f"Total normal lines: {sum(lines_per_day)}")

# --- Main generation ---
# Strategy: generate events day by day, sort within the day, then merge with attack events

uncompressed_size = 0
line_count = 0
attack_ptr = 0  # pointer into attack_events

with gzip.open(OUTPUT_PATH, 'wt', encoding='ascii', compresslevel=6) as f:
    for d in range(NUM_DAYS):
        day = START_DATE + timedelta(days=d)
        n_lines = lines_per_day[d]

        # Generate (timestamp_seconds_within_day, ...) for this day
        # We'll build a list of (ts, line_str) and sort by ts
        day_events = []

        for _ in range(n_lines):
            hour = sample_hour()
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            ts = day.replace(hour=hour, minute=minute, second=second)

            ip = random_ip()
            url = random_url()
            method = random_method_for_url(url)
            status = random_status(url, method)
            nbytes = random_bytes(status, url)
            referer = random_referer(url)
            ua = pick_ua()

            line = format_log_line(ip, ts, method, url, status, nbytes, referer, ua)
            day_events.append((ts, line))

        # Add any attack events that fall on this day
        day_start = day
        day_end = day + timedelta(days=1)
        while attack_ptr < len(attack_events) and attack_events[attack_ptr][0] < day_end:
            ev = attack_events[attack_ptr]
            ev_ts, ev_ip, ev_method, ev_url, ev_status, ev_nbytes = ev
            referer = "-"
            line = format_log_line(ev_ip, ev_ts, ev_method, ev_url, ev_status, ev_nbytes, referer, ATTACKER_UA)
            day_events.append((ev_ts, line))
            attack_ptr += 1

        # Sort by timestamp
        day_events.sort(key=lambda x: x[0])

        # Write all lines for this day
        for ts, line in day_events:
            f.write(line)
            uncompressed_size += len(line)
            line_count += 1
            if line_count % PROGRESS_INTERVAL == 0:
                print(f"  Progress: {line_count:,} lines written...")

# --- Final stats ---
compressed_size = os.path.getsize(OUTPUT_PATH)
print(f"\n=== Generation Complete ===")
print(f"Lines written:      {line_count:,}")
print(f"Uncompressed size:  {uncompressed_size / 1024 / 1024:.1f} MB")
print(f"Compressed size:    {compressed_size / 1024 / 1024:.1f} MB")
print(f"Compression ratio:  {uncompressed_size / compressed_size:.1f}x")
print(f"Output:             {OUTPUT_PATH}")

# Delete old uncompressed log if it exists
if os.path.exists(OLD_LOG_PATH):
    os.remove(OLD_LOG_PATH)
    print(f"Deleted old log:    {OLD_LOG_PATH}")
else:
    print(f"No old log to delete at {OLD_LOG_PATH}")
