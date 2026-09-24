#!/usr/bin/env python3
"""Generate the outstation hub, one landing page per route, and sitemap.xml.

Run from anywhere:  python3 _build/routes.py
Edit ROUTES below and re-run; the generated pages are committed as plain HTML.
(GitHub Pages skips folders that start with an underscore, so this script isn't published.)

Distances and drive times are approximate road figures. Never add a fixed fare:
drivers bid, so any price here would be made up.
"""
import datetime
import json
import pathlib
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://taxiyaar.com"
HUB = "outstation-cabs-bangalore"
RIDER_APP = "https://play.google.com/store/apps/details?id=com.taxiyaar"
TODAY = datetime.date.today().isoformat()
# Pages this script doesn't touch keep their real last-modified date in the sitemap.
LASTMOD = {"privacy/": "2026-09-12", "terms/": "2026-09-12", "delete/": "2026-09-12", "": "2026-09-23"}


def interstate(state):
    return ("Crossing into " + state,
            "Some states charge taxis an entry tax at the border. "
            "Ask on the call whether the driver's price covers it.")


BANDIPUR = ("Cross Bandipur in daylight",
            "The forest roads through Bandipur are closed to traffic from 9 PM to 6 AM. "
            "Leave Bengaluru early enough to clear them before dark.")

# slug, search name, local name, km, time, road, one-line pitch, stops, tips, car advice
ROUTES = [
    dict(slug="bangalore-to-mysore-taxi", city="Mysore", local="Mysuru", km=140, time="2½–3 hours",
         road="Bengaluru–Mysuru Expressway (NH 275)",
         pitch="The most popular trip out of Bengaluru. The expressway makes it an easy morning's drive, "
               "whether you want a one-way drop or a day in Mysuru.",
         stops=[("Bidadi", "Thatte idli stalls just off the highway, a classic breakfast stop."),
                ("Channapatna", "The town of lacquered wooden toys."),
                ("Maddur", "Famous for Maddur vade."),
                ("Srirangapatna", "Tipu Sultan's island fort and the Ranganathaswamy temple, 15 minutes short of Mysuru."),
                ("Mysuru", "Mysore Palace, Chamundi Hills and Brindavan Gardens.")],
         tips=[("The expressway is tolled", "Each bid says whether toll is included, so compare like with like before you accept."),
               ("Beat the city exit", "Leave before 7 AM to get past Kengeri and onto the expressway quickly.")],
         car="A sedan is comfortable for up to four people. Pick an SUV for five to seven, or for lots of luggage."),
    dict(slug="bangalore-to-coorg-taxi", city="Coorg", local="Madikeri", km=250, time="5–6 hours",
         road="via Mysuru, Hunsur and Kushalnagar",
         pitch="Coffee estates, homestays and misty hills. The last hour climbs into the Western Ghats, "
               "so a driver who knows the road makes a difference.",
         stops=[("Srirangapatna", "The fort and temple just before Mysuru."),
                ("Hunsur", "Where the road leaves the plains behind."),
                ("Bylakuppe", "The Namdroling 'Golden Temple' in the Tibetan settlement, a short detour."),
                ("Kushalnagar", "Gateway to Coorg. Dubare elephant camp is nearby."),
                ("Madikeri", "Raja's Seat, Abbey Falls and the estates around town.")],
         tips=[("Share your exact pin", "Many homestays sit down unmarked estate roads. Send the driver the location pin on the call."),
               ("Monsoon driving", "From June to September the ghat roads are wet and slow. Allow extra time.")],
         car="An SUV handles steep estate roads and luggage better. A sedan is fine if you're staying in Madikeri town."),
    dict(slug="bangalore-to-ooty-taxi", city="Ooty", local="Udhagamandalam", km=265, time="6–7 hours",
         road="via Mysuru, Gundlupet and Bandipur",
         pitch="Through two tiger reserves and up into the Nilgiris. It's one of the prettiest drives from Bengaluru, and it has rules worth planning around.",
         stops=[("Mysuru", "The halfway mark, good for a meal."),
                ("Gundlupet", "Sunflower and marigold fields in season."),
                ("Bandipur & Mudumalai", "Forest highway where you may spot elephants and deer."),
                ("Masinagudi or Gudalur", "The two ways up: a short, steep ghat with hairpin bends, or a longer, gentler road."),
                ("Ooty", "Botanical Gardens, the lake and Doddabetta.")],
         tips=[BANDIPUR,
               ("Check the Nilgiris e-pass", "The district has required an e-pass for vehicles entering in recent seasons. Check before you travel."),
               interstate("Tamil Nadu")],
         car="An SUV is the comfortable choice for the ghat climb, especially with a full car."),
    dict(slug="bangalore-to-chikmagalur-taxi", city="Chikmagalur", local="Chikkamagaluru", km=240, time="4½–5½ hours",
         road="via Kunigal and Hassan (NH 75)",
         pitch="Karnataka's coffee country, with the state's highest peak. Good for a weekend away, with temple towns along the way.",
         stops=[("Kunigal", "The first stretch of open highway past Nelamangala."),
                ("Channarayapatna", "Turn off here for Shravanabelagola's Bahubali statue."),
                ("Hassan", "A meal stop. Belur's Chennakeshava temple is a short detour."),
                ("Chikkamagaluru", "Mullayanagiri, Baba Budangiri and the coffee estates.")],
         tips=[("Plan the hill roads", "The road up to Mullayanagiri is narrow and busy on weekends. Go early."),
               ("Share your exact pin", "Estate stays are often off the main road. Send the driver the location pin on the call.")],
         car="An SUV if you'll drive up Mullayanagiri or into estates. Otherwise a sedan is fine."),
    dict(slug="bangalore-to-wayanad-taxi", city="Wayanad", local="Kalpetta", km=280, time="5½–6½ hours",
         road="via Mysuru, Gundlupet and Bandipur (NH 766)",
         pitch="Forests, waterfalls and plantation stays in north Kerala, reached through Bandipur.",
         stops=[("Mysuru", "The halfway mark, good for a meal."),
                ("Gundlupet", "The last Karnataka town before the forest."),
                ("Bandipur & Muthanga", "Forest highway through two wildlife sanctuaries."),
                ("Sulthan Bathery", "First big town in Wayanad. Edakkal Caves are nearby."),
                ("Kalpetta", "Base for Chembra Peak, Banasura Sagar and Pookode Lake.")],
         tips=[BANDIPUR, interstate("Kerala")],
         car="A sedan is fine for the highway. Choose an SUV if your stay is up an estate road."),
    dict(slug="bangalore-to-tirupati-taxi", city="Tirupati", local="Tirupati", km=260, time="4½–5½ hours",
         road="via the Bengaluru–Chennai Expressway (NE 7) and Chittoor",
         pitch="A well-worn pilgrimage road. Plan it around your darshan slot and agree the waiting time up front.",
         stops=[("Hoskote", "Where the city traffic finally eases."),
                ("Bengaluru–Chennai Expressway", "The fast new road east. Some drivers still take the older NH 75 via Kolar and Mulbagal."),
                ("Chittoor", "Halfway point in Andhra Pradesh."),
                ("Tirupati", "Foot of the hills. Tirumala is up the ghat road.")],
         tips=[("Going up to Tirumala?", "Say so on the call. The ghat road adds about an hour and there's a vehicle check at Alipiri."),
               interstate("Andhra Pradesh")],
         car="A sedan suits most families. An SUV for five or more pilgrims."),
    dict(slug="bangalore-to-chennai-taxi", city="Chennai", local="Chennai", km=330, time="6–7 hours",
         road="NH 48 via Hosur, Krishnagiri and Vellore",
         pitch="A straight run down NH 48 between two big cities. Handy when you have luggage, family or an odd-hour departure.",
         stops=[("Hosur", "Just across the Tamil Nadu border."),
                ("Krishnagiri", "Where the roads to Chennai and Salem split."),
                ("Ambur", "Famous for its biryani."),
                ("Vellore", "The fort, and the Sripuram Golden Temple nearby."),
                ("Chennai", "Drop anywhere in the city or at the airport.")],
         tips=[("Leave early", "Clear Electronic City and Hosur before the morning rush."), interstate("Tamil Nadu")],
         car="A sedan is the usual choice. An SUV for more people or luggage."),
    dict(slug="bangalore-to-pondicherry-taxi", city="Pondicherry", local="Puducherry", km=310, time="6–6½ hours",
         road="via Krishnagiri, Tiruvannamalai and Gingee",
         pitch="From the city to the French Quarter and the sea, past two of Tamil Nadu's great landmarks.",
         stops=[("Krishnagiri", "The turn-off from NH 48."),
                ("Tiruvannamalai", "The Arunachaleswarar temple at the foot of the hill."),
                ("Gingee", "A hill fort you can see from the road."),
                ("Puducherry", "The French Quarter, the promenade and Auroville.")],
         tips=[("Stopping at Auroville?", "Mention it on the call. It's a short detour before the town."),
               interstate("Tamil Nadu and Puducherry")],
         car="A sedan for up to four. An SUV for a group."),
    dict(slug="bangalore-to-hyderabad-taxi", city="Hyderabad", local="Hyderabad", km=570, time="9–10 hours",
         road="NH 44 via Anantapur and Kurnool",
         pitch="A long day on one of India's best highways. Useful when you're moving house, travelling with family or can't get a flight.",
         stops=[("Devanahalli", "Past the airport and out of the city."),
                ("Penukonda", "Into Andhra Pradesh."),
                ("Anantapur", "A good breakfast or lunch stop."),
                ("Kurnool", "Cross the Tungabhadra into the last stretch."),
                ("Hyderabad", "Drop anywhere in the city.")],
         tips=[("Plan for breaks", "It's a full day's drive. Build in meal and rest stops for you and the driver."),
               interstate("Andhra Pradesh and Telangana")],
         car="An SUV is more comfortable over nine hours, and needed for a full load of luggage."),
    dict(slug="bangalore-to-coimbatore-taxi", city="Coimbatore", local="Coimbatore", km=340, time="6–7 hours",
         road="via Hosur, Krishnagiri, Salem and Erode",
         pitch="Highway all the way to the gateway of the Nilgiris and Kerala.",
         stops=[("Hosur", "Just across the Tamil Nadu border."),
                ("Dharmapuri", "Hogenakkal Falls is a detour from here."),
                ("Salem", "The halfway point."),
                ("Perundurai", "Past Erode on the last stretch."),
                ("Coimbatore", "Isha's Adiyogi and the road up to Ooty are close by.")],
         tips=[("Leave early", "Clear Electronic City and Hosur before the morning rush."), interstate("Tamil Nadu")],
         car="A sedan is the usual choice. An SUV for more people or luggage."),
    dict(slug="bangalore-to-hampi-taxi", city="Hampi", local="Hampi", km=340, time="6–6½ hours",
         road="NH 48 via Tumakuru and Chitradurga",
         pitch="The ruins of Vijayanagara. Many riders keep the same driver for the sightseeing once they're there.",
         stops=[("Tumakuru", "The first big town north of the city."),
                ("Chitradurga", "The seven-walled stone fort, right off the highway."),
                ("Hosapete", "The town nearest Hampi, and the Tungabhadra dam."),
                ("Hampi", "Virupaksha temple, the Stone Chariot and the boulder hills.")],
         tips=[("Sightseeing too?", "The monuments are spread out. If you want the driver to stay for local trips, agree it and the price on the call."),
               ("Beat the heat", "From March to May, start early and plan the ruins for mornings.")],
         car="A sedan is fine. An SUV for a group or for rough village roads."),
    dict(slug="bangalore-to-mangalore-taxi", city="Mangalore", local="Mangaluru", km=345, time="6½–8 hours",
         road="via Hassan and the Shiradi Ghat (NH 75)",
         pitch="From the plateau down the Western Ghats to the coast. The ghat section is the part that needs an experienced driver.",
         stops=[("Kunigal", "The first stretch of open highway past Nelamangala."),
                ("Hassan", "A meal stop."),
                ("Sakleshpur", "Coffee and cardamom country at the top of the ghat."),
                ("Shiradi Ghat", "The winding descent to the coast."),
                ("Mangaluru", "The beaches, the temples and the fish curry.")],
         tips=[("Check the ghat", "Shiradi Ghat is sometimes closed for repairs or after heavy rain. Ask the driver about the Charmadi or Sampaje routes."),
               ("Monsoon driving", "From June to September, allow extra time on the ghat.")],
         car="An SUV is steadier on the ghat, especially in the monsoon."),
    dict(slug="bangalore-to-goa-taxi", city="Goa", local="Goa", km=580, time="11–12 hours",
         road="NH 48 via Chitradurga and Hubballi, then over the Western Ghats",
         pitch="A full-day road trip to the coast. It makes sense for a group, where one car costs less than several flights.",
         stops=[("Chitradurga", "The stone fort, a good first break."),
                ("Davanagere", "Stop for benne dosa."),
                ("Hubballi–Dharwad", "The halfway mark."),
                ("The Ghats", "The road drops through forest to the coast."),
                ("Goa", "North or South, drop at your stay.")],
         tips=[("Plan for breaks", "It's a full day's drive. Build in meal and rest stops for you and the driver."),
               interstate("Goa")],
         car="An SUV for a group of five to seven with luggage. That's where this trip makes most sense."),
    dict(slug="bangalore-to-kochi-taxi", city="Kochi", local="Kochi", km=515, time="10–11 hours",
         road="via Salem, Coimbatore and Palakkad",
         pitch="Across Tamil Nadu and through the Palakkad Gap into Kerala. A long day's drive, door to door.",
         stops=[("Salem", "Halfway across Tamil Nadu."),
                ("Coimbatore", "A good lunch stop."),
                ("Palakkad", "Into Kerala through the gap in the Ghats."),
                ("Thrissur", "The Vadakkunnathan temple, in the middle of town."),
                ("Kochi", "Fort Kochi, Marine Drive or the airport.")],
         tips=[("Plan for breaks", "It's a full day's drive. Build in meal and rest stops for you and the driver."),
               interstate("Tamil Nadu and Kerala")],
         car="An SUV is more comfortable over ten hours, and needed for a full load of luggage."),
]

LOGO = ('<svg viewBox="0 0 500 500" aria-hidden="true"><rect width="500" height="500" rx="110" fill="#0F6E6E"/>'
        '<rect x="60" y="268" width="380" height="148" rx="30" fill="#fff"/><path d="M100 268 L138 158 L362 158 L400 268Z" fill="#fff"/>'
        '<rect x="148" y="100" width="204" height="68" rx="18" fill="#fff"/>'
        '<circle cx="134" cy="418" r="52" fill="#fff" stroke="#0F6E6E" stroke-width="14"/><circle cx="134" cy="418" r="20" fill="#0F6E6E"/>'
        '<circle cx="366" cy="418" r="52" fill="#fff" stroke="#0F6E6E" stroke-width="14"/><circle cx="366" cy="418" r="20" fill="#0F6E6E"/></svg>')

STEPS = """<ol class="steps">
        <li><b>Post your trip</b>Route, date, time, passengers and car type. Drivers on your route are notified straight away.</li>
        <li><b>Drivers bid</b>Each bid has a price, a note, and whether toll and parking are included.</li>
        <li><b>Pick on trust</b>Open each driver's profile: ratings in 8 categories, photos of the car, reviews from real trips.</li>
        <li><b>Call, accept, go</b>Talk to the driver, accept the bid, and start the ride with your OTP. Pay the driver in cash or by UPI.</li>
      </ol>"""


def name(r):
    """'Mysore (Mysuru)' when the local name differs, else just the city."""
    return r["city"] if r["local"] == r["city"] else f'{r["city"]} ({r["local"]})'


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + "\n</script>"


def faq_block(faqs):
    items = "\n".join(
        f"        <details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faqs)
    return f'<div class="faq">\n{items}\n      </div>'


def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}


def crumbs_html(trail):
    lis = [f'<li><a href="{u}">{escape(n)}</a></li>' for n, u in trail[:-1]]
    lis.append(f'<li aria-current="page">{escape(trail[-1][0])}</li>')
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def route_cards(routes):
    return "\n".join(
        f'        <a class="rcard" href="/{r["slug"]}/"><b>Bangalore to {escape(r["city"])}</b>'
        f'<span>{r["km"]} km · {escape(r["time"])}</span></a>' for r in routes)


def page(*, path, title, description, schema, body):
    url = f"{SITE}/{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0F6E6E">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TaxiYaar">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
{ld({"@context": "https://schema.org", "@graph": schema})}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=IBM+Plex+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/assets/routes.css">
</head>
<body>

<header class="nav">
  <div class="wrap nav-row">
    <a class="brand" href="/" aria-label="TaxiYaar home">
      {LOGO}
      <b>Taxi<span>Yaar</span></b>
    </a>
    <nav class="nav-links" aria-label="Sections">
      <a href="/{HUB}/">Outstation routes</a>
      <a href="/#how">How it works</a>
      <a href="/#drivers">For drivers</a>
    </nav>
    <a class="btn btn-teal" href="{RIDER_APP}">Get the app</a>
  </div>
</header>

{body}

<footer class="wrap foot">
  <div class="foot-row">
    <a class="brand" href="/"><b>Taxi<span>Yaar</span></b></a>
    <nav aria-label="Footer">
      <a href="/{HUB}/">Outstation cabs from Bangalore</a>
      <a href="/privacy/">Privacy</a>
      <a href="/terms/">Terms</a>
      <a href="/delete/">Delete account</a>
      <a href="mailto:support@taxiyaar.com">Contact</a>
    </nav>
    <span>© 2026 TaxiYaar · taxiyaar.com</span>
  </div>
</footer>
</body>
</html>
"""


DOWNLOAD = f"""  <section class="section">
    <div class="wrap">
      <div class="download">
        <div><h2>Post your trip. See who wants to drive you.</h2><p>Free on Android. No booking fee, no commission. iPhone app coming soon.</p></div>
        <a class="btn" href="{RIDER_APP}">Get TaxiYaar on Google Play</a>
      </div>
    </div>
  </section>"""


def route_page(r):
    city, local, km, time = r["city"], r["local"], r["km"], r["time"]
    also = f" ({local})" if local != city else ""
    trail = [("Home", "/"), ("Outstation cabs from Bangalore", f"/{HUB}/"), (f"Bangalore to {city}", f'/{r["slug"]}/')]
    faqs = [
        (f"How far is {city} from Bangalore by road?",
         f"About {km} km by road ({r['road']}). The drive usually takes {time}, depending on traffic and stops."),
        (f"What is the taxi fare from Bangalore to {city}?",
         "There's no fixed fare. Post your trip in the TaxiYaar app and drivers on the route send you their price, "
         "saying whether toll and parking are included. You compare bids and pick one. You pay the driver directly "
         "in cash or by UPI, and TaxiYaar takes no commission or booking fee."),
        (f"Which car should I book for Bangalore to {city}?", r["car"] + " You choose the car type when you post your trip."),
        ("Can I book a round trip or keep the driver for a few days?",
         "Yes, if the driver agrees. Call them before you accept and agree the return, the waiting and the price. "
         "Any extra charges have to be agreed before the trip starts, not during or after."),
        ("How do I know the driver is safe?",
         "Every driver's Aadhaar, driving licence and vehicle RC are checked by a person before they go live. You see photos "
         "of the actual car and reviews from riders who travelled with them. The trip only starts with your OTP."),
    ]
    others = [o for o in ROUTES if o is not r]
    stops = "\n".join(f"        <li><b>{escape(s)}</b><span>{escape(d)}</span></li>" for s, d in r["stops"])
    tips = "\n".join(f"        <li><b>{escape(t)}</b><span>{escape(d)}</span></li>" for t, d in r["tips"])
    title = f"Bangalore to {city} Taxi — Verified Drivers | TaxiYaar"
    description = (f"Bangalore to {city}{also} taxi from verified drivers. {km} km, about {time}. "
                   "Compare bids, see car photos and reviews, pay the driver directly.")
    schema = [
        {"@type": "Service", "@id": f'{SITE}/{r["slug"]}/#service',
         "serviceType": "Outstation taxi", "name": f"Bangalore to {city} taxi",
         "description": description,
         "provider": {"@id": f"{SITE}/#org"},
         "areaServed": [{"@type": "City", "name": "Bengaluru"}, {"@type": "Place", "name": local}],
         "url": f'{SITE}/{r["slug"]}/'},
        crumbs_ld(trail),
        faq_ld(faqs),
    ]
    body = f"""{crumbs_html(trail)}

<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Outstation taxi · Bengaluru</div>
      <h1>Bangalore to {escape(city)} taxi, <em>with a driver you choose</em>.</h1>
      <p class="lede">{escape(r["pitch"])} On TaxiYaar you <strong>pick a verified driver by name</strong>: see their car, their ratings and reviews from real trips, then call them and pay them directly.</p>
      <div class="cta-row">
        <a class="btn btn-teal" href="{RIDER_APP}">Post your {escape(city)} trip</a>
        <a class="btn btn-ghost" href="/{HUB}/">All routes from Bangalore</a>
      </div>
      <dl class="facts-strip">
        <div><dt>Distance</dt><dd>~{km} km<small>by road from Bengaluru</small></dd></div>
        <div><dt>Drive time</dt><dd>{escape(time)}<small>depending on traffic and stops</small></dd></div>
        <div><dt>Road</dt><dd>{escape(r["road"])}</dd></div>
      </dl>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">On the way</div><h2>The road from Bangalore to {escape(city)}</h2></div>
      <ol class="road">
        <li><b>Bengaluru</b><span>Pickup from your door, anywhere in the city.</span></li>
{stops}
      </ol>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">Good to know</div><h2>Before you book</h2></div>
      <ul class="tips">
{tips}
        <li><b>Which car</b><span>{escape(r["car"])}</span></li>
      </ul>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">How booking works</div><h2>Book a driver, not a cab</h2><p>No fixed fares and no middleman. Drivers on the route bid for your trip and you pick.</p></div>
      {STEPS}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">Questions</div><h2>Bangalore to {escape(city)} taxi: FAQs</h2></div>
      {faq_block(faqs)}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">More routes</div><h2>Other outstation trips from Bangalore</h2></div>
      <div class="routes">
{route_cards(others)}
      </div>
    </div>
  </section>

{DOWNLOAD}
</main>"""
    return page(path=f'{r["slug"]}/', title=title, description=description, schema=schema, body=body)


def hub_page():
    trail = [("Home", "/"), ("Outstation cabs from Bangalore", f"/{HUB}/")]
    faqs = [
        ("How do I book an outstation cab from Bangalore on TaxiYaar?",
         "Install the TaxiYaar app, post your trip with the destination, date, time, passengers and car type, and drivers "
         "on your route send you bids. Compare their prices and profiles, call the one you like and accept their bid."),
        ("How much does an intercity taxi from Bangalore cost?",
         "Drivers set their own price for each trip, so there's no fixed fare. Every bid shows the price and whether toll and "
         "parking are included. You pay the driver directly in cash or by UPI, and TaxiYaar takes no commission."),
        ("Can I book a one-way drop?",
         "Yes. Post the trip as you need it. If you want a round trip, or want the driver to wait, agree it with them on the "
         "call before you accept."),
        ("Where can I travel from Bangalore?",
         "Any trip that starts in Bengaluru, from Mysuru and Coorg to Chennai, Hyderabad, Goa and beyond. "
         "The routes on this page are the most popular ones."),
        ("Are TaxiYaar drivers verified?",
         "Yes. Our team checks every driver's Aadhaar, driving licence and vehicle RC by hand before they can take trips. "
         "Riders can only review a driver after travelling with them."),
    ]
    near = sorted(ROUTES, key=lambda r: r["km"])
    title = "Outstation Cabs from Bangalore | Intercity Taxi — TaxiYaar"
    description = ("Outstation and intercity taxis from Bangalore to Mysore, Coorg, Ooty, Tirupati, Chennai, Goa and more. "
                   "Compare bids from verified drivers. Zero commission.")
    schema = [
        {"@type": "Service", "@id": f"{SITE}/{HUB}/#service", "serviceType": "Outstation taxi",
         "name": "Outstation and intercity taxis from Bangalore", "description": description,
         "provider": {"@id": f"{SITE}/#org"}, "areaServed": {"@type": "City", "name": "Bengaluru"},
         "url": f"{SITE}/{HUB}/"},
        {"@type": "ItemList", "name": "Popular outstation routes from Bangalore", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f"Bangalore to {r['city']} taxi", "url": f"{SITE}/{r['slug']}/"}
            for i, r in enumerate(near)]},
        crumbs_ld(trail),
        faq_ld(faqs),
    ]
    body = f"""{crumbs_html(trail)}

<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Intercity travel from Bengaluru</div>
      <h1>Outstation cabs from Bangalore, <em>from drivers you can see</em>.</h1>
      <p class="lede">Going out of the city for a weekend, a wedding or a move? Post your trip and verified drivers bid for it. You see <strong>each driver's name, car and reviews</strong> before you choose. You pay them directly, and TaxiYaar takes no commission.</p>
      <div class="cta-row">
        <a class="btn btn-teal" href="{RIDER_APP}">Post your trip</a>
        <a class="btn btn-ghost" href="/#how">How it works</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">Popular routes</div><h2>Intercity taxi routes from Bangalore</h2><p>Nearest first. Distances and times are approximate road figures from central Bengaluru.</p></div>
      <div class="routes">
{route_cards(near)}
      </div>
      <p class="lede" style="font-size:15px">Not listed? You can book any trip that starts in Bengaluru.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">How booking works</div><h2>Book a driver, not a cab</h2><p>No fixed fares and no middleman. Drivers on the route bid for your trip and you pick.</p></div>
      {STEPS}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="sec-head"><div class="eyebrow">Questions</div><h2>Outstation cabs from Bangalore: FAQs</h2></div>
      {faq_block(faqs)}
    </div>
  </section>

{DOWNLOAD}
</main>"""
    return page(path=f"{HUB}/", title=title, description=description, schema=schema, body=body)


def sitemap():
    paths = ["", f"{HUB}/"] + [f'{r["slug"]}/' for r in ROUTES] + ["privacy/", "terms/", "delete/"]
    urls = "\n".join(f"  <url>\n    <loc>{SITE}/{p}</loc>\n    <lastmod>{LASTMOD.get(p, TODAY)}</lastmod>\n  </url>" for p in paths)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")


def write(rel, text):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print("wrote", rel)


if __name__ == "__main__":
    write(f"{HUB}/index.html", hub_page())
    for r in ROUTES:
        write(f'{r["slug"]}/index.html', route_page(r))
    write("sitemap.xml", sitemap())
