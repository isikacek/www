# -*- coding: utf-8 -*-
"main.py tests."
import unittest

import main

MULTI = 'cv'
main.MULTILANGUAGE_TEMPLATES = [MULTI]


class MainTest(unittest.TestCase):

    _test_paths = [
        ['', 'ero'],
        ['/', ''],
        ['//', ''],
        # ---
        ['b', '404'],
        ['/b', '404'],
        ['b/', '404'],
        ['/b/', '404'],
        # ---
        ['/bingo', 'bingo'],
        ['/bingo/', 'bingo'],
        ['one/bingo', 'one/bingo'],
        ['one/bingo/', 'one/bingo'],
        ['/one/bingo', 'one/bingo'],
        ['/one/bingo/', 'one/bingo'],
        ['one/two/three/bingo', 'one/two/three/bingo'],
        ['one/two/three/bingo/', 'one/two/three/bingo'],
        ['/one/two/three/bingo', 'one/two/three/bingo'],
        ['/one/two/three/bingo/', 'one/two/three/bingo'],
        # ---
        ['/_bingo', '404'],
        ['/_bingo/', '404'],
        ['one/_bingo', '404'],
        ['one/_bingo/', '404'],
        ['/one/_bingo', '404'],
        ['/one/_bingo/', '404'],
        ['one/two/three/_bingo', '404'],
        ['one/two/three/_bingo/', '404'],
        ['/one/two/three/_bingo', '404'],
        ['/one/two/three/_bingo/', '404'],
        # ---
        ['/cv', '_cv_hr'],
        ['/cv/', '_cv_hr'],
        ['one/cv', 'one/_cv_hr'],
        ['one/cv/', 'one/_cv_hr'],
        ['/one/cv', 'one/_cv_hr'],
        ['/one/cv/', 'one/_cv_hr'],
        ['one/two/three/cv', 'one/two/three/_cv_hr'],
        ['one/two/three/cv/', 'one/two/three/_cv_hr'],
        ['/one/two/three/cv', 'one/two/three/_cv_hr'],
        ['/one/two/three/cv/', 'one/two/three/_cv_hr'],
        # ---
        ['/_cv', '404'],
        ['/_cv/', '404'],
        ['one/_cv', '404'],
        ['one/_cv/', '404'],
        ['/one/_cv', '404'],
        ['/one/_cv/', '404'],
        ['one/two/three/_cv', '404'],
        ['one/two/three/_cv/', '404'],
        ['/one/two/three/_cv', '404'],
        ['/one/two/three/_cv/', '404']
    ]

    def test_my_path(self):
        for x in self._test_paths:
            self.assertEqual(
                main.my_router(x[0], '404', 'hr'),
                x[1],
                (x[0] + ' -> ' +  x[1]))



if __name__ == '__main__':
    unittest.main()
