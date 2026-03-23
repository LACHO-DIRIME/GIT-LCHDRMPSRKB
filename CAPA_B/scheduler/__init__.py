"""
DIRIME_v2/scheduler — Scheduler OS soberano.
Disponibles:
  scheduler.py  — Scheduler OS con TOMO/SLICE/CLUSTER (activo)
  tether.py     — SOCIAL {tether} vinculación persistente (activo/stub)
Pendiente CAPA C:
  ime_ching.py  — IME Modo I CHING proceso background
  loan_ime.py   — LOAN-IME precarga pesos RAG
"""
from .scheduler import planifica, rise, set_dia, estado_semana
from .tether import anchor, get_state, release

__all__ = ['planifica', 'rise', 'set_dia', 'estado_semana',
           'anchor', 'get_state', 'release']
