// Bump this version whenever memory.html / assets change, so clients drop the old cache.
const CACHE_VERSION = 'v6';
const CACHE_NAME = `memory-quiz-cache-${CACHE_VERSION}`;
const ASSETS = [
  './',
  './index.html',
  './memory.html',
  './manifest.json',
  './icon.png',
  './icon-192.png',
  './icon-512.png'
];

// Install: pre-cache assets and activate the new SW immediately.
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      // Cache each asset independently: one failure must not abort the install.
      Promise.all(ASSETS.map((url) => cache.add(url).catch(() => null)))
    )
  );
});

// Activate: delete old caches and take control of open pages.
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      ))
      .then(() => self.clients.claim())
  );
});

function isDocumentRequest(request) {
  return request.mode === 'navigate' ||
    (request.destination === 'document') ||
    (request.headers.get('accept') || '').includes('text/html');
}

// Fetch strategy:
// - Navigations/documents: network first, cache fallback (never serve stale HTML).
// - Other assets: cache first, then network, and cache the response at runtime.
self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  if (isDocumentRequest(request)) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy)).catch(() => {});
          return response;
        })
        .catch(() =>
          caches.match(request).then((cached) =>
            cached || caches.match('./memory.html')
          )
        )
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        if (response && response.status === 200 && response.type === 'basic') {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy)).catch(() => {});
        }
        return response;
      });
    })
  );
});
