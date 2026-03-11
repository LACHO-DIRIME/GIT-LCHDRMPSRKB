"""ELPULSAR — Tool Key · índice · auth · bridge."""
from __future__ import annotations
from core.resources import get_all, get_connections, ResourceScope

def index(scope=None):
    idx = {s.value: [] for s in ResourceScope}
    for r in get_all(scope=scope):
        idx.get(r["scope"],[]).append(
            {"id":r["id"],"title":r["title"],
             "type":r["type"],"verified":r["verified"],
             "cluster":r.get("cluster")})
    return idx

def bridge(resource_id):
    all_r = get_all()
    resource = next((r for r in all_r if r["id"]==resource_id),None)
    if not resource:
        return {"error": f"recurso {resource_id} no encontrado"}
    return {"resource":resource,
            "connections":get_connections(resource_id),
            "scope":resource["scope"],
            "verified":bool(resource["verified"])}

def summary():
    all_r = get_all()
    return {"total":len(all_r),
            "verified":sum(1 for r in all_r if r["verified"]),
            "by_scope":{s.value:sum(1 for r in all_r
                        if r["scope"]==s.value)
                        for s in ResourceScope},
            "connections":len(get_connections())}
