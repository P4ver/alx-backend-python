#!/usr/bin/env python3
""" test utils,"""
import unittest
from unittest.mock import patch
import requests
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized, parameterized_class


class TestAccessNestedMap(unittest.TestCase):
    """ Access nested map,"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path_map, result_expec):
        """ Access nested method,"""
        self.assertEqual(access_nested_map(nested_map, path_map), result_expec)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path_map):
        """ Exception access nested method,"""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path_map)

        self.assertEqual(
            f'KeyError({str(error.exception)})', repr(error.exception))


class TestGetJson(unittest.TestCase):
    """ test JSON """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """ mock HTTP call,"""
        with patch('requests.get') as mock_req:
            mock_req.return_value.json.return_value = test_payld
            self.assertEqual(get_json(url=test_url), test_payld)


class TestMemoize(unittest.TestCase):
    """ test Class to memoize,"""

    def test_memoize(self):
        """ test memoize, """
        class TestClass:
            """ Test Class, """

            def a_method(self):
                """method """
                return 42

            @memoize
            def a_property(self):
                """ Decrator, """
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mck:
            test_clss = TestClass()
            test_clss.a_property()
            test_clss.a_property()
            mck.assert_called_once()
