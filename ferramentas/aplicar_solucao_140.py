#!/usr/bin/env python3
"""Site 1.40 - concluir Manutencao/Ocorrencia exige a solucao final (campo de texto obrigatorio na janela de conclusao;
a solucao aparece no follow-up da tarefa). Pareia com o Motor 0.38.0 (que tambem valida no servidor).
Uso: aplicar_solucao_140.py <index.html de entrada> <index.html de saida>
Confere o hash da base (1.39 = 2f8ebb367cba359c) e para se o site mudou."""
import sys, hashlib
BASE = '2f8ebb367cba359c'
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
h = hashlib.sha256(t.encode('utf-8')).hexdigest()
if not h.startswith(BASE):
    sys.exit('PARADO: o index nao e a 1.39 (hash %s). Refazer sobre o site novo.' % h[:16])
def troca(a, b):
    global t
    if t.count(a) != 1: sys.exit('PARADO: trecho nao encontrado uma vez so: ' + a[:70])
    t = t.replace(a, b)

troca("var VERSAO_SITE = '1.39';", "var VERSAO_SITE = '1.40';")

# CSS
troca(".anx-lembrete svg{flex:none;width:1.25em;height:1.25em;stroke:#7A5C27}",
""".anx-lembrete svg{flex:none;width:1.25em;height:1.25em;stroke:#7A5C27}
/* v1.40: solucao final obrigatoria ao concluir */
.sol-campo{display:flex;flex-direction:column;gap:.4em;margin:.25em 0}
.sol-campo textarea{min-height:6em;resize:vertical}
.sol-ajuda{display:flex;justify-content:space-between;gap:.75em;font-size:.8125em;color:var(--suave)}
.sol-ajuda.falta b{color:#8A5A1B}
.obs-sol{border:1px solid #CFE3D2;background:#F2F8F3;border-radius:.75em;padding:.65em .8em;display:flex;flex-direction:column;gap:.35em}
.obs-sol .sol-cab{display:flex;align-items:center;gap:.5em;font-size:.8125em;color:#2F6B3F}
.obs-sol .sol-cab svg{flex:none;width:1.1em;height:1.1em;stroke:#2F6B3F}
.obs-sol .sol-cab time{margin-left:auto;color:var(--suave)}
.obs-sol .sol-tx{font-size:.9375em;white-space:pre-wrap;overflow-wrap:anywhere;color:var(--texto,inherit)}
.obs-sol.excluida{opacity:.6}
.obs-sol.excluida .sol-tx{text-decoration:line-through}""")

# confirmar concluir: campo + botao travado
troca("""    '<p class="conf-tit">' + esc(t.titulo) + '</p>' +
    (lembrarDepois""", """    '<p class="conf-tit">' + esc(t.titulo) + '</p>' +
    '<div class="sol-campo"><label class="rot-campo" for="confSolucao">Descreva a solução final</label>' +
    '<textarea class="campo" id="confSolucao" rows="4" maxlength="1000" placeholder="O que foi feito para resolver? Ex.: troquei o disjuntor e testei o circuito" aria-required="true"></textarea>' +
    '<div class="sol-ajuda falta" id="confSolAjuda"><span>Obrigatório para concluir.</span><b id="confSolN"></b></div></div>' +
    (lembrarDepois""")
troca("""'<button class="bt claro" type="button" id="confConcluir"><span>Concluir sem foto</span></button>'""",
      """'<button class="bt claro" type="button" id="confConcluir" disabled><span>Concluir sem foto</span></button>'""")
troca("""'<button class="bt" type="button" id="confConcluir">' + IC.checkOuro + '<span>Concluir tarefa</span></button></div></div>');
  abrirJanela('Concluir esta tarefa?'""", """'<button class="bt" type="button" id="confConcluir" disabled>' + IC.checkOuro + '<span>Concluir tarefa</span></button></div></div>');
  abrirJanela('Concluir esta tarefa?'""")
troca("""    var ok = raiz.querySelector('#confConcluir');
    ok.addEventListener('click', function () {
      if (ok.classList.contains('ocupado')) return;
      ok.classList.add('ocupado');
      fecharCamadas(); concluir(id);
    });""", """    var ok = raiz.querySelector('#confConcluir');
    var tx = raiz.querySelector('#confSolucao'), aj = raiz.querySelector('#confSolAjuda'), nn = raiz.querySelector('#confSolN');
    var SOL_MIN = 10; // igual ao motor (SOLUCAO_MIN)
    function letras() { return String(tx.value || '').replace(/\\s+/g, '').length; }
    function confere() {
      var n = letras(), pronto = n >= SOL_MIN;
      ok.disabled = !pronto;
      aj.classList.toggle('falta', !pronto);
      nn.textContent = pronto ? '' : (n ? 'Faltam ' + (SOL_MIN - n) + ' letras' : 'Mínimo de ' + SOL_MIN + ' letras');
    }
    tx.addEventListener('input', confere); confere();
    ok.addEventListener('click', function () {
      if (ok.classList.contains('ocupado') || letras() < SOL_MIN) { if (letras() < SOL_MIN) { try { tx.focus(); } catch (e) {} } return; }
      ok.classList.add('ocupado');
      var solucao = String(tx.value || '').trim();
      fecharCamadas(); concluir(id, solucao);
    });""")
troca("setTimeout(function () { try { (fd || ok).focus(); } catch (e) {} }, 50);",
      "setTimeout(function () { try { tx.focus(); } catch (e) {} }, 50);")

# concluir(id, solucao)
troca("function concluir(id) {\n  if (emCurso['concluir:' + id]) return;", "function concluir(id, solucao) {\n  if (emCurso['concluir:' + id]) return;")
troca("api('tarefas.concluir', { id: id }).then(function (r) {", "api('tarefas.concluir', { id: id, solucao: solucao || '' }).then(function (r) {")

# follow-up: Solucao final
troca("""    if (o.tipo === 'Anexo') {
      var ax = (t.anexos || []).filter(""", """    if (o.tipo === 'Solução') {
      h += '<div class="obs-sol' + (o.excluida ? ' excluida' : '') + '"><div class="sol-cab"><svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>' +
        '<span><b>Solução final</b> · ' + esc(String(o.autor).split(' ')[0]) + (o.excluida ? ' · desfeita' : '') + '</span><time>' + esc(quando(o.em)) + '</time></div>' +
        '<div class="sol-tx">' + esc(o.texto) + '</div></div>';
      return;
    }
    if (o.tipo === 'Anexo') {
      var ax = (t.anexos || []).filter(""")
troca("['Sistema', 'Compra', 'Anexo'].indexOf(o.tipo) < 0; });", "['Sistema', 'Compra', 'Anexo', 'Solução'].indexOf(o.tipo) < 0; });")
open(out, 'w', encoding='utf-8').write(t)
print('OK site 1.40 ->', out)
