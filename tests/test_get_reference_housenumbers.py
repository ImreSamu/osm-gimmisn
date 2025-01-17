#!/usr/bin/env python3
#
# Copyright (c) 2019 Miklos Vajna and contributors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""The test_get_reference_housenumbers module covers the get_reference_housenumbers module."""

import os
import unittest
import unittest.mock
import helpers
import get_reference_housenumbers


class TestMain(unittest.TestCase):
    """Tests main()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        def get_abspath(path: str) -> str:
            if os.path.isabs(path):
                return path
            return os.path.join(os.path.dirname(__file__), path)
        with unittest.mock.patch('util.get_abspath', get_abspath):
            expected = helpers.get_content(get_abspath("workdir/street-housenumbers-reference-gazdagret.lst"))

            argv = ["", "gazdagret"]
            with unittest.mock.patch('sys.argv', argv):
                get_reference_housenumbers.main()

            actual = helpers.get_content(get_abspath("workdir/street-housenumbers-reference-gazdagret.lst"))
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
