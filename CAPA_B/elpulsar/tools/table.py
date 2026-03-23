"""ELPULSAR — Tool Table · grilla de recursos soberanos."""
from __future__ import annotations
from core.resources import get_all, create, verify, ResourceType, ResourceScope

def render_ascii(cluster=None, scope=None):
    rows = get_all(cluster=cluster, scope=scope)
    if not rows: return "TABLE vacía"
    lines = ["ID        TÍTULO       TIPO    SCOPE    CLUSTER  V"]
    lines.append("─" * 60)
    for r in rows:
        v = "✅" if r["verified"] else "○"
        lines.append(
            f"{r['id']:<10}{r['title'][:12]:<12} "
            f"{r['type'][:6]:<7}{r['scope'][:8]:<9}"
            f"{(r.get('cluster') or '')[:8]:<9}{v}")
    return "\n".join(lines)

def add_row(title, type_str, scope_str,
            content="", cluster="#CORE"):
    return create(title, ResourceType[type_str.upper()],
                  ResourceScope[scope_str.upper()],
                  content=content, cluster=cluster)
