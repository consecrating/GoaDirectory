# GoaDirectory Security and Integrity Audit

**Site:** https://www.goadirectory.in  
**Completed:** 2026-08-30 UTC  
**Production stack observed:** WordPress 7.1, PHP 8.1.34, MySQL 5.7.23, ClassiPress 4.1.4

## Outcome

No concrete malware, webshell, obfuscated payload, hidden administrator creation code, executable upload, or core/plugin integrity compromise was found. Confirmed exposure, authorization, CSRF, upload, TLS, spam-abuse, PHP compatibility, and obsolete attack-surface issues were remediated after validated backups.

## Validated rollback backups

- Database: `/projects/sandbox/work/gd-security-db-26806bfc.sql.gz`
  - 3,825,269 bytes; 183 tables; gzip integrity valid
  - SHA-256: `e632bda7dcaa94ade64254fa98a9449deb7c727752d7322da29b65b1bd1fbfec`
- Code/security snapshot: `/projects/sandbox/work/gd-security-code-26806bfc.zip`
  - 58,549,788 bytes; 9,731 entries; ZIP integrity valid
  - SHA-256: `7673e11fe8af5fd83608d1f305c9a7976948b70ac310a75ee52e0b5faaa0f8ca`
- Public root archives were individually downloaded, checksum-recorded, and ZIP-tested before deletion.

## Remediation completed

### Public exposure and attack surface

- Removed 7 public root backup/maintenance artifacts, including three full-site archives and unauthenticated `repair-wordpress-core.php`.
- Removed an expired public cookie file, stale static sitemap/URL list, and unused legacy Universal Analytics script.
- Removed all 11 inactive plugins and 4 obsolete inactive themes.
- Retained one recovery theme and updated Twenty Twenty-Five to 1.5.
- Removed 6 stale plugin upload directories, 2 unnecessary `.well-known` PHP stubs, 2 web-root theme rollback copies, and orphaned `admin_ips.txt`.
- Removed 35 orphaned cron events. All 14 remaining hooks have registered callbacks.
- Removed the temporary audit endpoint and revoked/deleted its local token.

### Active ClassiPress hardening

- Added nonce, capability, and object-level authorization to order-state AJAX actions.
- Added action/object-scoped nonces to dashboard listing pause, restart, delete, sold, and unsold operations.
- Added `manage_options`, nonce, strict positive-ID, duplicate-ID, and typed database-update checks to custom-field sorting.
- Bound uploads to an editable parent post; enforced server-side JPEG/PNG/GIF byte/MIME checks and safe upload error handling.
- Added attachment deletion authorization and reliable JSON/client failure behavior.
- Added report type, moderator capability, recipient consistency, and target-object authorization before report deletion.
- Enabled TLS certificate verification for PayPal IPN and PDT validation.
- Initialized and sanitized contact fields, required a published listing, capped message length, added a serialized per-actor rate limit, normalized JSON errors, and restored the form after transport failures.
- Added PHP 8.1/8.2 compatibility fixes for five optional-before-required signatures, P2P autoloader properties, and contact-method filter initialization.

## Final verification evidence

- WordPress 7.1 core: **3,338 / 3,338** official core-scope checksums matched; 0 missing, 0 mismatched.
- Active plugins: Classic Editor 1.7.0, Disable Gutenberg 3.3.2, and WP Bulk Delete 1.4.4 previously matched their exact WordPress.org releases byte-for-byte; no updates are pending.
- PHP: **7,207** PHP-family files linted; 0 syntax failures.
- JavaScript: 4 modified source/bundle files parsed; 0 syntax failures.
- Deployment: all **19** final modified active-theme files matched local SHA-256 hashes over FTPS.
- Routes returned HTTP 200: homepage, a current listing, login page, REST index, native sitemap, and cron endpoint.
- Authenticated Application Password checks succeeded for `/users/me`, edit-context posts, and password enumeration. The temporary test password was revoked; only the pre-existing requested `Sophia` password remains.
- Contact validation returned normalized JSON without sending mail; invalid upload/report requests were rejected; unauthenticated dashboard mutation redirected to login.
- Classic Editor remains forced site-wide (`classic-editor-replace=classic`, switching disabled).
- Final upload scan: 2,941 files, 0 executable files, 0 symlinks. Four image byte-pattern alerts retain the manually validated image hashes.
- Final root scan: 0 public archives and no unexpected PHP after audit-endpoint removal.
- Final PHP `error_log`: **0 bytes after all verification traffic**.

## Owner confirmation still required

The administrator accounts `admin`, `Liya`, and `sophia` were preserved because account legitimacy cannot be established from code or filesystem evidence. Confirm that all three are expected; remove or demote any account that is not recognized.

## Hosting-level recommendations

- Upgrade PHP 8.1 to a currently supported PHP 8.3+ release after staging compatibility verification.
- Upgrade MySQL 5.7 to MySQL 8.0+ through the hosting provider.
- Add a persistent object cache only if supported and monitored by the host.
- Confirm the browser-exposed Google Maps API key is restricted by HTTP referrer and only the required Maps APIs in Google Cloud Console.

## Deliberately not changed

The legacy escrow admin UI contains a `fail-order-refund` button without a matching handler, while a separate `refund-order` handler has no built-in caller. Because the intended financial state transition is ambiguous, this was not guessed or changed during security remediation. Confirm the desired escrow business rule before altering it.
