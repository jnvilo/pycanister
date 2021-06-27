from __future__ import print_function
import unittest
import mock

from packageskel import PackageSkel
from tests.utilities import module_function_name


class TestPackageSkel(unittest.TestCase):
    
    @mock.patch(module_function_name(print))
    def test_should_print_hello_world(self, mock_print):
        skeleton = python_skeleton.PythonSkeleton()
        skeleton.hello()
        mock_print.assert_called_once_with('Hello world!')
