/**
 * @file ui_language.c
 * @brief LVGL 多语言自动生成源文件 (动态语言版)
 * @author daijiale1396
 * @date 2025-11-03
 * @generated Automatically by LVLangGen
 */

#include "ui_language.h"

static lang_t current_lang = LANG_CN;

typedef struct {
    text_id_t id;
    const char *cn;
    const char *en;
    const char *tc;
    const char *jp;
} text_map_t;

static const text_map_t text_map[] = {
    { TEXT_OK, "确定", "OK", "確定", "確認" },
    { TEXT_CANCEL, "取消", "Cancel", "取消", "キャンセル" },
    { TEXT_SAVE, "保存", "Save", "儲存", "保存" },
    { TEXT_LOAD, "加载", "Load", "載入", "読み込み" },
    { TEXT_EXIT, "退出", "Exit", "退出", "終了" },
    { TEXT_FIRMWARE_UPGRADE, "升级固件", "Firmware", "升級韌體", "ファーム更新" },
    { TEXT_CONFIG_UPGRADE, "升级配置", "Config", "升級配置", "設定更新" },
    { TEXT_MENU, "功能菜单", "Menu", "功能選單", "メニュー" },
    { TEXT_HELP, "帮助", "Help", "幫助", "ヘルプ" },
    { TEXT_ABOUT, "关于", "About", "關於", "情報" },
    { TEXT_LANGUAGE, "语言", "Language", "語言", "言語" }
};

const char *get_label_text(text_id_t id)
{
    for (size_t i = 0; i < sizeof(text_map) / sizeof(text_map[0]); ++i) 
    {
        if (text_map[i].id == id) 
        {
            return (current_lang == LANG_CN) ? text_map[i].cn
               : (current_lang == LANG_EN) ? text_map[i].en
               : (current_lang == LANG_TC) ? text_map[i].tc
               : (current_lang == LANG_JP) ? text_map[i].jp
               : text_map[i].jp;  // fallback
        }
    }
    return "";
}

void set_language(lang_t lang)
{
    if (lang < LANG_MAX) current_lang = lang;
}

void get_label_text(lv_obj_t *parent)
{
    if (!parent) return;

    int32_t i = 0;
    lv_obj_t *child = NULL;
    while ((child = lv_obj_get_child(parent, i)) != NULL) 
    {
        if (lv_obj_check_type(child, &lv_label_class)) 
        {
            text_id_t id = (text_id_t)(uintptr_t)lv_obj_get_user_data(child);
            if (id > 0) 
            {
                lv_label_set_text(child, get_label_text(id));
            }
        }
        update_label_text_recursive(child);
        i++;
    }
}
