import copy
import csv
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / 'plugins/core-learning/skills/learn-core/scripts/export_anki.py'
spec = importlib.util.spec_from_file_location('export_anki', path)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.data = {'cards': [{'id': 'q-1', 'front': '为什么 x < y？\n说明',
                                'back': '不是 <script>代码</script>\t答案',
                                'source': 'https://example.org/?a=1&b=2',
                                'tags': ['数学', 'core']} ]}

    def test_chinese_multiline_and_html_safe(self):
        output = exporter.build_tsv(self.data)
        rows = list(csv.reader(io.StringIO('\n'.join(output.splitlines()[4:])), delimiter='\t'))
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(rows[0]), 3)
        self.assertEqual(rows[0][0], '为什么 x &lt; y？<br>说明')
        self.assertNotIn('<script>', rows[0][1])
        self.assertIn('a=1&amp;b=2', rows[0][1])
        self.assertIn('learning-id::q-1', rows[0][2])

    def test_duplicate_front_and_id_rejected(self):
        for field in ['id', 'front']:
            data = copy.deepcopy(self.data)
            other = copy.deepcopy(data['cards'][0])
            other.update(id='q-2', front='new')
            other[field] = data['cards'][0][field]
            data['cards'].append(other)
            with self.subTest(field=field), self.assertRaises(ValueError):
                exporter.build_tsv(data)

    def test_hash_prefixed_question_is_a_quoted_data_row(self):
        self.data['cards'][0]['front'] = '# is this a comment?'
        data_line = exporter.build_tsv(self.data).splitlines()[4]
        self.assertTrue(data_line.startswith('"#'))
        self.assertEqual(next(csv.reader([data_line], delimiter='\t'))[0], '# is this a comment?')

    def test_hardlinked_input_is_never_overwritten(self):
        import os
        with tempfile.TemporaryDirectory() as folder:
            source, destination = Path(folder) / 'input.json', Path(folder) / 'output.tsv'
            source.write_text(json.dumps(self.data), encoding='utf-8')
            original = source.read_bytes()
            try:
                os.link(source, destination)
            except OSError:
                self.skipTest('Filesystem does not permit hard links')
            with self.assertRaises(ValueError):
                exporter.export(source, destination, overwrite=True)
            self.assertEqual(source.read_bytes(), original)

    def test_invalid_cards(self):
        for field, value in [('front', ''), ('back', ' '), ('id', '../bad'),
                             ('tags', ['two words']), ('tags', 'core'),
                             ('source', 12), ('front', 'control\x00')]:
            data = copy.deepcopy(self.data)
            data['cards'][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                exporter.build_tsv(data)
        for data in [[], {}, {'cards': []}, {'cards': [None]}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                exporter.build_tsv(data)

    def test_safe_writes_bom_and_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            source, dest = Path(folder) / 'input.json', Path(folder) / 'out.tsv'
            source.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8-sig')
            exporter.export(source, dest)
            original = dest.read_bytes()
            self.assertIn('为什么'.encode(), original)
            with self.assertRaises(FileExistsError):
                exporter.export(source, dest)
            source.write_text('{}', encoding='utf-8')
            with self.assertRaises(ValueError):
                exporter.export(source, dest, overwrite=True)
            self.assertEqual(dest.read_bytes(), original)
            source.write_text(json.dumps(self.data), encoding='utf-8')
            exporter.export(source, dest, overwrite=True)
            self.assertEqual(dest.read_bytes(), original)

    def test_input_protected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'input.json'
            source.write_text(json.dumps(self.data), encoding='utf-8')
            with self.assertRaises(ValueError):
                exporter.export(source, source, overwrite=True)
            with self.assertRaises(ValueError):
                exporter.export(source, source.with_suffix('.txt'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
