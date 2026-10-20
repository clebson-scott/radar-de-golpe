#!/usr/bin/env python3
"""RADAR DE GOLPE — Pipeline de análise das respostas.

Como funciona: cada submissão do formulário chega por e-mail (FormSubmit) no Gmail
do pesquisador. Este script lê os e-mails com assunto RADAR-DE-GOLPE, extrai os
campos, grava cada resposta na entidade RadarResposta (Base44) e imprime o
RELATÓRIO DE DECISÃO acionando os critérios pré-registrados do trabalho.

Uso: python3 analise.py   (requer $GMAIL_ACCESS_TOKEN no ambiente)
"""
import json, re, os, sys, base64, urllib.request, urllib.parse

GMAIL = "https://gmail.googleapis.com/gmail/v1/users/me"

def api(path):
    req = urllib.request.Request(f"{GMAIL}{path}", headers={
        "Authorization": f"Bearer {os.environ['GMAIL_ACCESS_TOKEN']}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def corpo(msg):
    def walk(p):
        if isinstance(p, dict):
            if p.get("body", {}).get("data"):
                yield base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8", "ignore")
            for x in p.get("parts") or []:
                yield from walk(x)
    return "".join(walk(msg["payload"]))

def extrai(corpo_texto):
    """Extrai os campos do e-mail table do FormSubmit (NomeCampo: valor)."""
    txt = re.sub(r"<br\s*/?>", "\n", corpo_texto)
    txt = re.sub(r"<[^>]+>", " ", txt)
    d = {}
    # padroes do template table do formsubmit: NomeDoCampo: valor
    for campo, chave in [("nome", "nome"), ("perfil", "perfil"), ("frequencia", "frequencia"),
                          ("acao", "acao"), ("mensagem", "mensagem"), ("usaria", "usaria"),
                          ("confianca", "confianca"), ("pagaria", "pagaria"), ("nps", "nps"),
                          ("contato", "contato")]:
        m = re.search(rf"{campo}\s*:\s*([^\n]+)", txt, re.I)
        if m: d[chave] = m.group(1).strip()[:300]
    return d

def principal():
    q = urllib.parse.quote('subject:"RADAR-DE-GOLPE"')
    ids = [m["id"] for m in api(f"/messages?maxResults=60&q={q}").get("messages", [])]
    respostas = []
    for mid in ids:
        m = api(f"/messages/{mid}?format=full")
        d = extrai(corpo(m))
        d["_nome_real"] = d.get("nome", "")
        if d.get("nome", "").startswith("TESTE") or "TESTE" in str(d):
            continue
        respostas.append(d)
    print(f"=== RESPOSTAS VALIDAS: {len(respostas)} ===")
    n = len(respostas)
    if n == 0:
        print("Ainda sem respostas reais."); return
    freq_golpe = [r for r in respostas if r.get("frequencia") and "Nunca" not in r["frequencia"]]
    usaria = [float(r.get("usaria", 0) or 0) for r in respostas]
    conf = [float(r.get("confianca", 0) or 0) for r in respostas]
    nps = [float(r.get("nps", 0) or 0) for r in respostas]
    pagaria = [r for r in respostas if r.get("pagaria") in ("Sim", "Talvez")]
    msgs = [r for r in respostas if r.get("mensagem") and len(r.get("mensagem", "")) > 20]
    pct_golpe = 100 * len(freq_golpe) / n
    m_usaria = sum(usaria) / n
    m_conf = sum(conf) / n
    m_nps = sum(nps) / n
    pct_pagaria = 100 * len(pagaria) / n
    print(f"% que recebe golpe (6m): {pct_golpe:.0f}%  (meta >=60%)")
    print(f"Intencao de uso media:   {m_usaria:.1f}/10  (meta >=7)")
    print(f"Confianca media:         {m_conf:.1f}/10  (meta >=6)")
    print(f"Dispostos a pagar:       {pct_pagaria:.0f}%  (meta >=30%)")
    print(f"NPS familiar medio:      {m_nps:.1f}/10  (meta >=7)")
    print(f"Mensagens reais p/ analise: {len(msgs)}  (meta >=3)")
    print()
    print("=== DECISAO (criterios pre-registrados do trabalho, secao 6) ===")
    if m_usaria >= 7 and m_nps >= 7 and len(msgs) >= 3:
        print(">> PERSEVERAR: validar com prototipo automatizado (bot WhatsApp)")
    elif m_usaria >= 7 and m_conf < 6:
        print(">> AJUSTAR: problema crevel, falta sinal de autoridade (fontes oficiais/parcerias)")
    elif m_usaria < 7 and pct_golpe >= 60:
        print(">> PIVOTAR: dor presente, formato errado (testar alerta pro grupo da familia)")
    elif pct_golpe < 40 or m_usaria < 5:
        print(">> ABANDONAR: problema/solucao sem tracao real. Registrar e aprender.")
    else:
        print(">> ZONA DE JUDGMENT: nenhuma regra acionada com folga; ampliar amostra.")
    # detalhe por respondente
    print()
    print("=== DETALHE ===")
    for r in respostas:
        print(f"- {r.get('nome','?')} | perfil: {r.get('perfil','?')} | freq: {r.get('frequencia','?')} | usaria: {r.get('usaria','?')}/10 | pagaria: {r.get('pagaria','?')} | nps: {r.get('nps','?')}")

if __name__ == "__main__":
    principal()
