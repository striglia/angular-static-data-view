# -*- coding: utf-8 -*-
"""Tests for the main methods, including some smoke/integration tests."""
import cStringIO
import fileinput
import os.path

import mock
import simplejson

from static_html_data_view import generate_data_view
from static_html_data_view import main


@mock.patch.object(fileinput, 'input', return_value=['33\n'])
@mock.patch.object(main, 'post_generation', lambda *args, **kwargs: None)
@mock.patch.object(main, 'generate_data_view')
def test_arg_parsing(generate_data_view_mock, fileinput_mock):
    main.main(['basic', '-b'])
    ((settings,), _), = generate_data_view_mock.call_args_list
    assert settings.system_template_dir
    assert settings.template_dir
    assert settings.data == [33]


@mock.patch.object(fileinput, 'input', return_value=['33\n'])
@mock.patch.object(main, 'post_generation', lambda *args, **kwargs: None)
@mock.patch.object(generate_data_view, 'shutil')
@mock.patch.object(generate_data_view, '_write_file')
def test_generation(write_file_mock, shutil_mock, fileinput_mock):
    """
    The closest thing to a unit test right now.
    """
    main.main(['basic', '-b'])
    written_files = dict(
        (os.path.basename(filename), writer)
        for ((filename, writer), _) in write_file_mock.call_args_list
    )
    assert set(written_files.keys()) == set(['data.json', 'index.html'])
    assert all(
        call in [c[0] for c in shutil_mock.method_calls]
        for call in ['copytree', 'copy']
    )

    # hacky stuff to make sure data.json is written correctly
    stringio = cStringIO.StringIO()
    written_files['data.json'](stringio)
    data_reread = simplejson.loads(stringio.getvalue())
    assert data_reread == [33]
