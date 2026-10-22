import re,unittest
from pathlib import Path
EXPECTED=['kopia/kopia:0.22.3@sha256:4dcc208c1b191770bf4d0854f8deec06b4a16b35be4b63abdcfa9755cee7960e']
PINS=[['kopia/kopia:0.22.3', '4dcc208c1b191770bf4d0854f8deec06b4a16b35be4b63abdcfa9755cee7960e']]
def accept(ref,base,digest):
 if not re.fullmatch('[0-9a-f]{64}',digest) or ref!=base+'@sha256:'+digest:raise ValueError('mutable or unreviewed source reference')
class ImmutableRuntimeSource(unittest.TestCase):
 def test_actual_source_image_list(self):
  refs=re.findall(r'(?m)^\s*image:\s*["\']?([^"\'\s#]+)',(Path(__file__).parents[1]/'stack.runtime.yaml').read_text())
  self.assertEqual(EXPECTED,refs)
  for base,digest in PINS:accept(base+'@sha256:'+digest,base,digest)
 def test_floating_rejected(self):
  for base,digest in PINS:
   with self.subTest(base=base),self.assertRaises(ValueError):accept(base.rsplit(':',1)[0]+':latest',base,digest)
 def test_version_only_rejected(self):
  for base,digest in PINS:
   with self.subTest(base=base),self.assertRaises(ValueError):accept(base,base,digest)
 def test_malformed_digest_rejected(self):
  for base,digest in PINS:
   for bad in ['a'*63,'g'*64,'A'*64,'a'*65,'']:
    with self.subTest(base=base,bad=bad),self.assertRaises(ValueError):accept(base+'@sha256:'+bad,base,digest)
 def test_wrong_digest_rejected(self):
  for base,digest in PINS:
   with self.subTest(base=base),self.assertRaises(ValueError):accept(base+'@sha256:'+'0'*64,base,digest)
if __name__=='__main__':unittest.main()
