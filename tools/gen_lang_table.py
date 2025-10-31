#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言表自动生成工具
==================
从 language.csv 自动生成：
    - inc/ui_language.h
    - src/ui_language.c

该脚本会：
    1. 检查 CSV 文件中是否有重复 ID;
    2. 检查缺少的语言字段；
    3. 检查是否使用了全角标点；
    4. 自动生成语言枚举、文本表与访问函数；
    5. 支持彩色输出提示。

----------------------------------------------------------
CSV 文件说明
----------------------------------------------------------
文件名: language.csv
编码: UTF-8 (无 BOM)
路径: 与本脚本同级或上一级目录的 language.csv

格式要求:
    第一行必须是表头: id,cn,en,tc

每一行定义一个文本常量，例如：

    id,cn,en,tc
    TEXT_OK,确定,OK,確定
    TEXT_CANCEL,取消,Cancel,取消
    TEXT_SAVE,保存,Save,儲存
    TEXT_LOAD,加载,Load,載入
    TEXT_FIRMWARE_UPGRADE,升级固件,Firmware,升級韌體
    TEXT_CONFIG_UPGRADE,升级配置,Config,升級配置

字段说明:
    id  —— 文本ID (必须唯一、全大写、以 TEXT_ 开头)
    cn  —— 简体中文文本
    en  —— 英文文本
    tc  —— 繁体中文文本

----------------------------------------------------------
生成文件说明
----------------------------------------------------------
1. ui_language.h
   定义语言枚举 (LANG_CN, LANG_EN, LANG_TC)
   定义文本 ID 枚举 (TEXT_XXX)
   声明访问函数:
       const char *get_label_text(text_id_t id);
       void set_language(lang_t lang);
       void update_label_text_recursive(lv_obj_t *parent);

2. ui_language.c
   包含实际的语言映射表 text_map[]
   实现语言切换与递归更新函数。

----------------------------------------------------------
运行方式:
----------------------------------------------------------
    python3 gen_lang_table.py

执行成功后，会在控制台显示：
    ✅ 已生成:
      - inc/ui_language.h
      - src/ui_language.c

----------------------------------------------------------
常见问题:
----------------------------------------------------------
❌ 找不到 language.csv
    → 检查 CSV 文件路径和名称。

❌ 重复 ID
    → 每个文本 ID 必须唯一。

⚠️ 缺少字段
    → 某个语言文本为空，将提示但不会中断生成。

⚠️ 使用了全角逗号
    → 建议改为半角 "," 以避免 CSV 解析错误。
"""

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INC = ROOT / "inc"
SRC = ROOT / "src"
CSV = ROOT / "language.csv"

HEADER_PATH = INC / "ui_language.h"
SOURCE_PATH = SRC / "ui_language.c"

# 彩色输出
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def color(text, col):
    return f"{col}{text}{RESET}"

def main():
    if not CSV.exists():
        print(color(f"❌ 找不到 {CSV}", RED))
        sys.exit(1)

    rows = []
    seen_ids = set()
    errors = 0

    with open(CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        line_num = 1
        for row in reader:
            line_num += 1
            row = {k: v.strip() for k, v in row.items()}
            rid = row.get("id", "")
            if not rid:
                print(color(f"⚠️ 第{line_num}行缺少 id，已跳过。", YELLOW))
                continue

            if rid in seen_ids:
                print(color(f"❌ 重复 ID: {rid} (第{line_num}行)", RED))
                errors += 1
            seen_ids.add(rid)

            # 检查空字段
            for lang in ["cn", "en", "tc"]:
                if not row.get(lang):
                    print(color(f"⚠️ {rid} 缺少 {lang.upper()} 字段", YELLOW))

            # 检查全角逗号
            for key, val in row.items():
                if "，" in val:
                    print(color(f"⚠️ {rid} ({key}) 使用了全角逗号，建议改成半角 ,", YELLOW))

            rows.append(row)

    if errors > 0:
        print(color(f"\n🚫 检测到 {errors} 个严重错误，请修复后再生成。", RED))
        sys.exit(1)

    HEADER_PATH.write_text(gen_header(rows), encoding="utf-8")
    SOURCE_PATH.write_text(gen_source(rows), encoding="utf-8")

    print(color(f"\n✅ 已生成:", GREEN))
    print(f"  - {HEADER_PATH.relative_to(ROOT)}")
    print(f"  - {SOURCE_PATH.relative_to(ROOT)}")

def gen_header(rows):
    enum_items = ",\n    ".join([r["id"] for r in rows])
    return f"""/**
 * @file ui_language.h
 * @brief LVGL 多语言自动生成头文件
 * @author daijiale1396
 * @date 2025-10-31
 * @generated Automatically by LVLangGen
 */

#ifndef UI_LANGUAGE_H
#define UI_LANGUAGE_H

#include "lvgl.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {{
#endif

typedef enum {{
    LANG_CN = 0,
    LANG_EN,
    LANG_TC,
    LANG_MAX
}} lang_t;

typedef enum {{
    {enum_items}
}} text_id_t;

const char *get_label_text(text_id_t id);
void set_language(lang_t lang);
void update_label_text_recursive(lv_obj_t *parent);

#ifdef __cplusplus
}}
#endif

#endif // UI_LANGUAGE_H
"""

def gen_source(rows):
    table_entries = []
    for r in rows:
        table_entries.append(
            f'    {{ {r["id"]}, "{r["cn"]}", "{r["en"]}", "{r["tc"]}" }}'
        )

    table_text = ",\n".join(table_entries)

    return f"""/**
 * @file ui_language.c
 * @brief LVGL 多语言自动生成源文件
 * @author daijiale1396
 * @date 2025-10-31
 * @generated Automatically by LVLangGen
 */

#include "ui_language.h"

static lang_t current_lang = LANG_CN;

typedef struct {{
    text_id_t id;
    const char *cn;
    const char *en;
    const char *tc;
}} text_map_t;

static const text_map_t text_map[] = {{
{table_text}
}};

const char *get_label_text(text_id_t id)
{{
    for (size_t i = 0; i < sizeof(text_map) / sizeof(text_map[0]); ++i) {{
        if (text_map[i].id == id) {{
            return current_lang == LANG_CN ? text_map[i].cn :
                   current_lang == LANG_EN ? text_map[i].en :
                   text_map[i].tc;
        }}
    }}
    return "";
}}

void set_language(lang_t lang)
{{
    if (lang < LANG_MAX) current_lang = lang;
}}

void update_label_text_recursive(lv_obj_t *parent)
{{
    if (!parent) return;

    int32_t i = 0;
    lv_obj_t *child = NULL;
    while ((child = lv_obj_get_child(parent, i)) != NULL) {{
        if (lv_obj_check_type(child, &lv_label_class)) {{
            text_id_t id = (text_id_t)(uintptr_t)lv_obj_get_user_data(child);
            if (id > 0) {{
                lv_label_set_text(child, get_label_text(id));
            }}
        }}
        update_label_text_recursive(child);
        i++;
    }}
}}
"""

if __name__ == "__main__":
    main()
