import os
import json
import pytest
from src.prepend_title_cell import add_ipynb_title

def test_prepend_title(tmpdir):
    add_ipynb_title('test_title', 'tests/fixtures/ipynb_test.ipynb', f'{tmpdir}/out.ipynb')
    with open(tmpdir.join('out.ipynb')) as f:
        assert json.load(f).get('cells')[0].get('source') == ['test_title']

def test_template_overwrite(tmpdir):
    with pytest.raises(ValueError):
        add_ipynb_title('test_title', 'tests/fixtures/ipynb_test.ipynb', f'{tmpdir}/Metrics Template.ipynb')
        assert ValueError('Master Template overwrite is not permitted. Choose another output filepath') 
