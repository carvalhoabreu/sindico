#!/usr/bin/env python3
"""Site 1.42 - Bom dia, etapa 2: Aprovar / Questionar nos pagamentos. Pareia com o Motor 0.40.0 (bomdia.decidir).
Base: site 1.41 (hash fbf3e9040434d3d2). Uso: aplicar_bomdia_142.py <index.html 1.41> <index.html 1.42>"""
import sys, hashlib
BASE = 'fbf3e9040434d3d2'
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
h = hashlib.sha256(t.encode('utf-8')).hexdigest()
if not h.startswith(BASE):
    sys.exit('PARADO: o index nao e a 1.41 (hash %s). Refazer sobre o site novo.' % h[:16])
def troca(a, b):
    global t
    if t.count(a) != 1: sys.exit('PARADO: trecho nao encontrado uma vez so: ' + a[:70])
    t = t.replace(a, b)

troca("var VERSAO_SITE = '1.41';", "var VERSAO_SITE = '1.42';")

# CSS
troca("@media (min-width:768px){.bd-kpis{", r""".bd-acoes{display:flex;flex-wrap:wrap;gap:var(--esp-2);align-items:center}
.bd-bt.pri{border-color:var(--ouro);font-weight:600}
.bd-dec{display:flex;flex-direction:column;gap:var(--esp-2);background:var(--creme);border-radius:var(--raio);padding:var(--esp-3)}
.bd-dec p{margin:0;font-size:.875em;line-height:1.45;color:var(--azul)}
.bd-dec textarea{width:100%;min-height:5.5em;padding:.7em .8em;border:1px solid var(--linha);border-radius:var(--raio);font:inherit;font-size:.9375em;color:var(--texto);background:#fff;resize:vertical;box-sizing:border-box}
.bd-dec textarea:focus{outline:2px solid var(--ouro);outline-offset:1px}
.bd-feito{margin:0;font-size:.875em;font-weight:600;color:#2E6B3F;background:#E8F3EA;border-radius:var(--raio);padding:.7em .85em}
@media (min-width:768px){.bd-kpis{""")

# estado
troca("var BDS = { aba: 'voce', todos: false };", "var BDS = { aba: 'voce', todos: false, dec: null, feitos: {} }; // dec = { id, modo: 'a'|'q', texto, erro }")

# bloco de decisão no cartão
troca("""    (gm ? '<div class="bd-linha1"><a class="bd-bt" href="' + esc(gm) + '" target="_blank" rel="noopener">Abrir no Gmail</a></div>' : '') +
    '</article>';
}""", """    bdHtmlDecisao(p, gm) +
    '</article>';
}
function bdHtmlDecisao(p, gm) {
  var feito = BDS.feitos[p.id], dc = BDS.dec && BDS.dec.id === p.id ? BDS.dec : null, id = esc(p.id);
  var linkGm = gm ? '<a class="bd-bt suave" href="' + esc(gm) + '" target="_blank" rel="noopener">Abrir no Gmail</a>' : '';
  if (feito) return '<p class="bd-feito" role="status">✓ ' + esc(feito) + '</p>';
  if (dc && dc.modo === 'a') {
    return '<div class="bd-dec"><p>Aprovar este pagamento' + (p.valor ? ' de <b>R$ ' + esc(p.valor) + '</b>' : '') + '? Fica registrado e o Maestro executa depois. O portal não paga nada.</p>' +
      (dc.erro ? '<p class="bd-alerta">' + esc(dc.erro) + '</p>' : '') +
      '<div class="bd-acoes"><button class="bd-bt pri" data-bdok="' + id + '">Confirmar aprovação</button><button class="bd-bt suave" data-bdcancelar>Cancelar</button></div></div>';
  }
  if (dc && dc.modo === 'q') {
    return '<div class="bd-dec"><p><label for="bdTx">Qual é a sua dúvida?</label></p>' +
      '<textarea id="bdTx" data-bdtexto maxlength="300" placeholder="Ex.: por que o valor subiu em relação ao mês passado?">' + esc(dc.texto || '') + '</textarea>' +
      (dc.erro ? '<p class="bd-alerta">' + esc(dc.erro) + '</p>' : '') +
      '<div class="bd-acoes"><button class="bd-bt pri" data-bdenviar="' + id + '"' + (String(dc.texto || '').trim().length < 3 ? ' disabled' : '') + '>Enviar dúvida</button><button class="bd-bt suave" data-bdcancelar>Cancelar</button></div></div>';
  }
  return '<div class="bd-acoes"><button class="bd-bt pri" data-bdaprovar="' + id + '">Aprovar</button><button class="bd-bt" data-bdquestionar="' + id + '">Questionar</button>' + linkGm + '</div>';
}
function bdDecidir(id, decisao, texto) {
  var rotulo = decisao === 'Aprovar' ? 'Aprovado. O Maestro executa depois.' : 'Dúvida registrada. O Maestro vai tratar.';
  return gravar('bomdia.decidir', { id: id, decisao: decisao, texto: texto || '' }).then(function (r) {
    if (r && r.ok) { BDS.feitos[id] = rotulo; BDS.dec = null; bdDesenhar(); setTimeout(function () { bdCarregar(true); }, 1200); return; }
    if (r && r.ignorado) return;
    var msg = (r && r.mensagem) || 'Não consegui registrar agora. Tente de novo.';
    if (r && r.codigo === 'CONFLITO') { BDS.dec = null; bdCarregar(true); return; } // já decidido por outro caminho: a lista se atualiza
    if (BDS.dec && BDS.dec.id === id) BDS.dec.erro = msg;
    bdDesenhar();
  }, function () { if (BDS.dec && BDS.dec.id === id) BDS.dec.erro = 'Sem conexão agora. Tente de novo.'; bdDesenhar(); });
}""")

# cliques
troca("""  var b = e.target.closest ? e.target.closest('button') : null;
  if (!b) return;
  if (b.hasAttribute('data-bdatualizar'))""", """  var b = e.target.closest ? e.target.closest('button') : null;
  if (!b) return;
  if (b.hasAttribute('data-bdaprovar')) { BDS.dec = { id: b.getAttribute('data-bdaprovar'), modo: 'a' }; bdDesenhar(); return; }
  if (b.hasAttribute('data-bdquestionar')) { BDS.dec = { id: b.getAttribute('data-bdquestionar'), modo: 'q', texto: '' }; bdDesenhar(); var tx = $('bdTx'); if (tx) tx.focus(); return; }
  if (b.hasAttribute('data-bdcancelar')) { BDS.dec = null; bdDesenhar(); return; }
  if (b.hasAttribute('data-bdok')) { bdDecidir(b.getAttribute('data-bdok'), 'Aprovar'); return; }
  if (b.hasAttribute('data-bdenviar')) { var t1 = BDS.dec && BDS.dec.texto ? String(BDS.dec.texto).trim() : ''; if (t1.length >= 3) bdDecidir(b.getAttribute('data-bdenviar'), 'Questionar', t1); return; }
  if (b.hasAttribute('data-bdatualizar'))""")
troca("    raiz.addEventListener('click', bdClique);\n", """    raiz.addEventListener('click', bdClique);
    raiz.addEventListener('input', function (e) { // a dúvida digitada: libera o botão sem redesenhar (não perde o foco)
      if (!e.target || !e.target.hasAttribute || !e.target.hasAttribute('data-bdtexto') || !BDS.dec) return;
      BDS.dec.texto = e.target.value;
      var bt = raiz.querySelector('[data-bdenviar]'); if (bt) bt.disabled = String(e.target.value).trim().length < 3;
    });
""")
troca("Somente leitura por enquanto. Aprovar e Questionar chegam na próxima etapa.", "Aprovar e Questionar só registram a sua decisão. O pagamento em si é feito depois, pelo Maestro.")
# sair: limpa estado
troca("S.bd = null; S.bdErro = ''; S.bdCarregando = false;", "S.bd = null; S.bdErro = ''; S.bdCarregando = false; BDS.dec = null; BDS.feitos = {};")
open(out, 'w', encoding='utf-8').write(t)
print('OK: site 1.42 gerado em', out, 'hash', hashlib.sha256(t.encode('utf-8')).hexdigest()[:16])
