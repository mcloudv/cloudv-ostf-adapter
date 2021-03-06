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

from cloudv_ostf_adapter.common.logger import LOG
from oslo_utils import importutils


class Test(object):
    """Test description class."""

    def safe_import(self):
        """Performs safe import on demand of test class"""

        try:
            importutils.import_class(self._test_class)
        except ImportError:
            LOG.error("Cannot import test class: '%s'. "
                      "It is not installed." % self._test_class)

    def __init__(self, test_class):
        self._test_class = test_class
        self._test_caption = test_class

        self._duration = None
        self._report = None
        self._result = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @property
    def description(self):
        return {'test': self._test_caption,
                'report': self.report,
                'result': self.result,
                'duration': self.duration}

    def as_json(self):
        return {'test': self._test_caption,
                'suite': self._test_class,
                'report': self.report,
                'result': self.result,
                'duration': self.duration}

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def name(self):
        return self._test_caption

    @name.setter
    def name(self, name):
        self._test_caption = name

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, report):
        self._report = report
