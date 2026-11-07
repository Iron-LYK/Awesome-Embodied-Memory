# 贡献指南

[English](CONTRIBUTING.md)

请带来原始来源，以及具体的记忆机制说明。论文不必在标题中包含 memory，但纳入理由必须明确。纠正边界或移除无依据主张，与新增论文同样有价值。

## 新增研究文献

1. 先按未带版本号的 arXiv ID、DOI 和规范化标题检查 `data/papers.json`。同一工作的期刊或会议版本不自动算作另一篇。
2. 核验标题、作者、首次发表日期、实际来源版本与原始链接。保存 SHA-256，并说明哈希对应的内容。不能用访问日期代替发表日期。
3. 阅读足够的来源，确认保留的信息、持续范围和消费者。允许摘要级筛选，但必须明确标注，不能称为全文审计。依据不足时标为背景或暂缓纳入。
4. 在 `data/taxonomy.json` 中选择唯一的 `primary_domain` 和 `method_family`，以机制标签表达交叉关联。`primary/context/survey` 描述相关性，不代表阅读深度或同行评审状态。
5. 独立撰写双语 `summary_en/zh` 与 `analysis_en/zh`。前者归纳来源，后者给出局限、比较或研究问题。不能编造量化收益、硬件条件、消融或发表状态。
6. 保留双语纳入理由、真实 `review_depth`、证据定位、发现来源和 BibTeX，以 `first_included`、`inclusion_batch` 追踪版本。

校验器给出可执行的数据约束。已有记录保留旧分类，配套综述仍可使用独立的固定语料。

## 新增或更新实现观察

修改 `data/implementations.json`。记录固定提交、文件与行号、启用配置、状态寿命、重置行为、消费及交接接口。六个证据轴和部署备注均需双语。未核实独立论文时保留 `方法名: TODO ref`；父模型论文不能自动代替新实现论文。PR 更新后保留此前核查过的提交，不能静默转移结论。

待匹配论文的方法在统一 Research 目录中以“待正式发表的方法”筛选。核实匹配论文后填写 `related_ids`，构建器会将部署核查附在论文详情并保留旧 ID 映射；不能只因共享基模而合并不同方法。真实项目库的 README 代码入口显示实时 Star，benchmark PR／分支证据保留普通 Code 链接。

## 构建与检查

只需 Python 3.9+；网站没有运行时依赖。

```sh
python3 scripts/validate.py
python3 scripts/build.py
python3 scripts/check_site.py
node --check website/assets/app.js
node --check website/assets/i18n.js
node --check website/assets/constellation.js
python3 -m http.server 8765 --directory website
```

检查中英文切换、领域与方法筛选、空结果、论文与实现详情、引用导出，以及三项对比。不要手改生成的 README 或 `website/assets/catalogue.*`。

## 证据与权限

AI 辅助不得伪装为独立人工精读。明确保留有歧义或缺少证据的结论边界。公开包不加入私人实验、凭据、完整论文 PDF、复制的第三方源码树或原始作者摘要。整理内容按 CC BY 4.0 贡献，代码按 MIT 贡献，具体范围见 [NOTICE.md](NOTICE.md)；只贡献有权授权的材料。

## 表格短句与资源链接

每篇论文新增 `tldr_en` 和 `tldr_zh`：完整的一句话，建议英文 12–22 词、中文 25–55 字符，上限分别为 30 词与 75 字符。保留训练期检索等重要边界；完整简介与分析仍放在详情中。

`code_url`、`project_url` 必须有匹配的 `link_evidence` 来源、日期与字段。空仓库、仅网页模板、即将开源的承诺或重定向到另一作品的仓库，不展示普通 Code 图标；保留历史链接和状态以供后续更新。`publication_label` 需要 `publication_evidence`，区分作者自报会议与出版社独立核查，勿把首次 arXiv 日期改称会议发表日期。

视觉改动需检查星图与目录联动、年份筛选、键盘导航、动画暂停／减少动态效果和移动布局。星图连接表示编辑分类，不表示引用关系或性能排名。
