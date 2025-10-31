# 🌏 LVLangGen - LVGL 多语言文本系统

一个轻量、自动化的多语言文本管理框架，专为 LVGL (Light and Versatile Graphics Library) 设计。通过一个简单的 CSV 文件即可自动生成多语言表，实现 UI 文本的动态切换与递归更新。


## ✨ 特点
- 支持 简体中文 / English / 繁體中文
- 运行时动态切换语言，无需重新构建界面
- 自动递归更新所有绑定文本的 `lv_label`
- 通过 CSV 文件自动生成语言表 (`ui_language.h`/`.c`)
- 与原有 UI 逻辑零耦合
- 类型安全，兼容 32/64 位系统
- 纯 C 实现，适合嵌入式与桌面模拟器环境


## 📁 项目结构
```
lvgl_language_switching_management/
├── inc/
│   └── ui_language.h  # 自动生成的头文件
├── src/
│   └── ui_language.c  # 自动生成的源文件
├── tools/
│   └── gen_lang_table.py  # CSV 转换脚本
├── language.csv  # 多语言文本表
└── README.md  # 项目说明
```


## 🚀 使用方式
1. **创建标签并绑定文本 ID**
   ```c
   lv_obj_t *label = lv_label_create(parent);
   lv_label_set_text(label, get_label_text(TEXT_HORIZONTAL));
   lv_obj_set_user_data(label, (void *)(uintptr_t)TEXT_HORIZONTAL);
   ```

2. **动态切换语言并刷新 UI**
   ```c
   set_language(LANG_EN);
   update_label_text_recursive(lv_scr_act());
   ```

所有绑定了 `user_data` 的 `lv_label` 会自动更新为当前语言。


## 📄 CSV 文件格式
`language.csv` 是项目的语言资源表，只需维护这一份文件。缺失字段会在生成时警告，每个 `id` 必须唯一。

| id            | cn    | en        | tc    |
|---------------|-------|-----------|-------|
| TEXT_HELLO    | 你好  | Hello     | 你好  |
| TEXT_EXIT     | 退出  | Exit      | 離開  |
| TEXT_CONFIRM  | 确认  | Confirm   | 確認  |
| TEXT_TIMEZONE | 时区  | Time Zone | 時區  |


## ⚙️ 自动生成语言表
在终端执行以下命令，自动生成 `ui_language.h` 和 `ui_language.c`：
```bash
cd tools
python3 gen_lang_table.py
```

执行后会在 `inc/` 和 `src/` 目录下生成对应的语言表文件。


## 🔍 API 说明

| 函数名                          | 功能描述                                  |
|---------------------------------|-------------------------------------------|
| `set_language(lang_t lang)`     | 设置当前语言（可选值：`LANG_CN` / `LANG_EN` / `LANG_TC`） |
| `get_label_text(text_id_t id)`  | 获取指定 ID 对应的当前语言文本            |
| `update_label_text_recursive(lv_obj_t *parent)` | 递归更新指定父容器下所有绑定文本 ID 的标签 |


## 🧰 示例
```c
// 切换为繁体中文并刷新整个屏幕的标签
set_language(LANG_TC);
update_label_text_recursive(lv_scr_act());
```


## 🧑‍💻 开发者信息
- Author: daijiale1396
- Version: 1.0.0
- License: MIT
- Repository: https://github.com/Dai1396/LVLANG.git
- Description: Lightweight multilingual UI text management system for LVGL


## 📜 开源协议（MIT License）
Copyright (c) 2025 daijiale1396

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## 🌈 展望
- JSON / YAML 格式语言文件支持
- 自动 UI 扫描与文本绑定
- 更多语言支持（如日语、德语等）
- LVGL 编辑器插件自动集成

让 LVGL 的国际化更简单、更优雅、更自动化。