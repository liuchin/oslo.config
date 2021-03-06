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

from oslotest import base

from oslo_config import cfg


class TestConfigOpts(cfg.ConfigOpts):
    def __call__(self, args=None, default_config_files=[],
                 default_config_dirs=[]):
        return cfg.ConfigOpts.__call__(
            self,
            args=args,
            prog='test',
            version='1.0',
            usage='%(prog)s FOO BAR',
            description='somedesc',
            epilog='tepilog',
            default_config_files=default_config_files,
            default_config_dirs=default_config_dirs,
            validate_default_values=True)


class LocationTestCase(base.BaseTestCase):

    def test_user_controlled(self):
        self.assertTrue(cfg.Locations.user.is_user_controlled)

    def test_not_user_controlled(self):
        self.assertFalse(cfg.Locations.opt_default.is_user_controlled)
        self.assertFalse(cfg.Locations.set_default.is_user_controlled)
        self.assertFalse(cfg.Locations.set_override.is_user_controlled)


class GetLocationTestCase(base.BaseTestCase):

    def setUp(self):
        super(GetLocationTestCase, self).setUp()
        self.conf = TestConfigOpts()
        self.normal_opt = cfg.StrOpt(
            'normal_opt',
            default='normal_opt_default',
        )
        self.conf.register_opt(self.normal_opt)
        self.cli_opt = cfg.StrOpt(
            'cli_opt',
            default='cli_opt_default',
        )
        self.conf.register_cli_opt(self.cli_opt)

    def test_opt_default(self):
        self.conf([])
        loc = self.conf.get_location('normal_opt')
        self.assertEqual(
            cfg.Locations.opt_default,
            loc.location,
        )

    def test_set_default_on_config_opt(self):
        self.conf.set_default('normal_opt', self.id())
        self.conf([])
        loc = self.conf.get_location('normal_opt')
        self.assertEqual(
            cfg.Locations.set_default,
            loc.location,
        )

    def test_set_override(self):
        self.conf.set_override('normal_opt', self.id())
        self.conf([])
        loc = self.conf.get_location('normal_opt')
        self.assertEqual(
            cfg.Locations.set_override,
            loc.location,
        )
