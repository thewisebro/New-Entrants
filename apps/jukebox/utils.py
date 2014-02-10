"""
  For Some common fuctions, classes etc.
"""

def unique(seq, seen):
  """
    Return a generator where seq and seen are lists and return difference between these two(seq-seen) in order
  """
  seen = set(seen)
  for item in seq :
    if item not in seen :
      seen.add(item)
      yield item

