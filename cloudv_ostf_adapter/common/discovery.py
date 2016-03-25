#    Copyright 2015 Mirantis, Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pkgutil
import pyclbr

BASE_MODULE_NAME = 'fuel_health.tests'


class TestInspector(object):
    """Inspector for tests and suites."""

    def __init__(self, base_module_name):

        self.base_module_name = base_module_name
        self.modules = self._get_modules()
        self.suites = self._get_suites_and_tests()

    def _get_modules(self):
        """Get modules with tests on init."""
        modules = []

        # TODO(albartash): create a better function for onerror,
        # as we need to pass this info into log
        for module in pkgutil.walk_packages(onerror=lambda e: True):
            if self.base_module_name + '.' in module[1]:
                modules.append(module[1])

        return modules

    def _get_suites_and_tests(self):
        """Get suites with tests on init."""

        suites = []
        for module in self.get_modules():
            suite_dict = pyclbr.readmodule(module)

            for suite in suite_dict:
                tests = filter(lambda test: test.startswith('test_'),
                               suite_dict[suite].methods)

                if not tests:
                    continue

                suites.append({'suite': '.'.join([module, suite]),
                               'tests': tests})
        return suites

    def get_modules(self):
        """Get list of modules."""
        return self.modules

    def get_suites(self):
        """Get list of suites."""

        return [suite['suite'] for suite in self.suites]

    def get_tests(self):
        """Get all tests in all suites."""

        tests = []
        for suite in self.suites:
            test_list = map(lambda name: ':'.join([suite['suite'], name]),
                            suite['tests'])
            tests.extend(test_list)

        return tests
