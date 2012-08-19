#!/usr/bin/env python3

import unittest

from game.rect import Rect

class TestRect(unittest.TestCase):

    def test_attr(self):
        a = Rect(1, 2, 3, 4)
        self.assertEqual(a.x, 1)
        self.assertEqual(a.y, 2)
        self.assertEqual(a.width, 3)
        self.assertEqual(a.height, 4)

    def test_setattr(self):
        a = Rect(1, 2, 3, 4)
        a.x = 3
        self.assertEqual(a.x, 3)
        a.y = 8
        self.assertEqual(a.y, 8)
        a.width = 4
        self.assertEqual(a.width, 4)
        a.height = 10
        self.assertEqual(a.height, 10)

    def test_prop(self):
        a = Rect(1, 2, 3, 4)
        self.assertEqual(a.top, 6)
        self.assertEqual(a.bottom, 2)
        self.assertEqual(a.left, 1)
        self.assertEqual(a.right, 4)
        self.assertEqual(a.size, (3, 4))
        self.assertEqual(a.centerx, 2)
        self.assertEqual(a.centery, 4)
        self.assertEqual(a.center, (2, 4))

    def test_setprop(self):

        a = Rect(1, 2, 3, 4)
        a.top = 3
        self.assertEqual(a.y, -1)
        a.bottom = 1
        self.assertEqual(a.y, 1)
        a.left = 3
        self.assertEqual(a.x, 3)
        a.right = 10
        self.assertEqual(a.x, 7)
        self.assertEqual(a.width, 3)
        self.assertEqual(a.height, 4)

        a.size = (4, 4)
        self.assertEqual(a.width, 4)
        self.assertEqual(a.height, 4)

        a = Rect(1, 2, 3, 4)
        a.centerx = 3
        self.assertEqual(a.x, 2)
        self.assertEqual(a.centerx, 3)
        a.centery = 5
        self.assertEqual(a.y, 3)
        self.assertEqual(a.centery, 5)

        a.center = (5, 6)
        self.assertEqual(a.x, 4)
        self.assertEqual(a.y, 4)
        self.assertEqual(a.center, (5, 6))
        self.assertEqual(a.width, 3)
        self.assertEqual(a.height, 4)

    def test_eq(self):
        a = Rect(1, 2, 3, 4)
        b = Rect(1, 2, 3, 4)
        self.assertTrue(a == b)

    def test_copy(self):
        a = Rect(1, 2, 3, 4)
        b = a.copy()
        self.assertIsNot(a, b)
        self.assertTrue(a == b)

if __name__ == "__main__":
    unittest.main()
