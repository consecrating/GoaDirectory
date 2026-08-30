# GoaDirectory redesign audit

## Design read

A local discovery marketplace for Goa residents, visitors, and independent businesses. The redesign should feel trust-first and place-specific, combining Goa's editorial identity with fast category and location search.

**Design dials:** variance 8/10, motion 5/10, visual density 5/10.

## Live homepage audit

Source: https://www.goadirectory.in/

- Current title: `Goa Directory – Goa’s Trusted Local Classifieds`
- Current H1: `Goa Directory`
- Current sections: generic page-title hero, Featured Listings, full category list, Latest Listings, From the Blog.
- Current primary actions: Post an Ad, Login, category navigation, listing cards, View More Ads.
- Real listings selected for preview copy: S Nizami Interiors, Mahalaxmi Electric Co, 13 Studio Unisex Salon, SANCTIFY, Verlekar Jewellers, Vasco Pest Control, H.N. Techno Service, Royal Car & Bike Rental, A One Flowers, Ria's Hair & Beauty Salon.
- Visual baseline: white and light gray surfaces, solid red navigation/action color, wide empty hero, card grid, no prominent search experience.
- SEO baseline: canonical is present; WebSite, Organization, and WebPage JSON-LD exist; organization logo and page image incorrectly resolve to `No image found`; OG image is the theme logo rather than a purpose-built social image; there is one H1, but `Home` is an unnecessary H2; category links provide crawl depth but are visually overwhelming.
- UX/CWV opportunities: make search the primary hero task, surface location/category intent, reduce the 42-item category wall, reserve media dimensions, lazy-load below-fold imagery, and avoid a carousel as the LCP element.

## Live Counto Motors listing audit

Source: https://www.goadirectory.in/ads/counto-motors-mercedes-benz-dealership-ribandar-goa/

### Verified listing facts

- Listing name: Counto Motors | Mercedes Benz Dealership in Ribandar - Goa
- Category: Automobiles
- Contact number shown: 8308-10-5556
- Location shown: Mercedes Benz Showroom, Ribandar, Goa 403006
- Owner label: Liya, Listing Owner
- Published: April 13, 2016
- Status shown: This ad has expired
- Gallery: 13 images, including Mercedes-Benz logo and model photography
- Core description: Counto Motors is described as an Alcon Group sister company and the authorized Mercedes-Benz passenger-vehicle dealership for Goa.
- Primary intent: learn about the dealership, call/contact, locate it, browse gallery, and request a test drive.

### Structural and SEO findings

- Canonical and article Open Graph metadata are present.
- The page contains four H1 elements; the redesign must use one descriptive H1 and move content subheads to H2/H3.
- Existing Offer schema misinterprets the phone number as `price` and `Contact No.` as `priceCurrency`; this should be replaced with appropriate LocalBusiness/AutoDealer, BreadcrumbList, ImageObject, and WebPage markup, with Offer only when a real commercial offer and price exist.
- Gallery images have empty alt text; the redesign requires concise, factual alt text.
- The body contains a dense block of legacy external exact-match links and repeated keywords; this should not be reproduced in visible design copy.
- The listing ID says Porvorim while the title/address say Ribandar; implementation needs owner verification rather than silently changing the source record.
- Several outbound links are HTTP and appear obsolete; concepts use a clear verified Website/Test Drive action without inventing a destination.
- The current map loads synchronously and triggers a Google Maps performance warning. A static map preview with click-to-load interaction is preferred.
- Comments occupy substantial space despite zero comments; concepts prioritize business facts, actions, gallery, map, and related listings.

## Preview-level SEO architecture

### Homepage

1. One H1 focused on local discovery in Goa.
2. Search form with query, category, and location inputs plus crawlable category/location links.
3. Curated popular categories and local-area links rather than an unfiltered category wall.
4. ItemList markup for featured/latest listings, WebSite SearchAction, Organization, and WebPage schema.
5. Editorial guides as internal-link hubs for topical authority.
6. Purpose-built Open Graph image, descriptive metadata, and stable media dimensions.

### Listing detail

1. Breadcrumbs followed by one H1 with business name, service, and place.
2. Above-fold verified facts and Call, Directions, Contact, Save, and Website/Test Drive actions.
3. Accessible gallery with reserved aspect ratios and descriptive alt text.
4. Scannable About, Services, Location, Hours/verification state, and Related listings sections.
5. LocalBusiness/AutoDealer, PostalAddress, BreadcrumbList, ImageObject, and WebPage schema using only verified fields.
6. No fake reviews, opening hours, prices, ratings, or operational claims.

## Target delivery quality

- LCP under 2.5 seconds, CLS under 0.1, INP under 200 milliseconds.
- WCAG 2.2 AA contrast, visible focus states, 44 px minimum touch targets, semantic landmarks, and keyboard-operable galleries.
- Responsive HTML content remains indexable without requiring client-side JavaScript.
