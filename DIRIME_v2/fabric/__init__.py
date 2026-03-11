"""
DIRIME_v2/fabric — módulos soberanos de fabric.
Disponibles:
  poke_peek.py  — POKE+TRUST / PEEK+CRYPTO (activo)
  cat.py        — CAT(CODE) mínimo (activo)
Pendiente CAPA C:
  cat_os.py     — CAT(OS) syscalls directas
  cat_ssh.py    — CAT(SSH) túneles inter-nodo
  cat_scan.py   — CAT(SCAN) auditoría integridad
"""
from .poke_peek import poke, peek, peek_all, fabric_log
from .cat import cat_code, cat_log

__all__ = ['poke', 'peek', 'peek_all', 'fabric_log', 'cat_code', 'cat_log']
