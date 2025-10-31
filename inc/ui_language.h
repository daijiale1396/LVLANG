/**
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
extern "C" {
#endif

typedef enum {
    LANG_CN = 0,
    LANG_EN,
    LANG_TC,
    LANG_MAX
} lang_t;

typedef enum {
    TEXT_OK,
    TEXT_CANCEL,
    TEXT_SAVE,
    TEXT_LOAD,
    TEXT_EXIT,
    TEXT_FIRMWARE_UPGRADE,
    TEXT_CONFIG_UPGRADE,
    TEXT_MENU,
    TEXT_HELP,
    TEXT_ABOUT,
    TEXT_LANGUAGE
} text_id_t;

const char *get_label_text(text_id_t id);
void set_language(lang_t lang);
void update_label_text_recursive(lv_obj_t *parent);

#ifdef __cplusplus
}
#endif

#endif // UI_LANGUAGE_H
