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
    LANG_TC,
    LANG_JP,
    LANG_MAX
} lang_t;

typedef enum {
    TEXT_OK = 1,                         // 1: "确定" / "OK"
    TEXT_CANCEL,                         // 2: "取消" / "Cancel"
    TEXT_SAVE,                           // 3: "保存" / "Save"
    TEXT_LOAD,                           // 4: "加载" / "Load"
    TEXT_EXIT,                           // 5: "退出" / "Exit"
    TEXT_FIRMWARE_UPGRADE,               // 6: "升级固件" / "Firmware"
    TEXT_CONFIG_UPGRADE,                 // 7: "升级配置" / "Config"
    TEXT_MENU,                           // 8: "功能菜单" / "Menu"
    TEXT_HELP,                           // 9: "帮助" / "Help"
    TEXT_ABOUT,                          // 10: "关于" / "About"
    TEXT_LANGUAGE,                       // 11: "语言" / "Language"
} text_id_t;

const char *get_label_text(text_id_t id);
void set_language(lang_t lang);
void update_label_text_recursive(lv_obj_t *parent);

#ifdef __cplusplus
}
#endif

#endif // UI_LANGUAGE_H
