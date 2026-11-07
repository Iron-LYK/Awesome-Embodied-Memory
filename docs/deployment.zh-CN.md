# 发布项目库与网站

[English](deployment.md)

- 项目仓库：[Iron-LYK/Awesome-Embodied-Memory](https://github.com/Iron-LYK/Awesome-Embodied-Memory)
- 首次部署成功后的网址：[iron-lyk.github.io/Awesome-Embodied-Memory/](https://iron-lyk.github.io/Awesome-Embodied-Memory/)

两个地址已写入 `data/project.json`。准备好本地文件不等于已经上传仓库或部署网站。

## 应上传哪些文件

将干净的 **`Awesome-Embodied-Memory` 文件夹内的全部内容**上传到仓库根目录。不能只上传 README：分类图、链接徽章和文档是独立文件；保留数据和构建脚本，才能让 README、统计图和网站持续同步。

| 路径 | 用途 |
|:---|:---|
| `README.md`、`assets/` | 英文文献目录、分类图、本地链接徽章 |
| `data/`、两个 `.bib` 文件 | 规范条目、分类、来源元数据和引用 |
| `scripts/` | 校验、生成目录与分类图、导出干净发布包 |
| `docs/`、`CONTRIBUTING*` | 分类依据、来源说明、维护和部署指南 |
| `LICENSE*`、`NOTICE.md` | 整理内容 CC BY 4.0，网站及构建代码 MIT |
| `website/` | 双语静态网站及其全部资源 |
| `.github/`、`.gitignore` | 质量检查、手动 Pages 部署、贡献模板 |

独立的 **`Awesome-Embodied-Memory-website` 文件夹**与源码中的 `website/` 内容一致，可单独交给其他静态托管服务。使用下述 Pages 方案时，不用再创建一个网站仓库。发布目录已排除开发缓存、旧图、预览截图、本地工作日志、私人 PDF 和投稿论文文件。

## 1. 上传源码

以下命令适用于目标仓库尚无提交的情况。在干净的源码文件夹内运行，GitHub 身份验证沿用你本机的正常方式：

```sh
git init -b main
git add .
git commit -m "Initial public release"
git remote add origin https://github.com/Iron-LYK/Awesome-Embodied-Memory.git
git push -u origin main
```

如果远程仓库已经有提交，先 clone，再把干净文件复制进去提交，不要覆盖已有历史。仓库根目录应直接出现 `README.md`、`.github/` 和 `website/`，不要再套一层项目文件夹；隐藏的 `.github/` 也需要上传。

GitHub Description 可填写：

> A curated collection of embodied memory research for world models & WAM, VLA, and agentic robotics — with papers, code, and an interactive atlas.

README 保持英文，网站支持中英文切换。网站顶部项目名已链接到真实仓库。

## 2. 启用 GitHub Pages

进入仓库 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。

然后进入 **Actions → Deploy website → Run workflow**，选择 `main` 并运行。随附的 `.github/workflows/pages.yml` 会校验数据、重新构建网站，并仅部署 `website/`。成功后可从部署结果中打开网址；首次上线可能需要几分钟。

这是 GitHub 的项目站点，网址将是 `https://iron-lyk.github.io/Awesome-Embodied-Memory/`。**无需额外创建 `iron-lyk.github.io` 仓库。** 网站使用相对资源路径，支持这个项目子目录。依据见 GitHub 官方[站点地址规则](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)和[自定义工作流部署说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

部署由你手动触发：普通 push 只做质量检查，不自动上线。今后更新后，准备发布时再次运行 **Deploy website** 即可。不需要自定义域名、后端、Node 依赖安装或外部字体服务。

## 3. 创建版本 Release（可选）

GitHub 的 **Release** 用于记录版本，与上传 README、部署 Pages 是三件独立的事。首次提交且检查通过后，进入 **Releases → Draft a new release**，创建标签 `v1.0.0`、目标选择 `main`，填写更新说明后发布。GitHub 会自动提供源码压缩包；也可额外附上下面生成的网站 ZIP。

## 后续维护与打包

修改 `data/` 内的规范记录或 `website/` 内的网站源文件后运行：

```sh
python3 scripts/validate.py
python3 scripts/build.py
python3 scripts/check_site.py
python3 scripts/package_release.py
```

最后一条命令在已忽略的 `dist/` 内生成干净源码目录、网站目录、ZIP 包、SHA-256 文件清单和校验和。导出使用明确白名单，并验证新源码目录可以独立重新构建。不要把 `dist/` 上传仓库。

本地预览：

```sh
python3 -m http.server 8765 --directory website
```

打开 `http://localhost:8765/?lang=en` 或 `http://localhost:8765/?lang=zh`。独立网站导出目录也可用相同方式启动，只需换成对应目录。`index.html`、`assets/`、`resources/` 必须一起保留。语言偏好和收藏只保存在访问者本地浏览器中。

发布前检查两种语言、领域／方法筛选及手机布局，并核对数量和引用状态。目录同时包含研究出版物和明确标注的待正式发表方法。持续更新目录不会改变配套论文的固定检索范围和证据声明。
