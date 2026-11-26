from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'skills/olah-style-paper-posts/scripts/validate.py'
spec=importlib.util.spec_from_file_location('olah_validate',src)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_resnet_article():
    assert module.validate(ROOT/'examples/resnet/index.html')['pass']

def test_transformer_article():
    assert module.validate(ROOT/'examples/transformer/index.html')['pass']

def test_banned_copy_rejected(tmp_path):
    good=(ROOT/'examples/resnet/index.html').read_text(encoding='utf-8')
    good=good.replace('</body>','<p>原创图解 · 单文件离线 HTML</p></body>')
    example=tmp_path/'test.html';example.write_text(good,encoding='utf-8')
    assert not module.validate(example)['pass']

def test_standalone_svg_assets_parse():
    from xml.etree import ElementTree as ET
    assets=list((ROOT/'examples').glob('*/assets/*.svg'))
    assert len(assets)>=20
    for path in assets:
        tree=ET.parse(path)
        root=tree.getroot()
        assert root.tag.endswith('svg')
        assert any(k.lower()=='viewbox' for k in root.attrib),path
