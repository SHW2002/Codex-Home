# Vivian's Airplane 的 UI 插画案例

以下是本项目经验，其他项目应重新观察自己的画风。工程历史位置为 `E:/Projects/Unity/Vivian-s-Airplane/`，Unity 子目录为 `Unity Vivian's Airplane/`；路径迁移时从项目中搜索同名素材和文档。

## 画风

主参考是 `Assets/Art/Sprites/Scene/Home/HomeCounter.png`，补充参考是外卖导航仪现有插画。头部身份参考可使用 `Assets/Art/Sprites/Portraits/Enzo_Half.png`。

可复用的描述：

```text
Chunky 2D hand-inked game illustration, thick dark brown-black outlines,
simplified rounded/geometric shapes, clean warm color blocks, restrained flat
cel shading, cream highlights with ochre and coral accents, readable at small size.
No photorealism, CGI product render, fine paper grain, bloom or lens effects.
Borrow the style from the references; do not draw their objects.
```

看实际参考后再使用这些词；不得因为示例中出现暖色就把已有冷色角色或物品一律改暖。

## 已完成的素材及经验

| 案例 | 结构 | 制作重点 |
| --- | --- | --- |
| 五档订单钟表 | 同一钟表外壳，改变剩余时间扇区 | 48px 仍能看出档位；图间注册点和描边一致 |
| 叉号与纸质底图 | 独立印章、留白票据 | 叉号落在钟表位置；底图不烘焙头像、文字或时钟 |
| 恩佐头像 | 只保留帽、眼镜、头发、脸与胡须 | 明确截止在胡须下沿；禁止脖子、肩、胸口和身体 |
| 外卖包装袋 | 打开袋身与独立翻盖 | 同一纸色、边线和透视；配置铰链与重叠区，检查开合 |
| 咖啡徽章替换 | 局部遮罩编辑后合成 | 只把两处徽章合回原图，保留区域外像素及图层尺寸 |
| 导航仪圆底 | 完整圆形、内部不透明、外部透明 | 中央保持空白，供现有彩色物品图标覆盖 |

原始提示词和制作说明可从项目下列位置追溯，无需把项目原画复制到技能里：

- `Docs/Delivery/OrderStatus/`：钟表、底图、印章及恩佐头像。
- `Docs/Delivery/StartPresentation/`：袋身/翻盖、局部咖啡徽章、动画装配。
- `Docs/Delivery/NavigationHint/`：圆形图标底图。
- `output/imagegen/delivery-orders/`、`output/imagegen/delivery-start/`：历史选定原图。

关联历史会话标题是“更新外卖订单状态UI”“更新外卖玩法开始动画”和“添加外卖玩法导航仪提示UI”。需要更多原始上下文时，用会话工具定位标题并只读取相关消息，不把庞大的工具输出整批载入。

## 透明与布局

包装袋曾需要清除外部半透明光晕并恢复应为实色的内部区域；这是特定产物的修复，不是对所有生成图统一阈值化 alpha 的理由。

订单素材使用过 `1536x1024` 的 3×3 图集。1024 不能被 3 整除，切图应使用整数分割端点覆盖整图，不能固定每行 341 后丢掉最后一行像素。五档钟表应作为同一组使用公共裁切，印章和底图则独立处理。

角色急躁、呼吸及印章盖下使用运行时 Transform/颜色动效；不需要为每个挤压姿态生成新图片。随机顾客优先从已启用的头部 SpriteRenderer 截图，保留随机发型和肤色，固定角色可配置独立头像。

## Unity 接入与验证

- 先读项目 `AGENTS.md`、`Docs/设计规范.md` 和包内 `AGENT.md`。使用 Unity Agent Bridge 串行请求并遵守其命令发现/原子写入协议，不手写 prefab YAML 中的 CodeBind 引用。
- 资源放 `Assets/Art/UI/Delivery/<功能>/`；修改完成后 `refresh`，脚本变化还需 `recompile`、等待 `get_compile_result`。临时 Editor 工具用后删除。
- 不运行游戏。本项目使用静态布局合成及编辑器离线采样；合成图明确标注“布局合成预览”，不能写成实机截图。
- 历史头像 CommandBuffer 截图曾上下翻转，应检查投影矩阵与 RenderTexture 方向；使用 SpriteRenderer 颜色时避免材质 tint 再次相乘。这是截图流程检查项，不要求改生成图。
- 复杂 UGUI 临时截图为空白时，先检查采样工具、Canvas 与相机配置。预制体网格和资源正确不能证明整图渲染通过；空白采样也不能直接证明实际 UI 错误，应如实报告验证范围。
