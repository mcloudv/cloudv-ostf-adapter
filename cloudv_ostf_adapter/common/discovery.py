# Discovery tool for tests

import inspect
import pkgutil
import pyclbr

BASE_MODULE_NAME = 'fuel_health.tests'


class TestInspector(object):
    """Inspector for tests and suites."""

    def __init__(self, base_module_name):

        self.base_module_name = base_module_name

    def get_modules(self):
        """Get modules with tests."""
        modules = []

        for module in pkgutil.walk_packages():
            if self.base_module_name+'.' in module[1]:
                modules.append(module[1])

        return modules

    def _get_suites_and_tests(self):
        """Get suites with tests."""

        suites = []
        for module in self.get_modules():
            suite_dict = pyclbr.readmodule(module)

            for suite in suite_dict:
                tests = filter(lambda test: test.startswith('test_'),
                               suite_dict[suite].methods)

                if not tests: continue

                suites.append({'suite': '.'.join([module, suite]),
                               'tests': tests})

        return suites

    def get_suites(self):
        """Get list of suites."""

        suites = self._get_suites_and_tests()
        return [suite['suite'] for suite in suites]


    def get_tests(self):
        """Get all tests in all suites."""

        suites = self._get_suites_and_tests()
        tests = []
        for suite in suites:
            test_list = map(lambda name: ':'.join([suite['suite'], name]),
                    suite['tests'])
            tests.extend(test_list)

        return tests

