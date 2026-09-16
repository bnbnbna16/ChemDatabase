#!/usr/bin/env python3
"""用于查看 ChemDraw CDX/CDXML 并为原子添加标签的简易工具。"""

from __future__ import annotations

import argparse
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog
from xml.etree import ElementTree as ET

from chem_parser import Molecule, load_cdx_or_cdxml


class CdxTaggerApp:
    def __init__(self, root: tk.Tk, file_path: Path | None = None):
        self.root = root
        self.root.title("ChemDatabase 化学结构标注器")
        self.molecule = Molecule()
        self.atom_positions: dict[str, tuple[float, float]] = {}

        controls = tk.Frame(root)
        controls.pack(fill=tk.X, padx=8, pady=8)

        tk.Button(controls, text="打开 .cdx/.cdxml", command=self.open_file).pack(side=tk.LEFT)
        tk.Button(controls, text="清空标签", command=self.clear_tags).pack(side=tk.LEFT, padx=8)

        content = tk.PanedWindow(root, sashrelief=tk.RAISED)
        content.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(content, width=900, height=600, bg="white")
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        content.add(self.canvas, stretch="always")

        sidebar = tk.Frame(content)
        tk.Label(sidebar, text="化学标签").pack(anchor="w", padx=8, pady=(8, 4))
        self.tags_list = tk.Listbox(sidebar, width=40)
        self.tags_list.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        content.add(sidebar)

        if file_path:
            self.load_file(file_path)

    def open_file(self) -> None:
        file_name = filedialog.askopenfilename(
            title="打开 ChemDraw 文件",
            filetypes=[("ChemDraw 文件", "*.cdx *.cdxml"), ("所有文件", "*.*")],
        )
        if file_name:
            self.load_file(Path(file_name))

    def load_file(self, path: Path) -> None:
        try:
            self.molecule = load_cdx_or_cdxml(path)
        except (OSError, ValueError, ET.ParseError) as exc:
            messagebox.showerror("无法打开文件", str(exc))
            return
        self.draw_molecule()

    def draw_molecule(self) -> None:
        self.canvas.delete("all")
        self.atom_positions.clear()
        self.tags_list.delete(0, tk.END)

        atoms = list(self.molecule.atoms.values())
        min_x = min(atom.x for atom in atoms)
        min_y = min(atom.y for atom in atoms)
        max_x = max(atom.x for atom in atoms)
        max_y = max(atom.y for atom in atoms)

        width = max(max_x - min_x, 1)
        height = max(max_y - min_y, 1)
        canvas_w = int(self.canvas["width"])
        canvas_h = int(self.canvas["height"])
        scale = min((canvas_w - 80) / width, (canvas_h - 80) / height)

        def convert(atom: Atom) -> tuple[float, float]:
            x = 40 + (atom.x - min_x) * scale
            y = 40 + (atom.y - min_y) * scale
            return x, y

        for bond in self.molecule.bonds:
            start = self.molecule.atoms.get(bond.begin_id)
            end = self.molecule.atoms.get(bond.end_id)
            if not start or not end:
                continue
            sx, sy = convert(start)
            ex, ey = convert(end)
            self.canvas.create_line(sx, sy, ex, ey, width=2, fill="#333333")

        for atom in atoms:
            x, y = convert(atom)
            self.atom_positions[atom.atom_id] = (x, y)
            self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, outline="#1e88e5", fill="#e3f2fd")
            self.canvas.create_text(x, y - 16, text=atom.label, fill="#0d47a1")
            if atom.tag:
                self.canvas.create_text(x + 24, y, text=f"[{atom.tag}]", fill="#2e7d32", anchor="w")
                self.tags_list.insert(tk.END, f"{atom.label} ({atom.atom_id}): {atom.tag}")

    def on_canvas_click(self, event: tk.Event) -> None:
        closest_atom_id = None
        best_dist = 14.0
        for atom_id, (x, y) in self.atom_positions.items():
            dist = ((x - event.x) ** 2 + (y - event.y) ** 2) ** 0.5
            if dist <= best_dist:
                best_dist = dist
                closest_atom_id = atom_id

        if not closest_atom_id:
            return

        atom = self.molecule.atoms[closest_atom_id]
        tag = simpledialog.askstring(
            "标注化学对象",
            f"为原子 {atom.atom_id}（{atom.label}）设置标签：",
            initialvalue=atom.tag,
            parent=self.root,
        )
        if tag is None:
            return

        atom.tag = tag.strip()
        self.draw_molecule()

    def clear_tags(self) -> None:
        for atom in self.molecule.atoms.values():
            atom.tag = ""
        self.draw_molecule()


def main() -> None:
    parser = argparse.ArgumentParser(description="查看 ChemDraw CDX/CDXML 并为化学对象添加标签")
    parser.add_argument("file", nargs="?", help="可选：.cdx/.cdxml 文件路径")
    args = parser.parse_args()

    root = tk.Tk()
    app = CdxTaggerApp(root, Path(args.file) if args.file else None)
    root.minsize(900, 600)
    root.mainloop()


if __name__ == "__main__":
    main()
