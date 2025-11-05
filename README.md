# 🌏 LVLangGen - LVGL 多语言文本系统

一个轻量、自动化的多语言文本管理框架，专为 LVGL (Light and Versatile Graphics Library) 设计。通过一个简单的 CSV 文件即可自动生成多语言表，实现 UI 文本的动态切换与递归更新。


## ✨ 特点
- 🌍 多语言动态支持：自动识别 CSV 中的语言列（如 cn, en, tc, jp, fr...），支持任意语言数量
- ⚙️ 运行时动态切换语言，无需重新构建或刷新界面结构
- 🔄 自动递归更新 所有绑定 text_id 的 lv_label，即时生效
- 🧱 CSV 自动生成语言表（ui_language.h / ui_language.c），完全免手动维护
- 🔒 类型安全且跨平台：兼容 32/64 位系统与不同编译器
- 💡 纯 C 实现，无外部依赖，适配嵌入式与 PC 模拟器
- ⚡ 脚本自动化工具链：tools/gen_lang_table.py 一键生成完整语言代码
- ✅ 提供网页可视化界面，无需命令行
- 🧾 易扩展结构：添加新语言仅需在 CSV 新增列，无需改动源文件


## 📁 项目结构
```
ubuntu@ubuntu:~/LVLang$ tree
.
├── docs
│   └── index.html   # 网页版图形化语言生成工具
├── inc
│   └── ui_language.h
├── language.csv
├── LICENSE
├── README.md
├── src
│   └── ui_language.c
└── tools
    ├── gen_lang_table.py   # 自动生成语言表的 Python 脚本
    └── README.md

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

##  🌐 图形化网页工具（HTML）
在 docs/index.html 中提供了一个可视化编辑界面，适合不想使用命令行的用户。直接用浏览器打开即可使用，无需编译或安装。
✨ 功能亮点

| 功能           | 说明    
|---------------|-------|
| 多语言编辑表格    | 可同时录入多国语言字符串  |
| 自动生成代码     | 实时显示 .c/.h 文件内容  |
| 预览与导出  | 一键导出代码压缩包  |
| TEXT_TIMEZONE | 时区  |
	
🖼️ 网页使用方式
打开 docs/index.html
在表格中输入文本 ID 和对应多语言内容
点击 “生成代码”
查看右侧 .h/.c 文件预览
点击 “导出代码”，下载到本地
将生成的文件放入 inc/ 与 src/ 目录下即可使用

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
- LVGL 编辑器插件自动集成

让 LVGL 的国际化更简单、更优雅、更自动化。