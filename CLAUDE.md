# leadpost-maker

把 newsletter 文章改写成 Facebook 内容的工作目录：既能转成**引流帖**，也能做成**轮播图**。

## 目录约定

- `input/`：放 newsletter 原文 `.md`
- `output/<name>/`：一篇文章的所有产物都放在以它命名的目录下（`<name>` 与 input 同名）
  - `post.md`：leadpost 改写的 FB 引流帖
  - `carousel/`：carousel 做的轮播图（预览板、切片、最终 1080x1080 JPG 等）
- `.claude/skills/`：四个 Skill，分成「工作流」和「引擎」两层（见下）

## Skill 分工

工作流（编排流程、人工确认、落盘）：

- **leadpost**：文章 → FB 引流帖，落盘到 `output/<name>/post.md`。改写规则委托 fb-maker。
- **carousel**：文章 → FB 轮播图，落盘到 `output/<name>/carousel/`。视觉脚本委托 carousel-prompt，渲染委托 gpt-image-2，切图/转 JPG 用自带的 `scripts/carousel.py`。

引擎（只定规则/产物，不编排）：

- **fb-maker**：引流帖改写规则——三段式结构、三种标题、结尾 callback 句式轮换、改写原则。
- **carousel-prompt**：轮播图视觉脚本——9 张幻灯片弧线 + 一条 3x3 预览板 prompt。
- **gpt-image-2**：用 ChatGPT 订阅渲染图像（carousel 的渲染引擎）。

## 引流帖流程（leadpost）

1. 用户在 `input/<name>.md` 放入原文（或直接粘贴）
2. 调用 `/leadpost`（指明文件或说「转最新那篇」）
3. leadpost 委托 fb-maker，输出「三个标题选项 + 完整帖子」
4. 改写完直接写入 `output/<name>/post.md`（不等确认），用户可继续提修改指令

## 轮播图流程（carousel）

1. 调用 `/carousel`（指明文件或「最新那篇」）
2. carousel 委托 carousel-prompt 产出 9 张幻灯片脚本 + 一条 3x3 预览板 prompt
3. gpt-image-2 渲染 3x3 预览板，脚本切成 9 格，展示编号表 → **用户挑保留哪几格、什么顺序**
4. 取第一格作 `--ref` 重新渲染成 1080x1080 JPG 送审 → **用户确认风格 OK**
5. 确认后逐张生成其余幻灯片，全部落盘到 `output/<name>/carousel/slides/`

> 关键：3x3 是**概念板**（一次出图所以连贯），不是成品；挑中的格子作为 `--ref`
> 在 1080x1080 干净重出。精确尺寸/JPG 格式由 `carousel.py` 确定性完成，不依赖模型。

规则细节见各 `.claude/skills/<name>/SKILL.md`。
