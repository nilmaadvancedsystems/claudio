# -*- coding: utf-8 -*-
"""Arquivamento em lote de XML fiscais (NF-e, NFC-e, CT-e, NFS-e, eventos, inutilização).

Segue as mesmas regras da rotina /organizar (05d §1b, 03, 08): mesma pasta, mesmo nome,
conferência por hash, manifesto e quarentena. Só decide o que é exato pelas tags do XML;
o resto fica na origem para a rotina normal.

Uso:
  python xml_lote.py                 # simulação: só mostra o plano (nada é movido)
  python xml_lote.py --validar       # compara o resultado com XML já arquivados pela rotina
  python xml_lote.py --aplicar       # executa de verdade
  python xml_lote.py --aplicar --limite 500
"""
import argparse, collections, datetime as dt, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, unicodedata, zipfile
import xml.etree.ElementTree as ET

RAIZ_REGRAS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTL = os.path.join(RAIZ_REGRAS, "_CONTROLE")
ORIGEM = r"G:\Meu Drive\Claudio Secretario"
CLIENTES = r"G:\Meu Drive\2026"
CADASTRO = os.path.join(RAIZ_REGRAS, "necessario para o claude", "dados agentes", "cadastro_empresas_unificado.xlsx")
UNRAR = r"C:\Program Files\WinRAR\UnRAR.exe"
ESCRITORIO = {"27872981000113"}  # Nilma: só identifica a 284 quando é ela a emitente

REGIME_PASTA = {  # enquadramento da planilha -> (pasta do regime, pasta XML)
    "SIMPLES": ("SIMPLES NACIONAL", "12. XML"),
    "PRESUMIDO": ("LUCRO PRESUMIDO", "14. XML"),
    "REAL": ("LUCRO REAL", "14. XML"),
    "ISENTAS": ("ISENTA", "10. XML"),
    "FISICA": ("PESSOA FISICA", "06. XML"),
    "DOMESTICAS": ("DOMESTICA", "06. XML"),
}
# confirmações do responsável registradas no 03 (CPF/CNPJ com mais de uma linha na planilha)
CONFIRMADOS = {"42460727615": 62, "36857858691": 424}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm_nome(s):
    s = str(s or "").replace("0026", "&").replace("0027", "'")
    return re.sub(r"[^A-Z0-9]", "", sem_acento(s).upper())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sha_arq(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- cadastro
def carregar_cadastro():
    import openpyxl
    ws = openpyxl.load_workbook(CADASTRO, read_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    cab = [str(x).strip().lower() for x in rows[0]]
    ic, ir, idoc, ie = cab.index("código"), cab.index("razão social"), cab.index("cnpj"), cab.index("enquadramento")
    por_doc, por_cod, por_nome = collections.defaultdict(set), {}, {}
    for r in rows[1:]:
        if r[ic] is None:
            continue
        cod = int(r[ic])
        reg = norm_nome(r[ie])
        por_cod[cod] = {"razao": r[ir], "regime": reg}
        d = re.sub(r"\D", "", str(r[idoc] or ""))
        if d:
            por_doc[d].add(cod)
        por_nome[norm_nome(r[ir])] = cod
    pastas = {}
    for n in os.listdir(CLIENTES):
        m = re.match(r"(\d+)\s*-\s*", n)
        if m and os.path.isdir(os.path.join(CLIENTES, n)):
            pastas.setdefault(int(m.group(1)), os.path.join(CLIENTES, n))
    return por_doc, por_cod, por_nome, pastas


def cliente_do_doc(doc, cad):
    por_doc = cad[0]
    if doc in CONFIRMADOS:
        return {CONFIRMADOS[doc]}
    return por_doc.get(doc, set())


def cliente_da_subpasta(rel, cad):
    """Código do cliente pelo nome/código de alguma pasta do caminho (download SIEG do cliente)."""
    por_cod, por_nome = cad[1], cad[2]
    for parte in reversed(rel.replace("/", "\\").split("\\")[:-1]):
        m = re.match(r"(\d+)\b", parte)
        if m and int(m.group(1)) in por_cod and not re.match(r"\d{4}-\d{2}$", parte) and not re.match(r"\d{6}", parte):
            return int(m.group(1))
        n = norm_nome(re.sub(r"^SIEG \d{4}-\d{2} - ", "", parte))
        if len(n) >= 6:
            if n in por_nome:
                return por_nome[n]
            cands = [c for k, c in por_nome.items() if len(k) >= 6 and (k.startswith(n) or n.startswith(k))]
            if len(set(cands)) == 1:
                return cands[0]
    return None


# ---------------------------------------------------------------- leitura do XML
def strip_ns(root):
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    return root


def txt(root, *caminhos):
    for c in caminhos:
        el = root.find(c)
        if el is not None and el.text and el.text.strip():
            return el.text.strip()
    return None


def docs_de(el):
    if el is None:
        return []
    out = []
    for t in ("CNPJ", "CPF"):
        for x in el.iter(t):
            if x.text and x.text.strip():
                out.append(re.sub(r"\D", "", x.text))
    return out


def nomes_de(root):
    out = {}
    for t in ("emit", "dest", "rem", "exped", "receb", "toma", "toma4", "prest", "Prestador", "PrestadorServico", "Tomador", "TomadorServico"):
        for el in root.iter(t):
            ds = docs_de(el)
            nm = None
            for k in ("xNome", "RazaoSocial", "xFant"):
                x = el.find(".//" + k)
                if x is not None and x.text and x.text.strip():
                    nm = x.text.strip(); break
            if ds and nm:
                out.setdefault(ds[0], nm)
    return out


def mes_ano(data):
    m = re.match(r"(\d{4})-(\d{2})", data or "")
    return f"{m.group(2)}-{m.group(1)}" if m else None


def dia(data):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", data or "")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def evento_nome(desc):
    return re.sub(r"\s+", " ", sem_acento(desc or "").upper()).strip()


def num_chave(ch):
    return str(int(ch[25:34])) if ch and len(ch) == 44 and ch.isdigit() else None


def ler_xml(b):
    """Devolve dict(tipo, sub, nome, emit, partes, nomes) ou None se não for tipo tratado aqui."""
    try:
        root = strip_ns(ET.fromstring(b))
    except ET.ParseError:
        return None
    r = _ler_xml(root)
    if r:
        r["nomes"] = nomes_de(root)
    return r


def _ler_xml(root):
    tag = root.tag
    if tag in ("nfeProc", "NFe"):
        inf = root.find(".//infNFe")
        if inf is None:
            return None
        mod = txt(inf, "ide/mod")
        tipo = {"55": "NF-e", "65": "NFC-e"}.get(mod)
        n, d = txt(inf, "ide/nNF"), txt(inf, "ide/dhEmi", "ide/dEmi")
        if not tipo or not n or not mes_ano(d):
            return None
        emit = docs_de(inf.find("emit"))[:1]
        partes = emit + docs_de(inf.find("dest"))
        return {"tipo": tipo, "sub": "", "nome": f"{mes_ano(d)}_{tipo}_{int(n)}.xml", "emit": emit, "partes": partes}
    if tag in ("cteProc", "CTe"):
        inf = root.find(".//infCte")
        if inf is None:
            return None
        n, d = txt(inf, "ide/nCT"), txt(inf, "ide/dhEmi")
        if not n or not mes_ano(d):
            return None
        emit = docs_de(inf.find("emit"))[:1]
        partes = list(emit)
        for p in ("rem", "dest", "exped", "receb", "ide/toma4"):
            partes += docs_de(inf.find(p))
        return {"tipo": "CT-e", "sub": "", "nome": f"{mes_ano(d)}_CT-e_{int(n)}.xml", "emit": emit, "partes": partes}
    if tag in ("procEventoNFe", "procEventoCTe", "evento", "eventoCTe"):
        inf = root.find(".//infEvento")
        if inf is None:
            return None
        ch = txt(inf, "chNFe", "chCTe")
        tipo = "CT-e" if (tag.endswith("CTe") or inf.find("chCTe") is not None) else "NF-e"
        desc = txt(inf, "detEvento/descEvento", ".//descEvento")
        d = txt(inf, "dhEvento")
        n = num_chave(ch)
        if not (n and desc and dia(d)):
            return None
        emit_chave = [ch[6:20]]
        autor = [re.sub(r"\D", "", x) for x in (txt(inf, "CNPJ"), txt(inf, "CPF")) if x]
        extra = docs_de(inf.find("detEvento"))
        return {"tipo": tipo, "sub": "EVENTOS", "nome": f"{dia(d)} - {evento_nome(desc)} {tipo} {n}.xml",
                "emit": emit_chave, "partes": autor + emit_chave + extra, "evento": True}
    if tag in ("procInutNFe", "inutNFe", "retInutNFe"):
        inf = root.find(".//infInut")
        if inf is None:
            return None
        a, z_ = txt(inf, "nNFIni"), txt(inf, "nNFFin")
        d = txt(root, ".//infInut/dhRecbto", ".//dhRecbto")
        doc = docs_de(inf)[:1]
        if not (a and z_ and dia(d) and doc):
            return None
        return {"tipo": "NF-e", "sub": "EVENTOS", "nome": f"{dia(d)} - INUTILIZACAO NF-e {int(a)} A {int(z_)}.xml",
                "emit": doc, "partes": doc}
    # NFS-e (padrão nacional e ABRASF)
    if "nfse" in tag.lower() or root.find(".//infNFSe") is not None or root.find(".//InfNfse") is not None:
        inf = root.find(".//infNFSe")
        if inf is not None:
            n = txt(inf, "nNFSe")
            d = txt(inf, "DPS/infDPS/dhEmi", ".//dhEmi", "dhProc")
            emit = docs_de(inf.find("emit"))[:1] or docs_de(inf.find(".//prest"))[:1]
            partes = emit + docs_de(inf.find(".//toma"))
        else:
            inf = root.find(".//InfNfse")
            if inf is None:
                return None
            n = txt(inf, "Numero")
            d = txt(inf, "DataEmissao", ".//DataEmissao")
            emit = docs_de(inf.find(".//PrestadorServico")) or docs_de(inf.find(".//Prestador"))
            emit = emit[:1]
            partes = emit + docs_de(inf.find(".//TomadorServico")) + docs_de(inf.find(".//Tomador"))
        if not n or not mes_ano(d):
            return None
        return {"tipo": "NFS-e", "sub": "", "nome": f"{mes_ano(d)}_NFS-e_{int(n) if n.isdigit() else n}.xml",
                "emit": emit, "partes": partes}
    return None


# ---------------------------------------------------------------- decisão de cliente/destino
def decidir(info, rel, cad):
    """-> (codigo, motivo) ; codigo None = fica para a rotina."""
    cand = []
    for d in info["partes"]:
        for c in cliente_do_doc(d, cad):
            if c not in cand:
                cand.append(c)
    # escritório só vale quando é a emitente
    if "27872981000113" in info["partes"] and "27872981000113" not in info["emit"]:
        cand = [c for c in cand if c not in cliente_do_doc("27872981000113", cad)]
    sub = cliente_da_subpasta(rel, cad)
    if sub is not None and sub in cand:
        return sub, "subpasta+documento"
    if len(cand) == 1:
        return cand[0], "documento"
    if not cand and info.get("evento") and sub is not None:
        return sub, "evento órfão: cliente da subpasta (03)"
    if not cand:
        return None, "CLIENTE_NAO_LOCALIZADO"
    return None, "CLIENTE_AMBIGUO: " + ",".join(map(str, cand))


def nome_raiz(cod, info, cad):
    """Raiz nova: CNPJ/CPF do documento bate exato com a planilha (reconfirmação do 03)."""
    razao = cad[1][cod]["razao"]
    for d, nm in info.get("nomes", {}).items():
        if cod in cliente_do_doc(d, cad):
            razao = nm
            break
    razao = re.sub(r'[<>:"/\|?*]', "", str(razao)).strip().rstrip(".")
    return os.path.join(CLIENTES, f"{cod} - {razao.upper()}")


RAIZES_NOVAS = {}


def pasta_destino(cod, info, cad):
    por_cod, pastas = cad[1], cad[3]
    reg = por_cod[cod]["regime"]
    if reg not in REGIME_PASTA:
        return None, f"regime {reg or 'vazio'} sem pasta XML"
    if cod not in pastas:
        if not any(cod in cliente_do_doc(d, cad) for d in info["partes"]):
            return None, "pasta raiz do cliente não existe e o documento não traz o CNPJ dele"
        pastas[cod] = RAIZES_NOVAS.setdefault(cod, nome_raiz(cod, info, cad))
    rp, xp = REGIME_PASTA[reg]
    p = os.path.join(pastas[cod], "FISCAL", rp, xp, info["tipo"])
    if info["sub"]:
        p = os.path.join(p, info["sub"])
    return p, None


# ---------------------------------------------------------------- inventário
def inventario():
    for dp, dns, fns in os.walk(ORIGEM):
        dns[:] = [d for d in dns if d != "NÃO IDENTIFICADOS" and not d.startswith("ORGANIZACAO-MANUAL")]
        for f in fns:
            ext = f.lower().rsplit(".", 1)[-1]
            if ext in ("xml", "zip", "rar"):
                yield os.path.join(dp, f)


def membros_container(p):
    """-> lista (nome, bytes) ou None se tiver algo que não seja XML (rotina normal trata)."""
    out = []
    if p.lower().endswith(".zip"):
        try:
            z = zipfile.ZipFile(p)
        except zipfile.BadZipFile:
            return None
        for i in z.infolist():
            if i.is_dir():
                continue
            if not i.filename.lower().endswith(".xml"):
                return None
            out.append((i.filename, z.read(i)))
        return out
    tmp = tempfile.mkdtemp(prefix="xmllote_")
    try:
        r = subprocess.run([UNRAR, "x", "-o+", "-inul", p, tmp + os.sep], capture_output=True)
        if r.returncode != 0:
            return None
        for dp, _, fns in os.walk(tmp):
            for f in fns:
                if not f.lower().endswith(".xml"):
                    return None
                q = os.path.join(dp, f)
                out.append((os.path.relpath(q, tmp), open(q, "rb").read()))
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- manifesto
def carregar_manifesto():
    idx = {}
    p = os.path.join(CTL, "MANIFESTO", "manifesto.jsonl")
    for l in open(p, encoding="utf-8"):
        try:
            d = json.loads(l)
        except Exception:
            continue
        df, nf = str(d.get("destino_final") or ""), str(d.get("nome_final") or "")
        full = df if nf and df.lower().endswith(nf.lower()) else os.path.join(df, nf)
        for k in ("hash_origem", "hash_destino"):
            if d.get(k):
                idx.setdefault(d[k], []).append(full)
    return idx


class Pasta:
    """Cache de hash por pasta de destino (Fase 3-4: compara com a pasta inteira)."""
    def __init__(self):
        self.c = {}

    def get(self, p):
        if p not in self.c:
            m = {}
            if os.path.isdir(p):
                for f in os.listdir(p):
                    q = os.path.join(p, f)
                    if os.path.isfile(q):
                        m[sha_arq(q)] = f
            self.c[p] = m
        return self.c[p]


def nome_livre(pasta, nome, ocupados):
    base, ext = os.path.splitext(nome)
    cand, k = nome, 1
    while os.path.exists(os.path.join(pasta, cand)) or os.path.join(pasta, cand).lower() in ocupados:
        cand = f"{base} ({k}){ext}"
        k += 1
    return cand


# ---------------------------------------------------------------- validação
def validar(cad):
    """Reclassifica XML que a rotina já arquivou e compara pasta+nome."""
    ok = dif = sem = 0
    exemplos = []
    p = os.path.join(CTL, "MANIFESTO", "manifesto.jsonl")
    vistos = set()
    for l in open(p, encoding="utf-8"):
        try:
            d = json.loads(l)
        except Exception:
            continue
        nf = str(d.get("nome_final") or "")
        if not nf.lower().endswith(".xml") or nf in vistos:
            continue
        df = str(d.get("destino_final") or "")
        full = df if df.lower().endswith(nf.lower()) else os.path.join(df, nf)
        if not os.path.isfile(full):
            continue
        vistos.add(nf)
        info = ler_xml(open(full, "rb").read())
        if not info:
            sem += 1
            continue
        rel = str(d.get("nome_original") or nf)
        cod, mot = decidir(info, rel, cad)
        if cod is None:
            sem += 1
            if len(exemplos) < 15:
                exemplos.append(("SEM DECISAO", mot, full))
            continue
        pasta, err = pasta_destino(cod, info, cad)
        esperado = os.path.normcase(os.path.normpath(os.path.dirname(full)))
        nome_real = re.sub(r" \(\d+\)(\.xml)$", r"\1", os.path.basename(full))
        if pasta and os.path.normcase(os.path.normpath(pasta)) == esperado and nome_real == info["nome"]:
            ok += 1
        else:
            dif += 1
            if len(exemplos) < 40:
                exemplos.append(("DIFERENTE", f"{pasta}\\{info['nome']}", full))
        if ok + dif + sem >= 4000:
            break
    print(f"validação: iguais {ok} · diferentes {dif} · sem decisão {sem}")
    for e in exemplos:
        print("  ", " | ".join(e))


# ---------------------------------------------------------------- execução
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--validar", action="store_true")
    ap.add_argument("--limite", type=int, default=0)
    a = ap.parse_args()
    cad = carregar_cadastro()
    if a.validar:
        return validar(cad)

    agora = dt.datetime.now()
    id_exec = "XMLLOTE-" + agora.strftime("%Y%m%d-%H%M%S")
    lock = os.path.join(CTL, "_execucao.lock")
    if a.aplicar:
        if os.path.exists(lock) and (agora.timestamp() - os.path.getmtime(lock)) < 4 * 3600:
            sys.exit("Rotina em execução (_execucao.lock com menos de 4h). Tente depois.")
        json.dump({"id_execucao": id_exec, "inicio": agora.isoformat(), "fase_atual": "xml_lote"}, open(lock, "w"))
    man = carregar_manifesto()
    pastas = Pasta()
    ocupados = set()
    qdia = os.path.join(CTL, "BACKUP ROTINA", agora.strftime("%d-%m-%Y"))
    res = collections.Counter()
    motivos = collections.Counter()
    plano = []
    fman = fq = None
    if a.aplicar:
        os.makedirs(qdia, exist_ok=True)
        fman = open(os.path.join(CTL, "MANIFESTO", "manifesto.jsonl"), "a", encoding="utf-8")
        fq = open(os.path.join(qdia, "_quarentena.jsonl"), "a", encoding="utf-8")

    def tratar(nome_orig, b, rel, h_pai):
        """-> 'ARQUIVADO' | 'JA_ARQUIVADO' | None (fica)."""
        h = sha(b)
        for full in man.get(h, []):
            if os.path.isfile(full):
                res["JA_ARQUIVADO_ANTERIORMENTE"] += 1
                if a.aplicar and h_pai:
                    fman.write(json.dumps({"hash_origem": h, "hash_original": h_pai, "nome_original": nome_orig,
                                           "destino_final": os.path.dirname(full) + "\\", "nome_final": os.path.basename(full),
                                           "id_execucao": id_exec, "timestamp": dt.datetime.now().isoformat(), "status": "JA_ARQUIVADO_ANTERIORMENTE"},
                                          ensure_ascii=False) + "\n")
                return "JA", full
        info = ler_xml(b)
        if not info:
            motivos["tipo de XML não tratado aqui (fica para a rotina)"] += 1
            return None, None
        cod, mot = decidir(info, rel, cad)
        if cod is None:
            motivos[mot.split(":")[0]] += 1
            return None, None
        pasta, err = pasta_destino(cod, info, cad)
        if not pasta:
            motivos[err] += 1
            return None, None
        idx = pastas.get(pasta)
        if h in idx:
            res["JA_ARQUIVADO_ANTERIORMENTE"] += 1
            full = os.path.join(pasta, idx[h])
            if a.aplicar:
                fman.write(json.dumps({"hash_origem": h, "hash_original": h_pai or h, "nome_original": nome_orig,
                                       "destino_final": pasta + "\\", "nome_final": idx[h], "id_execucao": id_exec,
                                       "timestamp": dt.datetime.now().isoformat(), "status": "JA_ARQUIVADO_ANTERIORMENTE"}, ensure_ascii=False) + "\n")
            return "JA", full
        nome = nome_livre(pasta, info["nome"], ocupados)
        full = os.path.join(pasta, nome)
        ocupados.add(full.lower())
        plano.append((rel, cod, full))
        res["ARQUIVADO"] += 1
        if a.aplicar:
            os.makedirs(pasta, exist_ok=True)
            with open(full, "wb") as f:
                f.write(b)
            if sha_arq(full) != h:
                os.remove(full)
                raise RuntimeError("hash não confere após cópia: " + full)
            idx[h] = nome
            man.setdefault(h, []).append(full)
            fman.write(json.dumps({"hash_origem": h, "hash_original": h_pai or h, "nome_original": nome_orig,
                                   "destino_final": pasta + "\\", "nome_final": nome, "id_execucao": id_exec,
                                   "timestamp": dt.datetime.now().isoformat(), "status": "ARQUIVADO",
                                   "cliente_destino": os.path.basename(cad[3][cod])}, ensure_ascii=False) + "\n")
        return "ARQ", full

    def quarentenar(src, rel, h, destino, tipo):
        dst = os.path.join(qdia, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        base, ext = os.path.splitext(dst)
        k = 2
        while os.path.exists(dst):
            dst = f"{base}_{k}{ext}"
            k += 1
        shutil.move(src, dst)
        reg = {"hash_original": h, "arquivo_original_caminho": rel, "destino_final": destino and os.path.dirname(destino) + "\\",
               "nome_final": destino and os.path.basename(destino), "id_execucao": id_exec, "timestamp": dt.datetime.now().isoformat()}
        if tipo:
            reg.update({"destino_final": None, "nome_final": None, "tipo": tipo})
        fq.write(json.dumps(reg, ensure_ascii=False) + "\n")

    n_pais = 0
    try:
        for src in inventario():
            if a.limite and n_pais >= a.limite:
                break
            rel = os.path.relpath(src, ORIGEM)
            if src.lower().endswith(".xml"):
                n_pais += 1
                b = open(src, "rb").read()
                st, dest = tratar(os.path.basename(src), b, rel, None)
                if st and a.aplicar:
                    quarentenar(src, rel, sha(b), dest, None)
                if st:
                    res["pais_resolvidos"] += 1
                continue
            membros = membros_container(src)
            if membros is None:
                motivos["contêiner com arquivo que não é XML (fica para a rotina)"] += 1
                continue
            n_pais += 1
            h_pai = sha_arq(src)
            todos = True
            for nm, b in membros:
                st, _ = tratar(os.path.basename(nm), b, os.path.join(rel, nm), h_pai)
                todos = todos and bool(st)
            if todos:
                res["pais_resolvidos"] += 1
                res["contêineres esvaziados"] += 1
                if a.aplicar:
                    fman.flush()
                    quarentenar(src, rel, h_pai, None, "container_extraido")
            else:
                res["contêineres que ficam (algum XML não decidido)"] += 1
            if a.aplicar:
                fman.flush(); fq.flush()
    finally:
        if fman:
            fman.close(); fq.close()
        if a.aplicar and os.path.exists(lock):
            try:
                if json.load(open(lock)).get("id_execucao") == id_exec:
                    os.remove(lock)
            except Exception:
                pass

    por_cli = collections.Counter(os.path.basename(cad[3][c]) for _, c, _ in plano)
    linhas = [f"XML EM LOTE — {id_exec} — {'APLICADO' if a.aplicar else 'SIMULAÇÃO (nada foi movido)'}",
              f"itens de origem avaliados: {n_pais}"]
    linhas += [f"  {k}: {v}" for k, v in res.items()]
    linhas.append("ficam na origem para a rotina normal:")
    linhas += [f"  {k}: {v}" for k, v in motivos.most_common()]
    linhas.append(f"pastas de cliente novas (CNPJ do documento = planilha): {len(RAIZES_NOVAS)}")
    linhas += [f"  {v}" for v in RAIZES_NOVAS.values()]
    linhas.append("arquivos novos por cliente:")
    linhas += [f"  {v:5d}  {k}" for k, v in por_cli.most_common()]
    rel_txt = "\n".join(linhas)
    print(rel_txt)
    d = os.path.join(CTL, "LOGS", agora.strftime("%Y-%m"), agora.strftime("%d"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, id_exec + ".txt"), "w", encoding="utf-8") as f:
        f.write(rel_txt + "\n\n=== PLANO ===\n")
        for r, c, full in plano:
            f.write(f"{r} -> {full}\n")


if __name__ == "__main__":
    main()
