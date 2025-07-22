#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: main_mind.py
@time: 2025/7/21 13:57
@project: resonant-soul
@desc: 
"""

import gradio as gr

from api.apps.conversation_app import process_user_input
from api.apps.sas_app import process_sas_scores
from api.apps.statistics_app import generate_stats_charts, get_stats_text
from api.settings import DIARY_ENTRIES

# SAS焦虑自评量表题目
sas_questions = [
    "我感到比平常更加紧张和焦虑",
    "我无缘无故地感到害怕",
    "我容易心烦意乱或感到恐慌",
    "我感到我的身体好像被分成几块",
    "我感到一切都很好，不会发生什么不幸"
]

# 放松训练指导内容
relaxation_guides = {
    "呼吸放松": """
    1. 找一个安静、舒适的地方坐下
    2. 缓慢吸气，数4秒
    3. 屏住呼吸，数4秒
    4. 缓慢呼气，数6秒
    5. 重复以上步骤5-10次
    """,
    "渐进性肌肉放松": """
    1. 从脚趾开始，绷紧肌肉5秒
    2. 完全放松10秒
    3. 逐渐向上移动到小腿、大腿
    4. 继续到腹部、胸部、手臂
    5. 最后是面部肌肉
    """,
    "正念冥想": """
    1. 选择一个安静的环境
    2. 采用舒适的坐姿
    3. 闭上眼睛，关注呼吸
    4. 让思绪自然流动
    5. 温和地将注意力带回呼吸
    """
}


def create_gradio_interface():
    with gr.Blocks(title="心灵伙伴 - AI心理健康助手", theme=gr.themes.Soft()) as _interface:
        with gr.Tab("主对话"):
            gr.Markdown("# 🌟 心灵伙伴 - 您的AI心理健康助手")
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(height=400, type='messages')
                    input_text = gr.Textbox(label="在这里输入您想说的话...", placeholder="请告诉我您的想法或感受...")
                    submit = gr.Button("发送")
                with gr.Column(scale=1):
                    emotion_chart = gr.Plot(label="Emotion Trend")

        with gr.Tab("心理评估"):
            gr.Markdown("## 焦虑自评量表(SAS)")
            gr.Markdown("""
            ### 评分说明：
            1 = 很少或没有
            2 = 有时
            3 = 经常
            4 = 总是如此

            请根据最近一周的感受进行评分。
            """)

            sas_scores = []
            with gr.Column():
                for i, q in enumerate(sas_questions, 1):
                    sas_scores.append(
                        gr.Slider(
                            minimum=1,
                            maximum=4,
                            step=1,
                            value=1,
                            label=f"{i}. {q}",
                            interactive=True
                        )
                    )
                sas_submit = gr.Button("提交评估", variant="primary")
                sas_result = gr.Textbox(label="评估结果", interactive=False)

                sas_submit.click(
                    process_sas_scores,
                    inputs=sas_scores,
                    outputs=sas_result
                )

        with gr.Tab("放松训练"):
            relaxation_type = gr.Radio(
                choices=list(relaxation_guides.keys()),
                label="选择放松训练类型"
            )
            relaxation_guide = gr.Textbox(label="训练指导", value="请选择一种放松训练方式")

        def update_diary():
            data = [[entry['date'], entry['content'], ', '.join(entry['emotions'])]
                    for entry in DIARY_ENTRIES]
            return data

        with gr.Tab("情绪日记"):
            gr.Markdown("## 我的情绪日记")
            diary_list = gr.Dataframe(
                headers=["日期", "内容", "情绪"],
                label="日记记录"
            )
            # 添加刷新按钮
            refresh_diary_btn = gr.Button("刷新日记")
            refresh_diary_btn.click(update_diary, outputs=diary_list)
            # 在界面加载时更新日记数据
            _interface.load(update_diary, outputs=diary_list)

        # 添加统计分析标签页
        with gr.Tab("统计分析"):
            gr.Markdown("## 使用统计")
            stats_plot = gr.Plot()
            refresh_btn = gr.Button("刷新统计数据")

            # 统计信息文本显示
            stats_text = gr.Markdown()

            def update_stats():
                return generate_stats_charts(), get_stats_text()

            refresh_btn.click(
                update_stats,
                outputs=[stats_plot, stats_text]
            )

            # 初始加载统计数据
            stats_plot.value = generate_stats_charts()
            stats_text.value = get_stats_text()

        # 事件处理
        def update_relaxation_guide(choice):
            return relaxation_guides[choice]

        # 绑定事件
        relaxation_type.change(update_relaxation_guide, relaxation_type, relaxation_guide)

        # 主对话功能
        welcome_message = "你好！我是你的心灵伙伴，很高兴能和你交流。请告诉我你最近的感受或者有什么想聊的？"

        def set_welcome_message():
            return [{"role": "assistant", "content": welcome_message}]

        submit.click(
            fn=process_user_input,
            inputs=[input_text, chatbot],
            outputs=[chatbot, emotion_chart],
            queue=False
        ).then(
            fn=lambda: "",
            inputs=None,
            outputs=input_text,
            queue=False
        ).then(
            fn=update_diary,
            inputs=None,
            outputs=diary_list
        )

        # 在界面加载时设置欢迎消息
        _interface.load(set_welcome_message, outputs=chatbot)

    return _interface


interface = create_gradio_interface()
interface.launch()
