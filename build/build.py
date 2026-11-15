"""Build the whole static site into ../public.

Brand v3.0 ("Agent Ledger": AI Automation & Agentic AI). Everything a visitor reads is defined in this file:
header, footer, every page, structured data, sitemap.xml, llms.txt.
The stylesheet source is build/site.src.css and the script source is build/main.src.js;
this script copies both into public/.

Run:  python build.py
"""
import json, os, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
# Output folder. Defaults to the "public" folder next to "build". Set SITE_OUT to build somewhere else.
OUT = pathlib.Path(os.environ.get('SITE_OUT') or HERE.parent / 'public')

# ---------------------------------------------------------------- Brand rules (v3)
# Personal brand = the name. Descriptor = the category he leads with: AI automation and agentic AI.
# AI agents, GoHighLevel, n8n and Supabase RAG knowledge bases are the delivery stack, named in all public copy.
# Scope rule: no website-development or browser-extension services anywhere on the site.
BRAND_DESCRIPTOR = 'AI Automation & Agentic AI'
ROLE = 'AI Automation &amp; Agentic AI Specialist'        # job title used in hero kicker, About, structured data
ROLE_TXT = 'AI Automation & Agentic AI Specialist'
LOCKUP_LINE = 'AI automation &amp; agentic AI'          # small line under the name in the header and footer
BRAND = f'Waqar Ahmed | {BRAND_DESCRIPTOR}'
BRAND_HTML = BRAND.replace('&', '&amp;')
TAGLINE = 'Make every lead move forward.'
BASE = 'Khairpur District, Sindh, Pakistan'   # always written exactly like this (see brand guide, section 1)
REACH = 'Working remotely with clients worldwide'
LOCATION = f'Based in {BASE}. {REACH}.'
MARKET = 'US and UK remodeling contractors and GoHighLevel agencies'   # primary target market, named in hero, footer, meta and schema
TRADES_LINE = 'kitchens, bathrooms, extensions, loft conversions, basements, roofing and solar'
POSITIONING = ('AI agents, GoHighLevel and n8n for US and UK remodeling contractors and GoHighLevel agencies: a 24/7 AI website receptionist, '
               'Supabase RAG knowledge bases, GoHighLevel pipelines and n8n workflows, built with the controls of bank operations.')
FLAGSHIP = '24/7 AI Website Receptionist'   # productized service name for the RAG agent + chat widget

SITE = 'https://opswaqarahmed.pages.dev'
EMAIL = 'meetwith.waqarahmed@gmail.com'  # shown on the site; keep the Formspree form pointed at the same inbox
LINKEDIN = 'https://www.linkedin.com/in/opswaqarahmed/'
LOOP_CASE = 'https://loop.org.pk/student-projects/supplier-quote-request-automation-ghl-n8n/'
UPDATED = ('2026-11-15', '15 November 2026')
ASSET_V = '31'                           # bump when css/js change, so browsers fetch the new files

# Social links: only URLs the owner has supplied. Empty value = link left out.
SOCIAL = [
    ('LinkedIn', LINKEDIN),
    ('YouTube', 'https://www.youtube.com/@opswaqarahmed'),
    ('GitHub', 'https://github.com/opswaqarahmed'),
    ('X', 'https://x.com/opswaqarahmed'),
    ('Facebook', 'https://www.facebook.com/opswaqarahmed'),
    ('Instagram', 'https://www.instagram.com/opswaqarahmed/'),
    ('Threads', 'https://www.threads.com/@opswaqarahmed'),
    ('TikTok', 'https://www.tiktok.com/@opswaqarahmed'),
    ('Linktree', 'https://linktr.ee/opswaqarahmed'),
]

# ---------------------------------------------------------------- PLACEHOLDERS
# Fill these in when you have the real thing. While a value is empty, the site simply
# leaves that element out, so nothing invented or half-finished is ever published.
CERT_ISSUER = 'LOOP Institute of Applied AI'
CERT_TITLE = 'GoHighLevel certification training'  # PLACEHOLDER: exact title printed on the certificate
CERT_DATE = ''             # PLACEHOLDER: completion date on the certificate, e.g. "October 2026"
HEADSHOT = '/assets/img/waqar-ahmed.jpg'   # real portrait, 800x800, in public/assets/img. Empty = WA mark is shown
BOOKING_URL = ''           # PLACEHOLDER: calendar link (GHL calendar, Cal.com...). Empty = audit form only
TESTIMONIALS = []          # PLACEHOLDER: real, approved quotes only: [('Quote text', 'Name', 'Role, Company')]
PRICE_FROM = {}            # PLACEHOLDER: e.g. {'Tier 1: AI knowledge base foundation': 'Typical range $X to $Y'}. Empty = "Quoted in writing after the audit"
CASE_SHOTS = {}            # PLACEHOLDER: sanitized screenshot per case study: {'supplier-quote-requests': ('/assets/img/x.png', 'Alt text')}
FORMSPREE_ID = 'moeezrno'  # the part after https://formspree.io/f/ . Used while INTAKE_WEBHOOK_URL is empty
CF_ANALYTICS_TOKEN = '36599263344846338d6b1fcb73837786'  # Cloudflare Web Analytics (cookie-free). Empty = no beacon

# GoHighLevel + n8n intake. Paste the n8n Webhook node's PRODUCTION URL here, e.g.
# 'https://YOUR-N8N-HOST/webhook/portfolio-intake'. While empty, the form keeps sending through Formspree.
# When you set it, also add the n8n host to connect-src in public/_headers (see build/README.md).
INTAKE_WEBHOOK_URL = ''    # PLACEHOLDER: [INSERT_N8N_INTAKE_WEBHOOK_URL]

# Live floating 24/7 AI Website Receptionist widget. Script URL plus any data attributes the widget needs.
# While empty, only the empty hook <div id="ai-receptionist-widget"> is placed on /contact/ and no script loads.
CHAT_WIDGET_SRC = ''       # PLACEHOLDER: e.g. 'https://widgets.leadconnectorhq.com/loader.js'
CHAT_WIDGET_ATTRS = ''     # PLACEHOLDER: e.g. 'data-resources-url="..." data-widget-id="..."'

# Walkthrough video for the AI Knowledge Base & RAG Loader case study (about 3.5 minutes).
# Use an EMBED url: https://www.youtube-nocookie.com/embed/VIDEO_ID  or  https://www.loom.com/embed/VIDEO_ID
KB_VIDEO_EMBED = ''        # PLACEHOLDER: [INSERT_YOUTUBE_OR_LOOM_EMBED_URL]

# PLACEHOLDERS for the Website Estimate Assistant (24/7 AI Website Receptionist) case study.
# Only facts you confirm go here. Each empty value is simply left off the page.
RECEPTIONIST = {
    'stack': 'RAG knowledge base (n8n + Gemini Embeddings + Supabase pgvector), website chat widget, GoHighLevel and n8n lead operations',
    'sources': 'Eight structured policy sections of demo company facts, loaded by the <a href="/projects/ai-knowledge-base-rag-loader/">AI Knowledge Base &amp; RAG Loader</a>',
    'handoff': '',      # what happens with a ready lead, e.g. 'Details saved as a GoHighLevel contact tagged ai-qualified'
    'guardrails': '',   # e.g. 'Answers only from the knowledge base; says so and offers a call when it does not know'
    'demo_url': '',     # public demo page or Loom video of the assistant
    'tested': [],       # sample-run results you recorded: [('12', 'test questions asked'), ('11', 'answered from the knowledge base')]
}


def cert_line():
    s = f'{CERT_ISSUER}, {CERT_TITLE}: completed'
    return s + (f' ({CERT_DATE})' if CERT_DATE else '')


FORM_ACTION = (INTAKE_WEBHOOK_URL or (f'https://formspree.io/f/{FORMSPREE_ID}' if FORMSPREE_ID
                                      else f'mailto:{EMAIL}?subject=Automation%20audit%20request'))
AUDIT = '/contact/#audit-form'
CTA = 'Request an automation audit'
CTA_NOTE = 'A 15-minute call about one workflow. No sales pitch. You keep the map of where AI agents, GoHighLevel and n8n fit, either way.'

NEWTAB = '<span class="visually-hidden"> (opens in a new tab)</span>'
EXT = 'rel="noopener noreferrer" target="_blank"'

NAV = [('Services', '/services/'), ('AI Receptionist', '/projects/website-estimate-assistant/'), ('Work', '/projects/'), ('About', '/about/'), ('Contact', '/contact/')]


# ---------------------------------------------------------------- Shell
def header(active):
    links = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if active == h else ""}>{n}</a></li>' for n, h in NAV)
    return f'''  <a class="skip-link" href="#main">Skip to main content</a>

  <header class="site-header on-navy">
    <div class="container header-inner">
      <a class="brand" href="/" aria-label="Waqar Ahmed, home">
        <img src="/assets/img/wa-mark.svg" alt="" width="40" height="40">
        <span class="brand-name">Waqar Ahmed<small>{LOCKUP_LINE}</small></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
        <span class="nav-toggle-bars" aria-hidden="true"></span>
        Menu
      </button>
      <nav id="site-nav" class="site-nav" aria-label="Main">
        <ul>
          {links}
          <li><a class="btn" href="{AUDIT}">{CTA}</a></li>
        </ul>
      </nav>
    </div>
  </header>
'''


BEACON = (f'\n  <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{CF_ANALYTICS_TOKEN}"}}\'></script>'
          if CF_ANALYTICS_TOKEN else '')


def widget_hook():
    """Hook for the live floating 24/7 AI Website Receptionist widget. No script loads until CHAT_WIDGET_SRC is set."""
    script = f'\n  <script src="{CHAT_WIDGET_SRC}" {CHAT_WIDGET_ATTRS} defer></script>' if CHAT_WIDGET_SRC else ''
    state = 'live' if CHAT_WIDGET_SRC else 'placeholder'
    return (f'  <!-- 24/7 AI Website Receptionist widget hook. Set CHAT_WIDGET_SRC in build/build.py to load the live widget. -->\n'
            f'  <div id="ai-receptionist-widget" data-widget="{FLAGSHIP}" data-state="{state}"></div>{script}')


def footer(widget=False):
    nav = ''.join(f'<li><a href="{h}">{n}</a></li>' for n, h in [('Home', '/')] + NAV)
    soc = ''.join(f'<li><a href="{u}" {EXT}>{n}{NEWTAB}</a></li>' for n, u in SOCIAL if u.startswith('https://'))
    return f'''
  <footer class="site-footer on-navy">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/" aria-label="Waqar Ahmed, home">
          <img src="/assets/img/wa-mark.svg" alt="" width="40" height="40" loading="lazy">
          <span class="brand-name">Waqar Ahmed<small>{LOCKUP_LINE}</small></span>
        </a>
        <p class="footer-tagline">{TAGLINE}</p>
        <p>{ROLE}. 24/7 AI website receptionists, GoHighLevel pipelines and n8n workflows for {MARKET}.</p>
        <p class="meta"><span>{BASE}</span><span>{REACH}</span><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <nav aria-labelledby="footer-explore">
        <h2 class="footer-h" id="footer-explore">Site</h2>
        <ul class="footer-links">{nav}</ul>
      </nav>
      <nav aria-labelledby="footer-social">
        <h2 class="footer-h" id="footer-social">Profiles</h2>
        <ul class="footer-links footer-links--2">{soc}</ul>
      </nav>
    </div>
    <div class="container"><div class="footer-bottom">
      <p>© 2026 {BRAND_HTML}. All rights reserved.</p>
      <nav aria-label="Legal and site files">
        <ul>
          <li><a href="/privacy/">Privacy</a></li>
          <li><a href="/terms/">Terms</a></li>
          <li><a href="/llms.txt" title="Plain-text summary of this site for AI assistants">AI summary</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </nav>
    </div></div>
  </footer>

{widget_hook() if widget else ''}
  <script src="/js/main.js?v={ASSET_V}"></script>{BEACON}
</body>
</html>
'''


OG_ALT = 'Waqar Ahmed, AI Automation and Agentic AI Specialist. Make every lead move forward. 24/7 AI website receptionists, GoHighLevel, n8n and Supabase RAG for US and UK remodeling contractors and GoHighLevel agencies.'


def head(title, desc, path, og_type='website', jsonld=None, noindex=False):
    url = SITE + path
    ld = ''
    if jsonld:
        ld = '\n  <script type="application/ld+json">\n' + json.dumps(jsonld, ensure_ascii=False, separators=(',', ':')) + '\n  </script>'
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ''
    canon = '' if noindex else f'\n  <link rel="canonical" href="{url}">'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="Waqar Ahmed">
  <meta name="theme-color" content="#0B1626">{robots}{canon}

  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{BRAND_HTML}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{OG_ALT}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/assets/img/og-image.png">
  <meta name="twitter:image:alt" content="{OG_ALT}">

  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/assets/img/wa-mark.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preload" href="/assets/fonts/manrope-variable.ttf" as="font" type="font/ttf" crossorigin>
  <link rel="preload" href="/assets/fonts/dm-sans-latin.woff" as="font" type="font/woff" crossorigin>
  <link rel="stylesheet" href="/css/site.css?v={ASSET_V}">{ld}
</head>
<body>
'''


def crumbs(*items):
    """BreadcrumbList JSON-LD. items = (name, path) ... last item has no link."""
    out = []
    for i, (n, p) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": n}
        if p:
            el["item"] = SITE + p
        out.append(el)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": out}


def graph(*nodes):
    return {"@context": "https://schema.org", "@graph": [{k: v for k, v in n.items() if k != "@context"} for n in nodes]}


def crumb_nav(*items):
    lis = [f'<li><a href="{p}">{n}</a></li>' if p else f'<li><span aria-current="page">{n}</span></li>' for n, p in items]
    return '<nav class="breadcrumb" aria-label="Breadcrumb"><ol>' + ''.join(lis) + '</ol></nav>'


def page_hero(h1, lead, crumb_items, extra='', compact=False, kicker=''):
    cls = 'page-hero on-navy' + (' page-hero--compact' if compact else '')
    k = f'<p class="kicker">{kicker}</p>' if kicker else ''
    return f'''    <div class="{cls}">
      <div class="container">
        {crumb_nav(*crumb_items)}
        {k}<h1>{h1}</h1>
        <p class="lead">{lead}</p>{extra}
      </div>
    </div>
'''


def chip(kind, text):
    return f'<span class="chip chip--{kind}">{text}</span>'


def ticks(items, cls='ticks'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def tidy(html):
    """Drop indentation and blank lines (keeps pages light; no <pre> blocks on this site)."""
    return re.sub(r'\n[ \t]+', '\n', re.sub(r'\n\s*\n', '\n', html))


def write(path, html, raw=False):
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html if raw else tidy(html), encoding='utf-8')


# ---------------------------------------------------------------- Shared content
# (label, title, stack, description, bullets). Three productized packages + one agency partner track.
SERVICES = [
    ('Tier 1', 'AI knowledge base foundation', 'n8n + Gemini Embeddings + Supabase pgvector',
     'A one-click RAG library built from your approved business facts, organised into eight or more policy sections, so an AI assistant answers from verified company information instead of inventing prices or permit promises.',
     ['One n8n run clears and reloads the library, with no duplicates', 'Policy sections such as services, service area, pricing rules and permits', 'Stored in your own Supabase project with Row Level Security']),
    ('Tier 2 · Flagship', f'{FLAGSHIP} + GoHighLevel pipeline', 'RAG chat widget + n8n + GoHighLevel',
     'A RAG chat widget on your website that answers after-hours enquiries from verified company facts, qualifies the lead, and syncs the contact, tags and opportunity stage directly into GoHighLevel.',
     ['Answers grounded in your knowledge base, day and night', 'Lead qualified in the chat before your team picks it up', 'Contact, tags and opportunity stage created in GoHighLevel', 'Hands over to a person for prices and anything outside your content']),
    ('Tier 3', 'Lead operations, supplier quote automation and monthly retainer', 'GoHighLevel + n8n',
     'Multi-channel lead routing, automated supplier quote matching, weekly executive reporting and ongoing knowledge-base refreshes, run as a monthly retainer.',
     ['Leads from forms, chat and calls routed into one GoHighLevel pipeline', 'Suppliers matched by trade and city, with a dated follow-up task', 'Weekly executive report built from the same CRM data', 'Knowledge base refreshed as your services and policies change']),
    ('Agency partner track', 'White-label n8n + Supabase RAG backend', 'For US and UK GoHighLevel agencies',
     'Technical n8n and Supabase RAG backend fulfilment for US and UK GoHighLevel marketing agencies that serve home-service contractors. Your agency keeps the client relationship and the GoHighLevel account. I build the backend behind your brand.',
     ['n8n workflows and Supabase (pgvector) knowledge bases for each client sub-account', 'Built to your naming, documentation and handover standards', 'Access through team invites, with no direct client contact unless you ask']),
]

HANDOFFS = [
    ('Website visit to enquiry',
     'A visitor has a question at 10 pm. Nobody answers, so they leave and ask the next contractor.',
     'A 24/7 AI receptionist answers from your own content and captures the enquiry with the details your team needs.'),
    ('Enquiry to first reply',
     'Form and chat enquiries wait until morning, or never get a reply.',
     'Every form, call and chat becomes a tagged contact in GoHighLevel, and the first reply goes out automatically.'),
    ('Reply to site visit',
     'Nobody chases the leads that go quiet, and a large remodel waits in the same queue as a small repair.',
     'n8n scores each lead. Follow-up runs until the customer replies or books, then stops.'),
    ('Site visit to supplier quote',
     'Someone picks suppliers and emails each one by hand. Suppliers get missed and the quote waits.',
     'Suppliers are matched by trade and city, each gets its own request, and a dated follow-up task lands in the CRM.'),
    ('Quote to the owner\'s view',
     'Leads, visits and quotes live in inboxes, notebooks and spreadsheets.',
     'One pipeline shows every lead\'s stage, source and next step, and reports are built from the same data.'),
]

PRINCIPLES = [
    ('Every entry has an owner and a status.', 'Every lead, and every action an AI agent takes, has an owner, a status and a record.'),
    ('Nothing is posted without authority.', 'AI answers come from your approved content. Prices, promises and decisions stay with your team.'),
    ('Exceptions are dealt with, not hidden.', 'Every workflow has an error branch. When a step fails or the AI is unsure, a person is told.'),
    ('Access is given by role.', 'I work through a team-member invite with only the access the work needs. Never your password.'),
    ('The record has to explain itself.', 'CRM notes, written documentation and a Loom walkthrough, so your team can run it without me.'),
]

PROCESS = [
    ('Audit', 'A 15-minute call. We trace one workflow and find where leads stall and where AI would actually help.'),
    ('Map and scope', 'We agree the outcome, what is included, third-party and AI usage costs, and turnaround in writing before any build.'),
    ('Build and test', 'Built inside your accounts with test records and test questions first: duplicates, missing data, failed actions and questions the AI should not answer.'),
    ('Hand over', 'Documentation and a Loom walkthrough. You own every workflow, agent, knowledge base, login and record.'),
]

TIERS = [
    ('Tier 1: AI knowledge base foundation', 'Agreed in the scope',
     'Your approved business facts structured into policy sections, embedded with Gemini Embeddings and stored in Supabase pgvector, with a one-click n8n refresh workflow.'),
    (f'Tier 2: {FLAGSHIP} + GoHighLevel pipeline', 'Agreed in the scope',
     'Everything in Tier 1, plus the RAG chat widget on your website, lead qualification, and contacts, tags and opportunity stages synced into GoHighLevel.'),
    ('Tier 3: Lead operations and monthly retainer', 'Monthly, agreed in the scope',
     'Multi-channel lead routing, supplier quote automation, weekly executive reporting and ongoing knowledge-base refreshes in GoHighLevel and n8n.'),
    ('White-label partner track', 'Per client, agreed with your agency',
     'n8n and Supabase RAG backend fulfilment for US and UK GoHighLevel agencies, delivered under your brand.'),
]
PRICE_DEFAULT = 'Quoted in writing after the audit'

FIT_FOR = [f'US and UK remodeling and home-improvement contractors ({TRADES_LINE}) with steady enquiries that stall between first contact, site visit and quote.',
           'Owners who want AI to answer and qualify enquiries, with a person still in charge of prices and promises.',
           'Teams already on GoHighLevel, or ready to run their own GoHighLevel subscription.',
           'GoHighLevel marketing agencies that serve home-service contractors and need an n8n and Supabase RAG backend builder.',
           'Businesses that want documented systems their own team can run.']
FIT_NOT = ['Anyone looking for an ad agency or bought leads. I build the systems, not the traffic.',
           'An AI that quotes prices or makes commitments with no human check.',
           'Cold SMS or email blasts to people who never opted in.',
           'Sharing account passwords instead of using team invites.']

FAQ = [
    ('What is the 24/7 AI Website Receptionist?', 'An AI agent with a chat widget on your website. It answers visitor questions from a knowledge base built from your own approved content (this is called retrieval-augmented generation, or RAG), and captures the enquiry so a person on your team can follow up.'),
    ('Will the AI make things up or quote prices?', 'It is set up to answer from your approved content, and to hand over to a person when the answer is not there. Prices, commitments and anything that needs judgement stay with your team. We agree these rules in the scope and test them with real questions before launch.'),
    ('What does "agentic AI" mean for my business?', 'An AI agent does more than chat: it can take steps, such as looking something up, filling in a CRM record or starting a follow-up. I build those steps inside workflows with logs, limits and a human checkpoint, so you can see and approve what the agent does.'),
    ('Do I need a GoHighLevel account?', 'For CRM work, yes. I build inside your GoHighLevel account, so you own the workflows, contacts and data. The AI receptionist is added to the website you already have.'),
    ('Will you need my password?', 'No. I ask for a team-member invite with the access the work needs, never your password.'),
    ('When do you use n8n instead of GoHighLevel alone?', "GoHighLevel runs the CRM process: forms, pipelines, calendars, follow-up and tasks. I add n8n when the work needs integration, data handling, AI agent steps or exception paths that GoHighLevel can't do well alone."),
    ('What does it cost?', 'The build fee is quoted in writing after the audit, before any work starts. Running costs depend on your own plans, such as GoHighLevel, n8n hosting, AI model usage and any email or SMS usage. These are listed in the scope too, so there are no surprises.'),
    ('How do you test before going live?', 'I build with test records and test questions first, and check normal cases, duplicates, missing data, failed actions and questions the AI should decline, against tests we agree in the scope. Then I hand over with notes on ownership, monitoring and recovery.'),
    ('Where are you based, and who do you work with?', f"I'm based in {BASE}, and I work remotely with remodeling and home-improvement contractors in the US and UK, and with GoHighLevel agencies that serve them. Live calls are booked inside your business day, and everything is built inside your own accounts."),
    ('Do you work white-label for GoHighLevel agencies?', 'Yes. For US and UK GoHighLevel agencies that serve home-service contractors, I build the n8n workflows and the Supabase (pgvector) RAG knowledge base behind the agency\'s own brand. The agency keeps the client relationship and the GoHighLevel account, and I work through team invites.'),
    ('Are the projects on this site client work?', 'No. They are reference / sandbox builds for Elite Home Renovations, a practice company, using test or demo data. They are not paid client work. Results are labelled as tested in a sample run, as build specs, or as estimates.'),
]

PERSON = {
    "@type": "Person", "@id": SITE + "/#person", "name": "Waqar Ahmed", "alternateName": BRAND, "url": SITE + "/",
    "image": SITE + (HEADSHOT or "/assets/img/apple-touch-icon.png"),
    "jobTitle": ROLE_TXT,
    "description": "AI Automation & Agentic AI Specialist for US and UK remodeling and home-improvement contractors and GoHighLevel agencies: 24/7 AI website receptionists (RAG), GoHighLevel pipelines, n8n workflows and Supabase pgvector knowledge bases. MBA with about eight years in branch banking operations at MCB Bank. Based in Khairpur District, Sindh, Pakistan; works remotely.",
    "address": {"@type": "PostalAddress", "addressLocality": "Khairpur District", "addressRegion": "Sindh", "addressCountry": "PK"},
    "knowsAbout": ["AI automation", "Agentic AI", "AI agents", "AI website receptionist", "Retrieval-augmented generation (RAG)", "GoHighLevel", "n8n", "Supabase pgvector", "Google Gemini embeddings", "Workflow automation", "CRM automation", "Lead qualification", "Supplier quote automation"],
    "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "LOOP GoHighLevel certification training (completed)",
                      "recognizedBy": {"@type": "Organization", "name": "LOOP Institute of Applied AI", "url": "https://loop.org.pk/"}},
    "sameAs": [u for _, u in SOCIAL if u],
    "subjectOf": {"@type": "CreativeWork", "name": "Supplier quote request automation (GHL + n8n)", "url": LOOP_CASE},
}
AREAS = [{"@type": "Country", "name": "United States"}, {"@type": "Country", "name": "United Kingdom"}]   # primary market; delivery is remote
PRO_SERVICE = {
    "@type": "ProfessionalService", "@id": SITE + "/#service", "name": BRAND, "url": SITE + "/",
    "image": SITE + "/assets/img/og-image.png",
    "description": "Remote AI automation and agentic AI for US and UK remodeling contractors and GoHighLevel agencies: Supabase RAG knowledge bases, 24/7 AI website receptionists, GoHighLevel pipelines, n8n lead operations and white-label n8n + Supabase RAG backend fulfilment.",
    "audience": {"@type": "BusinessAudience", "name": "US and UK residential remodeling and home-improvement contractors; GoHighLevel marketing agencies"},
    "slogan": TAGLINE, "founder": {"@id": SITE + "/#person"}, "employee": {"@id": SITE + "/#person"},
    "areaServed": AREAS, "serviceType": [s[1] for s in SERVICES],
    "knowsAbout": ["AI automation", "Agentic AI", "AI agents", "RAG", "GoHighLevel", "n8n", "Supabase pgvector", "Workflow automation"],
    "sameAs": [u for _, u in SOCIAL if u],
}


def booking_btn():
    return f'<a class="btn btn--quiet ext" href="{BOOKING_URL}" {EXT}>Book a time directly{NEWTAB}</a>' if BOOKING_URL else ''


def cta_band(h2='Where do your leads get stuck?',
             p="Tell me the manual process, the tools you already use and what a better result would look like. I'll reply with where an AI agent or an automation would help first, and where it wouldn't."):
    return f'''
    <section class="section section--navy on-navy" aria-labelledby="cta-title">
      <div class="container cta">
        <div>
          <h2 id="cta-title">{h2}</h2>
          <p>{p}</p>
          <div class="btn-row">
            <a class="btn" href="{AUDIT}">{CTA}</a>
            {booking_btn()}
            <a class="btn btn--quiet ext" href="{LINKEDIN}" {EXT}>Message me on LinkedIn{NEWTAB}</a>
          </div>
        </div>
        <div>
          <h3>What happens after you ask</h3>
          <ol class="next" style="margin-top:16px">
            <li><div><strong>You send the short form.</strong> It takes about two minutes.</div></li>
            <li><div><strong>I reply by email.</strong> We set up a 15-minute call.</div></li>
            <li><div><strong>We map one workflow together.</strong> You keep the map either way.</div></li>
          </ol>
        </div>
      </div>
    </section>
'''


def services_rows():
    return '<ul class="rows">' + ''.join(
        f'<li><div><p class="flag">{lab}</p><h3>{t}</h3><p class="tools">{st}</p></div><p>{d}</p>{ticks(b)}</li>'
        for lab, t, st, d, b in SERVICES) + '</ul>'


def handoff_table():
    rows = ''.join(f'<tr><th scope="row">{a}</th><td data-label="Where it stalls today">{b}</td>'
                   f'<td data-label="What the system does">{c}</td></tr>' for a, b, c in HANDOFFS)
    return ('<table class="ruled stack"><caption class="visually-hidden">Five handoffs where leads stall, and what the system does at each</caption>'
            '<thead><tr><th scope="col">Handoff</th><th scope="col">Where it stalls today</th><th scope="col">What the system does</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')


def principles_block():
    return ('<div class="principles-head" aria-hidden="true"><span>In a bank branch</span><span>In your AI and lead systems</span></div>'
            '<ul class="principles">' + ''.join(
                f'<li><span class="from"><span class="visually-hidden">In a bank branch: </span>{a}</span>'
                f'<span class="to"><span class="visually-hidden">In your AI and lead systems: </span>{b}</span></li>' for a, b in PRINCIPLES) + '</ul>')


def steps_html(across=True):
    return f'<ol class="steps{" steps--across" if across else ""}">' + ''.join(
        f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in PROCESS) + '</ol>'


def fit_html():
    return (f'<div class="fit"><div><h3>A good fit</h3>{ticks(FIT_FOR)}</div>'
            f'<div><h3>Not a fit</h3>{ticks(FIT_NOT, "crosses")}</div></div>')


def faq_html():
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f'''
    <section id="faq" class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head"><h2 id="faq-title">Questions owners ask first</h2></div>
        <div class="faq">{items}</div>
      </div>
    </section>
'''


def testimonials_html():
    """Only rendered when TESTIMONIALS holds real, approved quotes."""
    if not TESTIMONIALS:
        return ''
    items = ''.join(f'<li><p>“{q}”</p><p class="small"><strong>{n}</strong>, {r}</p></li>' for q, n, r in TESTIMONIALS)
    return f'''
    <section class="section section--white" aria-labelledby="said-title">
      <div class="container">
        <div class="section-head"><h2 id="said-title">What clients say</h2></div>
        <ul class="rows rows--2">{items}</ul>
      </div>
    </section>
'''


SUPPLIER_TABLE = '''<table class="ruled">
            <caption class="visually-hidden">Results from one Full Home test run of the supplier quote workflow</caption>
            <thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">Evidence</th></tr></thead>
            <tbody>
              <tr><th scope="row">Matching suppliers found</th><td class="num"><span class="big">4</span></td><td>''' + chip('tested', 'Tested') + '''</td></tr>
              <tr><th scope="row">Emails accepted by Gmail</th><td class="num"><span class="big">4</span></td><td>''' + chip('tested', 'Tested') + '''</td></tr>
              <tr><th scope="row">Send failures in that run</th><td class="num"><span class="big">0</span></td><td>''' + chip('tested', 'Tested') + '''</td></tr>
              <tr><th scope="row">CRM note and follow-up task recorded</th><td>Yes</td><td>''' + chip('tested', 'Tested') + '''</td></tr>
              <tr><th scope="row">Delivery to supplier inboxes</th><td class="nowrap">Not confirmed</td><td>''' + chip('plain', 'Not tested') + '''</td></tr>
              <tr><th scope="row">Time saved each month</th><td class="nowrap">About 17 hours</td><td>''' + chip('estimate', 'Estimate') + '''</td></tr>
            </tbody>
          </table>'''
SUPPLIER_NOTE = 'One sample run in a sandbox account. Accepted by Gmail does not mean delivered. The time saving assumes eight site visits a week and was not measured with a live business.'

# ---------------------------------------------------------------- Case studies (data)
CASES = [
    {'slug': 'website-estimate-assistant', 'title': 'Website Estimate Assistant', 'crumb': FLAGSHIP, 'tools': 'RAG chat widget + n8n + GoHighLevel',
     'card': f'A RAG agent and chat widget for the Elite Home Renovations website that answers visitor questions from the business\'s own verified facts, day or night. Offered to clients as the {FLAGSHIP}.',
     'chip': ('sandbox', 'Reference / sandbox build'), 'flag': FLAGSHIP, 'about': ['AI agents', 'Retrieval-augmented generation', 'Website chat', 'GoHighLevel', 'n8n']},
    {'slug': 'ai-knowledge-base-rag-loader', 'title': 'AI Knowledge Base &amp; RAG Loader', 'plain': 'AI Knowledge Base and RAG Loader',
     'crumb': 'AI knowledge base and RAG loader', 'tools': 'n8n + Supabase pgvector + Gemini Embeddings',
     'card': 'A one-click n8n workflow that clears and reloads eight structured policy sections into Supabase pgvector with Gemini Embeddings, so the AI receptionist answers from verified company facts.',
     'chip': ('sandbox', 'Reference / sandbox build'), 'about': ['Retrieval-augmented generation', 'n8n', 'Supabase pgvector', 'Google Gemini embeddings', 'GoHighLevel']},
    {'slug': 'supplier-quote-requests', 'title': 'From site visit to supplier quote', 'crumb': 'Supplier quote requests', 'tools': 'GoHighLevel + n8n + Gmail',
     'card': 'After a site visit, n8n matches suppliers by trade and city, sends each one a quote request, and logs a note and a dated follow-up task in GoHighLevel.',
     'chip': ('tested', 'Tested in one sample run')},
    {'slug': 'quote-intake-followup', 'title': 'Quote intake and lead scoring', 'crumb': 'Quote intake and lead scoring', 'tools': 'n8n + GoHighLevel',
     'card': 'An 8-node n8n workflow scores new GoHighLevel contacts every 10 minutes and routes hot, warm and nurture leads to the right next step.',
     'chip': ('sandbox', 'Reference / sandbox build')},
    {'slug': 'lead-to-site-visit', 'title': 'Lead-to-site-visit system', 'crumb': 'Lead-to-site-visit system', 'tools': 'GoHighLevel',
     'card': 'A Free Estimate Request funnel, two pipelines, a 60-minute site-visit calendar and a four-email follow-up that stops when a visit is booked.',
     'chip': ('sandbox', 'Reference / sandbox build')},
    {'slug': 'reporting-dashboards', 'title': 'Reporting and lead-source attribution', 'crumb': 'Reporting and attribution', 'tools': 'GoHighLevel',
     'card': 'Five UTM contact fields, source-based workflow branching and owner notifications, so every lead shows where it came from.',
     'chip': ('sandbox', 'Reference / sandbox build, demo data')},
    {'slug': 'ai-customer-experiences', 'title': 'AI customer experiences', 'crumb': 'AI customer experiences', 'tools': 'GoHighLevel Conversation AI + Voice AI',
     'card': 'A 24/7 chat and voice qualifier, plus a post-job review system that routes happy and unhappy customers differently.',
     'chip': ('sandbox', 'Reference / sandbox build')},
]
C = {c['slug']: c for c in CASES}


def case_list(cases=CASES):
    return '<ul class="case-list">' + ''.join(
        f'<li{" class=is-flag" if c.get("flag") else ""}><div>' + (f'<p class="flag">{c["flag"]}</p>' if c.get("flag") else '') +
        f'<h3><a href="/projects/{c["slug"]}/">{c["title"]}</a></h3><p class="tools">{c["tools"]}</p></div>'
        f'<p>{c["card"]}</p>{chip(*c["chip"])}</li>' for c in cases) + '</ul>'


SANDBOX_LINE = ('These are reference / sandbox builds for Elite Home Renovations, a practice company, '
                'using test or demo data. They show how I build with AI agents, GoHighLevel and n8n. They are not paid client work.')
N_CASES = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten'][len(CASES)]

# ---------------------------------------------------------------- Home
# The agent log: brand signature. An illustration of how the pieces work together, labelled as such.
LEDGER = [
    ('21:47', 'Website chat opened', 'Homeowner asks about a kitchen remodel.', 'Answered', ''),
    ('21:47', 'Answer from the knowledge base', 'Process, service area and next step, from verified company facts.', 'Grounded', ''),
    ('21:50', 'Enquiry details captured', 'Project type, timeline and city.', 'Captured', ''),
    ('21:50', 'Contact and opportunity in GoHighLevel', 'Source tagged. Stage: new lead. Duplicate check passed.', 'Posted', ''),
    ('21:51', 'Lead scored in n8n', 'Marked hot. Call task due 9:00 next morning.', 'Assigned', ''),
    ('09:00', 'Owner calls back', 'A person takes over, with the details already on the record.', 'Open', ' posted--open'),
]
ledger_rows = ''.join(
    f'<tr><td>{t}</td><td><strong>{a}</strong><span class="sub">{b}</span></td><td><span class="posted{cls}">{s}</span></td></tr>'
    for t, a, b, s, cls in LEDGER)
LEDGER_HTML = f'''<figure class="ledger" aria-labelledby="ledger-title">
          <div class="ledger-head"><span class="ledger-title" id="ledger-title"><span class="live-dot" aria-hidden="true"></span>Agent log</span><span class="ledger-tag">Illustrative example</span></div>
          <table>
            <caption class="visually-hidden">Illustrative example: one after-hours website enquiry, from AI receptionist to owner call-back</caption>
            <thead><tr><th scope="col">Time</th><th scope="col">Entry</th><th scope="col">Status</th></tr></thead>
            <tbody>{ledger_rows}</tbody>
          </table>
          <figcaption class="ledger-foot"><span>Answered after hours: <strong>1</strong></span><span>Leads unaccounted for: <strong>0</strong></span></figcaption>
        </figure>'''

CALC_HTML = '''<div class="calc" id="calc" hidden>
          <div>
            <h3>What is the manual work costing you?</h3>
            <p>Put in your own numbers. This is plain arithmetic on what you enter: the cost of the manual work today, not a promise of savings.</p>
          </div>
          <form class="calc-form" novalidate>
            <div class="field"><label for="c-visits">Site visits per week</label><input id="c-visits" type="number" inputmode="numeric" min="0" max="500" step="1" value="8"></div>
            <div class="field"><label for="c-min">Admin minutes per visit <span class="hint">(supplier emails, chasing, CRM updates)</span></label><input id="c-min" type="number" inputmode="numeric" min="0" max="600" step="5" value="30"></div>
            <div class="field"><label for="c-rate">Hourly cost of that time <span class="hint">(your currency, optional)</span></label><input id="c-rate" type="number" inputmode="decimal" min="0" step="1" value=""></div>
          </form>
          <div class="calc-out" role="status" aria-live="polite">
            <p class="calc-label">Manual admin each month</p>
            <p class="calc-big"><span id="c-hours">17</span> hours</p>
            <p id="c-cost" class="calc-cost"></p>
            <p class="small">Starting values are examples. In the audit we measure your real figure before anyone estimates a saving.</p>
          </div>
        </div>'''

STACK = [('AI agents and RAG', 'Knowledge bases, retrieval and agent steps'),
         ('GoHighLevel', 'Contacts, tags, pipelines, workflows'),
         ('n8n', 'Integrations, scoring, agent workflows'),
         ('Supabase RAG knowledge bases', 'pgvector, Gemini Embeddings, Row Level Security')]
STACK_HTML = ('<ul class="stack-strip" aria-label="What I build with">' +
              ''.join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in STACK) + '</ul>')

home_title = 'AI Automation &amp; Agentic AI Specialist for US &amp; UK Remodelers | Waqar Ahmed'
home_desc = ('AI Automation &amp; Agentic AI Specialist: 24/7 AI website receptionists, GoHighLevel pipelines and n8n workflows '
             'for US &amp; UK remodelers and GoHighLevel agencies.')
home_ld = graph(
    {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND,
     "alternateName": "Waqar Ahmed", "inLanguage": "en", "publisher": {"@id": SITE + "/#person"}},
    PERSON, PRO_SERVICE)

home = head(home_title, home_desc, '/', jsonld=home_ld) + header('/') + f'''
  <main id="main">
    <section class="hero on-navy" aria-labelledby="home-title">
      <div class="container hero-grid">
        <div>
          <p class="kicker kicker--pill">{ROLE}</p>
          <h1 id="home-title">AI receptionists, GoHighLevel pipelines and n8n workflows that make every lead <span class="glow">move forward.</span></h1>
          <p class="hero-lead">I'm an {ROLE}. I build 24/7 AI website receptionists, GoHighLevel pipelines and n8n workflows for US and UK remodeling contractors, and the n8n and Supabase RAG backend for GoHighLevel agencies that serve them. Every enquiry is answered, qualified, followed up and accounted for.</p>
          <div class="btn-row">
            <a class="btn" href="{AUDIT}">{CTA}</a>
            <a class="btn btn--quiet" href="/projects/website-estimate-assistant/">See the AI receptionist</a>
          </div>
          <p class="btn-note">{CTA_NOTE}</p>
        </div>
        {LEDGER_HTML}
      </div>
      <div class="hero-facts">
        <div class="container">
          <ul aria-label="At a glance">
            <li><strong>About 8 years in bank operations</strong>Branch operations at MCB Bank, before automation.</li>
            <li><strong>In AI automation since May 2022</strong>{cert_line().replace(CERT_ISSUER + ", ", "LOOP ")}.</li>
            <li><strong>You own everything</strong>Built in your accounts through a team invite, never a password.</li>
            <li><strong>US and UK contractors and agencies</strong>Remote, from {BASE}.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section--tight" aria-label="What I build with">
      <div class="container">{STACK_HTML}</div>
    </section>

    <section class="section section--white" aria-labelledby="stall-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker">The problem</p>
          <h2 id="stall-title">Most leads aren't lost. They stall between handoffs.</h2>
          <p>A renovation job passes through five handoffs before it becomes a quote. Each one is a place where a lead can sit with no answer, no owner and no next step.</p>
        </div>
        {handoff_table()}
        {CALC_HTML}
      </div>
    </section>

    <section class="section" aria-labelledby="what-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker">What I build</p>
          <h2 id="what-title">Three packages and an agency partner track.</h2>
          <p>We start with the handoff that costs you the most, and build the smallest system that fixes it. The knowledge base keeps the AI agent to verified facts. The AI receptionist answers and qualifies. GoHighLevel runs the pipeline. n8n connects the rest.</p>
        </div>
        {services_rows()}
        <div class="btn-row"><a class="btn btn--quiet" href="/services/">Packages, partner track and FAQ</a></div>
      </div>
    </section>

    <section class="section section--navy on-navy section--glow" aria-labelledby="flag-title">
      <div class="container statement">
        <div>
          <p class="kicker">Flagship service</p>
          <h2 id="flag-title">The {FLAGSHIP}.</h2>
          <p style="margin-top:18px">Homeowners research at night and on weekends. An AI receptionist on your website answers their questions from your own verified company facts, qualifies the lead, then syncs the contact, tags and opportunity stage into GoHighLevel through n8n, so your team can call back with the details already on the record.</p>
          {ticks(['Answers grounded in your own knowledge base, not the open internet', 'Prices, promises and judgement calls stay with your team', 'Every conversation leaves a record your team can read'])}
          <div class="btn-row"><a class="btn" href="/projects/website-estimate-assistant/">See how it was built</a></div>
        </div>
        <div>
          <ol class="chat" aria-label="Illustrative website chat">
            <li class="chat-in"><span class="who">Visitor, 21:47</span>Do you do kitchen remodels in my area, and how does the estimate work?</li>
            <li class="chat-out"><span class="who">AI receptionist</span>Answers from the company's service area and estimate process pages, then asks for the project type, timeline and city.</li>
            <li class="chat-out"><span class="who">AI receptionist</span>Offers a call-back from the team for anything about price.</li>
          </ol>
          <p class="statement-note">Illustration of the conversation pattern. Not a transcript from a live business.</p>
        </div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="proof-title">
      <div class="container statement">
        <div>
          <p class="kicker">Evidence</p>
          <h2 id="proof-title">Evidence, labelled for what it is.</h2>
          <p style="margin-top:18px;color:var(--slate)">I'd rather show you one honest test than ten big claims. This is the supplier quote workflow, run once on a Full Home test job. Every figure says whether it was tested or estimated.</p>
          <div class="btn-row"><a class="btn btn--quiet" href="/projects/supplier-quote-requests/">Read how each number was produced</a></div>
        </div>
        <div>
          <div class="table-wrap">{SUPPLIER_TABLE}</div>
          <p class="statement-note">{SUPPLIER_NOTE}</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="work-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker">Work</p>
          <h2 id="work-title">{N_CASES} reference builds for one renovation business.</h2>
          <p>{SANDBOX_LINE}</p>
        </div>
        {case_list()}
      </div>
    </section>
{testimonials_html()}
    <section class="section section--navy on-navy" aria-labelledby="why-title">
      <div class="container split">
        <div>
          <p class="kicker">Why trust the agents</p>
          <h2 id="why-title">Agentic AI, run the way a bank branch runs its day.</h2>
          <p style="margin-top:18px">Before automation, I spent about eight years in branch banking operations at MCB Bank, where every entry has to be accounted for before the day closes. I build AI agents and lead systems with the same controls.</p>
          <div class="btn-row"><a class="btn btn--quiet" href="/about/">More about me</a></div>
        </div>
        <div>{principles_block()}</div>
      </div>
    </section>

    <section class="section" aria-labelledby="how-title">
      <div class="container">
        <div class="section-head">
          <p class="kicker">How we work</p>
          <h2 id="how-title">Four steps. Scope agreed in writing first.</h2>
        </div>
        {steps_html()}
        <div class="own on-navy" style="margin-top:56px">
          <h3>Everything is built in accounts you own.</h3>
          {ticks(['You own every workflow, agent, knowledge base, contact and login.', 'I work through a role-based team invite, never your password.', 'You can remove my access at any time. Nothing stops working when you do.'])}
        </div>
      </div>
    </section>
{cta_band()}  </main>
''' + footer()
write('index.html', home)

# ---------------------------------------------------------------- Services
tier_rows = ''.join(
    f'<tr><th scope="row">{n}</th><td data-label="What\'s included">{w}</td><td data-label="Turnaround" class="num">{d}</td>'
    f'<td data-label="Price">{PRICE_FROM.get(n, PRICE_DEFAULT)}</td></tr>' for n, d, w in TIERS)
SVC_LD = graph(
    crumbs(('Home', '/'), ('Services', None)),
    {"@type": "Service", "@id": SITE + "/services/#service",
     "name": "AI agents, GoHighLevel and n8n automation for remodeling contractors and GoHighLevel agencies",
     "serviceType": "AI automation", "provider": {"@id": SITE + "/#person"},
     "areaServed": AREAS, "url": SITE + "/services/",
     "description": "Three productized packages and an agency partner track: AI knowledge base foundation (n8n, Gemini Embeddings, Supabase pgvector), 24/7 AI Website Receptionist with GoHighLevel pipeline, lead operations and supplier quote automation in GoHighLevel and n8n, and white-label n8n + Supabase RAG backend fulfilment for GoHighLevel agencies.",
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Packages and partner track", "itemListElement": [
         {"@type": "Offer", "name": n, "description": f"{w} Turnaround: {d}.",
          "itemOffered": {"@type": "Service", "name": n}} for n, d, w in TIERS]}},
    {"@type": "FAQPage", "@id": SITE + "/services/#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
svc = head('AI Agents, GoHighLevel &amp; n8n Packages for Remodelers | Waqar Ahmed',
           'Three packages and an agency track: Supabase RAG knowledge base, 24/7 AI Website Receptionist with GoHighLevel pipeline, and n8n lead operations.',
           '/services/', jsonld=SVC_LD) + header('/services/') + f'''
  <main id="main">
{page_hero('AI where it helps. Automation where it pays. A person where it matters.', "Three productized packages for US and UK remodeling contractors, and a white-label track for GoHighLevel agencies. Each one is built from AI agents, GoHighLevel and n8n, scoped in writing, tested, and delivered remotely inside accounts you own.", [('Home', '/'), ('Services', None)], kicker='Services')}
    <section class="section" aria-labelledby="svc-title">
      <div class="container">
        <div class="section-head"><h2 id="svc-title">Three packages and an agency partner track</h2><p>Each package builds on the one before it. Start with the knowledge base, add the AI receptionist and the GoHighLevel pipeline, then run lead operations on a monthly retainer.</p></div>
        {services_rows()}
      </div>
    </section>

    <section class="section section--white" aria-labelledby="tiers-title">
      <div class="container">
        <div class="section-head">
          <h2 id="tiers-title">Ways to start</h2>
          <p>Turnaround counts from the day the scope is agreed and team-member access is in place.</p>
        </div>
        <div class="table-wrap">
          <table class="ruled stack">
            <caption class="visually-hidden">Packages, turnaround times and pricing</caption>
            <thead><tr><th scope="col">Package</th><th scope="col">What's included</th><th scope="col">Turnaround</th><th scope="col">Price</th></tr></thead>
            <tbody>{tier_rows}</tbody>
          </table>
        </div>
        <div class="btn-row"><a class="btn" href="{AUDIT}">{CTA}</a></div>
        <p class="btn-note">{CTA_NOTE}</p>
      </div>
    </section>

    <section class="section" aria-labelledby="proc-title">
      <div class="container">
        <div class="section-head">
          <h2 id="proc-title">How a build runs</h2>
          <p>AI and automation should make work easier to see and easier to recover. Every project has agreed tests, a human owner and a fallback.</p>
        </div>
        {steps_html()}
      </div>
    </section>

    <section class="section section--navy on-navy" aria-labelledby="std-title">
      <div class="container split">
        <div>
          <h2 id="std-title">The standard every build is held to.</h2>
          <p style="margin-top:18px">About eight years in bank branch operations taught me how records are kept when mistakes cost money. These are the same controls, applied to your AI agents and your leads.</p>
        </div>
        <div>{principles_block()}</div>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="fit-title">
      <div class="container">
        <div class="section-head"><h2 id="fit-title">Who this is for, and who it isn't</h2></div>
        {fit_html()}
      </div>
    </section>
{faq_html()}{cta_band()}  </main>
''' + footer()
write('services/index.html', svc)

# ---------------------------------------------------------------- Work (projects index)
KB_PILL = 'N8N · SUPABASE PGVECTOR · GEMINI EMBEDDINGS · GOHIGHLEVEL READY'
proj = head('AI Agent, GoHighLevel &amp; n8n Reference Builds for a Remodeler | Waqar Ahmed',
            'Reference builds for a renovation business: AI knowledge base and RAG loader, 24/7 AI website receptionist, supplier quote automation and GoHighLevel pipelines.',
            '/projects/', jsonld=graph(
                crumbs(('Home', '/'), ('Work', None)),
                {"@type": "ItemList", "name": "Elite Home Renovations reference builds", "itemListElement": [
                    {"@type": "ListItem", "position": i, "url": SITE + f"/projects/{c['slug']}/", "name": c.get('plain', c['title'])}
                    for i, c in enumerate(CASES, 1)]})) + header('/projects/') + f'''
  <main id="main">
{page_hero(f'{N_CASES} reference builds for one renovation business.', 'One operating story in AI agents, GoHighLevel and n8n: load verified facts, answer the demand, capture it, coordinate the work, and show the team what needs attention.', [('Home', '/'), ('Work', None)], kicker='Work')}
    <section class="section" aria-labelledby="flag-title">
      <div class="container">
        <p class="note" role="note" style="margin-bottom:56px"><strong>About this work.</strong> {SANDBOX_LINE} Nothing here has been independently audited.</p>
        <div class="statement">
          <div>
            <p class="kicker">Featured case study</p>
            <h2 id="flag-title">From site visit to supplier quote</h2>
            <p style="margin-top:18px;color:var(--slate)">When a job reaches the site-visit stage, n8n checks the project details, matches active suppliers by trade and city, sends individual quote requests, then records the result and a follow-up task in GoHighLevel.</p>
            {ticks(['The same job is never sent twice', 'Partial matches and failures are visible', 'CRM notes and dated follow-up tasks'])}
            <div class="btn-row">
              <a class="btn" href="/projects/supplier-quote-requests/">Read the case study</a>
              <a class="btn btn--quiet ext" href="{LOOP_CASE}" {EXT}>Published on LOOP{NEWTAB}</a>
            </div>
          </div>
          <div>
            <div class="table-wrap">{SUPPLIER_TABLE}</div>
            <p class="statement-note">{SUPPLIER_NOTE}</p>
          </div>
        </div>
      </div>
    </section>
    <section class="section section--navy on-navy" aria-labelledby="kb-title">
      <div class="container statement">
        <div>
          <p class="kicker">Reference build · Elite Home Renovations</p>
          <h2 id="kb-title">AI Knowledge Base &amp; RAG Loader</h2>
          <p style="margin-top:18px">A one-click n8n loader that clears the old knowledge, then saves eight structured policy sections into Supabase pgvector with Gemini Embeddings. It is the verified source the 24/7 AI Website Receptionist answers from.</p>
          <div class="btn-row">
            <a class="btn" href="/projects/ai-knowledge-base-rag-loader/">Read the case study</a>
            <a class="btn btn--quiet" href="/projects/website-estimate-assistant/">See the AI receptionist</a>
          </div>
        </div>
        <div>
          <ul class="chips" aria-label="Stack"><li>{chip('stack', KB_PILL)}</li></ul>
          {ticks(['4-node linear loader and 3 helper nodes in n8n', 'Gemini Embeddings at vector(3072)', 'Chunk size 900, overlap 120', 'Row Level Security and a 1-click deduplicated refresh'])}
        </div>
      </div>
    </section>
    <section class="section section--white" aria-labelledby="all-title">
      <div class="container">
        <div class="section-head"><h2 id="all-title">All case studies</h2></div>
        {case_list()}
      </div>
    </section>
{cta_band()}  </main>
''' + footer()
write('projects/index.html', proj)

# ---------------------------------------------------------------- About
if HEADSHOT:
    PORTRAIT = f'<div class="portrait"><img src="{HEADSHOT}" alt="Portrait of Waqar Ahmed" width="800" height="800"></div>'
else:
    PORTRAIT = '<div class="portrait portrait--mark"><img src="/assets/img/wa-mark.svg" alt="WA monogram, the Waqar Ahmed logo" width="128" height="128" loading="lazy"></div>'
about = head('About Waqar Ahmed | AI Automation &amp; Agentic AI Specialist',
             'Waqar Ahmed builds AI agents, GoHighLevel pipelines and n8n workflows for US and UK remodeling contractors and agencies. MBA, about 8 years in bank operations.',
             '/about/', jsonld=graph(PERSON, PRO_SERVICE, crumbs(('Home', '/'), ('About', None)))) + header('/about/') + f'''
  <main id="main">
{page_hero('Operations first. AI second.', 'I spent about eight years in branch banking operations before I moved into AI automation. I build AI agents, GoHighLevel pipelines and n8n workflows the way a branch runs its day: every item has an owner, and nothing is left unaccounted for.', [('Home', '/'), ('About', None)], kicker=ROLE)}
    <section class="section" aria-labelledby="about-title">
      <div class="container split">
        <div>
          {PORTRAIT}
        </div>
        <div>
          <h2 id="about-title">Hi, I'm Waqar Ahmed.</h2>
          <p style="margin-top:20px">I'm an {ROLE}. I work with US and UK remodeling and home-improvement contractors ({TRADES_LINE}), and with the GoHighLevel agencies that serve them. I build four things: Supabase RAG knowledge bases, 24/7 AI website receptionists that answer from a business's own verified facts, GoHighLevel pipelines, and n8n workflows and AI agents.</p>
          <p>Before automation, I spent about eight years in branch banking operations at MCB Bank, after a BBA (Honors) in 2013 and an MBA in 2015. In a branch, every entry is checked, owned and reconciled before the day closes. I build AI agents, GoHighLevel pipelines and n8n workflows to the same standard: duplicate checks, error branches, a person signing off prices and promises, and a record of what each agent did.</p>
          <p>I have worked in AI automation since May 2022. I aim to make AI understandable to the people who use it: clear statuses, safe retries, useful alerts, and honest reporting about what an agent or automation did.</p>
          <dl class="facts" style="margin-top:32px">
            <div><dt>Role</dt><dd>{ROLE}</dd></div>
            <div><dt>Focus</dt><dd>US and UK remodeling and home-improvement contractors, and GoHighLevel agencies</dd></div>
            <div><dt>Builds</dt><dd>24/7 AI website receptionists (RAG), Supabase knowledge bases, GoHighLevel pipelines, n8n workflows and AI agents</dd></div>
            <div><dt>Tools</dt><dd>GoHighLevel, n8n, Supabase (pgvector), Google Gemini Embeddings, OpenAI and Claude APIs</dd></div>
            <div><dt>Education</dt><dd>MBA (2015), BBA Honors (2013)</dd></div>
            <div><dt>Background</dt><dd>About eight years in branch banking operations at MCB Bank</dd></div>
            <div><dt>Training</dt><dd>{cert_line()}</dd></div>
            <div><dt>Location</dt><dd>{BASE}. {REACH}</dd></div>
          </dl>
          <div class="btn-row">
            <a class="btn" href="{AUDIT}">{CTA}</a>
            <a class="btn btn--quiet ext" href="{LINKEDIN}" {EXT}>View my LinkedIn profile{NEWTAB}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--navy on-navy" aria-labelledby="bank-title">
      <div class="container split">
        <div>
          <h2 id="bank-title">What banking taught me about AI agents.</h2>
          <p style="margin-top:18px">In a branch, an entry with no owner is a problem someone has to find before the day closes. A lead with no owner is the same problem, and so is an AI agent with no limits and no record. Both cost you quietly.</p>
        </div>
        <div>{principles_block()}</div>
      </div>
    </section>

    <section class="section" aria-labelledby="avail-title">
      <div class="container">
        <div class="section-head">
          <h2 id="avail-title">Remote, with calls inside your business day</h2>
          <p>I'm based in {BASE} (PKT, UTC+5) and work remotely, mainly with contractors and GoHighLevel agencies in the US and UK.</p>
        </div>
        <ul class="hours">
          <li><strong>Live calls</strong><span>Audits, reviews and handovers are booked inside your working day, in US or UK business hours.</span></li>
          <li><strong>Written updates</strong><span>Progress notes and Loom walkthroughs cover the hours we don't overlap.</span></li>
          <li><strong>Your accounts</strong><span>Everything is built inside your own GoHighLevel, n8n, Supabase and AI accounts, so nothing depends on where I sit.</span></li>
        </ul>
      </div>
    </section>

    <section class="section section--white" aria-labelledby="own-title">
      <div class="container">
        <div class="own on-navy">
          <h3 id="own-title">After handover, it's all yours.</h3>
          {ticks(['Built inside your own GoHighLevel, n8n and AI accounts, through a role-based team invite.', 'You own every workflow, agent, knowledge base, contact, record and login.', 'Handover includes documentation and a Loom walkthrough your team can follow.', 'You can remove my access at any time. Nothing stops working when you do.'])}
        </div>
      </div>
    </section>
{cta_band()}  </main>
''' + footer()
write('about/index.html', about)


# ---------------------------------------------------------------- Case study pages
def provenance(data='Test data shaped like real renovation jobs',
               results='Figures are labelled as build specs, sample-run results or estimates. None were measured with a live business or independently audited.',
               intro='I built and tested this workflow inside a dedicated GoHighLevel and n8n sandbox, so you can inspect the exact architecture without exposing any private client CRM data.'):
    rows = [
        ('Build type', 'Reference / sandbox build'),
        ('Practice company', 'Elite Home Renovations, a practice company in a dedicated GoHighLevel sandbox account'),
        ('Data', data),
        ('Deployment', 'Not paid client work'),
        ('Results', results),
    ]
    dl = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    return (f'<aside class="provenance" aria-labelledby="prov-title">{chip("sandbox", "Reference / sandbox build")}'
            f'<h2 id="prov-title">Build provenance</h2>'
            f'<p>{intro}</p>'
            f'<dl>{dl}</dl></aside>')


def video(embed, title):
    """Responsive 16:9 video container. Shows a labelled placeholder until an embed URL is set."""
    if embed:
        inner = (f'<iframe src="{embed}" title="{title}" loading="lazy" allowfullscreen '
                 f'allow="fullscreen; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin"></iframe>')
    else:
        inner = '<p class="video-empty">Walkthrough video, about 3.5 minutes. Being added here.</p>'
    return (f'<!-- Video embed: set KB_VIDEO_EMBED in build/build.py to [INSERT_YOUTUBE_OR_LOOM_EMBED_URL] -->\n'
            f'<figure class="video-wrap"><div class="video" id="kb-walkthrough">{inner}</div>'
            f'<figcaption>{title}</figcaption></figure>')


def chain(steps, caption):
    lis = ''.join(f'<li class="{"is-n8n" if "n8n" in tool else ("is-ai" if ("AI" in tool or "RAG" in tool) else "")}"><span class="tool">{tool}</span><strong>{a}</strong>'
                  + (f'<span class="does">{b}</span>' if b else '') + '</li>' for tool, a, b in steps)
    return f'<figure class="arch"><ol class="chain">{lis}</ol><figcaption>{caption}</figcaption></figure>'


def figures(figs):
    return '<ul class="figures">' + ''.join(
        f'<li>{chip(k, lab)}<span class="fig">{v}</span><span class="what">{t}</span></li>' for k, lab, v, t in figs) + '</ul>'


def spec(*figs):
    return figures([('plain', 'Build spec', v, t) for v, t in figs])


def shot(slug):
    if slug not in CASE_SHOTS:
        return ''
    src, alt = CASE_SHOTS[slug]
    return f'<figure class="shot"><img src="{src}" alt="{alt}" loading="lazy"></figure>'


BEFORE_LIVE = '''<h2>Before using this for a live business</h2>
<ul>
<li>Measure the current process first, so any improvement can be compared with a real baseline.</li>
<li>Agree which accounts, data and workflows the business owns. I work through a role-based team invite.</li>
<li>Confirm third-party costs, such as GoHighLevel, n8n and messaging plans.</li>
<li>Test normal, duplicate, missing-data and failure cases with the team's real rules.</li>
</ul>'''


def case_page(slug, title, desc, lead, body, prov=None, chips=None, extra_btn=''):
    c = C[slug]
    crumb = (('Home', '/'), ('Work', '/projects/'), (c['crumb'], None))
    ld = graph(crumbs(*crumb),
               {"@type": "Article", "@id": SITE + f"/projects/{slug}/#article", "headline": c.get('plain', c['title']), "description": desc,
                "author": {"@id": SITE + "/#person"}, "publisher": {"@id": SITE + "/#person"},
                "datePublished": "2026-11-07", "dateModified": UPDATED[0], "inLanguage": "en",
                "mainEntityOfPage": SITE + f"/projects/{slug}/", "about": c.get("about", ["GoHighLevel", "n8n", "Workflow automation"])})
    chips = chips or [c['chip']]
    extra = ('<ul class="chips" aria-label="Project labels">' + ''.join(f'<li>{chip(k, t)}</li>' for k, t in chips) + '</ul>'
             f'<p class="updated">{c["tools"]}. Last updated <time datetime="{UPDATED[0]}">{UPDATED[1]}</time>.</p>')
    active = f'/projects/{slug}/' if any(h == f'/projects/{slug}/' for _, h in NAV) else '/projects/'
    html = head(title, desc, f"/projects/{slug}/", og_type='article', jsonld=ld) + header(active) + f'''
  <main id="main">
{page_hero(c['title'], lead, crumb, extra)}
    <div class="section">
      <div class="container prose">
{body}
{shot(slug)}
{prov or provenance()}
{BEFORE_LIVE}
<div class="btn-row"><a class="btn" href="{AUDIT}">{CTA}</a>{extra_btn}<a class="btn btn--quiet" href="/projects/">All case studies</a></div>
      </div>
    </div>
  </main>
''' + footer()
    write(f"projects/{slug}/index.html", html)


# ---- Flagship: Website Estimate Assistant (24/7 AI Website Receptionist)
R = RECEPTIONIST
r_facts = [(k, v) for k, v in [('Stack', R['stack']), ('Knowledge base built from', R['sources']),
                               ('Handover to the team', R['handoff']), ('Guardrails', R['guardrails'])] if v]
r_facts_html = ('<h2>Build details</h2><dl class="facts">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in r_facts) + '</dl>') if r_facts else ''
r_tested = (figures([('tested', 'Tested in a sample run', v, t) for v, t in R['tested']])) if R['tested'] else ''
r_demo = f'<a class="btn btn--quiet ext" href="{R["demo_url"]}" {EXT}>Watch the demo{NEWTAB}</a>' if R['demo_url'] else ''
case_page('website-estimate-assistant',
          f'{FLAGSHIP}: RAG Agent and Chat Widget | Waqar Ahmed',
          f'Reference build: a RAG agent and chat widget for a renovation business that answers from verified company facts, 24/7, with GoHighLevel and n8n behind it.',
          'A retrieval-augmented (RAG) AI agent with a chat widget on the Elite Home Renovations website. It answers visitor questions from the business\'s own content, day or night.',
          r_tested + f'''
<p class="note note--teal" role="note"><strong>Service name:</strong> I offer this build to clients as the <strong>{FLAGSHIP}</strong>. The case study below is the reference / sandbox version, built for Elite Home Renovations, a practice company.</p>
<h2>The problem</h2>
<p>Homeowners research renovation work in the evening and at weekends, when nobody is in the office. They want quick answers to simple questions: what the company does, where it works and how an estimate is arranged. If nobody answers, they can easily move on to the next contractor's website.</p>
<h2>What I built</h2>
{chain([
    ('Website', 'Visitor opens the chat widget', 'The widget sits on the website and is available at any hour.'),
    ('AI agent', 'Question goes to the agent', 'The agent receives the visitor’s question.'),
    ('RAG', 'Relevant content is retrieved', 'The agent looks up the most relevant passages in the business’s own knowledge base.'),
    ('AI agent', 'Answer grounded in that content', 'The reply is written from the retrieved passages, not from general internet knowledge.'),
], 'How a visitor question moves through the assistant.')}
<h2>Why retrieval-augmented generation (RAG)</h2>
<ul>
<li>The business controls what the assistant knows: update the knowledge base, and the answers change.</li>
<li>Answers come from the company's own content, which keeps them specific to its services and process.</li>
<li>It is the foundation for an agent that can also capture enquiry details and sync them into GoHighLevel through n8n.</li>
<li>The knowledge base itself is a separate reference build: the <a href="/projects/ai-knowledge-base-rag-loader/">AI Knowledge Base &amp; RAG Loader</a>.</li>
</ul>
{r_facts_html}
<h2>How I would set it up for a live business</h2>
<ul>
<li>Build the knowledge base only from content the owner approves, and review it together.</li>
<li>Agree what the assistant must never do, such as quoting prices or promising dates, and what it says instead.</li>
<li>Test it with real customer questions, including ones it should decline, before it goes on the website.</li>
<li>Connect captured enquiries to GoHighLevel or n8n, so every conversation ends with an owner and a next step.</li>
</ul>''',
          prov=provenance('Test or demo content for Elite Home Renovations, a practice company',
                          'No live-visitor results are reported. Build details are added here only once confirmed.',
                          intro='I built this assistant for a practice company, so you can see how it works without exposing any private client data.'),
          chips=[('sandbox', 'Reference / sandbox build'), ('plain', 'RAG agent + chat widget + GoHighLevel + n8n')],
          extra_btn=r_demo)

case_page('ai-knowledge-base-rag-loader',
          'AI Knowledge Base &amp; RAG Loader: n8n + Supabase pgvector | Waqar Ahmed',
          'Reference build: a one-click n8n loader that saves eight policy sections into Supabase pgvector with Gemini Embeddings for a GoHighLevel-ready AI receptionist.',
          'A one-click n8n workflow that clears the old knowledge and reloads eight structured policy sections into Supabase pgvector, so an AI receptionist answers from verified company facts. Reference build for Elite Home Renovations.',
          spec(('4', 'nodes in the linear loader'), ('3', 'helper nodes'), ('8', 'structured policy sections'), ('3072', 'embedding dimensions, <code>vector(3072)</code>'), ('900 / 120', 'chunk size and overlap')) + f'''
<h2>The problem</h2>
<p>An AI assistant with no verified source will guess. For a remodeling contractor, a guessed price or a guessed permit answer becomes a promise the team has to take back. The assistant needs one approved library of company facts, and the owner needs a simple way to refresh it when those facts change.</p>
<h2>What I built</h2>
<p>A four-node linear loader in n8n. One click runs it from start to finish:</p>
{chain([
    ('n8n', 'Run to load knowledge base', 'The manual trigger. One click starts the load.'),
    ('n8n + Supabase', 'Clear old knowledge', 'Removes the existing rows first, so a refresh never leaves duplicates.'),
    ('n8n', 'Elite Knowledge Text', 'Holds the company facts as eight structured policy sections.'),
    ('n8n + Supabase', 'Save to Supabase', 'Writes each chunk and its embedding to the Supabase vector store (pgvector).'),
], 'The four-node linear loader: Run to load knowledge base, Clear old knowledge, Elite Knowledge Text, Save to Supabase.')}
<h3>Three helper nodes</h3>
<div class="table-wrap"><table class="ruled">
<caption class="visually-hidden">Helper nodes attached to the Save to Supabase node</caption>
<thead><tr><th scope="col">Node</th><th scope="col">Setting</th><th scope="col">What it does</th></tr></thead>
<tbody>
<tr><td>Gemini Embeddings</td><td><code>vector(3072)</code></td><td>Turns each chunk into a 3,072-dimension embedding.</td></tr>
<tr><td>Default Data Loader</td><td>Default</td><td>Passes the knowledge text to the vector store as documents.</td></tr>
<tr><td>Recursive Character Text Splitter</td><td>Chunk size <code>900</code>, overlap <code>120</code></td><td>Splits the text into overlapping chunks, so an answer is not cut off at a chunk edge.</td></tr>
</tbody></table></div>
<h2>How it is kept safe and repeatable</h2>
<ul>
<li><strong>Eight structured policy sections.</strong> The company facts are written as separate sections, so each answer can be traced to the policy it came from.</li>
<li><strong>Row Level Security.</strong> Row Level Security is enabled on the Supabase table that holds the knowledge.</li>
<li><strong>1-click deduplicated refresh.</strong> Each run clears the old knowledge before saving, so the library can be reloaded at any time without duplicate rows.</li>
<li><strong>GoHighLevel ready.</strong> This is the knowledge base behind the <a href="/projects/website-estimate-assistant/">{FLAGSHIP}</a>, which passes qualified leads to GoHighLevel through n8n.</li>
</ul>
<h2>Walkthrough</h2>
{video(KB_VIDEO_EMBED, 'AI Knowledge Base and RAG Loader: 3.5-minute walkthrough')}''',
          prov=provenance('Demo company facts written for Elite Home Renovations, a practice company',
                          'Build specs only. No live-visitor results or retrieval-accuracy figures are reported.',
                          intro='I built this loader in my own n8n and Supabase sandbox, so you can inspect the exact architecture without exposing any private client data.'),
          chips=[('sandbox', 'Reference / sandbox build'), ('stack', KB_PILL)])

case_page('supplier-quote-requests',
          'Supplier Quote Automation with GoHighLevel and n8n | Waqar Ahmed',
          'Reference build: a GoHighLevel and n8n workflow that matches suppliers by trade and city after a site visit, sends quote requests and logs CRM follow-up.',
          'An n8n workflow connected to GoHighLevel that matches active suppliers by trade and city, sends each one a quote request, and records the result and next follow-up in the CRM.',
          figures([('tested', 'Tested in a sample run', '4', 'matching suppliers found in one Full Home test run'),
                   ('tested', 'Tested in a sample run', '0', 'send failures in that run'),
                   ('estimate', 'Estimate, not measured', '~17 hrs', 'a month saved, assuming 8 site visits a week')]) + f'''
<h2>The problem</h2>
<p>In renovation and home-service work, jobs get lost between enquiries, appointments, suppliers and follow-up. After a site visit, someone has to choose the right suppliers and send each one the project details. Suppliers get missed, and the customer's quote waits.</p>
<h2>What I built</h2>
{chain([
    ('GoHighLevel', 'Opportunity reaches “site visit done”', 'A job reaches the site-visit stage in the pipeline.'),
    ('n8n', 'Check the project', 'n8n reads the project details and checks the request has not already been sent.'),
    ('n8n', 'Match suppliers', 'Active suppliers are matched by trade and city.'),
    ('n8n + Gmail', 'Send requests', 'Each matching supplier gets an individual quote request.'),
    ('GoHighLevel', 'Record the result', 'A CRM note and a dated follow-up task are added.'),
], 'How the workflow moves between GoHighLevel and n8n.')}
<h2>How it handles problems</h2>
<ul>
<li>Request cycles are duplicate-safe, so the same job is not sent twice.</li>
<li>Partial matches and send failures are visible instead of hidden.</li>
<li>CRM notes and dated follow-up tasks keep the team informed.</li>
</ul>
<h2>What was tested</h2>
<p>These results come from the published LOOP project page and describe one sample run.</p>
<div class="table-wrap">{SUPPLIER_TABLE}</div>
<h2>The estimate</h2>
<p class="note" role="note"><strong>Estimate, not a measured result:</strong> about 17 hours of manual work saved per month, assuming eight site visits each week.</p>
<p style="margin-top:1rem">A real business would need its own baseline first: how long supplier requests take today, and how many site visits it handles.</p>''',
          prov=provenance('Test data: a Full Home test job and a supplier sheet',
                          'One sample run is reported as tested; the time saving is an estimate. No savings were measured with a live business or independently audited.'),
          chips=[('sandbox', 'Reference / sandbox build'), ('tested', 'Tested in one sample run'), ('estimate', 'Includes an estimate')],
          extra_btn=f'<a class="btn btn--quiet ext" href="{LOOP_CASE}" {EXT}>Published on LOOP{NEWTAB}</a>')

case_page('quote-intake-followup',
          'Lead scoring and follow-up with n8n and GoHighLevel | Waqar Ahmed',
          'Reference build: an 8-node n8n workflow that scores GoHighLevel contacts every 10 minutes and routes hot, warm and nurture leads for a renovation business.',
          'An 8-node n8n workflow, Elite Lead Scoring, that checks GoHighLevel every 10 minutes, scores new contacts on four details and sends each lead to the right next step.',
          spec(('8', 'nodes in the n8n scoring workflow'), ('10 min', 'between scoring runs'), ('3', 'routing paths: hot, warm, nurture'), ('1 hr', 'due time for the hot-lead call task')) + f'''
<h2>The problem</h2>
<p>Renovation companies get estimate requests of very different value. Without scoring, a large kitchen remodel booked for next month waits in the same queue as a small repair someday, and the best leads go cold.</p>
<h2>What I built</h2>
<p>The <strong>Elite Lead Scoring</strong> workflow in n8n runs in eight nodes:</p>
{chain([
    ('n8n', 'Schedule trigger', 'Runs every 10 minutes.'),
    ('n8n + GoHighLevel API', 'Get contacts', 'Fetches contacts from GoHighLevel through the API.'),
    ('n8n', 'Filter', 'Keeps only contacts tagged <code>needs-scoring</code>.'),
    ('n8n', 'Score four details', 'Project Type, Budget Range, Timeline and City.'),
    ('GoHighLevel', 'Route the lead', 'Sends each contact down one of three paths based on its score.'),
], 'Workflow architecture as built in the sandbox account.')}
<h2>How leads are routed</h2>
<div class="table-wrap"><table class="ruled">
<caption class="visually-hidden">Routing rules</caption>
<thead><tr><th scope="col">Tag</th><th scope="col">What happens next</th></tr></thead>
<tbody>
<tr><td><code>hot-lead</code></td><td>A call task is created, due within 1 hour.</td></tr>
<tr><td><code>warm-lead</code></td><td>The contact joins the nurture sequence.</td></tr>
<tr><td><code>nurture-lead</code></td><td>The contact is added to the newsletter list.</td></tr>
</tbody></table></div>
<h2>Why it is built this way</h2>
<ul>
<li>A tag (<code>needs-scoring</code>) marks which contacts still need work, so each one is scored once.</li>
<li>Scoring rules sit in one place in n8n, so the business can change what counts as a hot lead.</li>
<li>The fast path for hot leads is a dated task for a person, not just another automated message.</li>
</ul>''')

case_page('reporting-dashboards',
          'UTM attribution and lead-source reporting in GoHighLevel | Waqar Ahmed',
          'Reference build: five UTM contact fields and source-based branching in GoHighLevel, so every renovation lead shows its source and the owner is notified.',
          'Five custom UTM contact fields and conditional workflow branching in GoHighLevel, so each lead is tagged by source and the owner sees where leads come from.',
          spec(('5', 'UTM fields stored on every contact'), ('2', 'channel tags: Facebook and Google'), ('1', 'owner alert per new lead, with its source')) + f'''
<h2>The problem</h2>
<p>Home-service owners spend on Facebook and Google ads but often can't tell which channel produced which job. Without source data on the contact, reporting is guesswork.</p>
<h2>What I built</h2>
<h3>Five UTM contact fields</h3>
<p>Each new contact stores the campaign details it arrived with:</p>
<ul class="code-list">
<li><code>utm_source</code></li><li><code>utm_medium</code></li><li><code>utm_campaign</code></li><li><code>utm_term</code></li><li><code>utm_content</code></li>
</ul>
<h3>Conditional workflow branching</h3>
{chain([
    ('GoHighLevel', 'New lead arrives', 'The UTM values are saved to the contact.'),
    ('GoHighLevel', 'Check the source', 'The workflow branches on where the lead came from.'),
    ('GoHighLevel', 'Tag by channel', 'Facebook leads get <code>fb lead</code>; Google leads get <code>google lead</code>.'),
    ('GoHighLevel', 'Notify the owner', 'The owner is told about the new lead and its source.'),
], 'Workflow architecture as built in the sandbox account.')}
<h2>What it makes possible</h2>
<ul>
<li>Pipeline and dashboard reports filtered by channel, built on the tags and fields above.</li>
<li>Owner and marketing views that use the same data, so totals can be checked against the source.</li>
<li>Demo opportunities were seeded safely for the dashboards, with each row's result logged.</li>
</ul>''')

case_page('lead-to-site-visit',
          'Lead-to-site-visit system in GoHighLevel | Waqar Ahmed',
          'Reference build: a GoHighLevel estimate funnel, two pipelines, a 60-minute site-visit calendar and a reply-aware four-email nurture for a renovator.',
          'A Free Estimate Request funnel, two pipelines, a 60-minute site-visit calendar and a reply-aware nurture sequence that stops as soon as a visit is booked.',
          spec(('2', 'pipelines: Sales and Jobs'), ('60 min', 'site-visit calendar slot'), ('4', 'nurture emails, Day 0 to Day 9'), ('1', 'Goal Event that stops the sequence')) + f'''
<h2>The problem</h2>
<p>Estimate requests arrive at all hours. If nobody books the site visit quickly, the homeowner calls the next contractor. Follow-up emails also need to stop the moment a visit is booked.</p>
<h2>What I built</h2>
{chain([
    ('GoHighLevel', 'Free Estimate Request funnel', 'A funnel and form capture the project details.'),
    ('GoHighLevel', 'Two pipelines', 'A <strong>Sales Pipeline</strong> for new opportunities and a <strong>Jobs Pipeline</strong> for won work.'),
    ('GoHighLevel', 'Site-visit calendar', 'A 60-minute <strong>Free Site Visit &amp; Consultation</strong> calendar for booking.'),
    ('GoHighLevel', 'Reply-aware nurture', 'Four emails on Day 0, Day 2, Day 5 and Day 9.'),
    ('GoHighLevel', 'Stop condition', 'A <code>site-visit-booked</code> Goal Event ends the sequence once the visit is booked.'),
], 'System architecture as built in the sandbox account.')}
<h2>The nurture sequence</h2>
<div class="table-wrap"><table class="ruled">
<caption class="visually-hidden">Four-email sequence</caption>
<thead><tr><th scope="col">Email</th><th scope="col">Sent on</th></tr></thead>
<tbody>
<tr><td>Email 1</td><td>Day 0</td></tr><tr><td>Email 2</td><td>Day 2</td></tr>
<tr><td>Email 3</td><td>Day 5</td></tr><tr><td>Email 4</td><td>Day 9</td></tr>
</tbody></table></div>
<p>The sequence is reply-aware: when the homeowner books, the Goal Event stops further emails, so nobody is chased after they have already said yes.</p>''')

case_page('ai-customer-experiences',
          'Conversation AI, Voice AI and review automation in GoHighLevel | Waqar Ahmed',
          'Reference build: a 24/7 GoHighLevel Conversation AI and Voice AI lead qualifier, plus a review system that routes 4–5 and 1–3 star ratings differently.',
          'A 24/7 Conversation AI and Voice AI qualifier in GoHighLevel, plus a post-job reputation system that sends happy customers to Google and unhappy ones to the owner.',
          spec(('24/7', 'chat and voice coverage'), ('4', 'qualifying details, one question at a time'), ('2', 'review routes: 4–5 and 1–3 stars')) + f'''
<h2>The problem</h2>
<p>Homeowners ask questions at night and on weekends. After the job, a business needs more good reviews without unhappy customers being pushed to post publicly before the owner can help.</p>
<h2>24/7 AI qualifier</h2>
{chain([
    ('Conversation AI + Voice AI', 'Chat or call comes in', 'GoHighLevel Conversation AI answers chat; Voice AI answers calls.'),
    ('AI', 'One question at a time', 'The assistant collects four qualifying details, one question at a time.'),
    ('GoHighLevel', 'Tag the contact', 'Once all four are collected, the contact is tagged <code>ai-qualified</code>.'),
    ('Your team', 'Human handoff', 'The team picks up qualified leads with the details already on the record.'),
], 'Conversation flow as built in the sandbox account.')}
<h2>Post-job reputation and review system</h2>
<div class="table-wrap"><table class="ruled">
<caption class="visually-hidden">Review routing</caption>
<thead><tr><th scope="col">Rating</th><th scope="col">What happens</th></tr></thead>
<tbody>
<tr><td>4–5 stars</td><td>The customer gets the Google Review link.</td></tr>
<tr><td>1–3 stars</td><td>The owner gets a private alert to follow up directly.</td></tr>
</tbody></table></div>
<p>Asking one question at a time keeps the AI conversation simple for the customer, and the private alert gives the owner a chance to put things right.</p>''')

# ---------------------------------------------------------------- Contact (audit form)
HONEYPOT = ('<div hidden aria-hidden="true" style="display:none">'
            '<input type="text" name="_gotcha" value="" tabindex="-1" autocomplete="off" style="display:none"></div>')
if INTAKE_WEBHOOK_URL:
    # n8n Webhook node -> GoHighLevel (create/update contact, add tags, create opportunity) -> notification email
    FORM_NOTE = f'Your answers go to my n8n intake workflow, which creates the contact and opportunity in GoHighLevel and notifies me at {EMAIL}. Nothing is stored on this website.'
    FORM_ENC = ''
    FORM_MODE = 'webhook'
    EMAIL_FIELD = 'email'
    FORM_HIDDEN = ('<input type="hidden" name="source" value="portfolio-contact-form">\n'
                   '            <input type="hidden" name="_subject" value="Automation audit request">\n            ' + HONEYPOT)
elif FORMSPREE_ID:
    FORM_NOTE = f'Your answers are sent securely through Formspree, a form service, straight to {EMAIL}. Nothing is stored on this website.'
    FORM_ENC = ''
    FORM_MODE = 'formspree'
    EMAIL_FIELD = 'email'  # Formspree uses the "email" field as the reply-to address
    FORM_HIDDEN = ('<input type="hidden" name="_subject" value="Automation audit request">\n            ' + HONEYPOT)
else:
    FORM_NOTE = f'Sending opens your email app with your answers filled in, addressed to {EMAIL}. Nothing is stored on this website.'
    FORM_ENC = ' enctype="text/plain"'
    FORM_MODE = 'mailto'
    EMAIL_FIELD = 'Work email'
    FORM_HIDDEN = ''
TRADES = ['Kitchen/Bath remodeling', 'Extension/Loft conversion', 'Basement', 'Roofing', 'Solar', 'General remodeling', 'GoHighLevel agency', 'Other']
HELP = ['AI knowledge base (Tier 1)', f'{FLAGSHIP} + GoHighLevel pipeline (Tier 2)', 'Lead operations and retainer (Tier 3)', 'White-label agency partnership', 'Not sure yet']
WIDGET_COPY = ('My own AI receptionist is live on this page. Open the chat in the corner to ask about packages, the stack or how an audit works.'
               if CHAT_WIDGET_SRC else
               'My own AI receptionist is being connected to this page. Until it is live, the audit form above and email both reach me directly.')
BOOKING_BLOCK = (f'<div><h2>Prefer to pick a time?</h2><p>Book the 15-minute call directly.</p>'
                 f'<a class="btn btn--quiet btn--block ext" href="{BOOKING_URL}" {EXT}>Book a time{NEWTAB}</a></div>') if BOOKING_URL else ''
contact = head('Request a 15-Minute AI Automation Audit | Contact Waqar Ahmed',
               'Request a 15-minute AI automation audit for your remodeling business or GoHighLevel agency: AI receptionist, GoHighLevel pipeline or n8n workflow.',
               '/contact/', jsonld=graph(
                   crumbs(('Home', '/'), ('Contact', None)),
                   {"@type": "ContactPage", "@id": SITE + "/contact/#page", "url": SITE + "/contact/",
                    "name": "Contact Waqar Ahmed", "about": {"@id": SITE + "/#person"}})) + header('/contact/') + f'''
  <main id="main">
{page_hero('Tell me where leads get stuck.', 'Request a 15-minute automation audit below. We trace one workflow together and find where leads stall, and where an AI agent or automation would help. No sales pitch, and you keep the map either way.', [('Home', '/'), ('Contact', None)], kicker='Contact')}
    <section class="section" aria-labelledby="audit-title">
      <div class="container contact-layout">
        <div class="form-sheet">
          <h2 id="audit-title">Request an automation audit</h2>
          <p class="small">{FORM_NOTE}</p>
          <form id="audit-form" class="audit-form" action="{FORM_ACTION}" method="post"{FORM_ENC} data-email="{EMAIL}" data-intake="{FORM_MODE}" novalidate>
            {FORM_HIDDEN}
            <div class="field">
              <label for="f-name">Full name <span class="req" aria-hidden="true">*</span></label>
              <input id="f-name" name="Full name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="f-email">Work email <span class="req" aria-hidden="true">*</span></label>
              <input id="f-email" name="{EMAIL_FIELD}" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="f-phone">Phone or WhatsApp <span class="opt">(optional)</span></label>
              <input id="f-phone" name="Phone or WhatsApp" type="tel" autocomplete="tel" inputmode="tel">
            </div>
            <div class="field">
              <label for="f-trade">Trade or business type <span class="req" aria-hidden="true">*</span></label>
              <select id="f-trade" name="Trade type" required>
                <option value="">Choose one</option>
                {''.join(f'<option>{x}</option>' for x in TRADES)}
              </select>
            </div>
            <div class="field">
              <label for="f-help">What would you like help with? <span class="req" aria-hidden="true">*</span></label>
              <select id="f-help" name="Help with" required>
                <option value="">Choose one</option>
                {''.join(f'<option>{x}</option>' for x in HELP)}
              </select>
            </div>
            <div class="field">
              <label for="f-bottleneck">Where do leads get stuck? <span class="req" aria-hidden="true">*</span></label>
              <span class="hint" id="f-bottleneck-hint">For example: estimate requests wait days for a site-visit booking.</span>
              <textarea id="f-bottleneck" name="Primary bottleneck" rows="4" required aria-describedby="f-bottleneck-hint"></textarea>
            </div>
            <fieldset class="consent">
              <legend class="visually-hidden">Consent</legend>
              <div class="check">
                <input id="f-consent" name="Contact consent" type="checkbox" value="Yes" required>
                <label for="f-consent">I agree that Waqar Ahmed may contact me by email, phone or WhatsApp about this request (transactional messages only). I have read the <a href="/privacy/">Privacy Policy</a> and <a href="/terms/">Terms</a>. <span class="req" aria-hidden="true">*</span></label>
              </div>
              <div class="check">
                <input id="f-marketing" name="Marketing consent" type="checkbox" value="Yes">
                <label for="f-marketing">Optional: send me occasional automation tips by email or SMS. Message frequency varies. Message and data rates may apply. Reply STOP to opt out at any time. Consent is not a condition of any service.</label>
              </div>
            </fieldset>
            <p class="form-error" id="form-error" role="alert" hidden></p>
            <button class="btn btn--block" type="submit">Send audit request</button>
            <p class="small form-status" id="form-status" role="status" aria-live="polite"></p>
          </form>
        </div>
        <aside class="side" aria-label="Other ways to reach me">
          <div>
            <h2>What happens next</h2>
            <ol class="next">
              <li><div><strong>I read your answers.</strong> I sketch where leads stall today.</div></li>
              <li><div><strong>We have a 15-minute call.</strong> We walk through one workflow together.</div></li>
              <li><div><strong>You keep the workflow map.</strong> It's yours whether or not we work together.</div></li>
            </ol>
          </div>
          {BOOKING_BLOCK}
          <div>
            <h2>Ask the {FLAGSHIP}</h2>
            <p>{WIDGET_COPY}</p>
          </div>
          <div>
            <h2>Message me on LinkedIn</h2>
            <p>LinkedIn is the quickest way to reach me. I am based in {BASE}, and work remotely with contractors and GoHighLevel agencies in the US and UK.</p>
            <a class="btn btn--quiet btn--block ext" href="{LINKEDIN}" {EXT}>Message me on LinkedIn{NEWTAB}</a>
          </div>
          <div>
            <h2>Prefer email?</h2>
            <p class="email-line"><a href="mailto:{EMAIL}" id="biz-email">{EMAIL}</a></p>
            <button class="btn btn--quiet btn--small copy-btn" type="button" data-copy="{EMAIL}">Copy email address</button>
            <p class="small copy-status" role="status" aria-live="polite"></p>
          </div>
        </aside>
      </div>
    </section>
  </main>
''' + footer(widget=True)
write('contact/index.html', contact)


# ---------------------------------------------------------------- Legal pages
def legal_page(path, title, desc, h1, lead, body):
    crumb = (('Home', '/'), (h1, None))
    html = head(title, desc, path, jsonld=crumbs(*crumb)) + header('') + f'''
  <main id="main">
{page_hero(h1, lead, list(crumb), compact=True)}
    <div class="section">
      <div class="container prose legal">
<p class="updated">Last updated: <time datetime="{UPDATED[0]}">{UPDATED[1]}</time></p>
{body}
      </div>
    </div>
  </main>
''' + footer()
    write(path.strip('/') + '/index.html', html)


FORM_PRIVACY = ('The audit form does not store anything on this website: your answers are passed to my n8n intake workflow, which saves them as a contact in my GoHighLevel account and emails them to me.'
                if INTAKE_WEBHOOK_URL else
                'The audit form does not store anything on this website: your answers are passed to Formspree, the form service that emails them to me.'
                if FORMSPREE_ID else 'The audit form does not store anything on this website: it opens your own email app, and the details reach me only when you send that email.')
legal_page('/privacy/', 'Privacy Policy | Waqar Ahmed', 'How Waqar Ahmed handles personal data from this website and enquiries, including GDPR, CCPA and SMS (A2P 10DLC) opt-in and opt-out.',
           'Privacy Policy', 'What personal data this website and my enquiry process use, why, and how you control it.', f'''
<h2>Who I am</h2>
<p>This website is run by Waqar Ahmed, an independent AI automation consultant (AI agents, GoHighLevel and n8n) based in {BASE}, working remotely with clients worldwide ("I", "me"). For privacy questions, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>What I collect</h2>
<ul>
<li><strong>Enquiry details you choose to send</strong>, such as your name, work email, phone or WhatsApp number, trade type and the bottleneck you describe. {FORM_PRIVACY}</li>
<li><strong>Messages</strong> you send me by email, LinkedIn or other platforms.</li>
<li><strong>Basic visit statistics</strong> from Cloudflare Web Analytics, which does not use cookies and does not identify individual visitors.</li>
</ul>
<p>This website does not use advertising or tracking cookies.</p>
<h2>Why I use it (legal bases)</h2>
<ul>
<li>To reply to your enquiry and prepare a proposal: steps taken at your request before a contract, or my legitimate interest in answering business enquiries.</li>
<li>To send occasional tips: only if you opted in, based on your consent, which you can withdraw at any time.</li>
<li>To keep the site secure and understand overall traffic: legitimate interest.</li>
</ul>
<h2>SMS and mobile messaging (A2P 10DLC)</h2>
<p>If you give a mobile number and agree to be contacted, I use it only for the purpose you agreed to. <strong>Mobile numbers and SMS opt-in data are never shared with or sold to third parties or affiliates for their marketing or promotional purposes.</strong> Message frequency varies, and message and data rates may apply.</p>
<p>To stop text messages, reply <strong>STOP</strong> to any message. You can also email <a href="mailto:{EMAIL}">{EMAIL}</a> to opt out of any messages. Reply HELP for help.</p>
<h2>Who receives data</h2>
<p>I do not sell personal information. Data is processed by the services I use to run this site and my work: Cloudflare (hosting and analytics), {"n8n and GoHighLevel (audit form intake), " if INTAKE_WEBHOOK_URL else "Formspree (audit form delivery), " if FORMSPREE_ID else ""}Google (email), LinkedIn (if you message me there) and, for client projects, the client's own GoHighLevel and n8n accounts. When we work together, your business data stays in accounts you own.</p>
<h2>How long I keep it</h2>
<p>I keep enquiry emails for as long as needed to respond and follow up, and delete them on request unless I must keep them for legal or accounting reasons.</p>
<h2>Your rights (GDPR and UK GDPR)</h2>
<p>You can ask to access, correct, delete or export your personal data, object to or restrict its use, and withdraw consent at any time. You can also complain to your local data protection authority.</p>
<h2>California residents (CCPA/CPRA)</h2>
<p>You have the right to know what personal information I collect, to delete it, to correct it, and not to be discriminated against for using these rights. I do not sell or share personal information for cross-context behavioural advertising.</p>
<h2>Contact and changes</h2>
<p>To use any of these rights, email <a href="mailto:{EMAIL}">{EMAIL}</a>. I may update this policy; the date above shows the latest version.</p>''')

legal_page('/terms/', 'Terms of Service | Waqar Ahmed', 'Terms for AI agent, GoHighLevel and n8n consulting by Waqar Ahmed: project scope, AI agent limits, account ownership, costs and portfolio disclosure.',
           'Terms of Service', 'The terms that apply when you use this website or work with me.', f'''
<h2>About these terms</h2>
<p>These terms apply to this website and to consulting work by Waqar Ahmed (AI agents, GoHighLevel, n8n and Supabase RAG knowledge bases). Each project also has a written scope, which takes priority if anything differs.</p>
<h2>Consulting scope</h2>
<ul>
<li>Work is agreed in a written scope that lists deliverables, turnaround, acceptance checks and any third-party costs before the build starts.</li>
<li>Turnaround times start once the scope is agreed and the access I need is in place.</li>
<li>Changes beyond the agreed scope are quoted separately before work continues.</li>
</ul>
<h2>Your accounts, your ownership</h2>
<ul>
<li>You own 100% of your GoHighLevel, n8n, Supabase and AI accounts, and the workflows, agents, knowledge bases, data and contacts in them.</li>
<li>I work through role-based team-member invites with only the access the work needs. I never ask for your passwords.</li>
<li>You can remove my access at any time.</li>
</ul>
<h2>Third-party services and costs</h2>
<p>Subscriptions and usage charges for GoHighLevel, n8n, Supabase, AI models, hosting, email, SMS or other tools are paid by you directly to those providers and follow their terms.</p>
<h2>AI agents and their limits</h2>
<p>AI agents and AI receptionists are built to answer from content you approve and to hand over to a person when they cannot. AI output can still be wrong. You decide what an agent may say and do, and you remain responsible for prices, commitments and advice given to your customers.</p>
<h2>Messaging compliance</h2>
<p>You are responsible for having consent to contact the people in your CRM. I will not build cold SMS or email campaigns to people who have not opted in.</p>
<h2>Portfolio disclosure</h2>
<p>The projects on this website are <strong>reference / sandbox builds for Elite Home Renovations, a practice company</strong>, using test or demo data. They show implementation skills. They are not paid client work, and results are labelled as tested in a sample run, as build specs or as estimates. Any practice prices shown are typical ranges, not quotes.</p>
<h2>No guaranteed results</h2>
<p>I build and test carefully, but I cannot guarantee business outcomes such as revenue, bookings or time saved, or that AI output will always be correct, as these depend on factors outside the system.</p>
<h2>Limitation of liability</h2>
<p>To the extent the law allows, my total liability for any project is limited to the fees paid for that project.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')

# ---------------------------------------------------------------- llms.txt
LLMS = f"""# {BRAND}

> {ROLE_TXT}. Builds 24/7 AI website receptionists (RAG), GoHighLevel (GHL) pipelines, n8n workflows and Supabase (pgvector) knowledge bases for US and UK residential remodeling and home-improvement contractors, and white-label n8n + Supabase RAG backends for US and UK GoHighLevel marketing agencies. {LOCATION} {TAGLINE}

Waqar Ahmed's client-facing work is AI agents, GoHighLevel, n8n workflows and Supabase RAG knowledge bases. The flagship service is the {FLAGSHIP}: a RAG knowledge base, a website chat widget, GoHighLevel and n8n lead operations. The AI agent answers from a business's own verified facts, and decisions such as prices and permit promises stay with a person. Clients keep full ownership of their accounts; he works through role-based team invites and never asks for passwords.

## Who it is for
- Direct clients: US and UK residential remodeling and home-improvement contractors ({TRADES_LINE}).
- White-label partners: US and UK GoHighLevel marketing agencies that need a technical n8n + Supabase (pgvector) RAG backend specialist.

## About
- Background: about eight years in branch banking operations at MCB Bank before moving into automation. MBA (2015), BBA Honors (2013).
- Working in AI automation since May 2022.
- Training: {cert_line()}.
- Stack: GoHighLevel, n8n, Supabase (pgvector), Google Gemini Embeddings, OpenAI and Claude APIs.
- Location: {BASE}. {REACH}; all work is remote.
- Handle: @opswaqarahmed
- Contact: {SITE}/contact/ (15-minute workflow audit request), email {EMAIL} or {LINKEDIN}

## Packages and partner track
""" + ''.join(f"- [{lab}: {t}]({SITE}/services/) ({st}): {d}\n" for lab, t, st, d, _ in SERVICES) + f"""
## Reference builds (Elite Home Renovations)
These are reference / sandbox builds for Elite Home Renovations, a practice company, using test or demo data. They are not paid client work.
- [Website Estimate Assistant / {FLAGSHIP}]({SITE}/projects/website-estimate-assistant/): {CASES[0]['card']}
- [AI Knowledge Base and RAG Loader]({SITE}/projects/ai-knowledge-base-rag-loader/): 4-node linear n8n loader (Run to load knowledge base, Clear old knowledge, Elite Knowledge Text, Save to Supabase) with 3 helper nodes (Gemini Embeddings at vector(3072), Default Data Loader, Recursive Character Text Splitter at chunk size 900 / overlap 120), 8 structured policy sections, Row Level Security and a 1-click deduplicated refresh.
- [Supplier quote automation]({SITE}/projects/supplier-quote-requests/): n8n + GoHighLevel supplier matching; one sample run found 4 matching suppliers with 0 send failures; about 17 hours a month saved is an estimate (8 site visits a week), not a measured result.
""" + ''.join(f"- [{c['title']}]({SITE}/projects/{c['slug']}/): {c['card']}\n" for c in CASES[3:]) + f"""
## Key pages
- [Home]({SITE}/)
- [Services and FAQ]({SITE}/services/)
- [Work]({SITE}/projects/)
- [About]({SITE}/about/)
- [Contact]({SITE}/contact/)
- [Privacy Policy]({SITE}/privacy/)
- [Terms of Service]({SITE}/terms/)

## Profiles
""" + ''.join(f"- [{n}]({u})\n" for n, u in SOCIAL if u) + f"- [Published supplier quote project]({LOOP_CASE})\n"
write('llms.txt', LLMS, raw=True)

# ---------------------------------------------------------------- 404
nf = head('Page not found | Waqar Ahmed', 'This page could not be found. Return to the Waqar Ahmed AI agents, GoHighLevel and n8n site.', '/404.html', noindex=True) + header('') + f'''
  <main id="main" class="section notfound">
    <div class="container">
      <h1>This page isn't here.</h1>
      <p>It has moved or never existed. These pages will get you back on track.</p>
      <div class="btn-row">
        <a class="btn" href="/">Go to the home page</a>
        <a class="btn btn--quiet" href="/services/">Services</a>
        <a class="btn btn--quiet" href="/projects/">Work</a>
      </div>
    </div>
  </main>
''' + footer()
write('404.html', nf)

# ---------------------------------------------------------------- sitemap, manifest, css, js
urls = ['/', '/services/', '/projects/'] + [f"/projects/{c['slug']}/" for c in CASES] + ['/about/', '/contact/', '/privacy/', '/terms/']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{UPDATED[0]}</lastmod>\n  </url>\n' for u in urls) + '</urlset>\n'
write('sitemap.xml', sm, raw=True)

write('site.webmanifest', json.dumps({
    "name": BRAND, "short_name": "Waqar Ahmed",
    "description": "AI agents, GoHighLevel and n8n automation for US and UK remodeling contractors and GoHighLevel agencies.",
    "start_url": "/", "display": "browser", "background_color": "#F4F6F8", "theme_color": "#0B1626",
    "icons": [{"src": "/assets/img/wa-mark.svg", "sizes": "any", "type": "image/svg+xml"},
              {"src": "/assets/img/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}, indent=2) + '\n', raw=True)

css = (HERE / 'site.src.css').read_text(encoding='utf-8')
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
css = re.sub(r'\n\s*\n+', '\n', css).strip() + '\n'
write('css/site.css', '/* Built from build/site.src.css. Edit that file, not this one. */\n' + css, raw=True)

js = (HERE / 'main.src.js').read_text(encoding='utf-8')
js = '\n'.join(l for l in js.splitlines() if not l.strip().startswith('//') and l.strip()) + '\n'
write('js/main.js', js, raw=True)

print('built', len(urls), 'pages into', OUT)
