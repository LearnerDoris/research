# 投研档案库 · Quartz 起步包

把 Obsidian 笔记发布成一个公开网站，类似 Becks Research Archive 那样，但功能更强 —— 双向链接可点击、关系图谱可视化、全站搜索、自动索引。

## 整体架构

```
你的电脑                       GitHub                   公网访问
  │                              │                         │
  ▼                              ▼                         ▼
Obsidian → 写笔记 → git push → GitHub Actions → GitHub Pages
                                  自动构建        https://你的用户名.github.io/research/
```

## 一次性环境准备（约 30 分钟）

### Step 1：装三样东西

1. **Git** — [git-scm.com](https://git-scm.com/downloads)
2. **Node.js** v22 或更高 — [nodejs.org](https://nodejs.org)（选 LTS 版）
3. **Obsidian** — [obsidian.md](https://obsidian.md)

装完打开终端（Mac 用 Terminal，Windows 用 PowerShell），输入下面命令验证：

```bash
git --version
node --version    # 必须 >= 22
npm --version
```

### Step 2：注册 GitHub 账号

去 [github.com](https://github.com) 注册。假设你的用户名是 `doris-w`。

### Step 3：克隆 Quartz

```bash
# 选一个你喜欢的目录，比如 ~/Documents
cd ~/Documents

# 克隆 Quartz 官方仓库
git clone https://github.com/jackyzha0/quartz.git research
cd research

# 安装依赖
npm install

# 初始化 Quartz
npx quartz create
```

初始化时它会问几个问题，按下面选：

- **Choose how to initialize the content** → 选 `Empty Quartz`
- **Choose how Quartz should resolve links** → 选 `Treat links as shortest path of note file name`

完成后，你就有了一个空的 Quartz 站点骨架。

### Step 4：替换配置文件

把本起步包里 `quartz.config.ts` 的内容，覆盖到 `research/` 目录下的同名文件。这是已经为投研场景调好的配置（中文界面、研究档案分类、关系图启用等）。

### Step 5：导入起步内容

把本起步包 `content/` 文件夹里的所有内容，复制到 `research/content/` 目录下。这是预设好的：

```
content/
├── index.md              （首页：投研档案库目录）
├── stocks/               （个股研究）
│   ├── _index.md
│   └── 示例-FCX-2026-Q1.md
├── weekly/               （周报/月报）
│   ├── _index.md
│   └── 示例-周报-2026-W18.md
├── daily/                （每日简报）
│   ├── _index.md
│   └── 示例-日报-2026-05-04.md
├── events/               （事件/会议笔记）
│   ├── _index.md
│   └── 示例-EY家办税务-2026-04.md
└── frameworks/           （研究框架与方法论）
    ├── _index.md
    └── 示例-六Agent投研框架.md
```

### Step 6：本地预览

```bash
npx quartz build --serve
```

打开浏览器访问 `http://localhost:8080`，看到你的站点了。每次改 `content/` 里的笔记，刷新即可看到变化。

### Step 7：发布到 GitHub Pages

**7.1 在 GitHub 上建一个新仓库**

去 GitHub，新建仓库名为 `research`（必须 Public），**不要**勾选任何初始化选项（README、.gitignore 等都不要）。

**7.2 把本地仓库推上去**

```bash
git remote set-url origin https://github.com/你的用户名/research.git
git add .
git commit -m "Initial setup"
git push -u origin v4
```

**7.3 配置 Pages**

在 GitHub 仓库页面：
- 点 `Settings` → `Pages`
- `Source` 选 `GitHub Actions`

**7.4 添加 Actions 工作流**

把本起步包 `.github/workflows/deploy.yml` 复制到你仓库的同名路径，然后：

```bash
git add .github
git commit -m "Add deploy workflow"
git push
```

推送后，GitHub 会自动构建。等 1-2 分钟，访问：

```
https://你的用户名.github.io/research/
```

站点就上线了。

## 日常工作流（30 秒发布新研报）

1. 在 Obsidian 里打开 `research/content/` 这个文件夹（作为 Vault）
2. 在对应分类目录下新建笔记（比如在 `stocks/` 下新建 `HWM-2026-05-10.md`）
3. 用模板（见 `templates/` 目录）填好 frontmatter 和内容
4. 终端运行：

```bash
cd ~/Documents/research
npx quartz sync
```

这一条命令会：自动 commit + push 到 GitHub → GitHub Actions 自动构建 → 站点 1-2 分钟内更新。

## 双向链接的妙用

在写新研报时，如果引用了之前的笔记，用 `[[ ]]` 包起来：

```markdown
FCX 的分析参考了 [[六Agent投研框架]] 的方法论。
对比标的见 [[HWM-2026-04-20]]。
```

发布到网站后，这些链接**都是可点击的**，访客能像逛 Wikipedia 一样浏览你的研究网络。**右下角的关系图谱**会把所有笔记的连接关系画成一张网。

## 进阶：选择性发布

如果某些笔记你不想公开（比如个人持仓、内部判断），在 frontmatter 里加 `draft: true`：

```yaml
---
title: 我的持仓快照
draft: true
---
```

带 `draft: true` 的笔记不会出现在网站上，但仍在你的 Obsidian 库里。

## 常用命令速查

```bash
npx quartz build --serve    # 本地预览
npx quartz sync             # 同步到 GitHub（= add + commit + push）
npx quartz update           # 升级 Quartz 本身到最新版
```

## 出问题怎么办

- **本地预览页面空白** → 检查 `quartz.config.ts` 里的 `baseUrl` 是否注释掉了（本地预览时应注释掉）
- **GitHub Actions 构建失败** → 仓库 Actions 标签页看错误日志，常见是 Node 版本不对
- **站点上线但样式乱** → `baseUrl` 必须是你的实际 GitHub Pages 地址，比如 `doris-w.github.io/research`

---

接下来读三个文件就能上手：

1. **`quartz.config.ts`** — 站点配置
2. **`content/index.md`** — 首页内容
3. **`templates/`** — 四种研报模板，写新内容时直接复制
