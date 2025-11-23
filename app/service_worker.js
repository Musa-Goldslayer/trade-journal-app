self.addEventListener('install', event => {
  console.log("Service Worker installed");
});

self.addEventListener('fetch', event => {
  // Mode simple : on laisse tout passer sans cache
  event.respondWith(fetch(event.request));
});
