# 场景物品提示词模板

只取当前任务需要的段落，替换方括号占位信息；不把所有约束无差别叠在每次生成上。英文模板方便沿用历史提示词，中文沟通不受影响。

## 独立场景道具

```text
Use case: stylized-concept
Asset type: production 2D game prop sprite, not a scene illustration.
Input images: Image 1 defines the game's linework, palette and shading.
Image 2 defines [the required view or silhouette, if supplied].
Primary request: one [object], with [recognizable structural features].
View: match the reference's [camera elevation, orientation and visible sides].
Style: match its [outline thickness], [broad color masses] and [shading treatment].
Keep the object readable at its intended small in-game display size.
Lighting: [direction, shadow level and material response from the scene].
Composition: one isolated object; [target silhouette and margin]; no accidental cropping.
Constraints: genuine transparent RGBA background; opaque solid surfaces;
no room, floor, extra props, characters, text or watermark.
[No cast shadow outside the object when the game supplies a separate shadow.]
```

小螺丝等微小道具优先放大头部、缩短细杆并简化细纹，让玩家在最终尺寸辨认；不要只以高分辨率原图中的精细程度验收。

## 按场景参考修正画风

```text
Use case: style-transfer
Input images: Image 1 is the exact object to repaint.
Image 2 is only the existing game's art-style reference, not content to insert.
Primary request: repaint Image 1 to match Image 2's clean bold contours,
chunky shapes and simple cel shading.
Preserve: silhouette, view, relative proportions, attachment points and framing.
Change only: [observed style mismatch].
Remove: [unwanted realistic wood grain, corrosion, glossy highlights or excess wear].
Constraints: preserve genuine transparency and opaque solid interiors;
do not copy the reference room or its furniture into the output.
```

参考图中本来存在的磨损或材质细节可以保留；删除项根据实际偏差选择，不把“无纹理”变成所有游戏的硬性风格。

## 背光屋架与近景遮挡物

```text
Use case: style-transfer
Asset type: backlit architectural foreground sprite for a stylized 2D game.
Input images: Image 1 is the object to edit; Image 2 is the room's style reference.
Primary request: keep the architecture and repaint it as a nearly black
[blue-violet / scene-matched hue] silhouette receiving no direct light.
Only a thin, subdued rim on downward-facing edges catches bounced light from below.
Use broad flat shapes and the reference's confident cartoon outlines.
Keep structural joins simple; [a hanging lamp is switched off].
Preserve: silhouette, dimensions, attachment points and the required solid occlusion area.
Constraints: opaque solid interior even when black; transparent exterior;
no frontal lighting, bright metal, scenery, text or watermark.
```

《薇薇安的飞机》历史暗部大致使用RGB `(8,10,18)` 到 `(18,18,28)`，这只是该场景的调色参考；实际仍需看现有物件和引擎光照。

## 建筑补件与吊挂结构

先描述“什么连着什么”，再描述材质：

```text
Primary request: one coherent [corner support / crossbeam / suspension assembly].
Structure: [upright post on the right], [short socket extending left from the top],
and [diagonal knee brace joining the socket back to the post].
All structural segments meet with visibly solid joins; no floating sections.
Attachment: reserve [overlap area] so this piece can connect behind [existing beam].
Style and lighting: match the supplied architectural and scene references.
Composition: one complete modular assembly, [view], isolated RGBA background.
```

吊挂补绳时可以使用：

```text
Keep the existing cable loops, mounting brackets and switched-off lamp unchanged.
Add taut suspension ropes from each existing upper mounting point toward the top
of the canvas, with a small knot or clamp at each lower connection.
The ropes continue beyond the top edge so their ends can hide behind the ceiling beam.
Allow enough visible rope length to make the support readable; do not crop the lamp.
```

门口梁端处理优先复用原图包边、螺栓或斜撑；确实需要生图时，要求“finish the exposed beam end with a matching cap/bracket; preserve the doorway opening and the remaining silhouette”，不要重新填满已经让出的门洞。

## 精确贴合主体的覆盖布

```text
Use case: precise-object-edit
Asset type: opaque cloth-cover sprite aligned to an existing game prop.
Image 1 is the exact geometry and camera-view reference.
Preserve its orientation, scale, center and full-frame placement.
Replace the visible [aircraft] with one physical [canvas] cover draped over its
entire body, including [wings, tail, landing gear and front propeller].
The cover silhouette must be slightly larger than the reference at every edge.
Broad cloth folds suggest the structure underneath without exposing it.
Match the game's outlines, palette and simple fabric shading.
Constraints: genuinely transparent outside the cloth; opaque cloth interior;
no visible underlying metal/glass/paint, extra props, floor, external cast shadow or text.
```

生成后仍需用原主体Alpha或实际合成图检查覆盖，提示词中的“完整覆盖”不能代替验证。

## 定向迭代

保持同一编辑目标和参考关系，每次清楚写出观察到的问题，例如：

- “实体黑色区域漏出背景”：修复实体Alpha，保留现有轮廓和边缘抗锯齿。
- “右侧屋架悬空”：补右侧支柱与角撑，其他梁段与画风不变。
- “门口梁像被刀切断”：只添加匹配的端盖/包边，不封住门洞。
- “布罩露出橙色机翼”：只扩大该侧覆盖轮廓，不改飞机方向和整体构图。
- “前景太写实或太亮”：保留轮廓，移除过密纹理，降低正面亮度与高光。
