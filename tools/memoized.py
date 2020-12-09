#!/usr/bin/env python3

import collections
import functools

_DEFAULT_TRACE = False

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)



def self_check():

  baz_call = 0

  class MemoizedTest(object):
    def __init__(self):
      self.foo_call = 0
      self.bar_call = 0

    def foo(self, v):
      self.foo_call += 1
      return v

    @memoized
    def bar(self, v):
      self.bar_call += 1
      return v

  @memoized
  def baz(v):
    nonlocal baz_call
    baz_call += 1
    return v

  test = MemoizedTest()
  for v in [1, 2, 3, 3, 4, 'a', 'b', 'b', 'c', (1, 2), (3, 4), (1, 2)]:
    _ = test.foo(v)
    _ = test.bar(v)
    _ = baz(v)

  if _DEFAULT_TRACE:
    print('foo_call', test.foo_call, 'bar_call', test.bar_call,
          'baz_call', baz_call)
  assert 12 == test.foo_call
  assert 9 == test.bar_call
  assert 9 == baz_call
  if _DEFAULT_TRACE:
    print('PASS:', __file__)


if __name__ == '__main__':
  _DEFAULT_TRACE = True

self_check()
