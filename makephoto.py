import pandas as pd

# 读取Excel文件
excel_file = 'D:\\Py\\forum\貼圖寫真.xls'
sheet_names=['貼圖_絲襪美腿','貼圖_清涼寫真','貼圖_歐美寫真','貼圖_性感激情','貼圖_ai寫真']

for sheet_name in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # 假设图片链接在名为 'Image Links' 的列中，描述在 'Alt Text' 列中（如果有）
    image_links = df[['url', 'title']].values.tolist()

    # 打开一个新的Markdown文件
    with open(f'{sheet_name}.md', 'w',encoding='utf-8') as f:
        for link, alt_text in image_links:
            # 生成Markdown格式的图片链接
            markdown_image_link = f'![{alt_text}]({link})\n'
            f.write(markdown_image_link)