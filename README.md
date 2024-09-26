## 这是什么？

这是一个借助于 GitHub Action 实现自动生成算法模板的项目！

- 你**不需要安装 Python 环境**；
- 你也并**不需要安装臃肿的 LaTeX 环境（你甚至不需要会 LaTeX 语法）**；
- 你**只需要提供你的模板文件并且加以简单配置**，就能借助 GitHub Action 生成你的模板 PDF 到 Releases 一栏！

具体生成结果可以参考本项目的 Releases 结果。

## 如何使用该项目？

你只需要的是：

1. Fork 该项目；
2. 把 Fork 后的项目 Clone 到本地；
3. 在 `templates` 目录下构建你自己的算法模板结构；
4. 修改项目根目录的 `config.yml`；
5. 运行项目根目录下的 `gen.sh` 或 `gen.ps1` 来生成模板目录的配置文件：

    例如：`./gen.sh -r ./templates` 或者 `.\gen.ps1 -r .\templates`，其中 `-r` 代表递归生成，`./templates` 指定需要生成配置文件的目录

6. 根据你期望的章节顺序或者章节名称对各个目录下的 `config.yml` 进行微调；
7. 提交修改，并 `push` 到 GitHub。

**Fork 后可能默认自动禁用 Action 功能，你需要在项目的 Actions 页面下开启 Action 功能**。

当一切准备完毕，你就可以通过以下步骤来构建你的模板文件：

```sh
# 给当前分支打 tag，tag 需要以 v 开头
git tag v1.0
# 推送 tag 到 GitHub
git push origin tag v1.0
```

此时就会触发 GitHub Action 构建你的模板文件！

在 Actions 页面会出现日志信息，当正确运行完毕，你就可以在项目的 Releases 页面发现你构建的 PDF 文件。

## 配置文件？

配置文件有两种，一种是项目根目录下的 `config.yml`，一种是算法模板目录下的 `config.yml`。

### 项目根目录的 `config.yml`

用于定义项目的元信息。

配置项|类型|描述
---|---|---
`root-directory`|String|指定算法模板目录
`latex-pre`|String|指定生成的 tex 文件的头部文件
`latex-post`|String|指定生成的 tex 文件的尾部文件
`title`|String|指定生成的 tex 文件的 title
`author`|String|指定生成的 tex 文件的 author

示例如下：

```yml
root-directory: templates
latex-pre: latex-pre.tex
latex-post: latex-post.tex
title: UESTC Nanana Templates
author: UESTC_Nanana
```

### 模板目录的 `config.yml`

配置项|类型|描述
---|---|---
`contents`|List|声明当前目录的组成结构

对于 `contents` List 的 Item 有两类：

一类是 `directory` 类型，该 Item 定义如下：

配置项|类型|描述
---|---|---
`name`|String|声明子目录显示名称
`directory`|String|指定子目录

一类是 `code` 类型，该 Item 定义如下：

配置项|类型|描述
---|---|---
`name`|String|声明该 code 名称
`code`|String|指定代码文件
`caption`|String|代码说明性文字
`code-pre`|String|在代码之前的说明性文字
`code-post`|String|在代码之后的说明性文字

示例如下：

```yml
contents:
  - name: 流
    directory: 流
  - name: 最近公共祖先
    code: lca.cpp
    code-pre: lca-pre.tex
    code-post: lca-post.tex
  - name: 树状数组
    caption: optional
    code: fenwick-tree.cpp
  # 如果未配置 code，就代表只会生成对应的文本
  - name: 排列组合
    code-pre: 排列组合-pre.tex
```

## gen.sh 和 gen.ps1 的生成逻辑？

`-r` 选项可以启用递归模式。

对于指定的目录而言：

对于子目录，生成对应子章节，如果启用递归模式，就会递归下去。

对于 `x.cpp`，`x-pre.tex` 和 `x-post.tex` 文件，会自动组装成一项到配置文件中，这三者可以自由搭配组合。

## 注意事项

1. Fork 后可能默认自动禁用 Action 功能，你需要在项目的 Actions 页面下开启 Action 功能；
2. 请使用 `UTF-8` 编码；
3. 使用 `/` 作为路径分隔符，不要使用 `\`；
4. 模板目录深度不要过深！可以将本项目示例中的 `maxFlow.cpp` 作为可以接受的最深深度；

## 更多的自定义

### 我想要修改格式

你可以通过更改 `latex-pre.tex` 和 `latex-post.tex` 达成效果。

### 我想要更改字体

你可以通过更改修改 `script.sh` 文件修改下载的字体，并在 `latex-pre.tex` 中指定字体。