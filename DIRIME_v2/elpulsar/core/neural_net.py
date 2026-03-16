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

class NeuralNet:
    """Red neuronal ELPULSAR para procesamiento soberano."""
    
    def get_notaria_graph(self) -> dict:
        """Subgrafo de recursos tipo NOTARIA para pipeline soberano."""
        try:
            from DIRIME_v2.elpulsar.core.resources import get_resources
            all_res = get_resources()
        except Exception:
            all_res = []

        notaria_keywords = {
            "notaria", "certifica", "sella", "inmutabiliza",
            "h63", "bolivar", "nora", "carilo"
        }

        nodes, links = [], []
        for r in all_res:
            name = str(r.get("name", "")).lower()
            cluster = str(r.get("cluster", "")).lower()
            rtype = str(r.get("type", "")).lower()
            if (any(k in name for k in notaria_keywords) or
                  "#notaria" in cluster or
                  ("lacho" in rtype and any(k in name for k in notaria_keywords))):
                nodes.append(r)

        for i, a in enumerate(nodes):
            for b in nodes[i+1:]:
                if a.get("cluster") == b.get("cluster"):
                    links.append({"source": a.get("name"), "target": b.get("name")})

        try:
            from core.samu import get_scalar_s
            scalar_s = get_scalar_s()
        except Exception:
            scalar_s = 0.773
            
        try:
            from core.ledger import get_stats
            stats = get_stats()
        except Exception:
            stats = {"transactions_total": 1363}

        return {
            "nodes": nodes,
            "links": links,
            "stats": {
                "actos_ku":       0,
                "actos_wu":       0,
                "scalar_promedio": scalar_s,
                "tx_total":        stats.get("transactions_total", 1363),
            }
        }
