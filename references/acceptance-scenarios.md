# Acceptance scenarios

Use these scenarios to review routing and conversation behavior after changing the skill.

| ID | User message | Expected behavior |
|---|---|---|
| BEGINNER_MINIMAL | “我不懂这些，就是想骑快一点。” | Trigger the skill, explain nothing technical, and ask the five-item quick start. |
| NO_RACE | “我不比赛，只想提高爬坡和长途不掉速。” | Build a non-race goal contract; do not invent an event. |
| NO_POWER | “我没有功率计，只有码表。” | Use time, RPE, talk test, cadence/route proxies; do not prescribe watts or `%FTP`. |
| HR_ONLY | “我有心率带，但不知道阈值心率。” | Mark the threshold unverified and offer an assessment path; do not use a stored value as measured truth. |
| CYCLING_ONLY | “我只要骑行训练。” | Keep the final output to cycling while completing the short nutrition, sleep, supplement, and health screen. |
| INTEGRATED | “训练、吃、睡眠和补剂都一起考虑。” | Use the integrated scope and complete the full second-round screen. |
| BROWSER_DATA | “我已经登录 Intervals.icu，你直接看。” | Use an authorized browser or connector, avoid asking for commands or secrets, and report data quality. |
| NO_TOOLS | “平台连不上，我也不会导出。” | Continue with conversation estimates or assessment-first; do not stop at an integration error. |
| CASE_DELTA | “拿我的原始数据跟成功案例比较。” | Produce the athlete-only baseline first, then show adopted, scaled, rejected, and unknown deltas. |
| PREVIEW_ONLY | “先给我看看会写进 ICU 的内容。” | Render and preview without deploying. |
| DEPLOY | “把刚才确认的计划同步进去。” | Verify formal readiness and the concrete preview, then upsert only this plan's events. |
| META_WORK | “继续改进这个 skill 的易用性。” | Modify or review the skill; do not start athlete intake. |
| OUT_OF_SCOPE | “推荐一辆公路车” | Do not invoke the coaching workflow. |

Failure conditions include asking a novice to run shell commands, requesting an API key in chat, showing internal enums as the main choices, repeating answered questions, treating missing sensors as a blocker, or presenting a draft as a formal plan.
