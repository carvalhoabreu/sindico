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

/* Receber do menu Compartilhar do Android (WhatsApp, Galeria, Arquivos): guarda no aparelho e abre o app
   na tela "Anexar a qual tarefa?". Nada sai do aparelho aqui; o envio é feito pelo app depois de escolher a tarefa. */
function abrirBanco() {
  return new Promise(function (ok, erro) {
    var r = indexedDB.open('sindico-app', 1);
    r.onupgradeneeded = function () {
      var db = r.result;
      if (!db.objectStoreNames.contains('fila')) db.createObjectStore('fila', { keyPath: 'idCliente' });
      if (!db.objectStoreNames.contains('compartilhado')) db.createObjectStore('compartilhado', { keyPath: 'id' });
    };
    r.onsuccess = function () { ok(r.result); };
    r.onerror = function () { erro(r.error); };
  });
}
self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'POST') return;
  var u = new URL(e.request.url);
  if (u.searchParams.get('compartilhar') !== '1') return;
  e.respondWith(e.request.formData().then(function (fd) {
    var arquivos = fd.getAll('arquivos').filter(function (f) { return f && typeof f !== 'string' && f.size; }).slice(0, 10)
      .map(function (f) { return { nome: f.name || 'arquivo', tipo: f.type || 'application/octet-stream', blob: f }; });
    var reg = { id: 'atual', titulo: String(fd.get('titulo') || ''), texto: String(fd.get('texto') || ''), link: String(fd.get('link') || ''), arquivos: arquivos, em: Date.now() };
    return abrirBanco().then(function (db) {
      return new Promise(function (ok) {
        var tx = db.transaction('compartilhado', 'readwrite');
        tx.objectStore('compartilhado').put(reg);
        tx.oncomplete = ok; tx.onerror = ok; tx.onabort = ok;
      });
    });
  }).catch(function () {}).then(function () {
    return Response.redirect(new URL('./?compartilhado=1', self.registration.scope).href, 303);
  }));
});
