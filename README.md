# 期末复习助手 (Exam Review Skill)

Claude Code 技能 — 根据教材 PDF、课件 PPT 和考题/提纲，自动定位考点、提炼知识点，输出详细解答与讲解的 Word 文档。

## 功能

- 支持多种知识来源：教材 PDF（扫描版/文字版）、老师课件 PPT/PPTX、课堂笔记图片
- 接收往年考题、复习提纲等资料（文本、图片、PDF 均可）
- 自动在知识来源中定位每道考题对应的考点章节
- 输出详细的解答与知识点讲解，生成格式化的 Word 文档
- 教材/课件中未覆盖的内容会用 AI 知识补充并明确标注来源
- 支持含图片的题目：电路图、函数图像、示意图等都能识别和分析
- 支持理工科风格（公式推导、解题步骤）和文科风格（概念辨析、论述框架）

## 前置条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3（系统自带）

### 可选依赖（推荐）

安装 [poppler](https://poppler.freedesktop.org/) 以支持所有类型的 PDF（包括扫描版）：

```bash
# macOS (Homebrew)
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

未安装 poppler 时，技能会自动回退到 Python 标准库方案，仅对扫描版 PDF（内嵌 JPEG 图片）有效。

## 安装

将技能目录复制到 Claude Code 的技能路径：

```bash
cp -r exam-review ~/.claude/skills/exam-review
```

## 使用方法

在 Claude Code 中，提供知识资料和考题即可自动触发。

**使用教材 PDF：**
```
这里是《模拟电子技术基础》的教材 PDF 和两道考题，帮我整理考点解析：
1. PN结所加的正向电压越大，空间电荷区越宽（）
2. 发光二极管正向导通状态时流过电流越大，发光强度越大（）
```

**使用课件 PPT（没有教材时）：**
```
这是我马原课的课件PPT，结合这几道往年考题帮我复习
```

**使用手写题纲：**
```
这是我手写的复习提纲照片，配合这本教材的PDF帮我整理重点
```

### 输入资料

| 类别 | 资料 | 说明 |
|------|------|------|
| 知识来源 | 教材 PDF | 课程教材，支持扫描版和文字版 |
| 知识来源 | 课件 PPT/PPTX | 老师上课用的演示文稿 |
| 知识来源 | 课堂笔记图片 | 手写或电子笔记的照片/扫描件 |
| 题目来源 | 考题 | 往年考试题，文本/图片/PDF 均可 |
| 题目来源 | 提纲 | 复习提纲、重点列表，文本/图片/PDF 均可 |
| 可选 | 风格偏好 | 默认自动判断（理工科/文科） |

### 输出

生成 Word 文档（`.docx`），包含：

- 每道题的答案与考点定位
- 基于教材原文的详细解析
- 相关知识点扩展与易错点
- AI 补充内容的来源标注

## 目录结构

```
exam-review/
├── SKILL.md              # 技能定义（触发条件、处理流程、输出格式）
├── README.md             # 本文件
└── scripts/
    └── pdf_to_images.py  # PDF 转图片脚本
```

## PDF 处理机制

技能内置了 `pdf_to_images.py` 脚本，自动选择最佳方案处理 PDF：

```
优先: poppler (pdftoppm) → 支持所有 PDF，可控制 DPI
回退: Python 标准库      → 零依赖，仅支持内嵌 JPEG 的扫描版 PDF
```

脚本也可独立使用：

```bash
# 默认 150 DPI
python3 scripts/pdf_to_images.py input.pdf output_dir/

# 指定 DPI
python3 scripts/pdf_to_images.py input.pdf output_dir/ --dpi 300
```

## 建议配置

为避免批量读取 PDF 图片时反复弹出权限确认，可在 Claude Code 设置中允许 Read 工具：

```json
{
  "permissions": {
    "allow": ["Read"]
  }
}
```

## License

MIT
