#!/usr/bin/env python
"Tests for wgm_search"

import os
import wgm_search
import wgm_search.database
import unittest

class WGMSearchTestCase(unittest.TestCase):

    def setUp(self):
        self.app = wgm_search.app.test_client()
        wgm_search.database.init_db()

    def tearDown(self):
        #wgm_search.g.close()
        os.unlink(wgm_search.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/list')
        assert 'Tut uns leid' in rv.data

if __name__ == '__main__':
    unittest.main()
