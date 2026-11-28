#!/usr/bin/env python3
"""Site 1.41 - modulo Bom dia, etapa 1 (so leitura). Pareia com o Motor 0.39.0 (Bom_Dia.gs).
O que faz no index.html:
  - card "Bom dia" na grade MODULOS do menu do portal, ao lado de Tarefas (subtitulo "N pagamento(s) a confirmar" + selo dourado
    = pagamentos a confirmar + prazos vencidos); item "Bom dia" na lateral do computador;
  - tela do modulo (?m=bomdia): KPIs, Pagamentos a confirmar, Acompanhando (Com voce / Aguardando), Rotinas de hoje;
  - bomdia.painel entra em API_LEITURA (so le; nada grava);
  - remove da grade os cards "Em breve" (Seguros, Contas de consumo, Orcamentos).
Uso: aplicar_bomdia_141.py <index.html de entrada> <index.html de saida>
Confere o hash da base (1.40 = 5cddbcbed727d1d1) e para se o site mudou."""
import sys, hashlib
BASE = '5cddbcbed727d1d1'
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
h = hashlib.sha256(t.encode('utf-8')).hexdigest()
if not h.startswith(BASE):
    sys.exit('PARADO: o index nao e a 1.40 (hash %s). Refazer sobre o site novo.' % h[:16])
def troca(a, b):
    global t
    if t.count(a) != 1: sys.exit('PARADO: trecho nao encontrado uma vez so: ' + a[:70])
    t = t.replace(a, b)

troca("var VERSAO_SITE = '1.40';", "var VERSAO_SITE = '1.41';")

# ---------------------------------------------------------------- CSS
troca("/* ================= v1.36 (C2): Meus condomínios e Como chegar", r"""/* ================= v1.41 (Bom dia, etapa 1): ?m=bomdia — tokens do bloco v1.30 ================= */
.bd-tile{position:relative}
.bd-selo{position:absolute;top:.5em;right:.5em;min-width:1.6em;height:1.6em;padding:0 .45em;border-radius:999px;background:var(--ouro);color:var(--azul);font-size:.75em;font-weight:700;display:flex;align-items:center;justify-content:center}
.bd{padding:.5em 1.5em 2.5em;flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;display:flex;flex-direction:column;gap:var(--esp-4)}
.bd>*{max-width:76em;width:100%}
.bd-hero{background:var(--azul);color:#fff;border-radius:var(--raio-g);border-bottom:3px solid var(--ouro);padding:var(--esp-4);display:flex;flex-direction:column;gap:var(--esp-4)}
.bd-hero-topo{display:flex;flex-wrap:wrap;gap:var(--esp-3);align-items:center;justify-content:space-between}
.bd-resumo{margin:0;flex:1 1 16em;font-size:.9375em;color:#D5DBE8}
.bd-kpis{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--esp-2)}
.bd-kpi{background:var(--azul2);border-radius:var(--raio-g);padding:var(--esp-3) var(--esp-4);display:flex;flex-direction:column;gap:.4em}
.bd-kpi b{font-family:Lora,Georgia,serif;font-size:1.75em;font-weight:600;line-height:1;color:#fff}
.bd-kpi.destaque b{color:var(--ouro-claro)}
.bd-kpi span{font-size:.75em;color:#C9D1DF;line-height:1.3}
.bd-aviso{margin:0;background:#FBF8F1;border:1px solid var(--linha);border-radius:var(--raio-g);padding:var(--esp-3) var(--esp-4);font-size:.8125em;color:#6B5433;line-height:1.45}
.bd-cols{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--esp-5);grid-template-areas:"pg" "ac" "rt";align-items:start}
.bd-sec{display:flex;flex-direction:column;gap:var(--esp-3);min-width:0}
.bd-sec.pg{grid-area:pg}.bd-sec.ac{grid-area:ac}.bd-sec.rt{grid-area:rt}
.bd-sec-cab{display:flex;justify-content:space-between;align-items:baseline;gap:var(--esp-3);margin:0 .25em}
.bd-sec-cab h2{margin:0;font-family:Lora,Georgia,serif;font-size:1.25em;color:var(--azul)}
.bd-sec-cab span{font-size:.75em;color:var(--suave)}
.bd-card{background:#fff;border-radius:1.125em;padding:var(--esp-4);display:flex;flex-direction:column;gap:var(--esp-3);box-shadow:0 1px 2px rgba(15,38,70,.06),0 6px 18px rgba(15,38,70,.06)}
.bd-linha1{display:flex;align-items:center;gap:var(--esp-2);flex-wrap:wrap}
.bd-cod{font-size:.6875em;font-weight:600;letter-spacing:.04em;color:var(--azul);background:var(--ouro-fundo);border-radius:.4em;padding:.25em .5em;flex:none}
.bd-quem{font-size:.75em;color:var(--suave);flex:1 1 6em;min-width:0}
.bd-urg{font-size:.6875em;font-weight:600;border-radius:999px;padding:.3em .7em;background:var(--creme2);color:var(--suave2)}
.bd-urg.u0{background:var(--vinho-fundo);color:var(--vinho)}
.bd-urg.u1{background:#FBEAE5;color:#9A3F2B}
.bd-urg.u2{background:#FFF2CC;color:#5C4300}
.bd-tit{margin:0;font-family:Lora,Georgia,serif;font-weight:600;font-size:1.125em;line-height:1.3;color:var(--azul)}
.bd-valor{display:flex;align-items:baseline;gap:.4em;color:var(--azul)}
.bd-valor small{font-size:1em;font-weight:600;color:#6B5433}
.bd-valor b{font-family:Lora,Georgia,serif;font-size:2.25em;font-weight:600;line-height:1.1}
.bd-dados{display:grid;grid-template-columns:1fr 1fr;gap:var(--esp-2) var(--esp-4)}
.bd-dados div{font-size:.75em;color:var(--suave)}
.bd-dados b{display:block;font-size:1.1667em;font-weight:600;color:var(--azul)}
.bd-txt{margin:0;font-size:.875em;color:var(--texto);overflow-wrap:anywhere}
.bd-alerta{margin:0;font-size:.8125em;line-height:1.4;color:#9A3F2B;background:#FBEAE5;border-radius:var(--raio);padding:.6em .75em}
.bd-bt{min-height:44px;padding:0 1em;border:1px solid var(--ouro);border-radius:var(--raio);background:none;color:var(--azul);font-weight:500;font-size:.875em;display:inline-flex;align-items:center;justify-content:center;text-decoration:none;white-space:nowrap}
.bd-bt:hover{background:var(--ouro-fundo)}
.bd-bt.claro{color:#fff;border-color:rgba(227,200,148,.6)}
.bd-bt.claro:hover{background:rgba(255,255,255,.08)}
.bd-bt.suave{border-color:var(--linha)}
.bd-bt:disabled{opacity:.6;cursor:default}
.bd-chips{display:flex;flex-wrap:wrap;gap:var(--esp-2)}
.bd-chip{min-height:44px;padding:0 1em;border-radius:var(--raio);border:1px solid var(--linha);background:none;color:var(--azul);font-size:.8125em;font-weight:500}
.bd-chip[aria-pressed="true"]{border-color:var(--ouro);background:#fff;font-weight:600}
.bd-lista{background:#fff;border-radius:1.125em;padding:.15em var(--esp-4);display:flex;flex-direction:column}
.bd-it{display:flex;gap:var(--esp-3);align-items:flex-start;padding:.8em 0;border-bottom:1px solid var(--linha2)}
.bd-it:last-child{border-bottom:0}
.bd-it .bd-cod{margin-top:.2em}
.bd-it-tx{flex:1;min-width:0;display:flex;flex-direction:column;gap:.2em}
.bd-it-tx b{font-size:.875em;font-weight:500;line-height:1.35;color:var(--azul);overflow-wrap:anywhere}
.bd-it-tx small{font-size:.75em;color:var(--suave);line-height:1.35;overflow-wrap:anywhere}
.bd-it-tx small.venc{color:#9A3F2B;font-weight:600}
.bd-it-tx small.hoje{color:#8A5A1B;font-weight:600}
.bd-ir{flex:none;width:44px;height:44px;margin:-.5em -.7em -.5em 0;display:flex;align-items:center;justify-content:center;border-radius:var(--raio);color:var(--suave2)}
.bd-ir:hover{background:var(--creme2)}
.bd-mais{display:flex;justify-content:center}
.bd-vazio,.bd-erro{margin:0;background:#fff;border-radius:1.125em;padding:var(--esp-4);font-size:.875em;color:var(--suave)}
.bd-erro{color:#9A3F2B;background:#FBEAE5}
.bd-rt{font-size:.875em;line-height:1.5;color:var(--azul)}
.bd-rt small{display:block;font-size:.8571em;color:var(--suave)}
.bd-rt b{font-weight:600}
@media (min-width:768px){.bd-kpis{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (min-width:1024px){.bd-cols{grid-template-columns:minmax(0,1fr) minmax(0,1fr);grid-template-areas:"pg ac" "rt ac"}}
@media (max-width:767px){.bd{padding:.25em .875em 2em}.bd-valor b{font-size:2em}}
@media (prefers-reduced-motion:no-preference){.bd-chip,.bd-bt{transition:background var(--mov) ease,border-color var(--mov) ease}}
/* ================= v1.36 (C2): Meus condomínios e Como chegar""")

# ---------------------------------------------------------------- HTML: item na lateral do computador
troca('      <div id="latSoVoce"></div>\n', r"""      <button class="lat-item" type="button" data-acao="bomdia" data-mod="bomdia" id="latBomDia" hidden>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#E3C894" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/></svg>
        <span style="flex:1">Bom dia</span><span class="cont" id="contBomDia" hidden></span>
      </button>
      <div id="latSoVoce"></div>
""")

# ---------------------------------------------------------------- JS: leitura e módulo
troca("condominios.lista condominios.abrir condominios.nf').split(' ')", "condominios.lista condominios.abrir condominios.nf bomdia.painel').split(' ')")
troca("  condominios: { pode: function () { return temCondominios(); }, abrir: function (arg) { cdMontar(arg); } } // v1.36 (C2)\n",
      "  condominios: { pode: function () { return temCondominios(); }, abrir: function (arg) { cdMontar(arg); } }, // v1.36 (C2)\n"
      "  bomdia: { pode: function () { return temBomDia(); }, abrir: function () { bdMontar(); } } // v1.41: Bom dia, etapa 1 (só leitura)\n")

troca("/* ================= Módulos e endereços (v1.30, Etapa D.1) =================", r"""/* ================= v1.41 (Bom dia, etapa 1): ?m=bomdia — SÓ LEITURA =================
   Lê do motor (bomdia.painel): KPIs, pagamentos a confirmar, acompanhamentos e resumo das rotinas. Nada grava.
   Quem vê é decidido pelo motor, por perfil (Configurações › Bom dia). Aprovar/Questionar (gravar()) é a etapa 2. */
var ICO_SOL = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#C9A46A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/></svg>';
var ICO_GMAIL_LINK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';
var BDS = { aba: 'voce', todos: false };
function temBomDia() { return ((S.portal && S.portal.modulos) || []).some(function (m) { return m.id === 'bomdia'; }); }
function bdN(n, um, varios) { return n + ' ' + (n === 1 ? um : varios); }
function bdLink(u) { return /^https:\/\/mail\.google\.com\//.test(String(u || '')) ? String(u) : ''; }
function bdTileSub() {
  var d = S.bd;
  if (!d) return S.bdErro ? 'Toque para abrir' : 'Carregando…';
  var p = d.kpis.pagamentos;
  return p ? bdN(p, 'pagamento a confirmar', 'pagamentos a confirmar') : 'Nenhum pagamento a confirmar';
}
function bdTileInterno() {
  var sel = S.bd && S.bd.selo > 0 ? '<span class="bd-selo" aria-label="' + S.bd.selo + ' itens pedindo atenção">' + S.bd.selo + '</span>' : '';
  return ICO_SOL + sel + '<b>Bom dia</b><small>' + esc(bdTileSub()) + '</small>';
}
function bdTileMenu() {
  return '<button class="mp-mod bd-tile' + (modAtual === 'bomdia' ? ' atual' : '') + '" data-acao="bomdia" data-bdtile>' + bdTileInterno() + '</button>';
}
/* Atualiza o card do menu e o número da lateral sem redesenhar mais nada. */
function bdAtualizarTiles() {
  Array.prototype.forEach.call(document.querySelectorAll('[data-bdtile]'), function (el) { el.innerHTML = bdTileInterno(); });
  var c = $('contBomDia'); if (c) { var n = S.bd ? S.bd.selo : 0; c.hidden = !n; c.textContent = n || ''; }
}
function bdTitulo() { return S.bd ? S.bd.saudacao + ', ' + S.bd.nome : 'Bom dia'; }
function bdSub() { var d = S.bd; return d ? d.dataTexto + (d.rotinasAs ? ' · rotinas rodaram às ' + d.rotinasAs : '') : 'Resumo do dia'; }
function bdMontar() {
  if (!temBomDia()) return;
  moduloTela(bdTitulo(), bdSub(), '<div class="bd" id="bd"><p class="vazio">Carregando…</p></div>', function (raiz) {
    raiz.addEventListener('click', bdClique);
    if (S.bd) bdDesenhar();
    if (!S.bd || Date.now() - (S.bdEm || 0) > 60000) bdCarregar(false);
  });
}
function bdCarregar(forcar) {
  if (S.bdCarregando) return;
  S.bdCarregando = true; S.bdErro = '';
  if ($('bd') && S.bd) bdDesenhar();
  var fim = function () {
    S.bdCarregando = false;
    bdAtualizarTiles();
    if ($('bd')) {
      bdDesenhar();
      var h = document.querySelector('#modHost .mod-cab h1');
      if (h) { h.textContent = bdTitulo(); if (h.nextElementSibling) h.nextElementSibling.textContent = bdSub(); }
    }
  };
  return api('bomdia.painel', forcar ? { atualizar: true } : {}).then(function (r) {
    if (r && r.ok !== false && r.kpis) { S.bd = r; S.bdEm = Date.now(); S.bdErro = ''; }
    else S.bdErro = (r && r.mensagem) || 'Não consegui carregar agora.';
    fim();
  }, function () { S.bdErro = 'Sem conexão agora. Tente de novo.'; fim(); });
}
function bdClique(e) {
  var b = e.target.closest ? e.target.closest('button') : null;
  if (!b) return;
  if (b.hasAttribute('data-bdatualizar')) { bdCarregar(true); return; }
  if (b.hasAttribute('data-bdaba')) { BDS.aba = b.getAttribute('data-bdaba'); BDS.todos = false; bdDesenhar(); return; }
  if (b.hasAttribute('data-bdtodos')) { BDS.todos = b.getAttribute('data-bdtodos') === '1'; bdDesenhar(); }
}
function bdPrazoTxt(x) {
  if (x.dias === null || x.dias === undefined) return { t: 'Sem prazo', c: '' };
  if (x.dias < -1) return { t: 'Venceu há ' + (-x.dias) + ' dias', c: 'venc' };
  if (x.dias === -1) return { t: 'Venceu ontem', c: 'venc' };
  if (x.dias === 0) return { t: 'Vence hoje', c: 'hoje' };
  if (x.dias === 1) return { t: 'Vence amanhã', c: '' };
  return { t: 'Prazo ' + String(x.prazo || '').slice(0, 5), c: '' };
}
function bdHtmlErro(msg) { return '<p class="bd-erro">Não consegui ler esta parte agora: ' + esc(msg) + '</p>'; }
function bdHtmlPagamento(p) {
  var urg = norm(p.urgencia), cl = urg === 'urgente' ? 'u0' : (urg === 'hoje' ? 'u1' : (urg === 'semana' ? 'u2' : ''));
  var dados = (p.vencimentos ? '<div>Vencimentos<b>' + esc(p.vencimentos) + '</b></div>' : '') + (p.maior ? '<div>Maior conta<b>' + esc(p.maior) + '</b></div>' : '');
  var gm = bdLink(p.gmail);
  return '<article class="bd-card" aria-label="' + esc(p.titulo) + '">' +
    '<div class="bd-linha1">' + (p.cod ? '<span class="bd-cod">' + esc(p.cod) + '</span>' : '') + '<span class="bd-quem">' + esc(p.quem) + '</span>' +
    (p.urgencia ? '<span class="bd-urg ' + cl + '">' + esc(p.urgencia) + '</span>' : '') + '</div>' +
    '<p class="bd-tit">' + esc(p.titulo) + '</p>' +
    (p.valor ? '<div class="bd-valor"><small>R$</small><b>' + esc(p.valor) + '</b></div>' : '') +
    (dados ? '<div class="bd-dados">' + dados + '</div>' : '') +
    (p.resumo ? '<p class="bd-txt">' + esc(p.resumo) + '</p>' : '') +
    (p.alerta ? '<p class="bd-alerta">' + esc(p.alerta) + '</p>' : '') +
    (gm ? '<div class="bd-linha1"><a class="bd-bt" href="' + esc(gm) + '" target="_blank" rel="noopener">Abrir no Gmail</a></div>' : '') +
    '</article>';
}
function bdHtmlItem(x, aguardando) {
  var pz = bdPrazoTxt(x), gm = bdLink(x.gmail);
  var l1 = (aguardando && x.quem ? 'Aguardando ' + x.quem + ' · ' : '') + pz.t;
  return '<div class="bd-it"><span class="bd-cod">' + esc(x.cod || '—') + '</span><div class="bd-it-tx"><b>' + esc(x.titulo) + '</b>' +
    '<small class="' + pz.c + '">' + esc(l1) + '</small>' + (x.proximo ? '<small>' + esc(x.proximo) + '</small>' : '') + '</div>' +
    (gm ? '<a class="bd-ir" href="' + esc(gm) + '" target="_blank" rel="noopener" aria-label="Abrir a conversa no Gmail">' + ICO_GMAIL_LINK + '</a>' : '') + '</div>';
}
function bdDesenhar() {
  var el = $('bd'); if (!el) return;
  var d = S.bd;
  if (!d) {
    el.innerHTML = '<p class="vazio">' + esc(S.bdErro || 'Carregando…') + '</p>' +
      (S.bdErro ? '<div><button class="bd-bt" data-bdatualizar>Tentar de novo</button></div>' : '');
    return;
  }
  var k = d.kpis, partes = [];
  if (k.pagamentos) partes.push(bdN(k.pagamentos, 'pagamento para confirmar', 'pagamentos para confirmar'));
  if (k.vencidos) partes.push(bdN(k.vencidos, 'prazo vencido', 'prazos vencidos'));
  var resumo = partes.length ? partes.join(' e ') + '.' : 'Tudo em dia por aqui.';
  var kpi = function (n, um, varios, dest) { return '<div class="bd-kpi' + (dest ? ' destaque' : '') + '"><b>' + n + '</b><span>' + (n === 1 ? um : varios) + '</span></div>'; };
  var h = '<section class="bd-hero" aria-label="Resumo do dia"><div class="bd-hero-topo"><p class="bd-resumo">' + esc(resumo) + '</p>' +
    '<button class="bd-bt claro" data-bdatualizar' + (S.bdCarregando ? ' disabled' : '') + '>' + (S.bdCarregando ? 'Atualizando…' : 'Atualizar') + '</button></div>' +
    '<div class="bd-kpis">' + kpi(k.pagamentos, 'Pagamento a confirmar', 'Pagamentos a confirmar', true) +
    kpi(k.vencidos, 'Prazo vencido', 'Prazos vencidos') + kpi(k.hoje, 'Vence hoje', 'Vencem hoje') +
    kpi(k.abertos, 'Acompanhamento aberto', 'Acompanhamentos abertos') + '</div></section>' +
    (S.bdErro ? '<p class="bd-erro">' + esc(S.bdErro) + ' Mostrando os últimos dados.</p>' : '') +
    '<p class="bd-aviso">Somente leitura por enquanto. Aprovar e Questionar chegam na próxima etapa.</p>';

  // Pagamentos a confirmar
  var pg = '<section class="bd-sec pg" aria-labelledby="bdTPg"><div class="bd-sec-cab"><h2 id="bdTPg">Pagamentos a confirmar</h2><span>' + bdN(k.pagamentos, 'pendente', 'pendentes') + '</span></div>';
  if (d.erros.pagamentos) pg += bdHtmlErro(d.erros.pagamentos);
  else if (!d.pagamentos.length) pg += '<p class="bd-vazio">Nenhum pagamento esperando confirmação.</p>';
  else pg += d.pagamentos.map(bdHtmlPagamento).join('');
  pg += '</section>';

  // Acompanhando
  var voce = BDS.aba === 'voce', lista = voce ? d.acompanhando.comVoce : d.acompanhando.aguardando;
  var lim = BDS.todos ? lista.length : d.itensVisiveis;
  var ac = '<section class="bd-sec ac" aria-labelledby="bdTAc"><div class="bd-sec-cab"><h2 id="bdTAc">Acompanhando</h2><span>' + bdN(k.abertos, 'aberto', 'abertos') + '</span></div>';
  if (d.erros.acompanhando) ac += bdHtmlErro(d.erros.acompanhando);
  else {
    ac += '<div class="bd-chips" role="group" aria-label="Quem está com a bola">' +
      '<button class="bd-chip" data-bdaba="voce" aria-pressed="' + voce + '">Com você · ' + k.comVoce + '</button>' +
      '<button class="bd-chip" data-bdaba="terceiro" aria-pressed="' + !voce + '">Aguardando · ' + k.aguardando + '</button></div>';
    if (!lista.length) ac += '<p class="bd-vazio">' + (voce ? 'Nada esperando por você.' : 'Nada aguardando terceiros.') + '</p>';
    else {
      ac += '<div class="bd-lista">' + lista.slice(0, lim).map(function (x) { return bdHtmlItem(x, !voce); }).join('') + '</div>';
      if (lista.length > d.itensVisiveis) ac += '<div class="bd-mais"><button class="bd-bt suave" data-bdtodos="' + (BDS.todos ? 0 : 1) + '">' + (BDS.todos ? 'Mostrar menos' : 'Ver todos os ' + lista.length) + '</button></div>';
    }
  }
  ac += '</section>';

  // Rotinas de hoje
  var rt = '<section class="bd-sec rt" aria-labelledby="bdTRt"><div class="bd-sec-cab"><h2 id="bdTRt">Rotinas de hoje</h2><span>' + esc(d.rotinasAs || '') + '</span></div>';
  if (d.erros.rotinas) rt += bdHtmlErro(d.erros.rotinas);
  else if (!d.rotinas.length) rt += '<p class="bd-vazio">Nenhuma rotina deixou resumo ainda.</p>';
  else rt += '<div class="bd-card">' + d.rotinas.map(function (r) {
    return '<div class="bd-rt"><b>' + esc(r.fluxo + (r.comp ? ' ' + r.comp : '')) + ':</b> ' + esc(r.resumo) + (r.quando ? '<small>' + esc(r.quando) + '</small>' : '') + '</div>';
  }).join('') + '</div>';
  rt += '</section>';

  el.innerHTML = h + '<div class="bd-cols">' + pg + ac + rt + '</div>';
}

/* ================= Módulos e endereços (v1.30, Etapa D.1) =================""")

# ---------------------------------------------------------------- menu do portal: card Bom dia; sem cards "Em breve"
troca("    if (m.id === 'condominios') { h += cdTileMenu(); return; } // v1.37 (C3)\n",
      "    if (m.id === 'condominios') { h += cdTileMenu(); return; } // v1.37 (C3)\n    if (m.id === 'bomdia') { h += bdTileMenu(); return; } // v1.41: card ao lado de Tarefas\n")
troca("""  var breve = emBreve().slice(1, 1 + (mods.length % 2 ? 3 : 2));
  breve.forEach(function (nome) { h += '<div class="mp-mod breve">' + IC.breve + '<b>' + esc(nome) + '</b><small>Em breve</small></div>'; });
""", "  /* v1.41: os cards \"Em breve\" (Seguros, Contas de consumo, Orçamentos) saíram da grade de módulos (decisão de 28/11/2026). */\n")

# menu do portal (celular): puxa o resumo ao abrir, para o card mostrar os números
troca("function abrirMenuPortal() {\n  if (!temMenuPortal()) return;\n",
      "function abrirMenuPortal() {\n  if (!temMenuPortal()) return;\n  if (temBomDia() && (!S.bd || Date.now() - (S.bdEm || 0) > 60000)) bdCarregar(false); // v1.41\n")

# lateral do computador: mostra o item e puxa o resumo
troca("  var eb = $('emBreve');\n  if (eb) eb.innerHTML",
      "  var lb = $('latBomDia'); // v1.41\n  if (lb) { lb.hidden = !temBomDia(); bdAtualizarTiles(); }\n  if (temBomDia() && !S.bd && !S.bdCarregando && !S.bdErro) bdCarregar(false);\n  var eb = $('emBreve');\n  if (eb) eb.innerHTML")
# clique
troca("    case 'condominios': fecharCamadas(); abrirCondominios(); break; // v1.36\n",
      "    case 'condominios': fecharCamadas(); abrirCondominios(); break; // v1.36\n    case 'bomdia': fecharCamadas(); ir('bomdia'); break; // v1.41\n")
# sair
troca("S.sessao = null; S.dados = null; S.det = null; S.selId = null; S.roteado = false;\n  mostrarModulo('tarefas');",
      "S.sessao = null; S.dados = null; S.det = null; S.selId = null; S.roteado = false; S.bd = null; S.bdErro = ''; S.bdCarregando = false;\n  mostrarModulo('tarefas');")

open(out, 'w', encoding='utf-8').write(t)
print('OK: site 1.41 gerado em', out, 'hash', hashlib.sha256(t.encode('utf-8')).hexdigest()[:16])
