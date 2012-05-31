# -*- coding: utf-8 -*-
#
#  SelfTest/st_common.py: Common functions for SelfTest modules
#
# Written in 2008 by Dwayne C. Litzenberger <dlitz@dlitz.net>
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================

"""Common functions for SelfTest modules"""

__revision__ = "$Id: st_common.py 4769 2010-04-09 17:53:50Z toddw $"

import unittest
import string
import binascii

class _list_testloader(unittest.TestLoader):
    suiteClass = list

def list_test_cases(class_):
    """Return a list of TestCase instances given a TestCase class

    This is useful when you have defined test* methods on your TestCase class.
    """
    return _list_testloader().loadTestsFromTestCase(class_)

def strip_whitespace(s):
    """Remove whitespace from a string"""
    table = string.maketrans(string.whitespace, " " * len(string.whitespace))
    s = s.translate(table).replace(" ", "")
    return s

def a2b_hex(s):
    """Convert hexadecimal to binary, ignoring whitespace"""
    return binascii.a2b_hex(strip_whitespace(s))

def b2a_hex(s):
    """Convert binary to hexadecimal"""
    # For completeness
    return binascii.b2a_hex(s)

# vim:set ts=4 sw=4 sts=4 expandtab: