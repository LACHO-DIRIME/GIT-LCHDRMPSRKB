"""ELPULSAR — Red Neuronal de Recursos · grafo soberano."""
from __future__ import annotations
from .resources import get_all, get_connections

def build_graph():
    resources = get_all()
    connections = get_connections()
    id_set = {r["id"] for r in resources}
    nodes = [{"id":r["id"],"title":r["title"],"type":r["type"],
               "scope":r["scope"],"cluster":r.get("cluster","#CORE"),
               "verified":r["verified"],"tomo_id":r.get("tomo_id"),
               "group":r["scope"]} for r in resources]
    links = [{"source":c["source_id"],"target":c["target_id"],
               "relation":c["relation"],"weight":c["weight"]}
              for c in connections
              if c["source_id"] in id_set and c["target_id"] in id_set]
    clusters = {}
    for r in resources:
        cl = r.get("cluster","#CORE")
        clusters[cl] = clusters.get(cl,0) + 1
    return {"nodes":nodes,"links":links,"clusters":clusters,
            "stats":{"total_nodes":len(nodes),"total_links":len(links),
                     "verified":sum(1 for n in nodes if n["verified"])}}

def neighbors(resource_id):
    result = set()
    for c in get_connections(resource_id):
        result.add(c["target_id"] if c["source_id"]==resource_id
                   else c["source_id"])
    return list(result)
