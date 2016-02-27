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

try:
    from oslo.config import cfg
except ImportError:
    from oslo_config import cfg

from cloudv_ostf_adapter import version


common_opts = [
    cfg.StrOpt("health_check_config_path",
               default='etc/cloudv_ostf_adapter/test.conf'),
    cfg.StrOpt("enabled_validation_plugins", default=['fuel_health']),
    cfg.StrOpt("nose_verbosity", default="-v")
]

cli_opts = [
    cfg.BoolOpt('no-format', short='F', default=False, required=True,
                help='Do not format the output as table'),
    cfg.BoolOpt('show-full-report', short='R', default=False, required=True,
                help='Show full report about a test (including traceback)'),
    cfg.BoolOpt('raw_format', default=False, required=True,
                help='Return results as JSON'),
    cfg.StrOpt('output-file', default='', required=False,
                help='File to store results of test running. Must be used with option --raw'),
]


rest_group = cfg.OptGroup("rest", "Cloudvalidation ReST API service options.")

rest_opts = [
    cfg.StrOpt('server_host',
               default='127.0.0.1',
               help="adapter host"),
    cfg.IntOpt('server_port',
               default=8777,
               help="Port number"),
    cfg.StrOpt('log_file',
               default='/var/log/ostf.log',
               help=""),
    cfg.StrOpt('debug',
               default=False,
               help="Debug for REST API."),
    cfg.StrOpt('jobs_dir',
               default='/var/log/ostf',
               help="Directory where jobs will be stored."),
]

rest_client_opts = [
    cfg.StrOpt("host", default=os.environ.get("MCLOUDV_HOST", "localhost")),
    cfg.IntOpt("port", default=os.environ.get("MCLOUDV_PORT", 8777)),
    cfg.StrOpt("api_version", default=os.environ.get("MCLOUDV_API", "v1"))
]

CONF = cfg.CONF
CONF.register_opts(common_opts)

CONF.register_group(rest_group)

CONF.register_opts(rest_opts, rest_group)

#client opts
CONF.register_opts(rest_client_opts)

# CLI opts
CONF.register_cli_opts(cli_opts)


def parse_args(argv, default_config_files=None):
    cfg.CONF(args=argv[1:],
             project='cloudv_ostf_adapter',
             version=version.version,
             default_config_files=default_config_files)
