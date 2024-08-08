
def generate_markdown_table(headers, table_data):
    # 定义Markdown表格的头部
    markdown_table = '| ' + ' | '.join(headers) + ' |\n'
    # 定义Markdown表格的分割线
    markdown_table += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'

    # 遍历二维数组中的每一行数据
    for row in table_data:
        # 添加一行到Markdown表格
        markdown_table += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
    markdown_table += '\n\n'
    return markdown_table

def generate_param_table(params):
    table_data = []
    for param in params:
        table_data.append([param['name'], param['type'], param['description']])

    return generate_markdown_table(["命名", "类型", "描述"], table_data)

def generate_function(data: dict):
    markdown = ""

    markdown += f"{data['displayname']}\n\n"

    markdown += f"**所属类：{data['classname']}**\n\n"

    markdown += f"{data['description']}\n\n\n\n"

    if data['is_static']:
        markdown += f"静态节点\n\n"

    if data['is_blueprintAsyncActionBase']:
        markdown += f"**蓝图异步节点**\n\n"

    markdown += "\n\n"


    input_params = data['input_params']
    if len(input_params) != 0:
        markdown += f" - **输入**\n\n"
        markdown += generate_param_table(input_params)


    output_params = data['output_params']
    if len(output_params) != 0:
        markdown += f" - **输出**\n\n"
        markdown += generate_param_table(output_params)

    if data['is_blueprintAsyncActionBase']:
        markdown += f" - **委托输出**\n\n"

        delegate_params = data['delegate_params']

        markdown += generate_param_table(delegate_params)

    markdown += "\n\n"
    return markdown, data['category']

def generate_markdown(json_data: dict):
    markdowns = []

    ufunctions = json_data['ufunctions']
    for ufunction in ufunctions:
        markdown, category = generate_function(ufunction)
        markdowns.append((markdown, category))

    return markdowns


# 定义一个函数来构建层级化的字典
def build_hierarchy(articles):
    hierarchy = {}
    for content, path in articles:
        parts = path.split('|')
        current_level = hierarchy
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level['contents'] = current_level.get('contents', []) + [content]
    return hierarchy

# 定义一个函数来将层级化的字典转换为Markdown格式的字符串
def hierarchy_to_markdown(hierarchy, level=1):

    markdown = ""
    for key, value in hierarchy.items():
        if 'contents' in value:
            # print(value)
            # 如果是叶子节点，列出文章内容
            markdown += f"{'#' * level} {key}\n"
            for content in value['contents']:
                markdown += f"{'#' * (level + 1)} {content}\n"
        else:
            if key != 'contents':
                markdown += f"{'#' * level} {key}\n"

        # 递归处理子分类
        if isinstance(value, dict):
            markdown += hierarchy_to_markdown(value, level + 1)

    return markdown

