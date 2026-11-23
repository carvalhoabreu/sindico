/* Síndico · service worker das notificações. Recebe o push do Firebase Cloud Messaging direto (sem carregar
   bibliotecas de fora, que alguns navegadores e antivírus bloqueiam) e mostra a notificação com o botão de ação. */

self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });

self.addEventListener('push', function (e) {
  var p = {};
  try { p = e.data ? e.data.json() : {}; } catch (err) { p = {}; }
  var d = p.data || p || {};
  e.waitUntil(self.registration.showNotification(d.titulo || 'Síndico', {
    body: d.corpo || '',
    icon: 'icon-192.png',
    badge: 'icon-192.png',
    tag: d.tag || undefined,
    renotify: !!d.tag,
    data: { link: d.link || './' },
    actions: [{ action: 'abrir', title: d.acao || 'Abrir' }]
  }));
});

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
