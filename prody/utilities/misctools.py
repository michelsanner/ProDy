# ProDy: A Python Package for Protein Dynamics Analysis
# 
# Copyright (C) 2010-2012 Ahmet Bakan
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""This module defines miscellaneous utility functions."""

__author__ = 'Ahmet Bakan'
__copyright__ = 'Copyright (C) 2010-2012 Ahmet Bakan'

from textwrap import wrap as textwrap

from numpy import unique

__all__ = ['Everything', 'rangeString', 'alnum', 'importLA', 'dictElement',
           'tabulate', 'wrap']
        
class Everything(object):
    
    """Everything is here."""
    
    def __contains__(self, what):
        
        return True

def rangeString(lint, sep=' ', rng=' to ', exc=False, pos=True):
    """Return a structured string for a given list of integers.
    
    :arg lint: integer list or array
    :arg sep: range or number separator     
    :arg rng: range symbol
    :arg exc: set **True** if range symbol is exclusive
    :arg pos: only consider zero and positive integers 

    >>> from prody.utilities import rangeString
    >>> lint = [1, 2, 3, 4, 10, 15, 16, 17]
    >>> rangeString(lint) 
    '1 to 4 10 15 to 17'
    >>> rangeString(lint, sep=',', rng='-') 
    '1-4,10,15-17'
    >>> rangeString(lint, ',', ':', exc=True)
    '1:5,10,15:18'
    """
        
    ints = unique(lint)
    if pos and ints[0] < 0:
        ints = ints[ints > -1]

    prev = ints[0]
    lint = [[prev]]
    for i in ints[1:]:
        if i - prev > 1:
            lint.append([i])
        else:
            lint[-1].append(i)
        prev = i
    exc = int(exc)
    return sep.join([str(l[0]) if len(l) == 1 else 
                     str(l[0]) + rng + str(l[-1] + exc) for l in lint])

def alnum(string, alt='_'):
    """Replace non alpha numeric characters with *alt*."""
    
    result = ''
    for char in string:
        if char.isalnum():
            result += char
        else:
            result += alt
    return result


def importLA():
    """Return one of :mod:`scipy.linalg` or :mod:`numpy.linalg`."""
    
    try:
        import scipy.linalg as linalg
    except ImportError:
        try:
            import numpy.linalg as linalg
        except:
            raise ImportError('scipy.linalg or numpy.linalg is required for '
                              'NMA and structure alignment calculations')
    return linalg


def dictElement(element, prefix=None):
    """Returns a dictionary built from the children of *element*, which must be
    a :class:`xml.etree.ElementTree.Element` instance.  Keys of the dictionary
    are *tag* of children without the *prefix*, or namespace.  Values depend on
    the content of the child.  If a child does not have any children, its text 
    attribute is the value.  If a child has children, then the child is the 
    value."""
    
    dict_ = {}
    length = False
    if isinstance(prefix, str):
        length = len(prefix)
    for child in element:
        tag = child.tag
        if length and tag.startswith(prefix):
            tag = tag[length:]
        if len(child) == 0:
            dict_[tag] = child.text
        else:
            dict_[tag] = child
    return dict_


def wrap(text, width=70, join='\n'):
    """Return wrapped lines from :func:`textwrap.wrap` after *join*\ing them.
    """
    
    return join.join(textwrap(text, width))
    
def tabulate(*cols, **kwargs):
    """Return a table for columns of data. 
    
    :kwarg header: make first row a header, default is **True**
    :type header: bool
    :kwarg width: 79
    :type width: int
    :kwargs space: number of white space characters between columns,
         default is 2
    :type space: int
    
    """
    
    space = kwargs.get('space', 2)
    widths = [max(map(len, cols[0]))]
    widths.append(kwargs.get('width', 79) - sum(widths) - len(widths) * space)
    space *= ' '
    bars = (space).join(['=' * width for width in widths])
    lines = [bars]
    
    for irow, items in enumerate(zip(*cols)):
        rows = []
        map(rows.append, [textwrap(item, widths[icol]) if icol else 
                          [item.ljust(widths[icol])] 
                          for icol, item in enumerate(items)])
        maxlen = max(map(len, rows))
        if maxlen > 1:     
            for i, row in enumerate(rows):
                row.extend([' ' * widths[i]] * (maxlen - len(row)))
        for line in zip(*rows):
            lines.append(space.join(line))
        if not irow and kwargs.get('header', True):
            lines.append(bars)
    if irow > 1:
        lines.append(bars)
    return '\n'.join(lines)
