# ── PARCHE grammar.py · $fri 17/04 · shard•relay•oracle•threshold ──
# APLICAR EN: DIRIME/IMV/core/grammar.py
# UBICACIÓN: después de INTENT_MAP en language_routing.py
# Y en grammar.py CJK_TOKEN_MAP agregar:

# En CJK_TOKEN_MAP (grammar.py línea ~29):
新增_CJK = {
    "阈值": ("METHOD",   "<threshold>",   "H61", +0.05),  # threshold
    "分片": ("STACKING", "UF[H04]",       "H04", +0.05),  # shard
    "中继": ("SOCIAL",   "{relay}",       "H08", +0.05),  # relay
    "神谕": ("METHOD",   "<stat_onto>",   "H50", +0.05),  # oracle
    "锻造": ("TRUST",    "FOUNDATION",    "H01", +0.05),  # forge
    "通道": ("CRYPTO",   "(link seat)",   "H29", +0.05),  # canal
}
# NOTA: integrar manualmente en dict CJK_TOKEN_MAP

# En INTENT_MAP (language_routing.py) agregar:
INTENT_MAP_KALIL_AGENTS = {
    "shard_corpus": {
        "library": "STACKING",
        "subject": "UF[H04]",
        "verb": "reserva",
        "object": "shard_corpus_slice_soberano",
        "knot": "Nudo de Ocho"
    },
    "relay_kalil": {
        "library": "SOCIAL", 
        "subject": "{relay}",
        "verb": "lanza",
        "object": "relay_kalil_6_nodos_soberano",
        "knot": "As de Guía"
    },
    "oracle_nora": {
        "library": "METHOD",
        "subject": "<stat_onto>",
        "verb": "calcula",
        "object": "oracle_rating_nora_threshold",
        "knot": "Ballestrinque"
    },
    "threshold_taxonomy": {
        "library": "TRUST",
        "subject": "FOUNDATION",
        "verb": "verifica",
        "object": "threshold_taxonomy_scalar_min",
        "knot": "As de Guía"
    }
}

# En ACTIVITY_MAP agregar nuevas actividades H61, H04, H08:
ACTIVITY_MAP_KALIL = {
    "H61": "threshold_validation",
    "H04": "shard_reservation", 
    "H08": "relay_transmission"
}

# NOTA: Integrar manualmente estos parches en grammar.py y language_routing.py
# [term] :: activo · shard•relay•oracle•threshold
