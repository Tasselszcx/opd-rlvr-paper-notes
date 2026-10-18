# 基于后续独立 RL 反馈的 OPD 元教学：论文调研与实验建议
调研日期：2026-10-14  
研究主题：在固定总训练预算下，通过 student 后续独立 RL 的结果，学习 teacher 的指导内容与调用时机，并探索教学经验在递归自改进中的复用。
> 本文由本次对话中的论文调研整理而成。论文事实与研究建议分别表述；“未核验录用”不等于“未录用”。本文提供研究方向判断，不构成穷尽性的首创性证明。
## 1. 核心判断
**这个 idea 有值得做的空间，但需要收窄主张。** 最有价值的问题是：
> 能否识别并学习那些“即时提升一般、却能让后续独立 RL 更有效”的指导，并在计入元训练成本后仍获得净收益？
OPD warmup、学生反馈训练教师、选择性指导和递归自改进，都已有很近的工作。潜在贡献在于形成一个**以独立 RL 后果为目标、能够跨训练阶段复用、且在完整预算下有效的教学机制**。现有文献支持研究动机，但还不能保证完整方案有效。
建议优先建立三类证据：
1. 不同指导对后续 RL 具有不同的学习价值，而且这种价值不能被即时分数或廉价代理指标充分解释。
2. 用后续 RL 反馈学习教学策略，在计入教师、warmup、RL、元训练、额外分支和评测成本后，仍带来净收益。
3. 在相同 student checkpoint 上，保留教学经验优于重置教学经验，证明收益不完全来自学生本身变强。
## 2. 调研范围与录用状态
本次整理了 **20 篇经会议官网、PMLR 或 ACL Anthology 核验的 2026 年录用论文**：
| 会议 | 数量 | 状态 |
|---|---:|---|
| ICML 2026 | 7 | 正式主会论文 |
| ACL 2026 | 8 | 4 篇 Main、4 篇 Findings；Main 中含 1 篇 Short |
| NeurIPS 2026 | 5 | 已列入官方录用论文目录；不等同于 proceedings 已出版 |
| 合计 | 20 | 不包含下述预印本及机构公告条目 |
另补充 **1 篇 EMNLP 2026 作者机构公告录用论文**。本次访问的 [EMNLP 官方 accepted 页面](https://2026.emnlp.org/program/main_papers/)正文只有标题，无法据此逐篇核验；这不等于断言会议尚未公布录用结果。
用户提供的 NPD 和 AutoNPO 属于同一篇论文的不同机制，不应计为两篇。
## 3. 20 篇 2026 年录用论文
### 3.1 ICML 2026
其中 **SOAR、PEAR、SCoRe** 最值得先精读。
| 编号 | 论文 | 主要发现及与本 idea 的关系 | 代表性评测 |
|---|---|---|---|
| 1 | **[Teaching Models to Teach Themselves: Reasoning at the Edge of Learnability](https://icml.cc/virtual/2026/poster/65098)**，SOAR；[原文](https://arxiv.org/abs/2601.18778) | 教师生成练习题，学生短程 RL 后在困难题上的进步构成教师奖励。“用学生训练后的收益训练教师”已有直接先例。差异需要落实到 OPD 指导及其对后续独立 RL 的作用。 | MATH、HARP 困难子集，OlympiadBench 迁移；pass@1–32、多随机种子。 |
| 2 | **[Good SFT Optimizes for SFT, Better SFT Prepares for Reinforcement Learning](https://proceedings.mlr.press/v306/zhang26hd.html)**，PEAR | 更强的 SFT checkpoint 可能在相同后续 RL 后更差；通过重要性重加权改善 SFT→RL 衔接。支持研究动机，也说明“起点表现不等于后续学习价值”已不是新发现。 | 可验证推理游戏、数学；后续 RL 的 pass@1/pass@8。 |
| 3 | **[Student-Centered Distillation Narrows the Agentic Gap Between Small and Large LLMs](https://proceedings.mlr.press/v306/lyu26j.html)**，SCoRe | 教师纠正学生轨迹中的最早错误，随后 SFT，再从错误前的有效前缀开始短程 RL。“指导关键错误，再让学生自主探索”已有很近的方法。旧标题 From Correction to Mastery 对应同一篇工作。 | 数学、深度检索等 12 个 benchmark；正确率、QA F1 等。 |
| 4 | **[Entropy-Aware On-Policy Distillation of Language Models](https://proceedings.mlr.press/v306/jin26e.html)**，EOPD | teacher 高熵位置加入 forward KL，兼顾精确模仿与多样性。应与这种廉价、自适应的蒸馏规则比较。 | MATH500、AIME、AMC、Minerva、OlympiadBench；Avg@8、Pass@8、熵。 |
| 5 | **[Reinforcement-aware Knowledge Distillation for LLM Reasoning](https://icml.cc/virtual/2026/poster/66775)**，RLAD；[原文](https://arxiv.org/abs/2602.22495) | 通过 advantage-aware、trust-region 蒸馏协调教师模仿与奖励优化。适合作为 teacher 持续参与 RL 的强基线。 | K&K、MATH500、AMC、AIME；Mean@32、Pass@32、收敛曲线。 |
| 6 | **[Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models](https://icml.cc/virtual/2026/poster/64784)**，OPSD；[原文](https://arxiv.org/abs/2601.18734) | 同一模型的 teacher 分支看到参考解，student 分支只看题，在学生轨迹上自蒸馏。提供可实现的 self-teacher 构造。 | AIME24/25、HMMT25；多次采样准确率、token 效率。 |
| 7 | **[Reinforcement Learning via Self-Distillation](https://icml.cc/virtual/2026/poster/64121)**，SDPO；[原文](https://arxiv.org/abs/2601.20802) | 将文本反馈转为 self-teacher 的密集监督。当后续训练本身已有丰富反馈时，额外 warmup 的优势可能缩小；这是需要实测的边界。 | 科学问答、ToolAlpaca、LiveCodeBench；准确率、固定时间表现、采样效率。 |
### 3.2 ACL 2026
其中 **CurioSFT、RSR、Prefix OPD、CRPS** 对方案设计尤其重要。
| 编号 | 论文与录用类别 | 主要发现及与本 idea 的关系 | 代表性评测 |
|---|---|---|---|
| 8 | **[Learning While Staying Curious: Entropy-Preserving Supervised Fine-Tuning via Adaptive Self-Distillation for Large Reasoning Models](https://aclanthology.org/2026.acl-long.617/)**，CurioSFT；Main | 自适应自蒸馏保留有用探索能力，并验证后续独立 GRPO 的收益。这是 warmup→RL 的直接竞品。 | AIME、AMC、MATH500、OlympiadBench、Minerva；Avg@8、Pass@32、OOD 准确率。 |
| 9 | **[Fast and Effective On-Policy Distillation from Reasoning Prefixes](https://aclanthology.org/2026.findings-acl.1276/)**；Findings | 只生成、蒸馏学生前缀，并逐步增加长度。指导范围与训练成本可以用简单调度改善。 | MATH500、AIME、GPQA、MMLU-Pro；平均准确率、FLOPs、GPU hours。 |
| 10 | **[Which Reasoning Trajectories Teach Students to Reason Better? A Simple Metric of Informative Alignment](https://aclanthology.org/2026.acl-long.1950/)**，RSR；Main | 用 token rank 与 surprisal 衡量教材对学生的适配度，预测蒸馏效果。价值估计器需要证明比这种廉价指标更能预测 post-RL 收益。 | AIME、AMC、MATH500；准确率、Spearman 排序相关性、选教师/选轨迹效果。 |
| 11 | **[Find Your Optimal Teacher: Personalized Data Synthesis via Router-Guided Multi-Teacher Distillation](https://aclanthology.org/2026.acl-long.666/)**，PerSyn；Main | 根据质量与学生可学性训练 query router，先选教师再生成。调用前路由已有先例。 | IFEval、TruthfulQA、LiveBench、GSM8K、MATH；任务分数与数据生成成本。 |
| 12 | **[Skill-Aware Data Selection and Fine-Tuning for Data-Efficient Reasoning Distillation](https://aclanthology.org/2026.acl-short.49/)**；Main Short | 按学生薄弱技能选训练数据。进一步的问题是：哪些薄弱技能值得用指导解决，哪些交给 RL 更划算？ | AMC、AIME、MATH Level-5、OlympiadBench；Avg@8、分技能准确率变化。 |
| 13 | **[Stable On-Policy Distillation through Adaptive Target Reformulation](https://aclanthology.org/2026.findings-acl.2094/)**，Veto；Findings | 在 logits 空间构造 teacher/student 混合目标，控制监督强度与稳定性。可作为学习监督分布时的简单参数化起点。 | GSM8K、HumanEval、DialogSum；accuracy、Pass@1/10、胜率。 |
| 14 | **[CRPS: Curriculum Replay via Progressive Suffixes from Successful Trajectories for Long-Horizon LLM Agents](https://aclanthology.org/2026.findings-acl.680/)**；Findings | 从成功轨迹的后缀状态开始探索，并按能力调整难度。是必须考虑的无 teacher 探索基线。 | ALFWorld、WebShop；固定交互预算下的成功率、score、全失败组比例。 |
| 15 | **[ProCeedRL: Process Critic with Explorative Demonstration Reinforcement Learning for LLM Agentic Reasoning](https://aclanthology.org/2026.findings-acl.800/)**；Findings | process critic 发现差步骤，进行修正并混合引导轨迹训练。本 idea 需体现干预策略由后续学习效果来训练。 | MuSiQue、WebWalkerQA、GAIA、ALFWorld；QA 正确率、环境成功率。 |
### 3.3 NeurIPS 2026
下列论文已在 NeurIPS 2026 官方目录列出。录用与 proceedings 出版是不同状态。
| 编号 | 论文 | 主要发现及与本 idea 的关系 | 代表性评测 |
|---|---|---|---|
| 16 | **[A Few Teacher Steps Go a Long Way: Cost-Efficient On-Policy Data Augmentation for Agent Post-Training](https://neurips.cc/virtual/2026/poster/150832)**，OP-Short；[原文](https://arxiv.org/abs/2607.04574) | 在学生访问到的状态提供少量教师续写，可以获得很好的成本收益；指导长度并非越长越好。learned gate 必须胜过“随机选位置＋少量指导”。 | HotpotQA、ALFWorld、Terminal-Bench-Dev；成功率、教师生成成本与训练 token 成本。 |
| 17 | **[Beyond SFT-to-RL: Pre-alignment via Black-Box On-Policy Distillation for Multimodal RL](https://neurips.cc/virtual/2026/poster/153111)**，PRISM；[原文](https://arxiv.org/abs/2604.28123) | 在 SFT 与 RLVR 之间加入黑盒 OPD，改善后续 RL。OPD 前置改善 RL 已有正式录用工作。 | MathVista、MathVerse、MathVision、WeMath、MMMU 等；accuracy。 |
| 18 | **[Relaxed On-Policy Distillation: Selective Credit Allocation for Scaling Reasoning Efficiently](https://neurips.cc/virtual/2026/poster/150064)**，REOPOLD；[原文](https://arxiv.org/abs/2603.11137) | 通过 credit clipping、熵选 token、阶段调度控制教哪里、教多强、何时教。选择性监督本身已有充分先例。 | 数学、视觉、工具使用；准确率、样本效率、test-time scaling。 |
| 19 | **[The Many Faces of On-Policy Distillation: Pitfalls, Mechanisms, and Fixes](https://neurips.cc/virtual/2026/poster/153073)**；[原文](https://arxiv.org/abs/2605.11182) | 分析 teacher、loss、学生前缀导致的失配和训练崩溃。这是判断方案边界必须读的负结果论文。 | 数学、知识、行为评测；准确率、长度、重复率、稳定性。 |
| 20 | **[Your Teacher Can’t Help You Here: Combating Supervision Fidelity Decay in On-Policy Distillation](https://neurips.cc/virtual/2026/poster/154216)**，LGR；[原文](https://arxiv.org/abs/2605.30833) | 长学生前缀可能使 teacher 的指导失真；用 lookahead 信号缓解。失败状态可能恰恰是教师不可靠的状态。 | AIME、HMMT、LiveCodeBench；Mean@8、Pass@8、teacher 置信度与长度分析。 |
### 3.4 EMNLP 2026：机构公告录用，全文待核验
**SPEC-Distill: Towards Efficient Speculative Distillation for Reinforcement Learning with Verifiable Rewards**
- **录用证据**：厦门大学作者机构公告明确标注 EMNLP 2026 Main Conference Long paper；[作者机构录用公告](https://cdmc.xmu.edu.cn/info/1002/5654.htm)，[课题组论文列表](https://xmudeeplit.github.io/publication/)。
- **公告介绍的方法**：离线缓存教师轨迹，在线接受兼容前缀并由学生续写，后期切换到学生历史轨迹。涉及教师早期引导及其退出时机。
- **与本 idea 的关系**：是“早期教师指导、后续释放学生探索、控制教师成本”的近邻。
- **证据限制**：本次未找到公开全文，因此不补写未经核验的 benchmark 名称，也不把机构简介视为完整实验核验。
## 4. 最接近的预印本与创新边界
下表论文对新颖性的影响很直接。本次未核验到其在指定四会议的正式录用证据，未计入前面的 20 篇。
| 工作 | 已经覆盖的内容 | 本项目仍需证明的内容 |
|---|---|---|
| [From Imitation to Reward Discovery: On-Policy Warmup for Agentic RL / OPW](https://arxiv.org/html/2609.39436v1) | OPD warmup 后教师退出，再独立训练 agent RL；也讨论即时分数与后续学习价值的区别。 | 教学方式由后续 RL 反馈学出来，且优于固定 warmup。 |
| [Learning from the Near Future: Temporal Self-Distillation for RLVR / NPD、AutoNPO](https://arxiv.org/html/2604.20733v2) | 近未来教师、时间关系选择、自适应自举；已有固定 GPUh 的比较。 | 新学到的教学策略、价值估计与跨轮迁移带来额外收益。 |
| [RISE: Recursive Improvement via Self-Extrapolating Policy Distillation](https://arxiv.org/html/2609.05295v1) | 用自身 RL 更新方向外推 teacher，循环 RL 与 OPD。 | 除能力积累外，教学经验积累是否有独立贡献。 |
| [Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models](https://arxiv.org/html/2609.38025v1) | 根据一次加权 OPD 更新后的任务收益分配 token credit；teacher 冻结。 | 更长独立 RL 后果能否提供短期收益无法提供的教学信号。 |
| [Adaptive Teacher Exposure for Self-Distillation in LLM Reasoning / ATESD](https://arxiv.org/html/2605.11458v3) | 学习 teacher 看到多少参考推理；奖励包含后续蒸馏进展。 | 将目标延伸到独立 RL 的最终任务价值，证明这种延伸值得成本。 |
| [MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation](https://arxiv.org/html/2610.11989) | 通过虚拟 student 更新后的 reference loss，元学习 token 权重。 | 长期 RL 目标相对一步验证损失的必要性，以及监督内容变化的收益。 |
| [Sequential Beats Joint: On the Interplay between On-Policy Distillation and RLVR](https://arxiv.org/abs/2609.04108) | 系统比较 OPD→RL 与联合训练，并研究切换时机。 | 学习式调度是否优于验证分数驱动的简单切换规则。 |
| [RL Starts before RL: On Policy Distillation for Better Reinforcement Learning](https://arxiv.org/html/2609.28145v1) | 发现蒸馏目标在 RL 前后可能发生优劣反转，pre-RL Pass@k 也不能完全解释后续表现。 | 能否提前预测这些反转，并据此提高实际训练收益。 |
元教学的概念本身历史更早：[BERT Learns to Teach: Knowledge Distillation with Meta Learning，ACL 2022](https://aclanthology.org/2022.acl-long.485/) 已经根据蒸馏后学生的表现优化教师。Related work 应明确承接这条线。
另外，[TailSFT: Filtered Fine-Tuning Improves Post-Training Performance](https://arxiv.org/abs/2608.25756) 通过过滤已充分拟合的样本改善后续 RL 初始化，适合作为廉价 warmup 基线。
### 4.1 对原始 idea 的必要澄清
1. **NPD 与 AutoNPO 是同一论文中的机制。**
2. **ATESD 控制的是 teacher 看到的参考推理量**，进而改变 teacher 的监督分布；不等同于直接把提示暴露给 student。
3. **Dr. OPD 与 MetaOPD 主要学习监督权重**；仅改变 loss 权重不能直接表述为 teacher 学会生成新的监督内容。
4. **OPD warmup 后独立 RL 已有直接先例**，不能作为单独的核心创新。
5. **预算感知的自适应自举已有近邻**；完整成本核算很重要，但仅增加成本表不足以构成方法贡献。
## 5. 四个值得探索的核心问题
### 5.1 教学价值是否具有跨 RL 阶段的排序差异？
仅观察“指导后 RL 涨得更多”不够，因为初始分数低的模型本来就可能有更大的上涨空间。需要同时记录：
- warmup 结束时的任务质量；
- 相同后续 RL 条件下的最终质量；
- 相同总预算下的最终质量。
最有说服力的现象是：指导 A 的即时表现优于 B，但 B 在后续 RL 后稳定反超；而且这种反转不能被当前准确率、熵、Pass@k、RSR 等廉价指标充分预测。
[RL Starts before RL](https://arxiv.org/html/2609.28145v1) 已提供这种现象的证据，但其附录明确说明，现有比较不等于固定总成本下的效率比较。可以进一步研究如何预测并利用这种差异。
### 5.2 价值估计器能否预测指导的增量收益？
建议以如下量为目标：
$$
\Delta_B(a)=
\mathbb E\left[
J\left(\mathrm{RL}(\mathrm{OPD}_a(\theta),B-C_a)\right)
\right]
-
\mathbb E\left[
J\left(\mathrm{RL}(\theta,B)\right)
\right].
$$
其中：
- \(\theta\)：相同的起始学生状态；实现中还需控制 optimizer 等训练状态。
- \(a\)：指导方案。
- \(C_a\)：该方案消耗的教师与 warmup 成本。
- \(B\)：这次对照可用的训练预算。
- \(J\)：预先规定的任务评价。
两边比较的是：接受指导后使用剩余预算训练，和将预算全部投入直接 RL。外层学习、额外分支和选择用评测的成本还需计入完整方法的总账，不能仅通过这个局部目标忽略。
如果只训练“最终成功率预测器”，它很容易学到强学生和简单任务的分数更高，无法回答当前这次指导是否值得。
训练标签最好来自同 checkpoint、同 optimizer 状态、匹配任务流和随机种子的配对分支。不同策略生成的轨迹不必相同。观察性训练日志可用于补充，但不能自动赋予指导以因果信用。
### 5.3 监督分配与监督内容分别怎么学习？
| 操作 | 实际改变 |
|---|---|
| 调整 token loss 权重 | 哪些教师信号更受重视 |
| 查询前决定是否调用教师 | 教师预算分配 |
| 改变教师条件输入、教学内容或参数 | 教师给出的目标分布 \(q_T\) |
如果只实现前两项，论文应定位为学习监督分配策略。若要支持“学会怎样提供指导”，需要证明 \(q_T\) 实际改变，而且在固定调用预算下仍有收益。
先调用 teacher 获得熵/KL，再决定跳过指导，并没有省掉该次 teacher 调用。查询前 gate 应使用学生侧状态、历史失败、已有统计和剩余预算。
### 5.4 RSI 中教学经验是否有独立贡献？
“新学生更强，所以新一轮更好”不能证明教学策略在积累经验。应从完全相同的 student、teacher、optimizer 状态出发，比较：
| | 重置价值估计器 | 保留价值估计器 |
|---|---|---|
| 重置教学策略 | 基础对照 | 价值经验的作用 |
| 保留教学策略 | 教学策略迁移 | 完整迁移 |
历史教学标签缓存也要控制一致。先测冻结迁移，再给各组相同追加预算做适应。
如果下一轮 teacher 与 student 是同一个 checkpoint，且看到相同输入，则初始分布相同，普通 OPD 没有有效学习信号。必须明确下一轮指导的信息来源，例如参考解、失败诊断、近未来回滚或外推教师。[OPSD](https://arxiv.org/abs/2601.18734)、[NPD](https://arxiv.org/html/2604.20733v2)、[RISE](https://arxiv.org/html/2609.05295v1) 分别给出了不同选择。
## 6. 建议的最小可实现方法
以下是研究设计建议，不是文献已经证明有效的结论。
第一版保留固定的教师能力底座，训练一个小 controller 和一个收益估计器：
1. **学生状态输入**：近期成功率、全失败组比例、重复/无效动作、分技能表现、训练阶段和剩余预算。
2. **少量教学动作**：不指导、普通 teacher 条件、部分参考解条件、失败诊断条件。
3. **固定 OPD 协议**：teacher 在同一学生生成前缀上打分；参考信息只给 teacher。
4. **独立 RL continuation**：teacher 完全退出，用任务反馈训练学生。
5. **外层更新**：用配对收益训练 critic，并通过 contextual bandit 或策略梯度更新教学选择。
训练流程：
> 学生状态与剩余预算 → 查询前 gate 与教学条件选择 → OPD warmup → 独立 RL → 评价增量收益 → 更新教学策略和 critic → 在新学生状态上复用。
### 6.1 保持干预语义一致
应把 teacher 接管动作单独作为扩展实验。接管会改变学生访问的轨迹分布，和仅改变同一前缀上的蒸馏目标不是同一干预。
第一轮实验应固定蒸馏 loss、rollout protocol 和学生训练规则，先比较教学条件。随后再分别加入监督长度、强度和调用时机，减少混杂。
### 6.2 Critic 与教师更新之间的实际路径
不要默认 critic 能把梯度一路反传到 teacher。对于离散教学选择，可以用真实收益做 bandit 或 REINFORCE 更新；critic 用于预测、减少评估需求和降低方差。
如果进一步训练教师生成新的教学文本，需要单独定义可采样的内容生成策略及其更新规则。只选择固定菜单时，应准确声称学习了监督构造与分配策略。
必须保留一定随机探索和周期性的真实收益验证，防止策略利用 critic 的预测误差。
### 6.3 短期反馈与长期目标
最难的技术问题是短 RL 分支能否预测长 RL 收益。短程标签 \(\Delta_h\) 不等于最终 \(\Delta_B\)。
建议：
- 把 continuation 长度和剩余预算纳入 critic。
- 在多个 RL horizon 上检查指导排序是否保持。
- 定期用真实长程分支校准。
- 先做到 episode、turn 或 warmup-block 级别信用分配，再研究 token 级别。
## 7. Benchmark 建议
采用“可控机制实验＋多步 agent 主实验＋跨领域验证”。
| 用途 | 推荐 benchmark | 主要看什么 |
|---|---|---|
| 低成本机制实验 | [Reasoning Gym](https://github.com/open-thought/reasoning-gym)：Countdown、逻辑、图任务等 | 可控难度、技能组合、未见随机种子；适合研究哪种指导对后续学习有效。 |
| 第一主实验 | [ALFWorld](https://github.com/alfworld/alfworld) | 多步成功率、unseen 环境泛化、关键动作和错误恢复。 |
| 第二主实验 | [ScienceWorld](https://aclanthology.org/2022.emnlp-main.775/) | 成功率、normalized score、子目标完成情况；考察技能指导对长程任务的作用。 |
| Agent 外部验证 | [WebShop](https://arxiv.org/abs/2207.01206) | task score 与完整成功率同时报告，区分部分进展和完成任务。 |
| 数学泛化 | MATH500、OlympiadBench、AMC、AIME24/25 | 对照 PEAR、CurioSFT、EOPD、MetaOPD；AIME 题量小，不宜单独支撑主结论。 |
| 可选代码泛化 | [LiveCodeBench](https://livecodebench.github.io/leaderboard.html) | 固定版本与时间切片的 Pass@1/Pass@k、执行反馈后的学习收益。 |
**首篇推荐组合：Reasoning Gym 做机制，ALFWorld＋ScienceWorld 做主实验。** WebShop 或数学选一个作为额外泛化域即可。
大型真实浏览器、SWE-bench 类环境更适合后续扩展，因为它们会明显增加元训练分支的成本和方差。
ScienceWorld、WebShop 含部分进度反馈。如果论文强调稀疏奖励瓶颈，应明确训练用的 reward 设置，并让所有方法保持一致。
## 8. 评测指标与完整预算核算
### 8.1 必报指标
| 目标 | 必报指标 | 作用 |
|---|---|---|
| 最终任务能力 | 固定总预算下的 success rate、Pass@1、normalized score | 直接检验项目核心目标。 |
| 训练效率 | 达到预设质量的总成本；质量—成本曲线及 AUC | 避免只挑一个预算点；未达到目标的运行也要保留。 |
| 奖励发现 | 首次成功所需环境交互/算力；全失败 rollout group 比例 | 检验是否改善探索瓶颈。 |
| 探索保留 | Pass@k 曲线、有效解法/状态覆盖、重复动作率 | 区分单次成功率提升与成功轨迹可达性变化。 |
| 价值估计 | held-out Spearman/Kendall、动作排序准确率、选策后的真实收益与 regret | 相关性好不代表实际选出的策略好。 |
| 教学成本 | teacher scoring/generation tokens、调用数、实际 GPUh/FLOPs | 验证 gate 是否真的省钱。 |
| 跨轮积累 | 保留/重置教学经验的收益差、累计成本、旧能力保留 | 区分教学迁移、能力提升和遗忘。 |
### 8.2 区分 Avg@k、Pass@k 与 Pass^k
- **Avg@8**：八次采样的平均正确率，衡量平均单次表现。
- **Pass@8**：八次尝试中至少一次成功，衡量多次探索下的可达性。
- **Pass^8**：八次都成功，衡量稳定性。
不同论文命名并不完全一致，复现时应按计算定义对齐。
熵只能作为诊断指标：更高的熵可能只是更多无效输出。[CurioSFT](https://aclanthology.org/2026.acl-long.617/) 对此有直接讨论。有限次数采样均失败，也不能直接证明模型对成功轨迹的真实概率为零。
### 8.3 总成本
$$
C_{\mathrm{total}}=
C_{\mathrm{teacher}}
+C_{\mathrm{warmup}}
+C_{\mathrm{RL}}
+C_{\mathrm{extra\ branches}}
+C_{\mathrm{meta}}
+C_{\mathrm{evaluation}}.
$$
额外分支包括用于评价教学动作、最后没有被选中的训练；为教学策略生成标签的评测也算成本。各项应互不重复计账。
若专门训练能力 teacher，还应计入这部分，或明确它是所有方法共享的已有资源。
一个值得重视的例子：MetaOPD 在相同 696 次 student updates 下报告 **88.5 GPUh**，普通 OPD 为 **45.0 GPUh**，约 **1.97 倍**；该账目还未包含 evaluation/diagnostics。小 controller 不意味着小元训练成本。[MetaOPD，附录 B.6](https://arxiv.org/html/2610.11989)
分别报告两种场景：
1. **冷启动收益**：为当前训练从零学习教学策略，全部成本计入。
2. **复用收益**：教学策略已经学习过，在预先规定的多个新任务/学生上摊销成本，同时给出收回成本所需的运行次数。
同硬件 GPUh、FLOPs 和环境交互数都应保留。只匹配 student steps 或总 tokens，通常不足以支持固定预算主张。用于模型选择和超参数选择的资源也应清楚披露，并给基线合理、可比的调参预算。
## 9. 三阶段实验路线
### 9.1 第一阶段：证明存在可利用的教学差异
选择一个小规模学生，在两个能力阶段的 checkpoint 上比较四种动作：
1. 不指导，直接 RL。
2. 普通 OPD。
3. 部分参考条件 OPD。
4. 失败诊断条件 OPD。
两个 checkpoint × 四种动作 × 三个训练种子，共 **24 个 continuation 分支**，可以作为探索性试验。这里四种动作已经包含 no-guidance 对照。
固定蒸馏形式，记录不同 RL horizon 的曲线。三种种子只用于初步估计效应量和方差，不能同时承担训练策略、调参和最终验证。
首先回答：
- 哪种指导在相同总预算下最好？
- 最好的指导是否随学生阶段变化？
- 即时分数与最终分数是否发生稳定排序反转？
- 在候选动作中做理想选择，是否存在足够大的潜在收益？
理想选择只能作为诊断上限，不能把使用事后结果选动作的收益当作可部署算法的收益。
**如果候选动作之间几乎没有真实差异，或者最好的指导也无法覆盖其成本，暂时没有理由训练复杂 critic。**
### 9.2 第二阶段：证明长期反馈比廉价规则更有用
训练 controller/critic，并在未见任务、未见训练种子及未见 checkpoint 上测试。
| 基线 | 排除的替代解释 |
|---|---|
| 直接 RL，把预算用于更多训练/rollout | 改进是否只是额外算力。 |
| 普通 SFT→RL；适用时加 PEAR 或 CurioSFT | 简单 warmup 改造是否已经足够。 |
| 固定 OPD→RL，并调好 warmup 长度 | 是否只是选到了更好的阶段划分。 |
| 熵、成功率、RSR 等规则选择指导 | 是否真的需要学习长期价值。 |
| MetaOPD、Dr. OPD 或 ATESD 式短期反馈 | 较长独立 RL 反馈是否必要。 |
| RLAD 等教师持续参与的方法 | 教师退出的训练设计是否占优。 |
| Agent 上的 CRPS | 不增加教师的探索改进是否更划算。 |
数学场景还应考虑 [TailSFT](https://arxiv.org/abs/2608.25756) 这样的廉价初始化改进。
至少拆开四个消融：
- 只学 gate；
- 只学内容构造；
- 两者都学；
- 两者都固定。
还需比较即时任务回报、一步验证损失、短程独立 RL 收益和较长独立 RL 收益作为外层目标的区别。
### 9.3 第三阶段：验证递归教学
固定教师构造方式，进行多轮自举，对比：
- 同总预算的一次持续 RL；
- 固定教学规则的循环；
- 每轮重新学习教学策略；
- 保留教学策略与 critic 的循环；
- 适用的 RISE/AutoNPO 基线。
数据应区分 student-train、meta-train、meta-validation 和 final-test。相邻 checkpoint 不能随机混分后就视为跨阶段泛化。
最终实验同时报告训练种子间波动和测试样本不确定性。对测试题做 bootstrap 不能替代独立训练种子。
## 10. 可行性、失败条件与建议主张
### 10.1 有希望奏效的条件
- 学生已有基本能力，但正奖励仍难发现。
- 教师能可靠纠正少数关键决策。
- 不同学生阶段确实需要不同指导。
- 教学策略可以复用，减少每轮重新试错的开销。
现有文献对局部机制有较好的支持。完整的预算受限 RSI 方案，仍需要独立验证长期反馈可预测性、成本回收和跨轮迁移。
### 10.2 最可能的失败条件
- 直接 RL 已能充分探索，warmup 挤占了更有用的 RL 预算。
- 学生错误前缀让教师也无法提供可靠监督。
- 短程收益与长期收益相关性弱，critic 不断选错。
- 教学策略只能适配训练时见过的 checkpoint。
- 元训练开销大于后续节省，递归轮次又不足以摊销。
- 所谓教学经验收益实际来自更强的学生、更多历史标签或额外数据。
### 10.3 第一版论文主张
> 以学生后续独立 RL 的增量收益为反馈，学习适配学生状态的 OPD 指导策略，并验证其在完整训练预算下的收益与跨 checkpoint 迁移。
RSI 可以作为这个机制成立后的扩展。
最先值得得到的两张实验图：
1. **不同指导在 warmup 后与独立 RL 后的排序变化。**
2. **计入全部必要开销后的质量—总成本曲线。**
这两张图会直接决定价值估计器和递归教学是否值得继续投入。
## 11. 建议精读顺序
1. **OPW**：对齐 agentic OPD warmup→独立 RL 的基础流程。
2. **SOAR**：理解以学生训练进步优化教师的已有方法及外层成本。
3. **RL Starts before RL、PEAR、CurioSFT**：理解即时表现与后续学习价值的区别。
4. **MetaOPD、Dr. OPD、ATESD**：明确一步元目标、任务回报信用和延迟蒸馏反馈的边界。
5. **OP-Short、Prefix OPD、RSR、CRPS**：构建足够强的廉价指导与探索基线。
6. **RISE、NPD/AutoNPO**：设计下一轮教师来源与递归机制。
7. **The Many Faces of OPD、LGR**：检查教师失配、错误前缀和训练稳定性风险。
