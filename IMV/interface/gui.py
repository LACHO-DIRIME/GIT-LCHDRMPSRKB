#!/usr/bin/env python3
"""
DIRIME IMV — interface/gui.py
Tkinter GUI soberana · V1 · $thu 30/04
Puerto 8742 · BUILDER live · ELPULSAR visual
Referencia: $wed.Nerve Cell ELPULSAR training.txt (NC_ELP_GUI_PENDING)
[term] :: activo
"""
from __future__ import annotations
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from core.grammar import validate, lacho_score, ValidationResult
from core.language_routing import route
from core.ledger import get_stats

# ── Constantes ────────────────────────────────────────────────
VERSION = "0.2"
TITLE   = f"DIRIME IMV GUI — V{VERSION} · V0.3.0 GATE"
LIBS    = ["TRUST","SAMU","CRYPTO","GATE","STACKING","WORK","SOCIAL","METHOD","ACTIVITY"]
KNOTS   = ["As de Guía","Nudo de Ocho","Ballestrinque","Nudo Corredizo","Nudo de Rizo"]

COLORS = {
    "bg":       "#ffffff",
    "fg":       "#1a1a2e",
    "accent":   "#2a7a4f",
    "warn":     "#d35400",
    "error":    "#c0392b",
    "purple":   "#8e44ad",
    "blue":     "#2980b9",
    "border":   "#e0e0e0",
    "bg_dark":  "#1a1a2e",
    "v030":     "#8e44ad",  # V0.3.0 accent color
}

# V0.3.0 GATE criteria status
V030_STATUS = {
    "scalar_s": {"current": 0.822, "target": 0.88, "status": "partial"},
    "tests": {"current": 44, "target": 44, "status": "complete"},
    "corpus": {"current": 58, "target": 65, "status": "partial"},
    "activity": {"current": "9/9 UF", "target": "H03-H05-H56-H06", "status": "complete"},
}


class IMVGui:
    """GUI Tkinter soberana DIRIME IMV."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(TITLE)
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(800, 600)

        self._build_ui()
        self._update_stats()

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=COLORS["bg_dark"], pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="DIRIME IMV V0.3.0", bg=COLORS["bg_dark"],
                 fg=COLORS["bg"], font=("Courier New", 14, "bold"),
                 padx=16).pack(side="left")
        self.stats_label = tk.Label(
            hdr, text="TX:— · S:— · cristales:—",
            bg=COLORS["bg_dark"], fg="#888",
            font=("Courier New", 9), padx=12)
        self.stats_label.pack(side="right")

        # V0.3.0 GATE Status Panel
        v030_panel = tk.LabelFrame(self.root, text="V0.3.0 GATE CRITERIA", bg=COLORS["bg"],
                                   fg=COLORS["v030"], font=("Courier New", 10, "bold"),
                                   padx=12, pady=8)
        v030_panel.pack(fill="x", padx=12, pady=8)
        
        self._build_v030_status(v030_panel)

        # Builder Section
        builder = tk.LabelFrame(self.root, text="BUILDER", bg=COLORS["bg"],
                               fg=COLORS["fg"], font=("Courier New", 10, "bold"),
                               padx=12, pady=8)
        builder.pack(fill="x", padx=12, pady=8)

        # Library dropdown
        tk.Label(builder, text="Library:", bg=COLORS["bg"], fg=COLORS["fg"],
                font=("Courier New", 9)).grid(row=0, column=0, sticky="w", padx=4)
        self.lib_var = tk.StringVar(value=LIBS[0])
        lib_combo = ttk.Combobox(builder, textvariable=self.lib_var, 
                                 values=LIBS, width=15, state="readonly")
        lib_combo.grid(row=0, column=1, padx=4, pady=2)

        # Subject entry
        tk.Label(builder, text="Subject:", bg=COLORS["bg"], fg=COLORS["fg"],
                font=("Courier New", 9)).grid(row=0, column=2, sticky="w", padx=4)
        self.subj_var = tk.StringVar()
        subj_entry = tk.Entry(builder, textvariable=self.subj_var, width=20)
        subj_entry.grid(row=0, column=3, padx=4, pady=2)

        # Verb dropdown
        tk.Label(builder, text="Verb:", bg=COLORS["bg"], fg=COLORS["fg"],
                font=("Courier New", 9)).grid(row=1, column=0, sticky="w", padx=4)
        self.verb_var = tk.StringVar(value="declara")
        verb_combo = ttk.Combobox(builder, textvariable=self.verb_var,
                                  values=["declara","ejecuta","penetra","inicia","evalúa","supera","transita","adapta","cruza","explora","resuelve","negocia","mantiene","crece"],
                                  width=15, state="readonly")
        verb_combo.grid(row=1, column=1, padx=4, pady=2)

        # Object entry
        tk.Label(builder, text="Object:", bg=COLORS["bg"], fg=COLORS["fg"],
                font=("Courier New", 9)).grid(row=1, column=2, sticky="w", padx=4)
        self.obj_var = tk.StringVar()
        obj_entry = tk.Entry(builder, textvariable=self.obj_var, width=20)
        obj_entry.grid(row=1, column=3, padx=4, pady=2)

        # Knot dropdown
        tk.Label(builder, text="Knot:", bg=COLORS["bg"], fg=COLORS["fg"],
                font=("Courier New", 9)).grid(row=2, column=0, sticky="w", padx=4)
        self.knot_var = tk.StringVar(value=KNOTS[0])
        knot_combo = ttk.Combobox(builder, textvariable=self.knot_var,
                                  values=KNOTS, width=15, state="readonly")
        knot_combo.grid(row=2, column=1, padx=4, pady=2)

        # Build button
        build_btn = tk.Button(builder, text="BUILD", bg=COLORS["accent"],
                             fg="white", font=("Courier New", 9, "bold"),
                             command=self._build_sentence)
        build_btn.grid(row=2, column=2, columnspan=2, padx=4, pady=4)

        # Sentence display
        sent_frame = tk.LabelFrame(self.root, text="SENTENCE", bg=COLORS["bg"],
                                  fg=COLORS["fg"], font=("Courier New", 10, "bold"),
                                  padx=12, pady=8)
        sent_frame.pack(fill="x", padx=12, pady=8)

        self.sentence_label = tk.Label(sent_frame, text="—", bg=COLORS["bg"],
                                     fg=COLORS["purple"], font=("Courier New", 11),
                                     wraplength=760, justify="left")
        self.sentence_label.pack(pady=4)

        # Validation section
        val_frame = tk.LabelFrame(self.root, text="VALIDATION", bg=COLORS["bg"],
                                 fg=COLORS["fg"], font=("Courier New", 10, "bold"),
                                 padx=12, pady=8)
        val_frame.pack(fill="x", padx=12, pady=8)

        self.val_result = tk.Label(val_frame, text="—", bg=COLORS["bg"],
                                  fg=COLORS["fg"], font=("Courier New", 10),
                                  wraplength=760, justify="left")
        self.val_result.pack(pady=4)

        # Score display
        self.score_label = tk.Label(val_frame, text="LACHO: —", bg=COLORS["bg"],
                                   fg=COLORS["accent"], font=("Courier New", 12, "bold"))
        self.score_label.pack(pady=2)

        # Action buttons
        btn_frame = tk.Frame(self.root, bg=COLORS["bg"])
        btn_frame.pack(fill="x", padx=12, pady=8)

        tk.Button(btn_frame, text="VALIDATE", bg=COLORS["blue"],
                 fg="white", font=("Courier New", 9, "bold"),
                 command=self._validate_sentence).pack(side="left", padx=4)
        tk.Button(btn_frame, text="CLEAR", bg=COLORS["warn"],
                 fg="white", font=("Courier New", 9, "bold"),
                 command=self._clear_builder).pack(side="left", padx=4)
        tk.Button(btn_frame, text="ROUTE", bg=COLORS["purple"],
                 fg="white", font=("Courier New", 9, "bold"),
                 command=self._route_sentence).pack(side="left", padx=4)

        # Log area
        log_frame = tk.LabelFrame(self.root, text="LOG", bg=COLORS["bg"],
                                 fg=COLORS["fg"], font=("Courier New", 10, "bold"),
                                 padx=12, pady=8)
        log_frame.pack(fill="both", expand=True, padx=12, pady=8)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80,
                                                  bg="#f8f8f8", fg=COLORS["fg"],
                                                  font=("Courier New", 9))
        self.log_text.pack(fill="both", expand=True)

    # ── ACTIONS ──────────────────────────────────────────────
    def _build_sentence(self):
        lib = self.lib_var.get()
        subj = self.subj_var.get()
        verb = self.verb_var.get()
        obj = self.obj_var.get() or "objeto_soberano"
        knot = self.knot_var.get()
        
        sentence = f"{lib} {subj} =><= .. {verb} .. {obj} --[{knot}] [term]"
        self.sentence_label.config(text=sentence)
        self._log(f"Built: {sentence}")

    def _validate_sentence(self):
        sentence = self.sentence_label.cget("text")
        if sentence == "—":
            self._log("No sentence to validate")
            return
        
        try:
            result = validate(sentence)
            score = lacho_score(result)
            
            status_color = COLORS["accent"] if result.value == "VALID" else COLORS["warn"]
            self.val_result.config(text=f"Result: {result.value}\nErrors: {result.errors}\nWarnings: {result.warnings}",
                                 fg=status_color)
            self.score_label.config(text=f"LACHO: {score:.3f}")
            
            self._log(f"Validated: {result.value} (score: {score:.3f})")
            
        except Exception as e:
            self.val_result.config(text=f"Error: {e}", fg=COLORS["error"])
            self._log(f"Validation error: {e}")

    def _route_sentence(self):
        sentence = self.sentence_label.cget("text")
        if sentence == "—":
            self._log("No sentence to route")
            return
        
        try:
            route_result = route(sentence)
            self._log(f"Routed to: {route_result}")
        except Exception as e:
            self._log(f"Routing error: {e}")

    def _clear_builder(self):
        self.subj_var.set("")
        self.obj_var.set("")
        self.sentence_label.config(text="—")
        self.val_result.config(text="—")
        self.score_label.config(text="LACHO: —")
        self._log("Builder cleared")

    def _build_v030_status(self, parent):
        """Build V0.3.0 GATE criteria status panel."""
        # Create grid for criteria
        for i, (criterion, data) in enumerate(V030_STATUS.items()):
            row = i // 2
            col = (i % 2) * 2
            
            # Criterion label
            crit_label = tk.Label(parent, text=criterion.upper().replace('_', ' '),
                                bg=COLORS["bg"], fg=COLORS["v030"],
                                font=("Courier New", 8, "bold"))
            crit_label.grid(row=row, column=col, sticky="w", padx=4, pady=2)
            
            # Status indicator
            status_color = COLORS["accent"] if data["status"] == "complete" else COLORS["warn"]
            status_text = f"{data['current']}/{data['target']}"
            status_label = tk.Label(parent, text=status_text,
                                   bg=COLORS["bg"], fg=status_color,
                                   font=("Courier New", 8))
            status_label.grid(row=row, column=col+1, sticky="w", padx=4, pady=2)

    def _update_stats(self):
        try:
            stats = get_stats()
            self.stats_label.config(
                text=f"TX:{stats.get('transactions_total', '—')} · S:{stats.get('scalar_s', '—')} · cristales:{stats.get('crystals_total', '—')}"
            )
        except Exception:
            self.stats_label.config(text="TX:— · S:— · cristales:—")

    def _log(self, message: str):
        timestamp = f"[{__import__('datetime').datetime.now().strftime('%H:%M:%S')}]"
        self.log_text.insert("end", f"{timestamp} {message}\n")
        self.log_text.see("end")


# ── MAIN ────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    app = IMVGui(root)
    
    # Auto-update stats every 5 seconds
    def auto_update():
        app._update_stats()
        root.after(5000, auto_update)
    
    auto_update()
    root.mainloop()


if __name__ == "__main__":
    main()
