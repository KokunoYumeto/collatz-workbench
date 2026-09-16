#!/usr/bin/env python3
"""Regenerate the corrected reader from its preserved Markdown sources.

Requires Pandoc. Compile latex/main.tex twice with XeLaTeX afterward.
Reader repairs affect presentation input only, never the Markdown files.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
root = parser.parse_args().root.resolve()
tex = root / 'latex'
chap = tex / 'chapters'
chap.mkdir(parents=True, exist_ok=True)
source_rows = json.loads((tex / 'SOURCE_MAP_INPUT.json').read_text(encoding='utf-8'))
repairs = json.loads((tex / 'READER_REPAIRS.json').read_text(encoding='utf-8'))
fmt = 'markdown+tex_math_single_backslash+tex_math_dollars+raw_tex-auto_identifiers-superscript-subscript'
records, inputs, changes = [], [], []

def math_inventory(obj):
    result = []
    def walk(x):
        if isinstance(x, list):
            for y in x:
                walk(y)
        elif isinstance(x, dict):
            if x.get('t') == 'Math':
                result.append({'kind': x['c'][0]['t'], 'text': x['c'][1]})
            for y in x.values():
                walk(y)
    walk(obj)
    return result

for row in source_rows:
    source = root / row['source']
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != row['source_sha256']:
        raise ValueError('Source identity changed: ' + row['source'])
    text = raw.decode('utf-8').replace('\r\n', '\n')
    for repair in repairs:
        if repair['source'] == row['source']:
            count = text.count(repair['from'])
            if count != repair.get('count', 1):
                raise ValueError(('Repair count changed', row['source'], repair['from'], count))
            text = text.replace(repair['from'], repair['to'])
            changes.append({**repair, 'applied_count': count})
    ast = json.loads(subprocess.check_output(['pandoc', '-f', fmt, '-t', 'json'], input=text.encode('utf-8')))
    math = math_inventory(ast)
    def walk(obj):
        if isinstance(obj, list):
            return [walk(x) for x in obj]
        if not isinstance(obj, dict):
            return obj
        if obj.get('t') in ('Superscript', 'Subscript'):
            raise ValueError('Unexpected prose super/subscript node')
        if obj.get('t') == 'Str' and len(obj.get('c', '')) > 23 and any(c.isdigit() for c in obj['c']) and not any(c in obj['c'] for c in '{}\\'):
            return {'t':'RawInline', 'c':['latex', r'\nolinkurl{' + obj['c'] + '}']}
        if obj.get('t') == 'Str' and obj.get('c','').startswith(('https://','http://')):
            return {'t':'RawInline', 'c':['latex', r'\url{' + obj['c'] + '}']}
        if obj.get('t') == 'Code' and '{' not in obj['c'][1] and '}' not in obj['c'][1]:
            return {'t':'RawInline', 'c':['latex', r'\nolinkurl{' + obj['c'][1] + '}']}
        if obj.get('t') == 'Math':
            kind, content = obj['c']
            if kind['t'] == 'DisplayMath':
                tags = re.findall(r'\\tag\*?\{([^{}]*)\}', content)
                if len(tags) > 1:
                    raise ValueError('Multiple equation tags')
                body = re.sub(r'\\tag\*?\{[^{}]*\}', '', content)
                body = re.sub(r'\n\s*\n', '\n', body).strip()
                return {'t':'RawInline', 'c':['latex', '\\SourceMath{' + body + '}{' + (tags[0] if tags else '') + '}']}
        return {k:walk(v) for k,v in obj.items()}
    ast = walk(ast)
    out = subprocess.check_output(['pandoc', '-f', 'json', '-t', 'latex', '--top-level-division=chapter', '--syntax-highlighting=none'], input=json.dumps(ast).encode('utf-8')).decode('utf-8')
    out = out.replace(r'\mathbb Q\otimes_\mathbb ZQ', r'\mathbb Q\otimes_{\mathbb Z}Q')
    out = out.replace('\\begin{verbatim}', '\\begin{Verbatim}[breaklines=true,breakanywhere=true,fontsize=\\scriptsize]').replace('\\end{verbatim}', '\\end{Verbatim}')
    title_end = out.find('\n')
    if out.startswith('\\chapter{'):
        depth, j = 1, len('\\chapter{')
        while depth:
            if out[j] == '{' and out[j-1] != '\\':
                depth += 1
            if out[j] == '}' and out[j-1] != '\\':
                depth -= 1
            j += 1
        title_end = j
    provenance = '\n{\\small\\sffamily Source: \\nolinkurl{' + row['source'] + '}.\\par}\n'
    out = out[:title_end+1] + provenance + out[title_end+1:]
    target = tex / row['latex']
    target.write_text(out, encoding='utf-8', newline='\n')
    target.with_suffix('.math.json').write_text(json.dumps(math, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    records.append({**row, 'math_tokens':len(math), 'display_math_tokens':sum(m['kind']=='DisplayMath' for m in math), 'reader_format':fmt})
    inputs.append('\\input{' + row['latex'] + '}')
(tex / 'SOURCE_MAP.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
front = (tex / 'FRONT_MATTER.tex').read_text(encoding='utf-8')
(tex / 'main.tex').write_text(front + '\n'.join(inputs) + '\n\\end{document}\n', encoding='utf-8', newline='\n')
(tex / 'CONVERSION_RECEIPT.json').write_text(json.dumps({'format':fmt, 'chapters':len(records), 'math_tokens':sum(r['math_tokens'] for r in records), 'reader_repairs':changes, 'original_markdown_rewritten_by_converter':False, 'superscript_subscript_markdown_disabled':True}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps({'chapters':len(records), 'math_tokens':sum(r['math_tokens'] for r in records), 'reader_repairs':len(changes)}))
