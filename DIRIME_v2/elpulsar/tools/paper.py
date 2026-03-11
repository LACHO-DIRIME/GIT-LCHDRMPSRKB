"""ELPULSAR — Tool Paper · documento renderizado."""
from __future__ import annotations
from core.resources import get_all

def render_html(cluster=None, title="PAPER SOBERANO"):
    rows = get_all(cluster=cluster)
    items = "".join(
        f'<tr class="{"verified" if r["verified"] else ""}">'
        f'<td>{"✅" if r["verified"] else "○"}</td>'
        f'<td>{r["title"]}</td><td>{r["type"]}</td>'
        f'<td>{r["scope"]}</td><td>{r.get("cluster","")}</td>'
        f'<td>{(r.get("content") or "")[:40]}</td></tr>'
        for r in rows)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>{title}</title><style>
body{{font-family:monospace;background:#1a1a2e;color:#eaeaea;padding:2rem}}
h1{{color:#e94560;font-size:1.2rem}}
table{{width:100%;border-collapse:collapse;font-size:.85rem}}
th{{background:#0f3460;padding:.4rem;text-align:left}}
td{{padding:.3rem .4rem;border-bottom:1px solid #333}}
.verified td{{color:#4ade80}}
</style></head><body><h1>{title}</h1>
<table><tr><th>V</th><th>Título</th><th>Tipo</th>
<th>Scope</th><th>Cluster</th><th>Contenido</th></tr>
{items}</table></body></html>"""
