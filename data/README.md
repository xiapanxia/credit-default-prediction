# 数据说明 · Give Me Some Credit

## 来源

- 竞赛页：<https://www.kaggle.com/c/GiveMeSomeCredit>（2011 年 Kaggle 竞赛）
- 本仓库文件：`cs-training.csv`、`cs-test.csv`，为竞赛原始文件（未经二次清洗）
- 获取日期：2026-11-08

## 文件

| 文件 | 行数 | 列数 | 说明 |
|---|---|---|---|
| `cs-training.csv` | 150,000 | 12 | 有标签；第 1 列是行号，无列名 |
| `cs-test.csv` | 101,503 | 12 | 无标签，用于生成提交文件 |

## 字段字典

| # | 字段 | 含义 |
|---|---|---|
| 1 | `SeriousDlqin2yrs` | **标签**：未来两年内是否出现 90 天以上严重逾期（1 = 是） |
| 2 | `RevolvingUtilizationOfUnsecuredLines` | 无担保循环额度使用率：信用卡与个人信用额度已用比例（除房贷车贷） |
| 3 | `age` | 借款人年龄 |
| 4 | `NumberOfTime30-59DaysPastDueNotWorse` | 30–59 天逾期次数（不含更严重的） |
| 5 | `DebtRatio` | 月负债支出 / 月收入（含房贷车贷等分期） |
| 6 | `MonthlyIncome` | 月收入 |
| 7 | `NumberOfOpenCreditLinesAndLoans` | 未结清的信贷笔数（信用卡 + 分期） |
| 8 | `NumberOfTimes90DaysLate` | 90 天以上逾期次数 |
| 9 | `NumberRealEstateLoansOrLines` | 房贷与房产抵押贷款笔数 |
| 10 | `NumberOfTime60-89DaysPastDueNotWorse` | 60–89 天逾期次数（不含更严重的） |
| 11 | `NumberOfDependents` | 除本人外的家属人数 |

## 已核实的脏数据（2026-11-08 实测，训练集）

| 问题 | 数量 | 占比 | 处理建议 |
|---|---|---|---|
| `MonthlyIncome` 缺失（字面值 `NA`） | 29,731 | 19.82% | 填补或加缺失指示变量；不可直接删（会丢五分之一样本） |
| `NumberOfDependents` 缺失（`NA`） | 3,924 | 2.62% | 填 0 或中位数 |
| 三个逾期字段同时出现 `98` | 264 | 0.18% | **特殊编码（拒绝透露/无记录）**，不能当真实次数 |
| 三个逾期字段同时出现 `96` | 5 | 0.003% | 同上 |
| `age` = 0 | 1 | — | 异常，按缺失或中位数处理 |
| `MonthlyIncome` = 0 | 1,634 | 1.09% | 低于任何合理收入，按缺失处理 |
| 正例 `SeriousDlqin2yrs` = 1 | 10,026 | **6.68%** | 类别不平衡，需采样/阈值/代价敏感处理 |

**关键坑**：三个逾期次数字段的 `96 / 98` 若被当作连续值，会把该字段均值拉高几十倍，直接污染特征与模型解释。这是这份数据最常被面试官追问的细节。

## 重新获取

数据体积较大，未纳入版本控制（见 `.gitignore`）。换机器时重新下载同名文件放到 `data/raw/` 即可：

```bash
curl -sL -o data/raw/cs-training.csv "https://cdn.jsdelivr.net/gh/streety/GiveMeSomeCredit@master/cs-training.csv"
curl -sL -o data/raw/cs-test.csv     "https://cdn.jsdelivr.net/gh/streety/GiveMeSomeCredit@master/cs-test.csv"
```
