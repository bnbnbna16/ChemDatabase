import unittest

from chem_parser import load_cdx_or_cdxml, parse_cdxml


SIMPLE_CDXML = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<CDXML>
  <page>
    <fragment>
      <n id=\"1\" p=\"10 10\" Element=\"C\" />
      <n id=\"2\" p=\"20 10\" Element=\"O\" />
      <b id=\"3\" B=\"1\" E=\"2\" />
    </fragment>
  </page>
</CDXML>
"""


class TestCdxParsing(unittest.TestCase):
    def test_parse_cdxml_extracts_atoms_and_bonds(self):
        molecule = parse_cdxml(SIMPLE_CDXML)

        self.assertEqual(set(molecule.atoms), {"1", "2"})
        self.assertEqual(molecule.atoms["1"].label, "C")
        self.assertEqual(molecule.atoms["2"].label, "O")
        self.assertEqual(len(molecule.bonds), 1)
        self.assertEqual((molecule.bonds[0].begin_id, molecule.bonds[0].end_id), ("1", "2"))

    def test_load_rejects_binary_cdx(self):
        with self.assertRaises(ValueError):
            from pathlib import Path
            import tempfile

            with tempfile.TemporaryDirectory() as tmp_dir:
                p = Path(tmp_dir) / "sample.cdx"
                p.write_bytes(b"VjCD0100\x00\x01\x02")
                load_cdx_or_cdxml(p)


if __name__ == "__main__":
    unittest.main()
