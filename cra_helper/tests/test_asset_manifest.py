import os
import logging
from unittest.mock import MagicMock, patch, mock_open

from django.test import TestCase
from django.conf import settings

import cra_helper
from cra_helper import asset_manifest

# Quiet down logging
logging.disable(logging.CRITICAL)

server_url = 'http://foo.bar:9999'

# The originally-supported version of the asset manifest, used through react-scripts v2.1.8
open_mock_v2 = mock_open(
    read_data='''{
        "main.css": "/static/css/main.80e572c9.chunk.css",
        "main.js": "/static/js/main.ef0788cc.chunk.js",
        "main.js.map": "/static/js/main.ef0788cc.chunk.js.map",
        "runtime~main.js": "/static/js/runtime~main.a8a9905a.js",
        "runtime~main.js.map": "/static/js/runtime~main.a8a9905a.js.map",
        "static/js/2.597565cd.chunk.js": "/static/js/2.597565cd.chunk.js",
        "static/js/2.597565cd.chunk.js.map": "/static/js/2.597565cd.chunk.js.map",
        "index.html": "/index.html",
        "precache-manifest.06aece505f403b62363ab3795d4669de.js": "/precache-manifest.06aece505f403b62363ab3795d4669de.js",
        "service-worker.js": "/service-worker.js",
        "static/css/main.80e572c9.chunk.css.map": "/static/css/main.80e572c9.chunk.css.map",
        "static/media/logo.svg": "/static/media/logo.25bf045c.svg"
    }'''
)

# A newer version of the asset manifest used in react-scripts v3.0.0 till v3.2.0
open_mock_v3_1_2 = mock_open(
    read_data='''{
        "files": {
            "main.css": "/static/css/main.b100e6da.chunk.css",
            "main.js": "/static/js/main.5745ba44.chunk.js",
            "main.js.map": "/static/js/main.5745ba44.chunk.js.map",
            "runtime-main.js": "/static/js/runtime-main.e5179790.js",
            "runtime-main.js.map": "/static/js/runtime-main.e5179790.js.map",
            "static/js/2.24ceb05b.chunk.js": "/static/js/2.24ceb05b.chunk.js",
            "static/js/2.24ceb05b.chunk.js.map": "/static/js/2.24ceb05b.chunk.js.map",
            "index.html": "/index.html",
            "precache-manifest.ed3a557b9335d6efb0f3f61d4c8baa40.js": "/precache-manifest.ed3a557b9335d6efb0f3f61d4c8baa40.js",
            "service-worker.js": "/service-worker.js",
            "static/css/main.b100e6da.chunk.css.map": "/static/css/main.b100e6da.chunk.css.map",
            "static/media/logo.svg": "/static/media/logo.25bf045c.svg"
        }
    }'''
)

# A newer version of the asset manifest used in react-scripts v3.2+
open_mock_v_3_2_0 = mock_open(
    read_data='''{
        "files": {
            "main.css": "/static/css/main.b100e6da.chunk.css",
            "main.js": "/static/js/main.f245946a.chunk.js",
            "main.js.map": "/static/js/main.f245946a.chunk.js.map",
            "runtime-main.js": "/static/js/runtime-main.7b0131e1.js",
            "runtime-main.js.map": "/static/js/runtime-main.7b0131e1.js.map",
            "static/js/2.7059510f.chunk.js": "/static/js/2.7059510f.chunk.js",
            "static/js/2.7059510f.chunk.js.map": "/static/js/2.7059510f.chunk.js.map",
            "index.html": "/index.html",
            "precache-manifest.68f3de19261ab9bb69c0c6a58c46215e.js": "/precache-manifest.68f3de19261ab9bb69c0c6a58c46215e.js",
            "service-worker.js": "/service-worker.js",
            "static/css/main.b100e6da.chunk.css.map": "/static/css/main.b100e6da.chunk.css.map",
            "static/media/logo.svg": "/static/media/logo.25bf045c.svg"
        },
        "entrypoints": [
            "static/js/runtime-main.7b0131e1.js",
            "static/js/2.7059510f.chunk.js",
            "static/css/main.b100e6da.chunk.css",
            "static/js/main.f245946a.chunk.js"
        ]
    }'''
)

# Build output from a CRA project with `"homepage": "/frontend"` set in package.json
open_mock_v3_4_0_homepage = mock_open(
    read_data='''{
        "files": {
            "main.css": "/frontend/static/css/main.d1b05096.chunk.css",
            "main.js": "/frontend/static/js/main.86964f0e.chunk.js",
            "main.js.map": "/frontend/static/js/main.86964f0e.chunk.js.map",
            "runtime-main.js": "/frontend/static/js/runtime-main.d13328da.js",
            "runtime-main.js.map": "/frontend/static/js/runtime-main.d13328da.js.map",
            "static/js/2.95e01bf1.chunk.js": "/frontend/static/js/2.95e01bf1.chunk.js",
            "static/js/2.95e01bf1.chunk.js.map": "/frontend/static/js/2.95e01bf1.chunk.js.map",
            "index.html": "/frontend/index.html",
            "precache-manifest.9548cd4af84bd065cd70d970ca469612.js": "/frontend/precache-manifest.9548cd4af84bd065cd70d970ca469612.js",
            "service-worker.js": "/frontend/service-worker.js",
            "static/css/main.d1b05096.chunk.css.map": "/frontend/static/css/main.d1b05096.chunk.css.map",
            "static/js/2.95e01bf1.chunk.js.LICENSE.txt": "/frontend/static/js/2.95e01bf1.chunk.js.LICENSE.txt",
            "static/media/logo.svg": "/frontend/static/media/logo.5d5d9eef.svg"
        },
        "entrypoints": [
            "static/js/runtime-main.d13328da.js",
            "static/js/2.95e01bf1.chunk.js",
            "static/css/main.d1b05096.chunk.css",
            "static/js/main.86964f0e.chunk.js"
        ]
    }'''
)


class TestGenerateManifest(TestCase):
    def test_returns_dict(self):
        self.assertIsInstance(asset_manifest.generate_manifest('', ''), dict)

    @patch('cra_helper.asset_manifest.hosted_by_liveserver', return_value=True)
    def test_returns_bundle_url_if_cra_is_running(self, mock_hosted_check):
        with mock_hosted_check:
            self.assertEqual(asset_manifest.generate_manifest(server_url, ''), {
                'bundle_js': [
                    'http://foo.bar:9999/static/js/bundle.js',
                    'http://foo.bar:9999/static/js/0.chunk.js',
                    'http://foo.bar:9999/static/js/1.chunk.js',
                    'http://foo.bar:9999/static/js/vendors~main.chunk.js',
                    'http://foo.bar:9999/static/js/main.chunk.js'
                ]
            })

    def test_returns_manifest_paths_when_cra_is_not_running(self):
        with patch('builtins.open', open_mock_v2):
            self.assertEqual(asset_manifest.generate_manifest(server_url, '.'), {
                'main_css': 'css/main.80e572c9.chunk.css',
                'main_js': 'js/main.ef0788cc.chunk.js',
                'main_js_map': 'js/main.ef0788cc.chunk.js.map',
                'runtime_main_js': 'js/runtime~main.a8a9905a.js',
                'runtime_main_js_map': 'js/runtime~main.a8a9905a.js.map',
                'static_css_main_80e572c9_chunk_css_map': 'css/main.80e572c9.chunk.css.map',
                'static_js_2_597565cd_chunk_js': 'js/2.597565cd.chunk.js',
                'static_js_2_597565cd_chunk_js_map': 'js/2.597565cd.chunk.js.map',
                'static_media_logo_svg': 'media/logo.25bf045c.svg'
            })

    def test_checks_static_root_when_manifest_missing_from_cra_build_dir(self):
        # Pretend this folder is STATIC_ROOT to emulate falling back and accessing the
        # collected asset-manifest.json
        _here_path = os.path.dirname(os.path.realpath(__file__))
        setattr(settings, 'BASE_DIR', _here_path)
        setattr(settings, 'STATIC_ROOT', os.path.join(_here_path, 'static'))
        self.assertEqual(asset_manifest.generate_manifest(server_url, 'not_a_real_dir'), {
            'main_js': 'js/main.1234.js',
            'main_css': 'css/main.1234.css',
        })

    def test_returns_empty_dict_if_file_not_found(self):
        open_mock = MagicMock(side_effect=Exception)
        with patch('builtins.open', open_mock):
            self.assertEqual(asset_manifest.generate_manifest(server_url, '.'), {})

    def test_handles_manifest_v_3_1_2(self):
        with patch('builtins.open', open_mock_v3_1_2):
            self.assertEqual(asset_manifest.generate_manifest(server_url, '.'), {
                'main_css': 'css/main.b100e6da.chunk.css',
                'main_js': 'js/main.5745ba44.chunk.js',
                'main_js_map': 'js/main.5745ba44.chunk.js.map',
                'runtime_main_js': 'js/runtime-main.e5179790.js',
                'runtime_main_js_map': 'js/runtime-main.e5179790.js.map',
                'static_css_main_b100e6da_chunk_css_map': 'css/main.b100e6da.chunk.css.map',
                'static_js_2_24ceb05b_chunk_js': 'js/2.24ceb05b.chunk.js',
                'static_js_2_24ceb05b_chunk_js_map': 'js/2.24ceb05b.chunk.js.map',
                'static_media_logo_svg': 'media/logo.25bf045c.svg'
            })

    def test_handles_manifest_v_3_2_0(self):
        self.maxDiff = None
        with patch('builtins.open', open_mock_v_3_2_0):
            self.assertEqual(asset_manifest.generate_manifest(server_url, '.'), {
                'main_css': 'css/main.b100e6da.chunk.css',
                'main_js': 'js/main.f245946a.chunk.js',
                'main_js_map': 'js/main.f245946a.chunk.js.map',
                'runtime_main_js': 'js/runtime-main.7b0131e1.js',
                'runtime_main_js_map': 'js/runtime-main.7b0131e1.js.map',
                'static_css_main_b100e6da_chunk_css_map': 'css/main.b100e6da.chunk.css.map',
                'static_js_2_7059510f_chunk_js': 'js/2.7059510f.chunk.js',
                'static_js_2_7059510f_chunk_js_map': 'js/2.7059510f.chunk.js.map',
                'static_media_logo_svg': 'media/logo.25bf045c.svg',
                'entrypoints': {
                    'css': [
                        'css/main.b100e6da.chunk.css'
                    ],
                    'js': [
                        'js/runtime-main.7b0131e1.js',
                        'js/2.7059510f.chunk.js',
                        'js/main.f245946a.chunk.js'
                    ]
                }
            })

    def test_handles_manifest_v_3_4_0_homepage(self):
        self.maxDiff = None
        with patch('builtins.open', open_mock_v3_4_0_homepage):
            self.assertEqual(asset_manifest.generate_manifest(server_url, '.'), {
                'main_css': 'css/main.d1b05096.chunk.css',
                'main_js': 'js/main.86964f0e.chunk.js',
                'main_js_map': 'js/main.86964f0e.chunk.js.map',
                'runtime_main_js': 'js/runtime-main.d13328da.js',
                'runtime_main_js_map': 'js/runtime-main.d13328da.js.map',
                'static_css_main_d1b05096_chunk_css_map': 'css/main.d1b05096.chunk.css.map',
                'static_js_2_95e01bf1_chunk_js': 'js/2.95e01bf1.chunk.js',
                'static_js_2_95e01bf1_chunk_js_map': 'js/2.95e01bf1.chunk.js.map',
                'static_js_2_95e01bf1_chunk_js_LICENSE_txt': 'js/2.95e01bf1.chunk.js.LICENSE.txt',
                'static_media_logo_svg': 'media/logo.5d5d9eef.svg',
                'entrypoints': {
                    'css': [
                        'css/main.d1b05096.chunk.css'
                    ],
                    'js': [
                        'js/runtime-main.d13328da.js',
                        'js/2.95e01bf1.chunk.js',
                        'js/main.86964f0e.chunk.js'
                    ]
                }
            })
