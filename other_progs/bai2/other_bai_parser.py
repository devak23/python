from bai2 import bai2
from bai2.models import *

with open('sample.bai2') as f:
    bai2_file = bai2.parse_from_file(f)

header = bai2_file.header
for r in bai2_file.rows:
    print(r)

print(bai2_file)