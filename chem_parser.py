from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET


@dataclass
class Atom:
    atom_id: str
    x: float
    y: float
    label: str = "C"
    tag: str = ""


@dataclass
class Bond:
    begin_id: str
    end_id: str


@dataclass
class Molecule:
    atoms: dict[str, Atom] = field(default_factory=dict)
    bonds: list[Bond] = field(default_factory=list)


def parse_cdxml(content: str) -> Molecule:
    root = ET.fromstring(content)
    atoms: dict[str, Atom] = {}
    bonds: list[Bond] = []

    for node in root.iter("n"):
        atom_id = node.attrib.get("id")
        point = node.attrib.get("p")
        if not atom_id or not point:
            continue

        coords = point.split()
        if len(coords) != 2:
            continue

        try:
            x, y = float(coords[0]), float(coords[1])
        except ValueError:
            continue

        atoms[atom_id] = Atom(
            atom_id=atom_id,
            x=x,
            y=y,
            label=node.attrib.get("Element", "C"),
        )

    for bond in root.iter("b"):
        begin_id = bond.attrib.get("B")
        end_id = bond.attrib.get("E")
        if begin_id and end_id:
            bonds.append(Bond(begin_id=begin_id, end_id=end_id))

    if not atoms:
        raise ValueError("No atoms were found in the file")

    return Molecule(atoms=atoms, bonds=bonds)


def load_cdx_or_cdxml(path: Path) -> Molecule:
    raw = path.read_bytes()
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "Unsupported binary CDX file. Please export as CDXML (XML-based ChemDraw format)."
        ) from exc

    if "<CDXML" not in decoded and "<cdxml" not in decoded:
        raise ValueError("Input is not a CDXML document")

    return parse_cdxml(decoded)
