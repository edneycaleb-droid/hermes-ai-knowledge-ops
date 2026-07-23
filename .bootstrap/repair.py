import hashlib
from pathlib import Path
P=1000003
E=[(6908, 589133, 958139, '95cc60173f03d017defd1d6fe2168bf53c81d1d8c21a6aaaf38626a661d2429b'), (6908, 592780, 281810, 'bd705b1ec786429f121be4064b93458b3ee5ce65d37b11ba51a8bbbfbe20be6c'), (6908, 588668, 226644, '7715767ccda83f0e5c3b1af3ea3fb6c6f5bea7ed4b38f4327896beed25f61f6d'), (6908, 595410, 548398, '247c465f22a635fb428eef97d1567caf0997326195d3ddc0cfda2553f6e3c3b3')]
for i,(n,a,w,h) in enumerate(E):
 p=Path(f".bootstrap/payload.part{i}"); b=bytearray(p.read_bytes())
 if len(b)!=n: raise SystemExit(f"payload {i} length {len(b)} != {n}")
 if hashlib.sha256(b).hexdigest()!=h:
  da=(a-sum(b))%P
  dw=(w-sum((j+1)*v for j,v in enumerate(b)))%P
  pos=(dw*pow(da,-1,P))%P
  if not 1<=pos<=n: raise SystemExit(f"payload {i} uncorrectable")
  delta=da if da<128 else da-P
  value=b[pos-1]+delta
  if not 0<=value<128: raise SystemExit(f"payload {i} invalid correction")
  b[pos-1]=value
  if hashlib.sha256(b).hexdigest()!=h: raise SystemExit(f"payload {i} checksum failure")
  p.write_bytes(b)
for p in Path(".bootstrap").glob("payload.tail*"): p.unlink()
print("bootstrap payload verified")
