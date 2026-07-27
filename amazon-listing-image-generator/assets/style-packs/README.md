# Style Pack 参考图库

每个可用套系占用一个独立目录，并包含一个便于人工阅读的 `style-pack.md`。所有本地参考图片放在该套系的 `references/` 目录内。

`_template` 只用于复制示例，不纳入推荐。复制后请重命名目录和 Style Pack ID，并补充真实的本地参考图片。

## 必需规则

- 每个启用套系必须包含至少一张 `generic` 通用参考图。
- 角色键可使用 `main`、`feature`、`lifestyle`、`size` 或 `steps`。
- 参考图片只提供视觉语言：氛围、配色、构图节奏、光影与排版感觉。
- 产品身份、结构、颜色、材质、配件和可见功能只能来自用户的原始产品图片。
- 不得从参考图迁移产品、品牌、Logo、文案、认证或主张。
- 套系中不得出现价格或价格定位字段。
- 图片路径必须位于当前套系目录内，并使用 `.png`、`.jpg`、`.jpeg` 或 `.webp`。

## 添加套系

1. 复制 `_template` 为新的套系目录。
2. 修改 `style-pack.md` 中的唯一 `id`、名称和匹配信息。
3. 把参考图放入 `references/`，并更新 JSON 路径。
4. 运行 `scripts/validate_style_packs.py assets/style-packs`。
