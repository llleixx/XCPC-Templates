import posixpath

import yaml


def get_config(directory):
    config_file = posixpath.join(directory, "config.yml")
    if not posixpath.exists(config_file):
        config_file = posixpath.join(directory, "config.yaml")
        if not posixpath.exists(config_file):
            raise FileNotFoundError(f"config.yml not found in {directory}")

    with open(config_file, "r", encoding="UTF-8") as f:
        config = yaml.safe_load(f)

    if config is None:
        raise Exception(f"config.yaml has an error in {directory}")

    return config


# 生成代码块 LaTeX 内容
def generate_latex_for_item(directory, item, depth):
    latex_parts = []

    # 添加 section/subsection 之类的标题
    if depth == 0:
        latex_parts.append(f"\\section{{{item['name']}}}\n")
    elif depth == 1:
        latex_parts.append(f"\\subsection{{{item['name']}}}\n")
    elif depth == 2:
        latex_parts.append(f"\\subsubsection{{{item['name']}}}\n")
    else:
        # TODO: delete
        latex_parts.append(f"\\paragraph{{{item['name']}}}\n")

    # 处理 pre-file 内容
    if "code-pre" in item:
        pre_file_path = posixpath.join(directory, item["code-pre"])
        if posixpath.exists(pre_file_path):
            with open(pre_file_path, "r", encoding="UTF-8") as pre_file:
                latex_parts.append(pre_file.read())
                latex_parts.append("\n")

    # 处理代码文件
    if "code" in item:
        code_file_path = posixpath.join(directory, item["code"])
        caption = item.get("caption", "")
        if posixpath.exists(code_file_path):
            latex_parts.append(
                f"\\lstinputlisting[caption={{{caption}}}]{{{code_file_path}}}\n"
            )

    # 处理 code-post 内容
    if "code-post" in item:
        suf_file_path = posixpath.join(directory, item["code-post"])
        if posixpath.exists(suf_file_path):
            with open(suf_file_path, "r", encoding="UTF-8") as suf_file:
                latex_parts.append(suf_file.read())
                latex_parts.append("\n")

    return "\n".join(latex_parts)


# 递归处理目录中的内容
def generate_latex_from_config(directory, depth=0):
    config = get_config(directory)

    latex_sections = []
    for item in config.get("contents", []):
        if "directory" in item:  # 处理子目录
            subdir_path = posixpath.join(directory, item["directory"])
            latex_sections.append(generate_latex_for_item(directory, item, depth))
            latex_sections.append(generate_latex_from_config(subdir_path, depth + 1))
        else:  # 处理文件项
            latex_sections.append(generate_latex_for_item(directory, item, depth))

    return "\n".join(latex_sections)


# 生成 LaTeX 文档
def generate_latex(root_dir):
    config = get_config(root_dir)

    # 加载前文和后文
    latex_pre = ""
    latex_post = ""

    # 处理 pre-latex
    if "latex-pre" in config:
        pre_file_path = posixpath.join(root_dir, config["latex-pre"])
        if posixpath.exists(pre_file_path):
            with open(pre_file_path, "r", encoding="UTF-8") as pre_file:
                latex_pre = pre_file.read()

    title = config.get("title", "UESTC Nanana Templates")
    author = config.get("author", "UESTC_Nanana")

    latex_pre = latex_pre.replace("{PLACEHOLDER:TITLE}", title).replace(
        "{PLACEHOLDER:AUTHOR}", author
    )

    # 处理 latex-post
    if "latex-post" in config:
        post_file_path = posixpath.join(root_dir, config["latex-post"])
        if posixpath.exists(post_file_path):
            with open(post_file_path, "r", encoding="UTF-8") as post_file:
                latex_post = post_file.read()

    # 代码根目录
    code_root = config.get("root-directory", "./templates")

    # 生成中间内容
    latex_content = generate_latex_from_config(posixpath.join(root_dir, code_root))

    # 最终拼接 LaTeX 文档
    return latex_pre + latex_content + latex_post


# 写入 LaTeX 文件
def write_latex_file(latex_content, output_file):
    with open(output_file, "w", encoding="UTF-8") as f:
        f.write(latex_content)


if __name__ == "__main__":
    root_dir = "./"  # 根目录

    latex_content = generate_latex(root_dir)
    config = get_config(root_dir)

    output_file = "output.tex"
    write_latex_file(latex_content, output_file)
    print(f"LaTeX 文件已生成：{output_file}")
