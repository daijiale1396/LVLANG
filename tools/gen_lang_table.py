#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言表自动生成工具 (动态语言版本 + CSV校验)
=========================================
可根据 CSV 动态适配任意语言列，如：
    id,cn,en,tc,jp,fr,...

自动生成：
    - inc/ui_language.h
    - src/ui_language.c

并自动检测：
    - 列名错误或重复
    - 缺少列、空值、非法符号
    - 行列数不匹配
"""

import csv
from pathlib import Path
import sys
import re

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
CYAN = "\033[96m"
RESET = "\033[0m"


def color(text, col):
    return f"{col}{text}{RESET}"


def main():
    # ====================== 文件检查 ======================
    if not CSV.exists():
        print(color(f"❌ 找不到 {CSV}", RED))
        sys.exit(1)

    # ====================== 结构检测 ======================
    print(color(f"🔍 正在检查 CSV 结构...", CYAN))

    with open(CSV, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        if not first_line:
            print(color("❌ CSV 文件为空！", RED))
            sys.exit(1)

        if "id" not in first_line.split(","):
            print(color("❌ 表头必须包含 'id'", RED))
            sys.exit(1)

        if re.search(r"[，；：]", first_line):
            print(color("⚠️ 检测到全角标点，建议改为英文逗号分隔", YELLOW))

    # ====================== 正式解析 ======================
    rows = []
    seen_ids = set()
    errors = 0

    with open(CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if not fieldnames:
            print(color("❌ 无法读取表头，可能是格式错误或包含BOM。", RED))
            sys.exit(1)

        # 检查重复列
        if len(fieldnames) != len(set(fieldnames)):
            print(color(f"❌ 表头存在重复字段: {fieldnames}", RED))
            sys.exit(1)

        # 检查列命名规范
        for col in fieldnames:
            if not col.strip():
                print(color(f"⚠️ 检测到空列名，请检查表头。", YELLOW))
            if " " in col:
                print(color(f"⚠️ 列名 '{col}' 含空格，建议去除。", YELLOW))

        # 语言列
        lang_cols = [col for col in fieldnames if col != "id"]
        print(color(f"🌍 检测到语言字段: {', '.join(lang_cols)}", GREEN))

        # ====================== 行检查 ======================
        line_num = 1
        for row in reader:
            line_num += 1

            # 自动清理非字符串值
            clean_row = {}
            for k, v in row.items():
                if v is None:
                    clean_row[k] = ""
                elif isinstance(v, list):
                    clean_row[k] = ",".join(str(x) for x in v)
                else:
                    clean_row[k] = str(v).strip()
            row = clean_row

            # 检查列数
            if len(row) != len(fieldnames):
                print(color(f"⚠️ 第{line_num}行列数异常 ({len(row)}/{len(fieldnames)})，请检查多余逗号或缺少引号。", YELLOW))

            rid = row.get("id", "")
            if not rid:
                print(color(f"⚠️ 第{line_num}行缺少 id，已跳过。", YELLOW))
                continue

            if rid in seen_ids:
                print(color(f"❌ 重复 ID: {rid} (第{line_num}行)", RED))
                errors += 1
            seen_ids.add(rid)

            # 检查空字段
            for lang in lang_cols:
                if not row.get(lang):
                    print(color(f"⚠️ {rid} 缺少 {lang.upper()} 字段", YELLOW))

            # 检查全角字符
            for key, val in row.items():
                if "，" in val or "。" in val:
                    print(color(f"⚠️ {rid} ({key}) 含全角标点，建议改为半角", YELLOW))

            rows.append(row)

    if errors > 0:
        print(color(f"\n🚫 检测到 {errors} 个严重错误，请修复后再生成。", RED))
        sys.exit(1)

    # ====================== 输出生成 ======================
    HEADER_PATH.write_text(gen_header(rows, lang_cols), encoding="utf-8")
    SOURCE_PATH.write_text(gen_source(rows, lang_cols), encoding="utf-8")

    print(color(f"\n✅ 已生成:", GREEN))
    print(f"  - {HEADER_PATH.relative_to(ROOT)}")
    print(f"  - {SOURCE_PATH.relative_to(ROOT)}")


def gen_header(rows, lang_cols):
    lang_enum_items = ",\n    ".join([f"LANG_{l.upper()}" for l in lang_cols])
    enum_items = ",\n    ".join([r["id"] for r in rows])

    return f"""/**
 * @file ui_language.h
 * @brief LVGL 多语言自动生成头文件 (动态语言版)
 * @author daijiale1396
 * @date 2025-11-03
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
    {lang_enum_items},
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


def gen_source(rows, lang_cols):
    lang_fields = ";\n    ".join([f"const char *{l}" for l in lang_cols]) + ";"

    # 构建表项
    table_entries = []
    for r in rows:
        langs = ", ".join([f'"{r[l]}"' for l in lang_cols])
        table_entries.append(f'    {{ {r["id"]}, {langs} }}')
    table_text = ",\n".join(table_entries)

    lang_return = "\n               : ".join(
        [f"(current_lang == LANG_{l.upper()}) ? text_map[i].{l}" for l in lang_cols]
    )

    return f"""/**
 * @file ui_language.c
 * @brief LVGL 多语言自动生成源文件 (动态语言版)
 * @author daijiale1396
 * @date 2025-11-03
 * @generated Automatically by LVLangGen
 */

#include "ui_language.h"

static lang_t current_lang = LANG_CN;

typedef struct {{
    text_id_t id;
    {lang_fields}
}} text_map_t;

static const text_map_t text_map[] = {{
{table_text}
}};

const char *get_label_text(text_id_t id)
{{
    for (size_t i = 0; i < sizeof(text_map) / sizeof(text_map[0]); ++i) {{
        if (text_map[i].id == id) {{
            return {lang_return}
               : text_map[i].{lang_cols[-1]};  // fallback
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
