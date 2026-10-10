#!/usr/bin/env python3
"""Create reusable application ledgers without replacing existing files."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    if target.exists() and not target.is_dir():
        parser.error('目标必须是目录')
    assets = Path(__file__).resolve().parents[1] / 'assets'
    target.mkdir(parents=True, exist_ok=True)
    folders = ['00-要求与底稿', '01-定位与规划', '02-课程与代表课',
               '03-申报书', '04-说课', '05-实录', '06-证据', '07-提交包']
    for folder in folders:
        (target / folder).mkdir(exist_ok=True)
    result = {'target': str(target), 'created': [], 'preserved': []}
    for source in sorted(assets.iterdir()):
        if not source.is_file():
            continue
        dest = target / '00-要求与底稿' / source.name
        try:
            with dest.open('xb') as stream:
                stream.write(source.read_bytes())
            result['created'].append(str(dest.relative_to(target)))
        except FileExistsError:
            result['preserved'].append(str(dest.relative_to(target)))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
