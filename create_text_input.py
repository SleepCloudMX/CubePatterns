import argparse
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit('缺少依赖 Pillow，请先安装: pip install pillow') from exc


def _to_center(value: str) -> float:
    if value in {'left', 'top'}:
        return 0.0
    if value in {'center', 'middle'}:
        return 0.5
    if value in {'right', 'bottom'}:
        return 1.0
    raise ValueError(f'不支持的对齐参数: {value}')


def image_to_binary_matrix(
    image_path: Path,
    size: int,
    threshold: int,
    invert: bool,
    fit_mode: str,
    h_align: str,
    v_align: str,
) -> list[list[bool]]:
    image = Image.open(image_path).convert('L')
    centering = (_to_center(h_align), _to_center(v_align))

    if fit_mode == 'cover':
        canvas = ImageOps.fit(image, (size, size), Image.Resampling.LANCZOS, centering=centering)
    else:
        resized = ImageOps.contain(image, (size, size), Image.Resampling.LANCZOS)
        canvas = Image.new('L', (size, size), color=255)
        x = int((size - resized.width) * centering[0])
        y = int((size - resized.height) * centering[1])
        canvas.paste(resized, (x, y))

    pixels = list(canvas.getdata())
    binary = [(pixel < threshold) for pixel in pixels]
    if invert:
        binary = [not value for value in binary]

    matrix: list[list[bool]] = []
    for row in range(size):
        start = row * size
        matrix.append(binary[start:start + size])
    return matrix


def write_input_file(path: Path, layer: int, matrix: list[list[bool]], on_char: str = '.', off_char: str = ' ') -> None:
    lines = [f'layer={layer}', 'pattern:']
    for row in matrix:
        lines.append(' '.join(on_char if cell else off_char for cell in row))
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='读取图片并生成 input.txt 图案（双色）')
    parser.add_argument('--layer', type=int, required=True, help='魔方阶数（图案网格为 layer-2）')
    parser.add_argument('--image', required=True, help='输入图片路径，例如 logo.png')
    parser.add_argument('--output', default='input.txt', help='输出文件路径（默认 input.txt）')
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
    output_path = Path(args.output)
    matrix = image_to_binary_matrix(
        image_path=image_path,
        size=size,
        threshold=args.threshold,
        invert=args.invert,
        fit_mode=args.fit,
        h_align=args.h_align,
        v_align=args.v_align,
    )
    write_input_file(output_path, args.layer, matrix)
    print(f'已生成图案文件: {output_path}')


if __name__ == '__main__':
    main()
