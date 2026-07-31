/**
 * ProfitPilot Service Worker — v7 (real caching SW)
 * ==================================================
 * Replaces the temporary "kill-switch" SW that only evicted broken clients.
 *
 * Strategy (per request type):
 *   • Fresh data (predictions.json, news_cache.json, /api/*): NETWORK-FIRST.
 *       Always hit the network so the app shows today's picks; fall back to the
 *       last cached copy only when offline. This is the fix for "stale / stalled"
 *       — data is never served from cache while a network is reachable.
 *   • Navigation (HTML documents): NETWORK-FIRST with cache fallback, then
 *       offline.html. A new deploy is picked up immediately; offline still works.
 *   • Static assets (icons, manifest, fonts, css): CACHE-FIRST (stale-while-
 *       revalidate) — instant load, refreshed in the background.
 *
 * Versioning: bump CACHE_VERSION on every shell change. `activate` deletes all
 * caches that don't match, so old shells can never get stuck.
 */

const CACHE_VERSION = 'v7.0.0';
const SHELL_CACHE = `pp-shell-${CACHE_VERSION}`;
const DATA_CACHE  = `pp-data-${CACHE_VERSION}`;
const ASSET_CACHE = `pp-assets-${CACHE_VERSION}`;
const ALL_CACHES  = [SHELL_CACHE, DATA_CACHE, ASSET_CACHE];

// App shell — precached on install so the app opens instantly / offline.
const SHELL_ASSETS = [
  './',
  './index.html',
  './offline.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
];

// Requests that must always try the network first (fresh data).
const DATA_PATHS = ['predictions.json', 'news_cache.json', '/api/'];

function isDataRequest(url) {
  return DATA_PATHS.some(p => url.pathname.includes(p) || url.href.includes(p));
}

function isStaticAsset(url) {
  return /\.(png|jpg|jpeg|svg|webp|ico|css|woff2?|ttf)$/i.test(url.pathname) ||
         url.hostname.includes('fonts.googleapis.com') ||
         url.hostname.includes('fonts.gstatic.com');
}

// ── INSTALL: precache the shell, activate immediately ──
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL_CACHE);
    // addAll fails the whole install if any single asset 404s; add resiliently.
    await Promise.all(SHELL_ASSETS.map(async (a) => {
      try { await cache.add(new Request(a, { cache: 'reload' })); } catch (e) { /* skip */ }
    }));
    self.skipWaiting();
  })());
});

// ── ACTIVATE: drop stale caches, take control of open clients ──
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => !ALL_CACHES.includes(k)).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

// ── Allow the page to force an immediate update ──
self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});

// ── FETCH ──
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  let url;
  try { url = new URL(req.url); } catch (e) { return; }

  // 1) Fresh data → network-first, cache fallback.
  if (isDataRequest(url)) {
    event.respondWith(networkFirst(req, DATA_CACHE));
    return;
  }

  // 2) Navigations (HTML) → network-first, cache fallback, then offline.html.
  if (req.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const fresh = await fetch(req);
        const cache = await caches.open(SHELL_CACHE);
        cache.put('./index.html', fresh.clone()).catch(() => {});
        return fresh;
      } catch (e) {
        const cache = await caches.open(SHELL_CACHE);
        return (await cache.match('./index.html')) ||
               (await cache.match('./')) ||
               (await cache.match('./offline.html')) ||
               Response.error();
      }
    })());
    return;
  }

  // 3) Static assets → cache-first (stale-while-revalidate).
  if (isStaticAsset(url)) {
    event.respondWith(staleWhileRevalidate(req, ASSET_CACHE));
    return;
  }

  // 4) Everything else same-origin → network, fall back to any cache.
  if (url.origin === self.location.origin) {
    event.respondWith((async () => {
      try { return await fetch(req); }
      catch (e) { return (await caches.match(req)) || Response.error(); }
    })());
  }
});

async function networkFirst(req, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(req, { cache: 'no-store' });
    if (fresh && fresh.ok) cache.put(req, fresh.clone()).catch(() => {});
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    if (cached) return cached;
    throw e;
  }
}

async function staleWhileRevalidate(req, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  const network = fetch(req).then(res => {
    if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()).catch(() => {});
    return res;
  }).catch(() => null);
  return cached || (await network) || Response.error();
}
