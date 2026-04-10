# 魔方图案求解器 (Rubik's Cube Pattern Solver)

一个十分莫名其妙的诡异小项目，将任意图片转换为魔方目标图案，并生成对应的公式。

65% 的代码和 99% 的 readme 由 ai 撰写，总而言之，非常莫名其妙。

## 📋 项目简介

本项目可以：
1. **读取图片** (PNG、JPG 等) 并转为二值化图案
2. **生成图案文件** (.txt 格式，魔方中心块可识别的布局)
3. **计算求解公式** (每个面都拼出指定图案的魔方公式)
4. **支持灵活的参数调整** (缩放、对齐、二值化阈值等)

特别适合：生成魔方贴纸图案、创意魔方设计、图片艺术化等场景。

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pillow
```

### 2. 一键转换 (推荐)

将图片 `logo.png` 转为 7 阶魔方图案并生成公式：

```bash
python main.py --layer 7 --image logo.png
```

**输出文件：**
- `pattern.txt` - 二值阵列图案
- `alg.txt` - 魔方求解公式

### 3. 使用 Windows 批处理

编辑 `run.bat` 中的参数后直接运行：

```bat
run.bat
```

---

## 📖 使用指南

### 方案 A: 完整流程 (`main.py`) ⭐ 推荐

从图片直接生成公式：

```bash
python main.py --layer 7 --image photo.jpg
```

**所有参数：**
```
--layer LAYER              魔方阶数 (≥3，默认无)
--image IMAGE              输入图片路径 (必需)
--pattern PATTERN          输出图案文件 (默认 pattern.txt)
--alg ALG                  输出公式文件 (默认 alg.txt)
--desc DESC                输出描述文件 (默认 desc.txt)
--threshold THRESHOLD      二值化阈值 0-255 (默认 128)
--invert                   黑白反相
--fit {contain, cover}     缩放策略 (默认 contain)
--h-align {left, center, 对齐方式 (默认 center)
--v-align {top, center, b  垂直对齐方式 (默认 center)
```

### 方案 B: 分步执行

**第 1 步：图片 → 图案**
```bash
python create_text_input.py --layer 7 --image logo.png --output input.txt
```

**第 2 步：图案 → 公式**
```bash
python patterns.py --input input.txt --output output.txt
```

### 方案 C: 手动编辑图案

直接编辑 `pattern.txt`：
```
layer=7
pattern:
  .   .     (点表示需要转动的位置，空格表示保持不変)
. . . . .
. . . . .
  . . .
    .
```

然后执行：
```bash
python patterns.py --input pattern.txt --output alg.txt
```

---

## 🎨 参数详解

### 缩放策略 `--fit`

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `contain` (默认) | 保持宽高比，图片适配到网格内，不裁切 | 保留完整图案 |
| `cover` | 保持宽高比，图片覆盖整个网格，可能裁切 | 铺满整个面 |

### 对齐方式

- `--h-align`：`left` / `center` / `right`
- `--v-align`：`top` / `center` / `bottom`

### 二值化阈值 `--threshold`

- 范围：0-255 (默认 128)
- **低阈值**（如 80）：更多像素转为黑色，图案更浓
- **高阈值**（如 200）：更多像素转为白色，图案更淡
- **对于黑底图片**：推荐 100-150
- **对于白底图片**：推荐 150-200

### 黑白反相 `--invert`

如果生成的图案是"反相"的，添加此参数即可：
```bash
python main.py --layer 7 --image logo.png --invert
```

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | 主程序，一步到位：图片 → 图案 → 公式 |
| `patterns.py` | 核心算法，图案 → 公式的转换逻辑 |
| `create_text_input.py` | 图片处理模块，读取图片并二值化 |
| `pattern.txt` / `input.txt` | 输入图案文件（二值阵列） |
| `alg.txt` / `output.txt` | 输出公式文件（魔方转动序列） |
| `run.bat` | Windows 快速运行脚本 |

---

## 💡 使用示例

### 示例 1: 简单 Logo 转魔方

```bash
python main.py --layer 7 --image logo.png --threshold 150
```

### 示例 2: 大尺寸魔方，图案铺满

```bash
python main.py --layer 15 --image photo.jpg --fit cover --threshold 120 --invert
```

### 示例 3: 微调对齐

```bash
python main.py --layer 11 --image emoji.png \
  --h-align left --v-align top --threshold 100
```

### 示例 4: 手工调试单个面

编辑 `custom_pattern.txt`：
```
layer=7
pattern:
. . . . .
. . . . .
. . . . .
. . . . .
. . . . .
```

执行：
```bash
python patterns.py --input custom_pattern.txt --output custom_alg.txt
```

---

## 🔧 故障排除

### 问题 1: 图案太浅或太深

**解决方案：** 调整 `--threshold` 参数

```bash
# 图案太浅，增加阈值
python main.py --layer 7 --image logo.png --threshold 100

# 图案太深，降低阈值  
python main.py --layer 7 --image logo.png --threshold 180
```

### 问题 2: 图案没有居中

**解决方案：** 使用对齐参数

```bash
python main.py --layer 7 --image logo.png --h-align center --v-align center
```

### 问题 3: 图像格式不支持

确保使用常见格式：`.png`, `.jpg`, `.bmp`, `.gif` 等。可先用图片编辑工具转换。

### 问题 4: 缺少 Pillow 库

```bash
pip install --upgrade pillow
```

---

## ⚙️ 技术细节

### 图案格式

- 每行的字符间以**空格**分隔
- 非空白字符表示"需要转动"
- 空格表示"保持不变"
- 行数 = 列数 = `layer - 2`

### 公式输出格式

标准魔方记号：
- `L`, `R`, `U`, `D`, `F`, `B` - 基础转动
- `Lw`, `Rw` 等 - 宽转动
- `'` - 逆向转动
- `2` - 180° 转动
- 前缀数字如 `3L` - 第 3 层转动

---

## 📝 示例文件

项目包含示例图片 `emoji.jpg` 和对应的运行脚本 `run.bat`：

```bash
# 直接运行预设
.\run.bat

# 或自定义参数
python main.py --layer 32 --image emoji.jpg --threshold 150
```

---

## 🛠️ 开发信息

- **语言**：Python 3.10+
- **依赖**：
  - `Pillow` - 图像处理
- **无外部 API** - 完全离线运行

---

## 📄 许可

本项目用于教育与研究目的。

---

## 💬 常见问题

**Q: 可以生成彩色图案吗？**  
A: 当前仅支持黑白二值化。可通过 `--invert` 反相，或修改源码支持多阈值。

**Q: 最大支持多少阶魔方？**  
A: 理论无限制，取决于图片分辨率和计算量。推荐 17-100 阶。

**Q: 公式能直接用吗？**  
A: 是的！输出的 `alg.txt` 包含标准魔方记号，可在任何魔方求解器中使用。

**Q: 可以调整输出的转动数学吗？**  
A: 目前只支持标准记号。可修改 `patterns.py` 中的 `build_moves()` 函数自定义。

---

**更多问题？** 检查源代码注释或参考文件内的帮助信息：

```bash
python main.py --help
python patterns.py --help
python create_text_input.py --help
```
