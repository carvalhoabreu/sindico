#!/usr/bin/env python3
"""Site 1.39 - menu do usuario (conta) reorganizado + correcao do nome duplicado abrirPerfil (Perfil 1.36 tomava o botao da foto). Uso: aplicar_menu_139.py <index 1.38> <saida>
Confere o hash da base (1.38 = 5f47385f...) e para se o site mudou."""
import sys, hashlib
BASE = '5f47385fff9a85f0'
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
h = hashlib.sha256(t.encode('utf-8')).hexdigest()
if not h.startswith(BASE):
    sys.exit('PARADO: o index nao e a 1.38 (hash %s). Refazer sobre o site novo.' % h[:16])
def troca(a, b):
    global t
    if t.count(a) != 1: sys.exit('PARADO: trecho nao encontrado uma vez so: ' + a[:60])
    t = t.replace(a, b)
troca("var VERSAO_SITE = '1.38';", "var VERSAO_SITE = '1.39';")
css = """.menu-item:hover{background:var(--creme)}
/* v1.39: menu do usuario */
.menu.conta{padding:.4em}
.mc-cab{display:flex;align-items:center;gap:.75em;padding:.55em .6em .75em;border-bottom:1px solid var(--linha2);margin-bottom:.25em}
.mc-cab .avatar{width:2.75em;height:2.75em;border:2px solid var(--ouro);background:var(--azul);color:var(--ouro-claro)}
.mc-cab .tx{min-width:0}
.mc-cab b{display:block;color:var(--azul);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mc-cab small{display:block;color:var(--suave);font-size:.8125em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mc-papel{display:inline-block;margin-top:.3em;padding:.1em .65em;border:1px solid var(--ouro);border-radius:2em;background:var(--creme);color:#6B4F1B;font-size:.75em;font-weight:500}
.mc-rot{padding:.7em .75em .15em;font-size:.6875em;letter-spacing:.06em;color:#8A6A2F;font-weight:600;text-transform:uppercase}
.mc-sep{height:1px;background:var(--linha2);margin:.3em .5em}
.menu.conta .menu-item{min-height:44px}
.menu.conta .menu-item.mc-sair{background:var(--creme);margin-top:.15em}
.menu.conta .menu-item.mc-sair:hover{background:var(--creme2)}"""
troca(".menu-item:hover{background:var(--creme)}", css)
velho = t[t.index("function abrirPerfil() {"):t.index("/* ================= Nova tarefa (v1.18")]
novo = """function abrirMenuConta() {
  var u = S.dados ? S.dados.usuario : (S.portal ? S.portal.usuario : {});
  var guia = itensGuiaMenu();
  var h = '<div class="mc-cab">' + avatarDe(S.google, u.nome) + '<div class="tx"><b>' + esc(u.nome) + '</b><small>' + esc(u.email) + '</small>' +
      '<span class="mc-papel">' + esc(papelTexto(u)) + '</span></div></div>' +
    '<div class="mc-rot">No aparelho</div>' +
    '<button class="menu-item" data-acao="atualizar">' + IC.att + 'Atualizar lista</button>' +
    guia +
    '<div class="mc-sep"></div>' +
    '<a class="menu-item" href="privacidade.html">' + IC.doc + 'Política de privacidade</a>' +
    '<div class="mc-sep"></div>' +
    '<button class="menu-item mc-sair" data-acao="sair">' + IC.sair + 'Sair</button>' +
    '<div class="menu-vazio" style="font-size:.75em;padding:.4em .75em">Site v' + VERSAO_SITE + ' · ' + esc((S.dados && S.dados.versaoApp) || '') + '</div>';
  abrirMenu($('btPerfil'), h, function (m) { m.classList.add('conta'); });
}

"""
t = t.replace(velho, novo)
# v1.39: a funcao do Perfil dos condominios (1.36) tinha o mesmo nome e tomava o lugar do menu da conta
troca("if (b.id === 'btPerfil') abrirPerfil();", "if (b.id === 'btPerfil') abrirMenuConta();")
open(out, 'w', encoding='utf-8').write(t)
print('ok', hashlib.sha256(t.encode('utf-8')).hexdigest()[:16])
