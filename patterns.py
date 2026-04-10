# 对于 n 阶魔方, 输入内层的 (n-1)×(n-1) 的色块.
# 不需要改变的颜色用空格表示, 需要改变的颜色用任意非空白字符表示.
# 为了美观起见, 每行的每个字符间有一个空格.
pattern = """
  .   .
. . . . .
. . . . .
  . . .
    .
"""
layer = 7
mid = layer // 2
with open('output.txt', 'w') as fp:
    for row, line in enumerate(pattern.split('\n'), 1):
        cols = []
        for col, char in enumerate(line[::2], 2):
            if char == ' ':
                continue
            if cols and cols[-1][1] == col - 1:
                cols[-1][1] = col
            else:
                cols.append([col, col])
        print(cols)
        if not cols:
            continue
        moves = []
        for left, right in cols:
            if right <= mid:
                if left == right:
                    moves.append(f'{left}L\'')
                else:
                    moves.append(f'{right}Lw\'')
                    if left == 2:
                        moves.append('L')
                    elif left == 3:
                        moves.append('Lw')
                    else:
                        moves.append(f'{left-1}Lw')
            else:
                left = layer - left + 1
                right = layer - right + 1
                if left == right:
                    moves.append(f'{right}R')
                else:
                    moves.append(f'{left}Rw')
                    if right == 2:
                        moves.append('R\'')
                    elif right == 3:
                        moves.append('Rw\'')
                    else:
                        moves.append(f'{right-1}Rw\'')
        moves.append(f'{row}U')
        for left, right in cols:
            if right <= mid:
                if left == right:
                    moves.append(f'{left}L')
                else:
                    moves.append(f'{right}Lw')
                    if left == 2:
                        moves.append('L\'')
                    elif left == 3:
                        moves.append('Lw\'')
                    else:
                        moves.append(f'{left-1}Lw\'')
            else:
                left = layer - left + 1
                right = layer - right + 1
                if left == right:
                    moves.append(f'{right}R\'')
                else:
                    moves.append(f'{left}Rw\'')
                    if right == 2:
                        moves.append('R')
                    elif right == 3:
                        moves.append('Rw')
                    else:
                        moves.append(f'{right-1}Rw')
        moves.append(f'{row}U\'')
        fp.write(' '.join(moves) + '\n')
