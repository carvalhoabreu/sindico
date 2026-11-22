/* Síndico · service worker das notificações (Firebase Cloud Messaging). A configuração vem no endereço (?cfg=). */
importScripts('https://www.gstatic.com/firebasejs/10.12.5/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.5/firebase-messaging-compat.js');

var cfg = {};
try { cfg = JSON.parse(new URL(self.location.href).searchParams.get('cfg') || '{}'); } catch (e) { cfg = {}; }

self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });

if (cfg && cfg.projectId) {
  firebase.initializeApp(cfg);
  firebase.messaging().onBackgroundMessage(function (p) {
    var d = (p && p.data) || {};
    return self.registration.showNotification(d.titulo || 'Síndico', {
      body: d.corpo || '',
      icon: 'icon-192.png',
      badge: 'icon-192.png',
      tag: d.tag || undefined,
      renotify: !!d.tag,
      data: { link: d.link || './' },
      actions: [{ action: 'abrir', title: d.acao || 'Abrir' }]
    });
  });
}

/* Toque na notificação (ou no botão de ação): abre o app direto na tela certa. */
self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  var link = (e.notification.data && e.notification.data.link) || './';
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (janelas) {
    for (var i = 0; i < janelas.length; i++) {
      var w = janelas[i];
      if (w.url.indexOf(self.registration.scope) === 0 && 'focus' in w) {
        return w.focus().then(function (c) { return c.navigate ? c.navigate(link) : null; }).catch(function () { return self.clients.openWindow(link); });
      }
    }
    return self.clients.openWindow(link);
  }));
});
