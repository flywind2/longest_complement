#!/usr/bin/env python

import collections
import sys

SEED=64
DIST=100
MM=0

def log(msg):
  sys.stderr.write(msg)

rev = { 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N' }
def complement(s):
  return ''.join([rev[x] for x in s])

def of_interest(s):
  if 'N' in s or s == len(s) * s[0]:
      return False
  else:
      return True

log('seeding with size {0} mismatch {1} dist {2}...\n'.format(SEED, MM, DIST))
position = 0
seeds = {}
current = ''
current_start = 0
for linenum, line in enumerate(sys.stdin):
  if line.startswith('>'):
    continue
  if linenum % 100000 == 0:
    log('read {0} lines...'.format(linenum))
  
  current += line.strip().upper()
  while position + SEED <= current_start + len(current):
    block = current[position - current_start:position - current_start + SEED]
    if of_interest(block):
      complemented = complement(block)
      if block in seeds:
        sys.stdout.write('{0} {1}:{2} {3}\n'.format(block, position, ','.join([ str(x) for x in seeds[block]]), complemented))
      if complemented in seeds:
        seeds[complemented].add(position)
      else:
        seeds[complemented] = set([position])
    position += 1
  # remove old
  current = current[position - current_start:]
  current_start = position

