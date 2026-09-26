# -*- coding: utf-8 -*-
"""BBDownNext 命令兼容回归测试."""
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.services import bili_dl


class FakeProc:
    def __init__(self, returncode=0, output=''):
        self.returncode = returncode
        self._output = output
        self.killed = False

    def communicate(self, timeout=None):
        return self._output, None

    def kill(self):
        self.killed = True
        self.returncode = 1

    def poll(self):
        return self.returncode


class BBDownInvocationTests(unittest.TestCase):
    def test_cookie_uses_long_option_not_config_short_option(self):
        cmd = bili_dl.build_bbdown_cmd(
            'BBDown', '123', '/tmp/out',
            'SESSDATA=abc; bili_jct=def',
        )
        self.assertIn('--cookie', cmd)
        self.assertNotIn('-c', cmd)
        self.assertEqual(cmd[cmd.index('--cookie') + 1], 'SESSDATA=abc; bili_jct=def')
        self.assertIn('--work-dir', cmd)
        self.assertIn('-F', cmd)
        self.assertEqual(cmd[cmd.index('-p') + 1], 'all')
        self.assertNotIn('--allow-preview', cmd)

    def test_preview_exit_code_is_not_marked_success(self):
        fake = FakeProc(2, 'charging preview detected')
        captured = {}

        def fake_popen(cmd, **kwargs):
            captured['cmd'] = cmd
            return fake

        with tempfile.TemporaryDirectory() as d:
            with patch.object(bili_dl, 'find_bbdown', return_value='BBDown'):
                with patch.object(bili_dl.subprocess, 'Popen', side_effect=fake_popen):
                    ok, err = bili_dl.download_one(
                        '123', d, cookie='SESSDATA=abc; bili_jct=def'
                    )

        self.assertFalse(ok)
        self.assertIn('充电权限不足', err)
        self.assertIn('--cookie', captured['cmd'])
        self.assertNotIn('-c', captured['cmd'])

    def test_normal_exit_zero_is_success(self):
        fake = FakeProc(0, 'done')
        with tempfile.TemporaryDirectory() as d:
            with patch.object(bili_dl, 'find_bbdown', return_value='BBDown'):
                with patch.object(bili_dl.subprocess, 'Popen', return_value=fake):
                    ok, err = bili_dl.download_one('123', d, cookie=None)
        self.assertTrue(ok)
        self.assertIsNone(err)


if __name__ == '__main__':
    unittest.main()
