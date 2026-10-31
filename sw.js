// Network-first: always loads the latest files when online, and only falls back
// to the cache when offline. The cache refreshes itself on every visit, so there
// is no version number to bump when you change your site.
const CACHE = 'woq';
const FONT_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com'];

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin && !FONT_HOSTS.includes(url.hostname)) return;

  event.respondWith(
    fetch(req)
      .then(res => {
        if (res && (res.ok || res.type === 'opaque')) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
        }
        return res;
      })
      .catch(async () => {
        const cache = await caches.open(CACHE);
        let hit = await cache.match(req, { ignoreSearch: true });
        if (!hit && req.mode === 'navigate') {
          const path = url.pathname;
          const guess = path.endsWith('/') ? 'index.html' : path.replace(/^.*\//, '') + '.html';
          hit = (await cache.match(guess)) || (await cache.match('index.html'));
        }
        return hit || Response.error();
      })
  );
});
