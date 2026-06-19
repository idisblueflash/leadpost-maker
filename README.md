# leadpost-maker

这是一个演示用的小项目，目的是展示怎么把自己写的文章（比如 newsletter）自动改写成适合发到 Facebook 的引流帖。

写文章和发社群其实是两件事。一篇适合放在 newsletter 里的长文，直接搬到 Facebook 上往往没人看完——开头不够抓人、节奏太慢、结尾没有引导。如果每发一篇都要手动重写一遍，太累。

这个项目把改写这件事固定成一个流程：放一篇文章进 `input/`，跑一下，`output/` 里就能拿到改写好的帖子，附带三个标题选项和一个引流到 newsletter 的结尾。

整套流程包成两个随仓库提交的 skill：`leadpost` 负责流程编排，`fb-maker` 负责改写规则。

---

## 怎么用

### 一、安装 skill

两个 skill 都在 `.claude/skills/` 下，随仓库一起克隆即可，无需单独安装。

### 二、跑一次改写

1. 把文章原文放进 `input/<name>.md`
2. 在 Claude Code 里运行：

   ```
   /leadpost @input/<name>.md
   ```

   （也可以直接说「把这篇转成 FB 帖」「转最新那篇」）

3. leadpost 委托 fb-maker 输出三个标题选项 + 完整改写帖，并直接写入 `output/<name>.md`
4. 不满意就直接说「换读者处境型标题」「压缩到 200 字以内」之类的，它会改

### 三、目录结构

```
input/                      文章原文（.md）
output/                     改写后的 FB 帖（.md，文件名与 input 同名）
.claude/skills/leadpost/    工作流 skill（流程编排）
.claude/skills/fb-maker/    改写引擎 skill（改写规则）
CLAUDE.md                   项目说明（Claude Code 自动加载）
```

### 四、改写规则在哪

帖子结构、三种标题类型、结尾 callback 的句式轮换这些规则，全部写在 `.claude/skills/fb-maker/SKILL.md` 里，想改规则直接改这个文件。流程编排（取文章、落盘、回报）写在 `.claude/skills/leadpost/SKILL.md`。
