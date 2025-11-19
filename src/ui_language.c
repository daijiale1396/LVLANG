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
} text_map_t;

static const text_map_t text_map[] = {
    { TEXT_OK, "确定", "OK" },
    { TEXT_CANCEL, "取消", "Cancel" },
    { TEXT_SAVE, "保存", "Save" },
    { TEXT_LOAD, "加载", "Load" },
    { TEXT_EXIT, "退出", "Exit" },
    { TEXT_FREQUENCY, "频率", "Frequency" },
    { TEXT_DC_VOLTAGE, "直流电压", "DC Voltage" },
    { TEXT_DC_CURRENT, "直流电流", "DC Current" },
    { TEXT_AUTO, "自动", "Auto" },
    { TEXT_TIME_BASE, "时基", "Time Base" },
    { TEXT_THRESHOLD, "阈值", "Threshold" }
};

const char *get_label_text(text_id_t id)
{
    for (size_t i = 0; i < sizeof(text_map) / sizeof(text_map[0]); ++i) 
    {
        if (text_map[i].id == id) 
        {
            return (current_lang == LANG_CN) ? text_map[i].cn
               : (current_lang == LANG_EN) ? text_map[i].en
               : text_map[i].en;  // fallback
        }
    }
    return "";
}

void set_language(lang_t lang)
{
    if (lang < LANG_MAX) current_lang = lang;
}

void update_label_text_recursive(lv_obj_t *parent)
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
