import argparse
import re


def _extract_layer(line: str) -> int:
    match = re.search(r'\d+', line)
    if not match:
        raise ValueError('input.txt 第一行需要包含阶数，例如: 7 或 layer=7')
    return int(match.group(0))


def _parse_pattern_lines(lines: list[str], size: int) -> list[list[bool]]:
    matrix: list[list[bool]] = []
    for row in range(size):
        line = lines[row] if row < len(lines) else ''
        if len(line) >= size * 2 - 1:
            samples = [line[col * 2] for col in range(size)]
        else:
            padded = line.ljust(size)
            samples = [padded[col] for col in range(size)]
        matrix.append([not char.isspace() for char in samples])
    return matrix


def read_input(path: str) -> tuple[int, list[list[bool]]]:
    with open(path, 'r', encoding='utf-8') as fp:
        raw_lines = fp.read().splitlines()

    if not raw_lines:
        raise ValueError('input.txt 为空')

    header_index = None
    for idx, line in enumerate(raw_lines):
        stripped = line.strip()
        if stripped:
            header_index = idx
            break

    if header_index is None:
        raise ValueError('input.txt 中未找到阶数')

    layer = _extract_layer(raw_lines[header_index].strip())
    if layer < 3:
        raise ValueError('阶数必须 >= 3')

    size = layer - 1
    pattern_start = header_index + 1
    if pattern_start < len(raw_lines) and raw_lines[pattern_start].strip().lower() in {'pattern:', '[pattern]'}:
        pattern_start += 1

    pattern_lines = raw_lines[pattern_start:pattern_start + size]
    matrix = _parse_pattern_lines(pattern_lines, size)
    return layer, matrix


def find_runs(cells: list[bool]) -> list[list[int]]:
    cols: list[list[int]] = []
    for col_idx, active in enumerate(cells, 2):
        if not active:
            continue
        if cols and cols[-1][1] == col_idx - 1:
            cols[-1][1] = col_idx
        else:
            cols.append([col_idx, col_idx])
    return cols


def build_moves(layer: int, mid: int, row: int, cols: list[list[int]]) -> list[str]:
    moves: list[str] = []
    for left, right in cols:
        if right <= mid:
            if left == right:
                moves.append(f"{left}L'")
            else:
                moves.append(f"{right}Lw'")
                if left == 2:
                    moves.append('L')
                elif left == 3:
                    moves.append('Lw')
                else:
                    moves.append(f'{left - 1}Lw')
        else:
            left = layer - left + 1
            right = layer - right + 1
            if left == right:
                moves.append(f'{right}R')
            else:
                moves.append(f'{left}Rw')
                if right == 2:
                    moves.append("R'")
                elif right == 3:
                    moves.append("Rw'")
                else:
                    moves.append(f"{right - 1}Rw'")

    moves.append(f'{row}U')

    for left, right in cols:
        if right <= mid:
            if left == right:
                moves.append(f'{left}L')
            else:
                moves.append(f'{right}Lw')
                if left == 2:
                    moves.append("L'")
                elif left == 3:
                    moves.append("Lw'")
                else:
                    moves.append(f"{left - 1}Lw'")
        else:
            left = layer - left + 1
            right = layer - right + 1
            if left == right:
                moves.append(f"{right}R'")
            else:
                moves.append(f"{left}Rw'")
                if right == 2:
                    moves.append('R')
                elif right == 3:
                    moves.append('Rw')
                else:
                    moves.append(f'{right - 1}Rw')

    moves.append(f"{row}U'")
    return moves


def solve(input_path: str, output_path: str) -> None:
    layer, matrix = read_input(input_path)
    mid = layer // 2
    with open(output_path, 'w', encoding='utf-8') as fp:
        for row, cells in enumerate(matrix, 1):
            cols = find_runs(cells)
            if not cols:
                continue
            moves = build_moves(layer, mid, row, cols)
            fp.write(' '.join(moves) + '\n')


def main() -> None:
    parser = argparse.ArgumentParser(description='从 input.txt 读取图案，生成 output.txt 魔方公式')
    parser.add_argument('--input', default='input.txt', help='输入文件路径（默认 input.txt）')
    parser.add_argument('--output', default='output.txt', help='输出文件路径（默认 output.txt）')
    args = parser.parse_args()
    solve(args.input, args.output)
    print(f'已生成: {args.output}')


if __name__ == '__main__':
    main()
