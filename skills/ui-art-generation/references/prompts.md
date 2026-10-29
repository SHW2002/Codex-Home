# 可复用的 UI 提示词与切图方式

模板中的括号字段按任务替换，删除无关要求。中文和英文都可以表达约束；下列英文保留了本次项目中验证过的描述方式，不意味着模型必须使用英文。

## 单个透明图标或空白底图

```text
Use case: stylized-concept
Asset type: [HUD icon / illustrated backing / character head], displayed at [size] px.
Primary request: [one clearly defined subject and function].
Reference images: Image 1 is the primary style reference. Image 2 supplies [identity / palette / outline treatment]. Borrow the stated qualities; do not draw the reference objects.
Style: [specific outline, proportions, color blocks, shading and texture].
Composition: [front-on / other required viewpoint], one complete silhouette centered on [aspect ratio] canvas, with safe transparent margins.
Background: actual transparent alpha outside the silhouette; [opaque / intentionally translucent] interior.
Text: no text or letters; the application will render labels separately.
Constraints: [exact invariants and empty area needed for overlay content].
Avoid: cropped outlines, checkerboard pixels, extra objects, ground shadow, watermarks, [specific style mismatches].
```

空白底图须明确“中间保持干净、留给现有图标/文字”，否则模型容易自行填入物品、标记或按钮。

## 同一图标的多状态

```text
Asset type: [count] states of the SAME [object], displayed at [size] px.
Reference: use the approved base image as the identity, silhouette and style source.
Layout: [columns] columns by [rows] rows, ordered left to right, top to bottom. Each sprite stays completely inside its cell with [margin] px safety space. No grid lines, labels, panels or overlap. Unused cells remain transparent.
Invariant: identical outline, camera, scale, center, anchor, casing, stroke thickness, light direction and shading in every state.
Only changing element: [specific region / expression / symbol].
States: [explicit mapping of cell to visual meaning].
Background: actual transparent alpha; no painted checkerboard.
```

生成的“20%”不能只靠提示词保证精确。涉及准确时间扇区时，检查状态顺序和面积；偏差较大时用同一底图与确定性遮罩绘制扇区，保留插画的外壳与描边。

## 动画分层

```text
Asset type: animation-ready [prop] consisting of separate [body / flap / other necessary parts].
Layout: each part occupies its own [specified cell or region], with full silhouette and generous transparent margins; no overlapping parts.
Assembly: [how parts meet, which edge is the hinge, what the closed/open poses require].
Invariant: matching width, perspective, paper/material color, outline thickness and shading.
Part A: [complete body; required interior and overlap area].
Part B: [separate moving part; contact edge and proportions].
Avoid: flattened composite of the whole prop, duplicate pieces, extra handles or contents, ground shadows, text.
```

开合素材要为遮挡留出少量重叠，避免两个图层边缘恰好接触产生缝隙。不同图层可以有不同尺寸，但导入后必须配置正确 pivot/偏移，不能仅把各自图像中心对齐。

## 固定身份的头部图

```text
Use case: identity-preserve
Asset type: head-only portrait sticker for a [size] px HUD.
Reference: preserve the exact character identity from Image 1 and the game's illustration style.
Show ONLY: [hair / hat / glasses / eyebrows / face / beard and other identifying features].
Framing: complete head silhouette, including the entire hat brim and hair tips; cut off at [chin / bottom of beard].
Constraints: no neck, shoulders, torso, hands or props outside the head; no redesign of facial proportions, costume details or colors.
Output: centered on real transparent alpha, with safe margins and crisp game-readable outlines.
```

## 小范围图标替换

```text
Use case: precise-object-edit
Change only [the emblem region] to [new symbol].
Keep the surrounding artwork, silhouette, composition, material colors and alpha unchanged.
Match the local outline weight, palette, perspective and shading.
Do not add text or modify any other region.
```

编辑返回的整图可能仍有细微漂移；对需要逐像素保留的区域，用目标区域遮罩把结果合回原图，再比较区域外像素。

## 切图辅助脚本

依赖 Pillow。以下为参数示例，在 PowerShell 中把参数写在同一行，脚本路径相对于此技能目录，图片路径按当前任务替换。

```text
python scripts/src/slice_ui_sheet.py --input sheet.png --out-dir clocks --columns 3 --rows 3 --names Clock1 Clock2 Clock3 Clock4 Clock5 --mode shared --padding 8 --preview-size 48
python scripts/src/slice_ui_sheet.py --input sheet.png --out-dir ornaments --columns 3 --rows 3 --names - - - - - FailureStamp CellBacking --mode trim --padding 8
```

- `names` 按行优先排列，`-` 跳过；未列出的末尾格子不导出。
- `cell`：保留整格，统一到最大格子尺寸，固定注册点；默认选项。
- `shared`：取所有选中格子内容边界的公共外包矩形，统一裁切；适用于已对齐的状态组。
- `trim`：每张分别紧裁；适用于独立图标，不适用于帧切换。
- 分格使用整数边界覆盖整幅图，最后一行/列余下像素不会丢失。
- 输出 `slice-report.json` 包含来源矩形、内容边界、alpha 统计及裁切方式，`contact-sheet.png` 显示指定像素尺寸的明暗底预览。
- 脚本不修复模型生成时已有的位置漂移，也不自动扣背景。检查报告和预览后再决定修图。
- 默认不覆盖已有文件。明确替换本次产物时才使用 `--overwrite`。
