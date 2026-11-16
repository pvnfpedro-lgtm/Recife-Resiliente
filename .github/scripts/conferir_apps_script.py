"""Trava de segurança antes de enviar o painel ao Apps Script.

Compara o projeto como está hoje no Apps Script (baixado com `clasp pull` em <pasta_remota>) com as versões
que o repositório já teve. Se não bater com nenhuma, alguém editou direto no editor do Apps Script e enviar
agora apagaria essa edição: o script falha e explica o que fazer.

Uso: python3 conferir_apps_script.py <pasta_remota> <pasta_no_repo>
"""
import os
import subprocess
import sys

remota, pasta_repo = sys.argv[1], sys.argv[2]


def ler_remoto():
    arqs = {}
    for raiz, _, nomes in os.walk(remota):
        for n in nomes:
            if n.startswith(".clasp"):
                continue
            caminho = os.path.join(raiz, n)
            arqs[os.path.relpath(caminho, remota)] = open(caminho, encoding="utf-8").read()
    return arqs


def ler_commit(ref):
    if not ref:
        return None
    lista = subprocess.run(["git", "-c", "core.quotepath=off", "ls-tree", "-r", "--name-only", ref, "--", pasta_repo],
                           capture_output=True, text=True)
    if lista.returncode != 0:
        return None
    arqs = {}
    for caminho in lista.stdout.splitlines():
        rel = os.path.relpath(caminho, pasta_repo)
        if rel.startswith(".") or os.sep in rel or not rel.endswith((".js", ".gs", ".html", ".json")):
            continue
        conteudo = subprocess.run(["git", "show", f"{ref}:{caminho}"], capture_output=True, text=True).stdout
        arqs[rel] = conteudo
    return arqs


def normalizar(arqs):
    return {k: v.replace("\r\n", "\n").rstrip("\n") for k, v in arqs.items()}


remoto = normalizar(ler_remoto())
commits = subprocess.run(["git", "log", "--format=%H", "-n", "50", "--", pasta_repo],
                         capture_output=True, text=True).stdout.split()
for ref in commits:
    esperado = ler_commit(ref)
    if esperado is not None and normalizar(esperado) == remoto:
        print(f"OK: o projeto no Apps Script é igual a uma versão do repositório ({ref[:7]}). Pode enviar.")
        sys.exit(0)

esperado = normalizar(ler_commit(commits[0]) if commits else {})
diferentes = sorted(n for n in set(esperado) | set(remoto) if esperado.get(n) != remoto.get(n))
print("PARADO: o projeto no Apps Script foi alterado fora do repositório.")
print("Arquivos diferentes da versão atual do repositório: " + ", ".join(diferentes))
print("Enviar agora apagaria essas alterações. Traga-as para appscript/ (clasp pull, ou peça ao Claude para")
print("baixar o projeto e juntar) ou, se elas podem ser descartadas, rode de novo com 'ignorar_trava' marcado.")
sys.exit(1)
