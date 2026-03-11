"""ELPULSAR — Tool Sprint · dashboard soberano 16/8/4."""
from __future__ import annotations
from core.resources import get_all
import time

SCHEMA = {"LACHO":{"target":16,"color":"#4a9eff"},
          "DIRIME":{"target":8,"color":"#ff6b4a"},
          "ELPULSAR":{"target":4,"color":"#4aff9e"}}

def get_sprint() -> dict:
    rs = get_all()
    progress = {c: {"done": sum(1 for r in rs
                    if r.get("cluster","").upper()==f"#{c}" and r.get("verified")),
                    "target": cfg["target"], "color": cfg["color"]}
                for c, cfg in SCHEMA.items()}
    for c in progress:
        t = progress[c]["target"]
        progress[c]["pct"] = round(progress[c]["done"]/t*100) if t else 0
    return {"timestamp": time.time(), "progress": progress,
            "errors": [{"id":r["id"],"title":r["title"]}
                       for r in rs if not r.get("verified")][:10],
            "total": len(rs),
            "verified": sum(1 for r in rs if r.get("verified"))}
