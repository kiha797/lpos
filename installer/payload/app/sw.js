const CACHE='labelpos-msi-v1-0-1';
const FILES=['./','./index.html','./style.css','./app.js','./icon.svg','./icon-192.png','./icon-512.png','./manifest.webmanifest','./vendor/bwip-js-min.js','./vendor/xlsx.full.min.js','./vendor/lucide.min.js'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('labelpos-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{if(event.request.method!=='GET'||new URL(event.request.url).origin!==location.origin||event.request.url.endsWith('.zip'))return;event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request)));});
