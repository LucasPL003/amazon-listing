# 输出失败返工路由

输出质量门禁失败时，按类别执行以下确定性返工路由：

| 失败类别 | 下一步动作 |
| --- | --- |
| `product-truth` | `regenerate-visual-plate` |
| `visual-composition` | `regenerate-visual-plate` |
| `text-accuracy` | `rerender-typography-overlay` |
| `typography-harmony` | `redesign-composition` |
| `style-id` | `restart-direction-selection` |

自动返工完成两次后必须停止重试。交付当前最佳结果，并明确报告失败的质量门禁、建议的下一步动作，以及请求用户提供方向后再继续。
