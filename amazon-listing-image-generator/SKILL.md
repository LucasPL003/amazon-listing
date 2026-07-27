---
name: amazon-listing-image-generator
description: Use when generating Amazon main and secondary images from 图片解析摘要, 附图策划, original product images, local reference-image style packs, image design requests, internal image prompts, or confirmed listing-image generation.
---

# Amazon Listing Image Generator

## 概览

把上游 Listing 图片分析与本地风格套系转为可审核、确认后才执行的 Amazon 主副图。产品原图定义身份与事实；Style Pack 只定义视觉语言。

## 必读文件

先完整读取 `references/workflow.md`。进入对应阶段时读取：

- 风格推荐与逐图审核：`references/design-output-template.md`
- 内部任务与提示词：`references/prompt-contract.md`
- 生成验收与返工：`references/quality-checklist.md`

## 执行顺序

1. 检查 `图片解析摘要`、`附图策划`、原始产品图片、目标站点与文案语言。缺少或明显冲突时停止，不猜测、不创建提示词、不生图。
2. 运行 `scripts/validate_style_packs.py assets/style-packs`。只使用报告中的有效风格套系；零个可用套系时停止并指向 `assets/style-packs/README.md`。
3. 按品类、人群、情绪、场景、图片角色覆盖和色彩兼容性推荐至多三个真实候选。等待用户选择一个 Style Pack ID。
4. 将每条 `附图策划` 映射为一张图和一个核心销售任务，用模板展示逐图设计。除结构、尺寸、步骤、分层材料和合规对比等明确的信息图任务外，副图按场景优先：至少 60% 必须展示已确认的真实使用场景。场景背景必须同时适配已确认的产品用途、目标人群和该图唯一销售任务；不得借人物、道具或环境暗示未经确认的功能、参数、效果或安全主张。完整提示词、负面约束、来源映射和模型设置默认保持内部。
5. 等待用户明确回复“确认生成”或同义确认；此前不得调用生成工具。

## 生成与验收

**REQUIRED SUB-SKILL: imagegen** — use the selected local product and Style Pack reference images together, preserving the role separation in prompt-contract.md.

主图必须无文字。每张副图在一次 Image Gen 请求中同时生成画面与已批准的准确文案。逐图按质量清单检查；只返工失败图片，每张自动返工最多 2 次。达到上限仍失败时交付当前最佳结果与未通过项，不宣称整套合格。
