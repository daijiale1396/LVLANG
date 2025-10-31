#include "ui_language.h"

void demo_multilang(void)
{
    lv_obj_t *scr = lv_scr_act();

    // 中文 label
    lv_obj_t *label = lv_label_create(scr);
    lv_label_set_text(label, get_label_text(TEXT_HORIZONTAL));
    lv_obj_set_user_data(label, (void *)(uintptr_t)TEXT_HORIZONTAL);
    lv_obj_align(label, LV_ALIGN_CENTER, 0, -20);

    // 英文 label
    lv_obj_t *label2 = lv_label_create(scr);
    lv_label_set_text(label2, get_label_text(TEXT_TRIGGER));
    lv_obj_set_user_data(label2, (void *)(uintptr_t)TEXT_TRIGGER);
    lv_obj_align(label2, LV_ALIGN_CENTER, 0, 20);

    // 模拟切换语言
    lv_timer_t *timer = lv_timer_create_basic();
    lv_timer_set_cb(timer, [](lv_timer_t *t){
        static int lang = 0;
        lang = (lang + 1) % LANG_MAX;
        set_language((lang_t)lang);
        update_label_text_recursive(lv_scr_act());
    });
    lv_timer_set_period(timer, 2000);
}
