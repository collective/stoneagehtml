Changelog
=========

1.0.0 (2020-01-25)
------------------

- Adding tox test environment.
  [thet]

- Python 3 support
  [reinhardt, thet]

- Ported to BeautifulSoup4.
  [ale-rt, reinhardt]


0.2.1 (2010-06-14)
------------------

- Missing 'docs' directory added. Fixes broken egg.
  [thet]


0.2 (2010-06-13)
----------------
- Updates regarding various changes in cssutils API
  [thet]

- If styles_in_tags enabled, remove the inline style tags instead of emptying
  them.
  [thet]

- Workaround for cssutils bug:
  http://code.google.com/p/cssutils/issues/detail?id=39
  Reassigning of a cssRule to a cssSheet doesn't work in python2.6 because
  cssutils tries to reassign the append and extend methods to a native python
  list.
  [thet]

- Allow wildcard css selectors
  [thet]

- Set more compactifying cssutils preferences
  [thet]

- Avoid 1 letter variable names because they cause troubles in pdb
  [thet]

0.1.5 (2008-05-20)
------------------
0.1.4 (2008-01-07)
------------------
0.1.3 (2008-01-07)
------------------
0.1.2 (2008-01-07)
------------------
0.1.1 (2008-01-07)
------------------
0.1 (2007-06-14)
----------------
- Initial releases
  [mborch]
