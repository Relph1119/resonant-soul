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

from api.apps.admin_app import get_all_users, update_user_status, delete_user
from api.apps.conversation_app import process_user_input
from api.apps.emotion_app import get_all_emotion_records
from api.apps.sas_app import process_sas_scores
from api.apps.statistics_app import generate_stats_charts, get_stats_text
from api.apps.user_app import user_login, user_register, get_user_info_by_username, update_password, get_user_info_by_id

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

is_logged_in = False


def create_gradio_interface():
    with gr.Blocks(title="心灵伙伴 - AI心理健康助手", theme=gr.themes.Soft()) as _interface:
        current_user = gr.State({"id": None, "name": None, "is_admin": False})

        # 用户认证面板
        with gr.Column(visible=True) as auth_panel:
            gr.Markdown("# 🌟 心灵伙伴 - 您的AI心理健康助手")
            with gr.Tabs():
                with gr.Tab("登录", id="login"):
                    login_username = gr.Textbox(label="用户名")
                    login_password = gr.Textbox(label="密码", type="password")
                    login_btn = gr.Button("登录")
                    login_status = gr.Textbox(label="登录状态", interactive=False)

                with gr.Tab("注册", id="register"):
                    register_username = gr.Textbox(label="用户名")
                    register_password = gr.Textbox(label="密码", type="password")
                    register_name_nick = gr.Textbox(label="昵称")
                    register_btn = gr.Button("注册")
                    register_status = gr.Textbox(label="注册状态", interactive=False)

        with gr.Column(visible=False, elem_id="main_panel") as main_panel:
            # 修改Markdown为动态显示
            current_user_display = gr.Markdown("### 当前用户：未登录")
            # 主对话选项卡
            with gr.Tab("主对话"):
                gr.Markdown("# 🌟 心灵伙伴 - 您的AI心理健康助手")
                with gr.Row():
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(height=400, type='messages')
                        input_text = gr.Textbox(label="在这里输入您想说的话...",
                                                placeholder="请告诉我您的想法或感受...",
                                                submit_btn=True,
                                                stop_btn=True)
                    with gr.Column(scale=1):
                        emotion_chart = gr.Plot(label="Emotion Trend")

            with gr.Tab("心理评估"):
                gr.Markdown("## 焦虑自评量表(SAS)")
                gr.Markdown("""
                ### 评分说明：
                1 = 很少或没有</br>
                2 = 有时</br>
                3 = 经常</br>
                4 = 总是如此</br>
                </br>
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
                    sas_result = gr.Markdown(label="评估结果")

                    def process_sas_scores_wapper(current_user, *sas_scores):
                        user_id = current_user['id']
                        return process_sas_scores(user_id, *sas_scores)

                    sas_submit.click(
                        process_sas_scores_wapper,
                        inputs=[current_user, *sas_scores],
                        outputs=sas_result
                    )

            with gr.Tab("放松训练"):
                relaxation_type = gr.Radio(
                    choices=list(relaxation_guides.keys()),
                    label="选择放松训练类型"
                )
                relaxation_guide = gr.Textbox(label="训练指导", value="请选择一种放松训练方式")

            def update_diary(current_user):
                user_id = current_user['id']
                DIARY_ENTRIES = get_all_emotion_records(user_id)
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
                refresh_diary_btn.click(update_diary,
                                        inputs=current_user,
                                        outputs=diary_list)
                # 在界面加载时更新日记数据
                _interface.load(update_diary,
                                inputs=current_user,
                                outputs=diary_list)

            # 添加统计分析标签页
            with gr.Tab("统计分析"):
                gr.Markdown("## 使用统计")
                stats_plot = gr.Plot()
                refresh_btn = gr.Button("刷新统计数据")

                # 统计信息文本显示
                stats_text = gr.Markdown()

                def update_stats(current_user):
                    user_id = current_user['id']
                    return generate_stats_charts(user_id), get_stats_text(user_id)

                refresh_btn.click(
                    update_stats,
                    inputs=current_user,
                    outputs=[stats_plot, stats_text]
                )
                user_id = current_user.value['id']
                # 初始加载统计数据
                stats_plot.value = generate_stats_charts(user_id)
                stats_text.value = get_stats_text(user_id)

            with gr.Tab("用户信息"):
                gr.Markdown("## 个人信息管理")

                # 用户信息展示
                with gr.Column():
                    user_info = gr.Textbox(label="用户名", interactive=False)
                    nick_info = gr.Textbox(label="用户昵称", interactive=False)
                    reg_date_info = gr.Textbox(label="注册时间", interactive=False)

                # 密码修改模块
                with gr.Column():
                    with gr.Row():
                        new_password = gr.Textbox(label="新密码", type="password")
                        confirm_password = gr.Textbox(label="确认新密码", type="password")
                    update_pwd_btn = gr.Button("修改密码", variant="primary")
                    pwd_status = gr.Textbox(label="操作结果", interactive=False)

                # 信息更新函数
                def update_user_info(current_user):
                    if current_user is not None:
                        user = get_user_info_by_id(current_user['id'])
                        if user:
                            return [
                                user['username'],
                                user['name'],
                                user['created_at']
                            ]
                    return ["", "", ""]

                # 密码修改处理
                def change_password(current_user, new_pwd, confirm_pwd):
                    if new_pwd != confirm_pwd:
                        return "新密码与确认密码不一致"
                    if len(new_pwd) < 8:
                        return "密码长度至少8位"

                    try:
                        update_password(current_user['id'], new_pwd)
                        return "密码修改成功"
                    except Exception as e:
                        return f"密码修改失败：{str(e)}"

                # 绑定事件
                update_pwd_btn.click(
                    change_password,
                    inputs=[current_user, new_password, confirm_password],
                    outputs=pwd_status
                )

            # 添加管理员标签页
            with gr.Tab("管理员功能", visible=False) as admin_tab:
                gr.Markdown("## 用户管理")

                # 用户列表
                users_table = gr.Dataframe(
                    headers=["用户ID", "用户名", "昵称", "状态", "注册时间"],  # 新增操作列
                    label="用户列表",
                    interactive=False,
                    value=get_all_users()  # 直接在创建时加载数据
                )

                with gr.Row():
                    refresh_users_btn = gr.Button("刷新用户列表", variant="primary")

                with gr.Row():
                    with gr.Column(scale=1):
                        selected_user_id = gr.Number(label="选择用户ID", precision=0, minimum=1, value=2)
                    with gr.Column(scale=1):
                        # 将单选按钮改为操作选择下拉菜单
                        user_actions = gr.Radio(
                            choices=[
                                ("🛑启用用户", "enable"),
                                ("✅禁用用户", "disable"),
                                ("❌删除用户", "delete")
                            ],
                            label="选择操作",
                            type="value"
                        )
                    with gr.Column(scale=1):
                        execute_action_btn = gr.Button("执行操作", variant="secondary")

                operation_status = gr.Textbox(label="操作结果", interactive=False)

                # 更新用户列表函数
                def update_users_list():
                    users = get_all_users()
                    if users:
                        return [[
                            user['id'],
                            user['username'],
                            user['name'],
                            user['status'],
                            user['created_at'],
                        ] for user in users]
                    return []

                # 绑定事件
                refresh_users_btn.click(
                    update_users_list,
                    outputs=users_table
                )

                # 新增统一操作处理函数
                def handle_user_action(user_id, action):
                    if not user_id:
                        return "请选择用户ID", None
                    try:
                        if action == "disable":
                            result = update_user_status(user_id, False)
                        elif action == "enable":
                            result = update_user_status(user_id, True)
                        elif action == "delete":
                            result = delete_user(user_id)
                        else:
                            return "无效的操作类型", None

                        if result:
                            return f"操作成功：{action}", update_users_list()
                        return "操作失败", None
                    except Exception as e:
                        return f"操作出错：{str(e)}", None

                # 绑定新的事件
                execute_action_btn.click(
                    handle_user_action,
                    inputs=[selected_user_id, user_actions],
                    outputs=[operation_status, users_table]
                )

        # 事件处理
        def login(username, password):
            user_data = user_login(username, password)
            if not user_data:
                return "用户名或密码错误", None
            if user_data.get("error"):
                return user_data["error"], None

            # 获取完整的用户信息
            user = get_user_info_by_username(username)
            return "登录成功", user

        login_event = lambda method: method(
            login,
            inputs=[login_username, login_password],
            outputs=[login_status, current_user]
        ).success(
            # 根据登录结果决定面板显示状态
            lambda status, user: (
                gr.Column(visible=user is None),
                gr.Column(visible=user is not None),
                gr.Tab(visible=user and user.get('is_admin', False))
            ),
            inputs=[login_status, current_user],
            outputs=[auth_panel, main_panel, admin_tab]
        ).success(
            # 更新用户显示
            fn=lambda user: gr.Markdown(
                f"### 当前用户：{user['name']} {'(管理员)' if user.get('is_admin') else ''}"
                if user else "### 当前用户：未登录"
            ),
            inputs=[current_user],
            outputs=current_user_display
        ).success(
            # 更新用户信息
            fn=update_user_info,
            inputs=current_user,
            outputs=[user_info, nick_info, reg_date_info]
        ).success(
            fn=update_diary,
            inputs=current_user,
            outputs=diary_list
        ).success(
            # 如果是管理员，刷新用户列表
            fn=lambda user: update_users_list() if user and user.get('is_admin') else None,
            inputs=[current_user],
            outputs=users_table
        )

        # 应用统一处理到两个登录入口
        login_event(login_btn.click)
        login_event(login_password.submit)

        # 注册功能事件绑定
        def register(username, name_nick, password):
            result = user_register(username, name_nick, password)
            if result and 'id' in result:
                return "注册成功", result
            return "注册失败，用户名已存在", None

        register_btn.click(
            register,
            inputs=[register_username, register_name_nick, register_password],
            outputs=[register_status, current_user]
        ).success(
            # 根据注册结果动态显示面板
            lambda status, user: (gr.Column(visible=user is None), gr.Column(visible=user is not None)),
            inputs=[register_status, current_user],
            outputs=[auth_panel, main_panel]
        ).success(
            # 添加空值检查
            fn=lambda user: gr.Markdown(f"### 当前用户：{user['name']}" if user else "### 当前用户：未登录"),
            inputs=[current_user],
            outputs=current_user_display
        ).success(
            # 更新用户信息
            fn=update_user_info,
            inputs=current_user,
            outputs=[user_info, nick_info, reg_date_info]
        )

        def update_relaxation_guide(choice):
            return relaxation_guides[choice]

        # 绑定事件
        relaxation_type.change(update_relaxation_guide, relaxation_type, relaxation_guide)

        # 主对话功能
        welcome_message = "你好！我是你的心灵伙伴，很高兴能和你交流。请告诉我你最近的感受或者有什么想聊的？"

        def set_welcome_message():
            return [{"role": "assistant", "content": welcome_message}]

        input_text.submit(
            fn=process_user_input,
            inputs=[current_user, input_text, chatbot],
            outputs=[chatbot, emotion_chart],
            queue=False
        ).then(
            fn=lambda: "",
            inputs=None,
            outputs=input_text,
            queue=False
        ).then(
            fn=update_diary,
            inputs=current_user,
            outputs=diary_list
        )

        # 在界面加载时设置欢迎消息
        _interface.load(set_welcome_message, outputs=chatbot)

    return _interface


interface = create_gradio_interface()
interface.launch()
