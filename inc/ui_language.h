/**
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
extern "C" {
#endif

typedef enum {
    LANG_CN,
    LANG_EN,
    LANG_MAX
} lang_t;

typedef enum {
    TEXT_OK = 1,                         // 1: "确定" / "OK"
    TEXT_CANCEL,                         // 2: "取消" / "Cancel"
    TEXT_SAVE,                           // 3: "保存" / "Save"
    TEXT_LOAD,                           // 4: "加载" / "Load"
    TEXT_EXIT,                           // 5: "退出" / "Exit"
    TEXT_FREQUENCY,                      // 6: "频率" / "Frequency"
    TEXT_DC_VOLTAGE,                     // 7: "直流电压" / "DC Voltage"
    TEXT_DC_CURRENT,                     // 8: "直流电流" / "DC Current"
    TEXT_AUTO,                           // 9: "自动" / "Auto"
    TEXT_TIME_BASE,                      // 10: "时基" / "Time Base"
    TEXT_THRESHOLD,                      // 11: "阈值" / "Threshold"
} text_id_t;

const char *get_label_text(text_id_t id);
void set_language(lang_t lang);
void update_label_text_recursive(lv_obj_t *parent);

#ifdef __cplusplus
}
#endif

#endif // UI_LANGUAGE_H
