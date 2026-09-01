#!/usr/bin/env python3
"""Build redesigned content pages: Login, Terms, Refund, Privacy, FAQ.

Reuses the live site chrome (base CSS + header + mobile-nav assets + footer +
scroll-to-top) extracted from home-live.html so every page matches the current
design exactly. Outputs into ../../deploy:
  goa-login.html, goa-terms.html, goa-refund.html, goa-privacy.html, goa-faq.html
Routers (goa-login.php, goa-legal.php) are written separately.
"""
from __future__ import annotations
import re, json, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY = HERE.parent.parent / "deploy"
SITE = "https://www.goadirectory.in"
EMAIL = "help@goadirectory.in"
PHONE = "+91 99233 52923"
TEL = "+919923352923"
WA = "https://wa.me/919923352923"
UPDATED = "29 August 2026"

_home = (HERE / "home-live.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", _home, re.S).group(1)
HEADER = re.search(r'<header class="hd">.*?</header>', _home, re.S).group(0)
NAV_ASSETS = re.search(r'</header>(<style>.*?</script>)', _home, re.S).group(1)
FOOTER = re.search(r'<footer class="foot">.*?</footer>', _home, re.S).group(0)
SCROLLTOP = re.search(r'</footer>(<button id="goaTop".*?</script>)', _home, re.S).group(1)

def e(s): return html.escape(str(s), quote=True)

PAGE_CSS = """
/* ---- content pages ---- */
.crumbbar{background:var(--soft);border-bottom:1px solid var(--border)}
.crumbbar .wrap{padding-block:.7rem}
.crumbs{display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;font-size:.82rem;color:var(--muted)}
.crumbs a{color:var(--muted)}.crumbs a:hover{color:var(--blue)}
.crumbs .sep{color:#c4ccdb}.crumbs .cur{color:var(--navy);font-weight:600}
.pg-hero{background:linear-gradient(180deg,#16244a,#1f3d7a);color:#fff}
.pg-hero .wrap{padding-block:clamp(34px,4.5vw,52px);text-align:center}
.pg-hero .eyebrow{color:#9fc0ff}
.pg-hero h1{color:#fff;font-size:clamp(1.8rem,3.6vw,2.6rem);font-weight:800;margin-top:.4rem}
.pg-hero p{color:rgba(255,255,255,.9);max-width:60ch;margin:.7rem auto 0}
.doc{max-width:820px;margin:0 auto}
.doc .updated{color:var(--muted);font-size:.85rem;margin-bottom:1.4rem}
.prose{font-size:1rem;line-height:1.75;color:#334}
.prose h2{font-size:1.3rem;font-weight:700;color:var(--navy);margin:1.9rem 0 .7rem;scroll-margin-top:80px}
.prose h3{font-size:1.06rem;font-weight:700;color:var(--navy);margin:1.3rem 0 .5rem}
.prose p{margin:0 0 1rem}
.prose ul{margin:0 0 1.1rem;padding-left:1.2rem}
.prose li{margin:.35rem 0}
.prose a{color:var(--blue);font-weight:600}
.callout{background:var(--soft);border:1px solid var(--border);border-left:4px solid var(--blue);border-radius:10px;padding:1rem 1.2rem;margin:1.2rem 0;font-size:.95rem}
.callout.warn{border-left-color:#e0554e;background:#fdecea;border-color:#f5c6c2}
.toc{background:var(--soft);border:1px solid var(--border);border-radius:12px;padding:1rem 1.2rem;margin:0 0 1.6rem}
.toc b{display:block;color:var(--navy);font-size:.9rem;margin-bottom:.5rem}
.toc ul{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:.3rem .9rem}
@media(max-width:600px){.toc ul{grid-template-columns:1fr}}
.toc a{color:var(--blue);font-size:.9rem;font-weight:500}
.contactcard{background:var(--soft);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.3rem;margin-top:1.8rem}
.contactcard h3{color:var(--navy);font-size:1.05rem;margin-bottom:.5rem}
.contactcard a{color:var(--blue);font-weight:600}
/* login */
.authwrap{max-width:440px;margin:0 auto}
.authcard{background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:var(--sh);padding:1.9rem}
.authcard h1{font-size:1.5rem;font-weight:800;color:var(--navy);text-align:center}
.authcard .sub{color:var(--muted);font-size:.9rem;text-align:center;margin:.3rem 0 1.4rem}
.field{margin-bottom:1rem;display:flex;flex-direction:column;gap:.35rem}
.field label{font-size:.84rem;font-weight:600;color:var(--navy)}
.field input{width:100%;border:1.5px solid var(--border);border-radius:10px;padding:.75rem .9rem;font:inherit;color:var(--ink);background:#fdfefe;transition:border-color .15s,box-shadow .15s}
.field input:focus{outline:0;border-color:var(--blue);box-shadow:0 0 0 3px rgba(31,95,208,.14)}
.authrow{display:flex;align-items:center;justify-content:space-between;gap:.6rem;margin:.2rem 0 1.2rem;font-size:.85rem}
.authrow label{display:flex;align-items:center;gap:.4rem;color:#3a4664;cursor:pointer}
.authrow a{color:var(--blue);font-weight:600}
.authbtn{width:100%;padding-block:.85rem;font-size:1rem}
.authalt{text-align:center;color:var(--muted);font-size:.9rem;margin-top:1.2rem;padding-top:1.1rem;border-top:1px solid var(--border)}
.authalt a{color:var(--blue);font-weight:700}
.authnote{text-align:center;font-size:.78rem;color:var(--muted);margin-top:1rem}
/* faq */
.faq{max-width:820px;margin:0 auto}
.faq .cat{font-size:1.15rem;font-weight:700;color:var(--navy);margin:1.6rem 0 .8rem}
.faq details{border:1px solid var(--border);border-radius:12px;margin-bottom:.7rem;background:#fff;overflow:hidden}
.faq summary{cursor:pointer;padding:1rem 1.15rem;font-weight:600;color:var(--navy);list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary .pl{color:var(--blue);font-size:1.35rem;line-height:1;transition:transform .2s;flex:none}
.faq details[open] summary .pl{transform:rotate(45deg)}
.faq .ans{padding:0 1.15rem 1.15rem;color:#4a556e;font-size:.94rem;line-height:1.7}
.faq .ans a{color:var(--blue);font-weight:600}
"""

def head(title, desc, canonical, ld_list, robots="index,follow,max-image-preview:large,max-snippet:-1"):
    p = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         f'<title>{e(title)}</title>',
         f'<meta name="description" content="{e(desc)}">',
         f'<meta name="robots" content="{robots}">',
         f'<link rel="canonical" href="{e(canonical)}">',
         '<meta property="og:type" content="website"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">',
         f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(canonical)}">',
         '<meta name="twitter:card" content="summary">',
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">',
         "<style>" + CSS + PAGE_CSS + "</style>"]
    for ld in ld_list:
        p.append('<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    p.append("</head><body>")
    p.append(HEADER)
    p.append(NAV_ASSETS)
    return "".join(p)

def crumb(name):
    return ('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
            f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
            f'<span class="cur">{e(name)}</span></nav></div></div>')

def hero(eyebrow, h1, sub):
    return ('<section class="pg-hero"><div class="wrap">'
            f'<span class="eyebrow">{e(eyebrow)}</span><h1>{e(h1)}</h1><p>{e(sub)}</p></div></section>')

def breadcrumb_ld(name, url):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": url}]}

def wrap_page(parts):
    return "".join(parts) + FOOTER + SCROLLTOP + "</body></html>"

CONTACT_CARD = (f'<div class="contactcard"><h3>Questions?</h3>'
                f'<p style="color:var(--muted);font-size:.92rem;margin-bottom:.5rem">Contact the Goa Directory team:</p>'
                f'<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; '
                f'Phone/WhatsApp <a href="{WA}" target="_blank" rel="noopener">{PHONE}</a></p></div>')

# --------------------------------------------------------------- section helper
def sections_to_html(sections):
    """sections: list of (id, heading, [blocks]) where block is ('p', text) | ('ul', [items]) | ('h3', text) | ('callout', text) | ('warn', text)"""
    out = []
    toc = ['<div class="toc"><b>On this page</b><ul>']
    for sid, hd, _ in sections:
        toc.append(f'<li><a href="#{sid}">{e(hd)}</a></li>')
    toc.append('</ul></div>')
    out.append("".join(toc))
    for sid, hd, blocks in sections:
        out.append(f'<h2 id="{sid}">{e(hd)}</h2>')
        for b in blocks:
            kind = b[0]
            if kind == 'p':
                out.append(f'<p>{b[1]}</p>')
            elif kind == 'h3':
                out.append(f'<h3>{e(b[1])}</h3>')
            elif kind == 'ul':
                out.append('<ul>' + "".join(f'<li>{it}</li>' for it in b[1]) + '</ul>')
            elif kind == 'callout':
                out.append(f'<div class="callout">{b[1]}</div>')
            elif kind == 'warn':
                out.append(f'<div class="callout warn">{b[1]}</div>')
    return "".join(out)

# =============================================================== LOGIN
def build_login():
    url = SITE + "/login-2/"
    title = "Login | Goa Directory"
    desc = "Log in to your Goa Directory account to manage your business listings, ads and details."
    parts = [head(title, desc, url, [breadcrumb_ld("Login", url)], robots="noindex,follow")]
    parts.append(crumb("Login"))
    parts.append('<main class="sec"><div class="wrap"><div class="authwrap"><div class="authcard">')
    parts.append('<h1>Welcome back</h1><p class="sub">Log in to manage your Goa Directory listings.</p>')
    parts.append(f'<form action="{SITE}/wp-login.php" method="post">')
    parts.append('<div class="field"><label for="user_login">Username or email</label>'
                 '<input type="text" name="log" id="user_login" autocomplete="username" required></div>')
    parts.append('<div class="field"><label for="user_pass">Password</label>'
                 '<input type="password" name="pwd" id="user_pass" autocomplete="current-password" required></div>')
    parts.append('<div class="authrow"><label><input type="checkbox" name="rememberme" value="forever"> Remember me</label>'
                 f'<a href="{SITE}/wp-login.php?action=lostpassword">Forgot password?</a></div>')
    parts.append(f'<input type="hidden" name="redirect_to" value="{SITE}/">')
    parts.append('<input type="hidden" name="testcookie" value="1">')
    parts.append('<button type="submit" name="wp-submit" class="btn btn-blue authbtn">Log In</button>')
    parts.append(f'<div class="authalt">New to Goa Directory? <a href="{SITE}/plans/">List your business</a></div>')
    parts.append('<p class="authnote">Secured by WordPress. We never share your password.</p>')
    parts.append('</form></div></div></div></main>')
    (DEPLOY / "goa-login.html").write_text(wrap_page(parts), encoding="utf-8")
    print("built goa-login.html")

# =============================================================== TERMS
def build_terms():
    url = SITE + "/terms-of-use/"
    title = "Terms of Use | Goa Directory"
    desc = ("The terms and conditions for using Goa Directory — listing rules, user responsibilities, "
            "payments, intellectual property, disclaimers and governing law (Goa, India).")
    S = [
     ("acceptance", "1. Acceptance of these terms", [
        ('p', 'These Terms of Use ("Terms") govern your access to and use of the Goa Directory website at '
              f'<a href="{SITE}/">www.goadirectory.in</a> and all related services (the "Service"). '
              'By accessing the Service, creating an account, or submitting a listing, you agree to be bound by these Terms. '
              'If you do not agree, please do not use the Service.'),
     ]),
     ("service", "2. The service", [
        ('p', 'Goa Directory is an online local business directory and classifieds platform that helps businesses across Goa '
              'get discovered by local customers. We provide listing, category, search and enquiry features. We may add, '
              'change or remove features at any time to improve the Service.'),
     ]),
     ("accounts", "3. Accounts &amp; eligibility", [
        ('p', 'You must provide accurate, current and complete information when creating an account or submitting a listing, '
              'and keep it up to date. You are responsible for maintaining the confidentiality of your login details and for '
              'all activity under your account. You must be at least 18 years old, or have the authority to act for the business you list.'),
     ]),
     ("listings", "4. Listings &amp; user content", [
        ('p', 'You retain ownership of the text, images and information you submit ("Content"). By submitting Content, you grant '
              'Goa Directory a non-exclusive, royalty-free licence to host, display, resize and promote it in connection with the Service.'),
        ('p', 'You represent that you own or have the right to use all Content you submit, and that it is accurate and not misleading. '
              'All submissions are reviewed before publishing and may be edited, declined or removed at our discretion.'),
     ]),
     ("prohibited", "5. Prohibited use", [
        ('p', 'When using the Service you agree not to:'),
        ('ul', [
            'Post false, misleading, illegal, offensive, or infringing content;',
            'List prohibited goods or services, or impersonate another person or business;',
            'Upload viruses or malicious code, or attempt to gain unauthorised access to the Service;',
            'Scrape, harvest or copy listings or data without written permission;',
            'Use the Service to send spam or unsolicited communications.',
        ]),
     ]),
     ("payments", "6. Plans, payments &amp; refunds", [
        ('p', 'Paid listing plans are billed annually and described on our '
              f'<a href="{SITE}/plans/">Plans</a> page. Prices are in Indian Rupees (INR) and may change with notice. '
              f'All fees are non-refundable — please read our <a href="{SITE}/refund-policy/">Refund Policy</a> before purchasing.'),
     ]),
     ("ip", "7. Intellectual property", [
        ('p', 'The Goa Directory name, logo, design, and all site software and content (other than user Content) are owned by '
              'Goa Directory and its licensors and are protected by applicable laws. You may not copy, reproduce or create '
              'derivative works without our prior written consent.'),
     ]),
     ("thirdparty", "8. Third-party links", [
        ('p', 'The Service may contain links to third-party websites and businesses. We do not control and are not responsible '
              'for their content, products, services or practices. Dealing with any business listed is solely between you and that business.'),
     ]),
     ("disclaimer", "9. Disclaimers", [
        ('p', 'The Service and all listings are provided on an "as is" and "as available" basis without warranties of any kind. '
              'We do not guarantee the accuracy, completeness or reliability of any listing, or that the Service will be uninterrupted or error-free. '
              'Goa Directory is a platform and is not a party to any transaction between users and listed businesses.'),
     ]),
     ("liability", "10. Limitation of liability", [
        ('p', 'To the maximum extent permitted by law, Goa Directory shall not be liable for any indirect, incidental, special or '
              'consequential damages, or any loss of profits, data or goodwill, arising from your use of (or inability to use) the Service. '
              'Our total liability for any claim shall not exceed the amount you paid to us in the twelve months before the claim.'),
     ]),
     ("indemnity", "11. Indemnity", [
        ('p', 'You agree to indemnify and hold harmless Goa Directory and its team from any claims, damages, losses or expenses '
              '(including legal fees) arising out of your Content, your use of the Service, or your breach of these Terms.'),
     ]),
     ("termination", "12. Suspension &amp; termination", [
        ('p', 'We may suspend or remove your listing or account, with or without notice, if you breach these Terms or if we consider '
              'it necessary to protect the Service or other users. You may stop using the Service at any time.'),
     ]),
     ("changes", "13. Changes to these terms", [
        ('p', 'We may update these Terms from time to time. The updated version will be posted on this page with a revised date, '
              'and continued use of the Service after changes means you accept the revised Terms.'),
     ]),
     ("law", "14. Governing law", [
        ('p', 'These Terms are governed by the laws of India. Any disputes shall be subject to the exclusive jurisdiction of the '
              'courts of Goa, India.'),
     ]),
     ("contact", "15. Contact us", [
        ('p', f'Questions about these Terms? Email us at <a href="mailto:{EMAIL}">{EMAIL}</a> or call/WhatsApp '
              f'<a href="{WA}" target="_blank" rel="noopener">{PHONE}</a>.'),
     ]),
    ]
    parts = [head(title, desc, url, [breadcrumb_ld("Terms of Use", url)])]
    parts.append(crumb("Terms of Use"))
    parts.append(hero("Legal", "Terms of Use", "The rules for using Goa Directory. Please read them carefully."))
    parts.append('<main class="sec"><div class="wrap"><div class="doc"><div class="prose">')
    parts.append(f'<p class="updated">Last updated: {UPDATED}</p>')
    parts.append(sections_to_html(S))
    parts.append(CONTACT_CARD)
    parts.append('</div></div></div></main>')
    (DEPLOY / "goa-terms.html").write_text(wrap_page(parts), encoding="utf-8")
    print("built goa-terms.html")

# =============================================================== REFUND
def build_refund():
    url = SITE + "/refund-policy/"
    title = "Refund Policy — No Refund | Goa Directory"
    desc = ("Goa Directory operates a strict no-refund policy. All listing and advertising fees are "
            "non-refundable once payment is made. Read the full policy and the reasons here.")
    S = [
     ("overview", "1. Overview", [
        ('p', 'This Refund Policy explains how payments for listings and advertising on Goa Directory '
              f'(<a href="{SITE}/">www.goadirectory.in</a>) are handled. By purchasing any plan or paid service, '
              'you acknowledge and agree to this policy.'),
     ]),
     ("norefund", "2. No refund policy", [
        ('warn', '<b>All payments made to Goa Directory are final and non-refundable.</b> Once a listing plan or advertising '
                 'service has been purchased, we do not offer refunds, cancellations or credits, whether in full or in part.'),
        ('p', 'This applies to all plans — Basic, Standard and Premium — and to any add-ons, renewals or promotional purchases.'),
     ]),
     ("why", "3. Why fees are non-refundable", [
        ('p', 'Our listing services are digital and begin immediately after purchase. Costs such as review, publishing, '
              'design placement, and distribution across our network are incurred as soon as your listing goes live. '
              'For this reason, fees cannot be returned once the service has started.'),
     ]),
     ("cancel", "4. Cancellation", [
        ('p', 'You may choose to stop using the Service or not renew at the end of your billing period. Cancelling does not '
              'entitle you to a refund for the current or any past term, and your listing will remain live until the end of '
              'the paid period unless removed for a breach of our '
              f'<a href="{SITE}/terms-of-use/">Terms of Use</a>.'),
     ]),
     ("exceptions", "5. Limited exceptions", [
        ('p', 'The only situations we may consider are:'),
        ('ul', [
            'A <b>duplicate payment</b> caused by a technical error on our side (the duplicate amount will be returned);',
            'A payment for which <b>no service was ever provided</b> due to a verified fault on our part.',
        ]),
        ('p', 'Any such request must be raised within 7 days of payment with proof of the transaction. Approval is at our sole '
              'discretion and is not guaranteed.'),
     ]),
     ("chargebacks", "6. Chargebacks", [
        ('p', 'If you initiate a chargeback or payment dispute without first contacting us to resolve the issue, we reserve '
              'the right to suspend or remove your listing and account. Please reach out to us first — we are happy to help.'),
     ]),
     ("changes", "7. Changes to this policy", [
        ('p', 'We may update this Refund Policy from time to time. The current version will always be available on this page '
              'with a revised date.'),
     ]),
     ("contact", "8. Contact us", [
        ('p', f'For any billing question, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call/WhatsApp '
              f'<a href="{WA}" target="_blank" rel="noopener">{PHONE}</a> before raising a dispute.'),
     ]),
    ]
    parts = [head(title, desc, url, [breadcrumb_ld("Refund Policy", url)])]
    parts.append(crumb("Refund Policy"))
    parts.append(hero("Legal", "Refund Policy", "Goa Directory operates a strict no-refund policy on all paid services."))
    parts.append('<main class="sec"><div class="wrap"><div class="doc"><div class="prose">')
    parts.append(f'<p class="updated">Last updated: {UPDATED}</p>')
    parts.append(sections_to_html(S))
    parts.append(CONTACT_CARD)
    parts.append('</div></div></div></main>')
    (DEPLOY / "goa-refund.html").write_text(wrap_page(parts), encoding="utf-8")
    print("built goa-refund.html")

# =============================================================== PRIVACY
def build_privacy():
    url = SITE + "/privacy-policy/"
    title = "Privacy Policy | Goa Directory"
    desc = ("How Goa Directory collects, uses and protects your personal information when you use our "
            "local business directory, submit a listing or contact us.")
    S = [
     ("intro", "1. Introduction", [
        ('p', 'Goa Directory ("we", "us", "our") respects your privacy. This Privacy Policy explains what information we '
              f'collect through <a href="{SITE}/">www.goadirectory.in</a>, how we use it, and the choices you have. '
              'By using the Service you agree to this policy.'),
     ]),
     ("collect", "2. Information we collect", [
        ('h3', 'Information you provide'),
        ('ul', [
            'Account details such as your name, username, email and password;',
            'Business listing details — business name, category, description, address, phone/WhatsApp, email, website and photos;',
            'Messages you send us through forms, email or WhatsApp.',
        ]),
        ('h3', 'Information collected automatically'),
        ('ul', [
            'Basic usage and device data (IP address, browser type, pages viewed) via server logs and cookies;',
            'Listing view counts and interactions to improve the directory.',
        ]),
     ]),
     ("use", "3. How we use your information", [
        ('ul', [
            'To create and display your business listing and account;',
            'To review, publish, edit and manage listings;',
            'To respond to your enquiries and provide support;',
            'To operate, secure, maintain and improve the Service;',
            'To send important service or account notices.',
        ]),
     ]),
     ("cookies", "4. Cookies", [
        ('p', 'We use cookies and similar technologies to keep you logged in, remember preferences, and understand how the '
              'Service is used. You can control cookies through your browser settings; disabling them may affect some features.'),
     ]),
     ("sharing", "5. How we share information", [
        ('p', 'We do not sell your personal information. Listing details you submit are published publicly as part of your '
              'directory listing. We may share limited data with trusted service providers (such as hosting and email) who '
              'help us run the Service, and where required by law. Premium listings may also be displayed on our partner '
              'network sites as described on the Plans page.'),
     ]),
     ("retention", "6. Data retention", [
        ('p', 'We keep your information for as long as your listing or account is active and as needed to provide the Service, '
              'comply with legal obligations, resolve disputes and enforce our agreements.'),
     ]),
     ("rights", "7. Your rights &amp; choices", [
        ('p', 'You may request to access, correct or delete your personal information, or ask us to unpublish your listing, '
              f'by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. We will respond within a reasonable time.'),
     ]),
     ("security", "8. Security", [
        ('p', 'We use reasonable technical and organisational measures to protect your information. However, no method of '
              'transmission or storage is completely secure, and we cannot guarantee absolute security.'),
     ]),
     ("children", "9. Children", [
        ('p', 'The Service is intended for users aged 18 and above and is not directed at children. We do not knowingly '
              'collect personal information from children.'),
     ]),
     ("changes", "10. Changes to this policy", [
        ('p', 'We may update this Privacy Policy from time to time. The revised version will be posted here with a new date.'),
     ]),
     ("contact", "11. Contact us", [
        ('p', f'For any privacy question or request, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call/WhatsApp '
              f'<a href="{WA}" target="_blank" rel="noopener">{PHONE}</a>.'),
     ]),
    ]
    parts = [head(title, desc, url, [breadcrumb_ld("Privacy Policy", url)])]
    parts.append(crumb("Privacy Policy"))
    parts.append(hero("Legal", "Privacy Policy", "How we collect, use and protect your information on Goa Directory."))
    parts.append('<main class="sec"><div class="wrap"><div class="doc"><div class="prose">')
    parts.append(f'<p class="updated">Last updated: {UPDATED}</p>')
    parts.append(sections_to_html(S))
    parts.append(CONTACT_CARD)
    parts.append('</div></div></div></main>')
    (DEPLOY / "goa-privacy.html").write_text(wrap_page(parts), encoding="utf-8")
    print("built goa-privacy.html")

# =============================================================== FAQ
def build_faq():
    url = SITE + "/faq-help/"
    title = "FAQ &amp; Help — Listing Your Business in Goa | Goa Directory"
    desc = ("Answers to common questions about listing your business on Goa Directory — how to add a listing, "
            "plans and pricing, editing, photos, categories, payments and support.")
    GROUPS = [
     ("Getting started", [
        ("What is Goa Directory?",
         'Goa Directory is a trusted local business directory and classifieds platform for Goa. It helps shops, services, '
         'restaurants, hotels and professionals get discovered by customers searching online across Goa.'),
        ("How do I list my business on Goa Directory?",
         f'Choose a plan on our <a href="{SITE}/plans/">Plans</a> page, then fill in the '
         f'<a href="{SITE}/form/">listing form</a> with your business details and up to 16 photos. Our team reviews every '
         'submission and publishes it once approved.'),
        ("Do I need an account to list my business?",
         'You can submit your business through our listing form without logging in. If you have an account, you can '
         f'<a href="{SITE}/login-2/">log in</a> to manage your listings.'),
     ]),
     ("Plans &amp; pricing", [
        ("How much does a listing cost?",
         'We offer three annual plans: Basic at ₹3,500/year, Standard at ₹6,000/year, and Premium at ₹10,000/year '
         f'(discounted from ₹12,000). See full features on the <a href="{SITE}/plans/">Plans</a> page.'),
        ("What extra reach do I get with Premium?",
         'Premium lists your business on GoaDirectory.in plus our partner network — goa.sanctify.in, goa.sanctify.biz, '
         'goa.sanctify.co.in, goa.sanctify.info, goa.sanctify.co and www.vc.goa.guru — for maximum visibility, along with '
         'up to 16 photos and top placement.'),
        ("How do I pay?",
         'After you submit your listing and choose a plan, our team confirms your details and shares payment options with you. '
         'No payment is taken online at submission.'),
        ("Are payments refundable?",
         f'No. All fees are non-refundable. Please review our <a href="{SITE}/refund-policy/">Refund Policy</a> before purchasing.'),
     ]),
     ("Managing your listing", [
        ("How long until my listing goes live?",
         'Most listings are reviewed and published within one business day after we receive your details and confirm your plan.'),
        ("How many photos can I add?",
         'Basic allows up to 5 photos, Standard up to 10, and Premium up to 16. The first photo becomes your cover image.'),
        ("Can I edit my listing after it is published?",
         f'Yes. Contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or WhatsApp '
         f'<a href="{WA}" target="_blank" rel="noopener">{PHONE}</a> with your changes and we will update it for you.'),
        ("Which category should I choose?",
         f'Pick the category that best matches your main business activity. You can browse all categories on our '
         f'<a href="{SITE}/categories/">Categories</a> page. Premium listings can appear in multiple categories.'),
     ]),
     ("Support", [
        ("How do I contact Goa Directory?",
         f'Email <a href="mailto:{EMAIL}">{EMAIL}</a>, call or WhatsApp '
         f'<a href="{WA}" target="_blank" rel="noopener">{PHONE}</a>, or use our '
         f'<a href="{SITE}/contact-us/">Contact</a> page. We usually reply within one business day.'),
        ("I found a wrong or outdated listing — what should I do?",
         f'Please let us know at <a href="mailto:{EMAIL}">{EMAIL}</a> with the listing name and the correction, and we will '
         'review and update it.'),
     ]),
    ]
    # FAQPage schema (flatten all Q&A)
    faq_items = []
    for _, qas in GROUPS:
        for q, a in qas:
            plain = re.sub('<[^>]+>', '', a)
            faq_items.append({"@type": "Question", "name": re.sub('<[^>]+>', '', q),
                              "acceptedAnswer": {"@type": "Answer", "text": plain}})
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}

    parts = [head(title, desc, url, [breadcrumb_ld("FAQ / Help", url), faqpage])]
    parts.append(crumb("FAQ / Help"))
    parts.append(hero("Help Centre", "FAQ &amp; Help",
                      "Everything you need to know about listing and growing your business on Goa Directory."))
    parts.append('<main class="sec"><div class="wrap"><div class="faq">')
    for cat, qas in GROUPS:
        parts.append(f'<div class="cat">{cat}</div>')
        for q, a in qas:
            parts.append(f'<details><summary>{q}<span class="pl">+</span></summary><div class="ans">{a}</div></details>')
    parts.append(CONTACT_CARD)
    parts.append('</div></div></main>')
    (DEPLOY / "goa-faq.html").write_text(wrap_page(parts), encoding="utf-8")
    print("built goa-faq.html")

if __name__ == "__main__":
    build_login()
    build_terms()
    build_refund()
    build_privacy()
    build_faq()
    print("chrome sizes -> CSS:", len(CSS), "HEADER:", len(HEADER), "NAV_ASSETS:", len(NAV_ASSETS),
          "FOOTER:", len(FOOTER), "SCROLLTOP:", len(SCROLLTOP))
