---
name: carousel
description: 把一篇文章走完整条流程做成 Facebook 轮播图（carousel）——生成 3x3 预览板、让用户挑格子、切图、再逐张渲染成 1080x1080 JPG 落盘到 output/<name>/carousel/。当用户说「把这篇做成轮播图」「做个 carousel」「转成多图帖」「carousel」，或指派 input/ 下的文章让你做轮播图时激活。这是编排整条流程的工作流 skill：图像 prompt 委托给 carousel-prompt，渲染委托给 gpt-image-2，切图与转 JPG 用本 skill 的脚本。
---

# carousel：文章 → Facebook 轮播图（完整工作流）

这是**编排 skill**。它串起三个引擎，自己只负责流程、人工确认点、和落盘：

- **carousel-prompt**（视觉脚本）：文章 → 9 张幻灯片脚本 + 一条 3x3 预览板 prompt
- **gpt-image-2**（渲染）：prompt → 图像像素
- **scripts/carousel.py**（几何）：切 3x3、转 1080x1080 JPG（GPT Image 2 给不了精确尺寸，这步必须确定性地做）

每篇文章的所有产物都放在 `output/<name>/carousel/` 下，和 `leadpost` 的 `output/<name>/post.md` 同属一个文章目录。

## 设计要点（先读）

- **3x3 是概念板，不是成品。** 9 格一次性出图所以天然连贯，但每格分辨率低、可能带网格线。
  用户挑中的格子是**参考图**，不是最终图。
- **最终图是重新生成的。** 第 5/6 步把挑中的格子作为 `--ref` 喂回 gpt-image-2，
  在 1080x1080 干净重出。格子本身已带统一风格，所以**不需要单独的风格锁**（KISS）。
  仅当用户主动给了风格参考图，才作为额外 `--ref` 一并传入。
- **尺寸/格式是脚本的活，不是模型的活。** 精确 1080x1080、JPG 格式由 `carousel.py` 完成。
- **有两个人工确认点**（第 3 步挑格、第 6 步审第一张），不要跳过。

---

## 流程

### 第 1 步：确定要处理的文章

和 `leadpost` 同一套规则取原文和 `<name>`：

| 指派方式 | 怎么处理 |
| --- | --- |
| `@input/<name>.md` 或指明 input/ 下某文件 | 读取该文件；`<name>` = 文件名去掉 `.md` |
| 直接粘贴原文 | 约定一个 kebab-case 的 `<name>`（据标题拟，或问用户） |
| 「最新那篇 / 还没做的那篇」 | 列出 `input/` 里没有对应 `output/<name>/carousel/` 的文件；多于一篇让用户确认 |

### 第 2 步：生成视觉脚本

读取 `.claude/skills/carousel-prompt/SKILL.md`，按其流程产出：
9 张幻灯片脚本、一条 3x3 预览板 prompt、编号对照表。
若用户提供了风格参考图，记下其路径，后续渲染作为额外 `--ref`。

### 第 3 步：渲染 3x3 预览板

调用 gpt-image-2，把预览板 prompt 渲染成一张图：

```bash
bash .claude/skills/gpt-image-2/scripts/gen.sh \
  --prompt "<3x3 预览板 prompt>" \
  --out output/<name>/carousel/preview.png
# 用户给了风格图时追加： --ref <用户的风格图路径>
```

然后切成 9 格（`--inset` 默认 0.015，已实测能干净削掉 GPT Image 2 的贴边网格；
若仍有边框渗入再往 0.03 调）：

```bash
python3 .claude/skills/carousel/scripts/carousel.py split \
  --in  output/<name>/carousel/preview.png \
  --out-dir output/<name>/carousel/cells
```

把对照表写到 `output/<name>/carousel/cells.md`，并在对话里**展示预览图 + 一张编号表**
（№ | 描述），问用户保留哪几格、以及顺序。

### 第 4 步：用户挑格子

让用户回「保留哪几号、按什么顺序」。把结果写进
`output/<name>/carousel/selection.json`，例如：

```json
{ "order": [1, 4, 5, 8, 9] }
```

`order` 数组的顺序就是最终轮播图的播放顺序；切好的 `cells/cell-N.png` 即对应的参考图。
不需要再单独「split 一次」——第 3 步已经把 9 格都切好了，这里只是记录选择。

### 第 5 步：生成第一张（1080x1080 JPG）并送审

取 `order` 的第一格，把它作为 `--ref` 重新渲染成干净大图，再转成 FB 格式：

```bash
bash .claude/skills/gpt-image-2/scripts/gen.sh \
  --prompt "<该格对应的幻灯片文案，要求 1:1 square, high detail>" \
  --ref output/<name>/carousel/cells/cell-<第一格>.png \
  --out output/<name>/carousel/slides/_raw-1.png
# 用户给了风格图时再追加一个： --ref <用户的风格图路径>

python3 .claude/skills/carousel/scripts/carousel.py fbjpg \
  --in  output/<name>/carousel/slides/_raw-1.png \
  --out output/<name>/carousel/slides/slide-1.jpg
```

在对话里展示 `slide-1.jpg`，**等用户确认风格/版式 OK**。
不 OK 就按指令调 prompt 重出这一张，直到通过——**先把第一张定下来，再批量。**

### 第 6 步：用户确认后，生成其余各张

对 `order` 里剩下的每一格，重复第 5 步的「渲染 → fbjpg」，
输出 `slides/slide-2.jpg`、`slide-3.jpg` …（编号 = 在 `order` 里的位置）。
全部完成后回报：列出 `output/<name>/carousel/slides/` 下的成品清单，并展示。

---

## 产物布局

```
output/<name>/
  post.md                    # leadpost 的 FB 帖（如果也跑了）
  carousel/
    preview.png              # 3x3 概念板
    cells/cell-1..9.png      # 切好的 9 格（参考图）
    cells.md                 # 编号对照表
    selection.json           # 用户选了哪几格、什么顺序
    slides/slide-1..N.jpg    # 最终 1080x1080 JPG 成品（_raw-*.png 是中间产物）
```

---

## 边界

- 只编排流程，不发明视觉规则——脚本规则以 carousel-prompt 为准。
- 不修改 `input/` 原文。
- 两个确认点（挑格、审第一张）必须等用户，不要自动跨过。
- 一次处理一篇。
