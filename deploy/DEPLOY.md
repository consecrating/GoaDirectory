# Go-live plan for the Goa Directory homepage redesign

Target: https://www.goadirectory.in/ (WordPress + ClassiPress `online-classified` theme)

The redesign is a self-contained page (its own header/footer/CSS). Deploying it as a
WordPress **page template + static front page** keeps WordPress routing intact and is
fully reversible (no theme core edits, no static index.html at web root).

## What I need from you (pick one)
1. **FTPS access** (host, username, password) — same as the earlier remediation — plus WordPress admin, OR
2. **WordPress admin login** (URL + user + password / application password), OR
3. Add me via the hosting panel.

Credentials are used only for this deploy, kept in an ephemeral shell variable, and never printed, logged, or committed.

## Deploy steps (I will run these, with a backup first)
1. **Back up first:** database export + copy of the current active theme, verified by hash (same procedure as the security audit).
2. Upload `template-goadirectory-home.php` to the active theme:
   `wp-content/themes/online-classified/template-goadirectory-home.php`
3. In WordPress: create a Page titled "Home (New)", assign template **"Goa Directory Home (Redesign)"**, publish.
4. Settings → Reading → "Your homepage displays" = **A static page** → Home page = the new page. (Records the previous setting for instant rollback.)
5. Flush caches; verify the live homepage renders and every link resolves.

## Rollback (instant)
- Settings → Reading → restore the previous "Your homepage displays" setting.
- Optionally delete the template file and page. No other files are touched.

## Notes before go-live
- **Images:** featured/blog/card images currently use neutral placeholders. For production I should swap in each listing's real featured image from the site (recommended before or right after go-live).
- **Fonts:** loaded from Google Fonts CDN (Poppins, Caveat).
- **Brand name** is "Goa Directory". Tell me if you want "GoaBiz" instead.
- All 33 internal links are real and were verified returning HTTP 200.
