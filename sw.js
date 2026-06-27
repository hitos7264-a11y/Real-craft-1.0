const CACHE = "hrgm-voxel-v2";
const ASSETS = [
  "/",
  "/index.html",
  "/hrgm_voxel_world.html",
  "/manifest.webmanifest",
  "/native.js",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
  "/icons/icon-512-maskable.png",
  "/icons/icon.svg"
];

self.addEventListener("install", (ev) => {
  ev.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (ev) => {
  ev.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (ev) => {
  if (ev.request.method !== "GET") return;
  const url = new URL(ev.request.url);
  if (url.origin !== self.location.origin) return;

  ev.respondWith(
    caches.match(ev.request).then((cached) => {
      const fetchLive = fetch(ev.request).then((res) => {
        if (res && res.status === 200) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(ev.request, copy));
        }
        return res;
      });
      return cached || fetchLive.catch(() => cached);
    })
  );
});
