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

import os
import sys

from cloudv_ostf_adapter.common import cfg
from cloudv_ostf_adapter.common import discovery
from cloudv_ostf_adapter.common import utils

from oslo_utils import importutils


CONF = cfg.CONF


class SuiteDescriptor(object):

    suite_attrs = ['test_group', 'tests']
    test_attrs = ['tests']

    def __init__(self, test_group_definition, tests):
        self.test_group = test_group_definition
        self.tests = tests

    def print_tests_description(self):
        utils.print_list(self, self.test_attrs)

    def print_description(self):
        utils.print_dict(self)


class ValidationPlugin(object):

    test_executor = "%(test_module_path)s:%(class)s.%(test)s"

    def __init__(self, name, load_tests=True):

        # TODO(albartash): load_tests becomes ambigous because
        # loading is going here anyway. We need to reinvestigate
        # requirement of using self.suites, etc in plugin when
        # load_tests = False
        self.test_inspector = discovery.TestInspector(name + '.tests')
        __suites = self.test_inspector.get_suites()

        self.name = name
        self.suites = __suites
        self._suites = self.suites
        self.tests = (self.get_tests()
                      if load_tests else [])

    def get_tests(self):
        return self.test_inspector.get_tests()

    def _collect_test(self, tests):
        test_suites_paths = []
        for test in tests:
            classpath, test_method = test.split(":")
            classname = classpath.split(".")[-1]
            module = importutils.import_class(
                classpath).__module__
            test_module_path = os.path.abspath(
                sys.modules[module].__file__)
            if test_module_path.endswith("pyc"):
                test_module_path = test_module_path[:-1]
            test_suites_paths.append(
                self.test_executor %
                {
                    'test_module_path': test_module_path,
                    'class': classname,
                    'test': test_method
                })
        return test_suites_paths

    def get_tests_by_suite(self, suite):
        tests = []
        for test in self.tests:
            if suite in test:
                tests.append(test)
        return tests

    def descriptor(self):
        return {"name": self.name,
                "suites": self.suites,
                "tests": self.tests}

    def run_suites(self):
        raise Exception("Plugin doesn't support suites execution.")

    def run_suite(self, suite):
        raise Exception("Plugin doesn't support suite execution.")

    def run_test(self, test):
        raise Exception("Plugin doesn't support test execution.")

    def run_suite_within_cli(self, suite):
        raise Exception("CLI execution is not supported.")

    def run_suites_within_cli(self):
        raise Exception("CLI execution is not supported.")

    def run_test_within_cli(self, test):
        raise Exception("CLI execution is not supported.")
