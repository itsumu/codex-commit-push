# codex-commit-push

**简体中文** | [English](README.en.md)

让 Codex 根据真实 Git diff 撰写提交说明、创建提交，再把当前分支推送到指定远端。它在本机调用 Codex CLI 和 Git，不托管代码，也不需要额外的 GitHub Token。

## 安装

需要 Git、Python 3 和已登录的 Codex CLI；推送沿用本机 Git 的认证。以下命令适用于 macOS 和 Linux：

```sh
git clone https://github.com/itsumu/codex-commit-push.git
cd codex-commit-push
sh install.sh
```

安装器将 skill 复制到 `${CODEX_HOME:-$HOME/.codex}/skills/commit-push`，并添加用户级 Git 别名。不覆盖同名但内容不同的 skill 或别名。

## 使用

在要提交的仓库内运行：

```sh
git codex-push
```

也可以在 Codex 对话中输入 `$commit-push`。这会请求**提交并推送**，不仅是预览提交说明。若已暂存文件，默认只提交暂存内容；否则由 Codex 审阅工作区，选取相关改动。没有改动时不创建空提交。多个仓库并列时，可以用 `git -C <仓库路径> codex-push` 明确指定目标。

Codex 会展示拟用的提交说明、范围、目标远端和分支。发布脚本核对 HEAD、分支和已审阅的暂存树，保留 Git hooks 与签名设置，不使用强推。推送被拒绝时，本地提交仍保留。模型对差异或敏感信息的判断不是保证，请留意提交范围。

## 验证

在本工具的仓库目录中运行测试。测试只向临时本地裸仓库推送：

```sh
python3 -m unittest discover -s tests
```

## 卸载

在本工具的仓库目录中运行：

```sh
sh install.sh --uninstall
```

卸载仅移除与当前发行内容一致的 skill 文件和别名，不会删除仓库或撤销提交。
