import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing, eventtesting

from Testing import ZopeTestCase as ztc

from jyu.rsslisting.tests import base

# import interlude # for interactive console with ``>>> interact(locals())``

def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='jyu.rsslisting',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.IGNORE_EXCEPTION_DETAIL |
                        doctest.NORMALIZE_WHITESPACE |
                        doctest.ELLIPSIS,
#            globs=dict(interact=interlude.interact,),
            ),
        ])

# For more options (e.g. doctest.REPORT_ONLY_FIRST_FAILURE), see:
# http://docs.python.org/library/doctest.html#doctest-options

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
