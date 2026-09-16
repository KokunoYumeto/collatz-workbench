#!/usr/bin/env python3
"""Local negative controls for the common additive writer; no network used."""
from pathlib import Path
import tempfile,unittest
from safe_files import apply_additions

class Checks(unittest.TestCase):
 def test_roundtrip(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);(r/'sentinel').write_text('untouched')
   data={'a/b':b'x','a/c':b'y'}
   self.assertEqual(apply_additions(r,data,apply=False)['written'],0)
   self.assertFalse((r/'a').exists())
   self.assertEqual(apply_additions(r,data,apply=True)['written'],2)
   self.assertEqual(apply_additions(r,data,apply=True)['written'],0)
   self.assertEqual((r/'sentinel').read_text(),'untouched')
 def test_preflight(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);(r/'z').write_bytes(b'original')
   with self.assertRaises(ValueError):apply_additions(r,{'a':b'x','z':b'conflict'},apply=True)
   self.assertFalse((r/'a').exists());self.assertEqual((r/'z').read_bytes(),b'original')
 def test_paths(self):
  with tempfile.TemporaryDirectory() as d:
   for p in ('../escape','/absolute','.git/config','a\\b'):
    with self.assertRaises(ValueError):apply_additions(Path(d),{p:b'x'},apply=True)
 def test_symlink(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);(r/'real').mkdir();(r/'link').symlink_to(r/'real',target_is_directory=True)
   with self.assertRaises(ValueError):apply_additions(r,{'link/a':b'x'},apply=True)

if __name__=='__main__':unittest.main()
