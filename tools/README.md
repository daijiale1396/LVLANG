# LVLangGen

**LVLangGen** 是一个针对 **LVGL** 项目的多语言自动生成工具，  
由 Daijiale 开发，用于从 `language.csv` 自动生成 `ui_language.h` / `ui_language.c`。

## 功能
- 支持多语言文本映射（简体 / 英文 / 繁体）
- 自动检测重复 ID 和缺失字段
- 友好的彩色输出日志
- 轻量、纯 Python3 编写

## 使用方法
```bash
python3 gen_lang_table.py
