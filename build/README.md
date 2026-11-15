# How to update opswaqarahmed.pages.dev

The live site is the `public` folder. Cloudflare Pages publishes it automatically every time
the `main` branch of github.com/opswaqarahmed/opswaqarahmed-website changes.

## Easiest way: ask Claude

1. Start a chat and say what to change, for example:
   "Update my portfolio website: add a new case study about X."
2. Attach `build/build.py` from this folder (or let Claude read it from your Desktop folder),
   so Claude can rebuild every page consistently.
3. Claude saves the updated `public` folder back to your Desktop project folder.
4. Publish it:
   - Open https://github.com/opswaqarahmed/opswaqarahmed-website/upload/main
   - Drag in the `public` folder
   - Choose "Commit directly to the main branch", add a short message, click Commit changes
5. The site updates in about 1 minute.

Note: Windows can skip folders whose names start with a dot, such as `public/.well-known`.
That folder rarely changes. If it does, add the file in GitHub with "Add file > Create new file".

## Small text fix yourself

1. Open the file on GitHub, for example `public/about/index.html`.
2. Click the pencil icon, edit the text, then click Commit changes on `main`.
3. Tell Claude next time, so `build.py` gets the same change. Otherwise the next full
   rebuild will overwrite your edit.

## What build.py controls

- Brand rules: name (BRAND_DESCRIPTOR, ROLE, LOCKUP_LINE, FLAGSHIP), tagline, location (BASE, REACH), email, social links (SOCIAL list)
- Header, footer, every page's copy, title, description and structured data
- sitemap.xml, llms.txt and site.webmanifest
- It also copies `build/site.src.css` to `public/css/site.css` and `build/main.src.js` to `public/js/main.js`

Change these, then run `python build.py`. It writes into the `public` folder next to `build`
automatically (no path to edit). After a CSS or JS change, raise `ASSET_V` in build.py by one.

## Placeholders

The PLACEHOLDERS block near the top of build.py holds things only you can supply: certificate
title and date, booking link, testimonials, prices (typical ranges), case-study screenshots,
the n8n intake webhook (`INTAKE_WEBHOOK_URL`), the live chat widget (`CHAT_WIDGET_SRC`, `CHAT_WIDGET_ATTRS`)
and the knowledge-base walkthrough video (`KB_VIDEO_EMBED`).
The RECEPTIONIST block holds the AI receptionist's confirmed build details (stack, sources, handoff, guardrails, demo link, test results).
While a value is empty the site leaves that element out, so nothing unfinished is published.

## Brand

Brand guide v3.0 ("Agent Ledger"), logo files and social banners are in the `brand` folder.
Fonts are Manrope (headings) and DM Sans (text), self-hosted in `public/assets/fonts`.

## Scope rule

Client-facing services are AI agents, GoHighLevel, n8n workflows and Supabase RAG knowledge bases only.
Do not add website-development or browser-extension services to any page, meta tag or schema.

## Audit form: GoHighLevel + n8n intake webhook

Set `INTAKE_WEBHOOK_URL` in build.py to the n8n Webhook node's Production URL. The form then posts its
fields (multipart form data) straight to n8n. In n8n:

- Webhook node: HTTP Method `POST`, Path `portfolio-intake`, Respond `Immediately`,
  Options > Allowed Origins (CORS) `https://opswaqarahmed.pages.dev`
- Fields arrive under `{{ $json.body }}`: `Full name`, `email`, `Phone or WhatsApp`, `Trade type`,
  `Help with`, `Primary bottleneck`, `Contact consent`, `Marketing consent`, `source`, `page`, `submitted_at`
- Drop spam first: IF node, `{{ $json.body._gotcha }}` is empty
- Then HighLevel node: Contact > Create or Update, add tag `portfolio-audit-request`,
  then Opportunity > Create in your pipeline's first stage

Also add your n8n host to `connect-src` in `public/_headers`, or the browser blocks the request.
For a widget that is not from GoHighLevel, add its host to `script-src` and `connect-src` too.

## Audit form (Formspree, used while INTAKE_WEBHOOK_URL is empty)

The contact form sends through Formspree when `FORMSPREE_ID` in build.py is set (the part after
https://formspree.io/f/). If it is empty, the form falls back to opening the visitor's email app
(mailto). `public/_headers` already allows https://formspree.io.
