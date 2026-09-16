# ChemDatabase

一个用于 ChemDraw 结构图查看与标注的最小原型。

## 功能

- 打开 ChemDraw `.cdxml` 文件（以及包含 CDXML 文本的 `.cdx` 文件）
- 在画布上绘制原子与化学键
- 点击每个化学原子并添加自定义标签
- 在右侧列表中查看已添加的标签

## 运行

```bash
python cdx_tagger.py
```

或直接打开指定文件：

```bash
python cdx_tagger.py /absolute/path/to/file.cdxml
```

## 测试

```bash
python -m unittest discover -s tests
```

> 说明：当前原型不能直接解析二进制 ChemDraw `.cdx` 文件。请先在 ChemDraw 中导出为 `.cdxml`，即可完整使用绘图与标注功能。
