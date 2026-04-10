import argparse
from pathlib import Path

from create_text_input import image_to_binary_matrix, write_input_file
from patterns import solve


def main() -> None:
    parser = argparse.ArgumentParser(description='读取图片并生成 input.txt 图案（双色）')
    parser.add_argument('--layer', type=int, required=True, help='魔方阶数（图案网格为 layer-2）')
    parser.add_argument('--image', required=True, help='输入图片路径，例如 logo.png')
    parser.add_argument('--pattern', default='temp/pattern.txt', help='输出文件路径（默认 pattern.txt）')
    parser.add_argument('--alg', default='temp/alg.txt', help='公式输出文件路径（默认 alg.txt）')
    parser.add_argument('--desc', type=str, default='temp/desc.txt', help='描述文件路径（默认 desc.txt）')
    parser.add_argument('--url', type=str, default='url.txt', help='链接文件路径（默认 url.txt）')
    parser.add_argument('--threshold', type=int, default=128, help='二值化阈值 0-255（默认 128）')
    parser.add_argument('--invert', action='store_true', help='反相：黑白互换')
    parser.add_argument('--fit', choices=['contain', 'cover'], default='contain', help='缩放策略')
    parser.add_argument('--h-align', choices=['left', 'center', 'right'], default='center', help='水平对齐')
    parser.add_argument('--v-align', choices=['top', 'center', 'bottom'], default='center', help='垂直对齐')
    args = parser.parse_args()

    if args.layer < 3:
        raise ValueError('layer 必须 >= 3')
    if not 0 <= args.threshold <= 255:
        raise ValueError('threshold 必须在 0~255 之间')

    size = args.layer - 2
    image_path = Path(args.image)
    pattern_path = Path(args.pattern)
    pattern_path.parent.mkdir(parents=True, exist_ok=True)
    matrix = image_to_binary_matrix(
        image_path=image_path,
        size=size,
        threshold=args.threshold,
        invert=args.invert,
        fit_mode=args.fit,
        h_align=args.h_align,
        v_align=args.v_align,
    )
    write_input_file(pattern_path, args.layer, matrix)
    print(f'已生成图案文件: {pattern_path}')

    alg_path = Path(args.alg)
    alg_path.parent.mkdir(parents=True, exist_ok=True)
    solve(str(pattern_path), str(alg_path))
    print(f'已生成公式文件: {alg_path}')

    print('desc:')
    n = args.layer
    s = ' '.join(f"f {2*i/n-1}" for i in range((n + 1) // 2, n))    # 适用于奇数阶和偶数阶
    desc_path = Path(args.desc)
    desc_path.parent.mkdir(parents=True, exist_ok=True)
    with open(desc_path, 'w', encoding='utf-8') as fp:
        fp.write(f"c {s}\n")
    print(f'已生成描述文件: {args.desc}')

    with open(args.url, 'w', encoding='utf-8') as fp:
        with open(alg_path, 'r', encoding='utf-8') as alg_fp:
            alg = alg_fp.read().strip().replace('\n', '%0A').replace(' ', '+').replace("'", "%27")
        with open(desc_path, 'r', encoding='utf-8') as desc_fp:
            desc = desc_fp.read().strip().replace(' ', '+')
        url = f"https://alpha.twizzle.net/explore/?puzzle-description={desc}&alg={alg}"
        fp.write(url)
    print(f'已生成链接文件: {args.url}')

    html = f'''<meta http-equiv="refresh" content="0;url={url}">
    <a href="{url}"></a>'''
    with open(f"twizzle.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == '__main__':
    main()
