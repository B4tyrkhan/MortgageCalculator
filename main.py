from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line, Ellipse
import datetime
import calendar

from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.datatables import MDDataTable


KV = '''
<ItemDrawer>:
    theme_text_color: "Custom"
    text_color: root.text_color

    IconLeftWidget:
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color


<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "data/logo/logo3-min.png"

    MDLabel:
        id: app_title_label
        text: app.title
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1

    MDLabel:
        id: app_author_label
        text: app.by_who
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 0.7

    ScrollView:
        DrawerList:
            id: md_list


<Tab>:
    BoxLayout:
        orientation: "vertical"
        Widget:


Screen:
    MDNavigationLayout:

        ScreenManager:
            Screen:

                BoxLayout:
                    orientation: "vertical"

                    MDTopAppBar:
                        id: toolbar
                        title: app.title
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["translate", lambda x: app.open_language_menu()],
                                             ["star-outline", lambda x: app.on_star_click()]]
                        md_bg_color: 0, 0, 0, 1
                        specific_text_color: 1, 1, 1, 1

                    MDTabs:
                        id: tabs
                        on_tab_switch: app.on_tab_switch(*args)
                        tab_indicator_anim: False
                        background_color: 0.1, 0.1, 0.1, 1

                        Tab:
                            id: tab_input
                            icon: "calculator-variant"
                            title: "Input"

                            BoxLayout:
                                orientation: "vertical"
                                padding: "14dp"
                                spacing: "14dp"

                                BoxLayout:
                                    orientation: "horizontal"
                                    size_hint_y: None
                                    height: "56dp"
                                    spacing: "8dp"

                                    MDIconButton:
                                        id: icon_date
                                        icon: "calendar-month"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1
                                        on_release: app.show_date_picker()

                                    MDTextField:
                                        id: start_date
                                        hint_text: "Start date"
                                        color_mode: "custom"
                                        readonly: True

                                BoxLayout:
                                    orientation: "horizontal"
                                    size_hint_y: None
                                    height: "56dp"
                                    spacing: "8dp"

                                    MDIconButton:
                                        id: icon_loan
                                        icon: "cash"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1

                                    MDTextField:
                                        id: loan
                                        hint_text: "Loan"
                                        input_filter: "float"
                                        color_mode: "custom"

                                BoxLayout:
                                    orientation: "horizontal"
                                    size_hint_y: None
                                    height: "56dp"
                                    spacing: "8dp"

                                    MDIconButton:
                                        id: icon_months
                                        icon: "clock-time-five-outline"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1

                                    MDTextField:
                                        id: months
                                        hint_text: "Months"
                                        input_filter: "int"
                                        color_mode: "custom"

                                BoxLayout:
                                    orientation: "horizontal"
                                    size_hint_y: None
                                    height: "56dp"
                                    spacing: "8dp"

                                    MDIconButton:
                                        id: icon_interest
                                        icon: "bank"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1

                                    MDTextField:
                                        id: interest
                                        hint_text: "Interest, %"
                                        input_filter: "float"
                                        color_mode: "custom"

                                    MDTextField:
                                        id: payment_type
                                        hint_text: "Payment type"
                                        text: "annuity"
                                        readonly: True
                                        on_focus: if self.focus: app.open_payment_menu()
                                        color_mode: "custom"

                                MDRaisedButton:
                                    id: calc_button
                                    text: "Calc"
                                    pos_hint: {"center_x": 0.5}
                                    on_release: app.calculate()

                                MDLabel:
                                    id: result_label
                                    text: ""
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

                                Widget:

                        Tab:
                            id: tab_table
                            icon: "table-large"
                            title: "Table"

                            BoxLayout:
                                id: table_box
                                orientation: "vertical"
                                padding: "16dp"

                                MDLabel:
                                    id: table_label
                                    text: "Table"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

                        Tab:
                            id: tab_graph
                            icon: "chart-areaspline"
                            title: "Graph"

                            BoxLayout:
                                orientation: "vertical"
                                padding: "16dp"
                                spacing: "10dp"

                                MDLabel:
                                    id: graph_label
                                    text: "Graph payments"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1
                                    size_hint_y: None
                                    height: "30dp"

                                Widget:
                                    id: graph_widget

                                BoxLayout:
                                    orientation: "horizontal"
                                    size_hint_y: None
                                    height: "30dp"
                                    spacing: "20dp"
                                    padding: "10dp", 0

                                    MDLabel:
                                        id: graph_interest_legend
                                        text: "[color=0000ff]■[/color] Interest"
                                        markup: True
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1

                                    MDLabel:
                                        id: graph_principal_legend
                                        text: "[color=ff0000]■[/color] Principal"
                                        markup: True
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1

                        Tab:
                            id: tab_chart
                            icon: "chart-pie"
                            title: "Chart"

                            BoxLayout:
                                orientation: "vertical"
                                padding: "16dp"
                                spacing: "10dp"

                                MDLabel:
                                    id: chart_label
                                    text: "Chart payments"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1
                                    size_hint_y: None
                                    height: "30dp"

                                Widget:
                                    id: chart_widget

                                BoxLayout:
                                    orientation: "horizontal"
                                    size_hint_y: None
                                    height: "30dp"
                                    spacing: "20dp"
                                    padding: "10dp", 0

                                    MDLabel:
                                        id: chart_interest_legend
                                        text: "[color=0000ff]■[/color] Interest"
                                        markup: True
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1

                                    MDLabel:
                                        id: chart_principal_legend
                                        text: "[color=ff0000]■[/color] Principal"
                                        markup: True
                                        halign: "center"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1

                        Tab:
                            id: tab_sum
                            icon: "book-open-variant"
                            title: "Sum"

                            BoxLayout:
                                orientation: "vertical"
                                padding: "16dp"
                                spacing: "12dp"

                                MDLabel:
                                    id: sum_label
                                    text: "Sum"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

                                MDLabel:
                                    id: total_amount_label
                                    text: "Total amount of payments: "
                                    halign: "left"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

                                MDLabel:
                                    id: overpayment_label
                                    text: "Overpayment loan: "
                                    halign: "left"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

                                MDLabel:
                                    id: effective_rate_label
                                    text: "Effective interest rate: "
                                    halign: "left"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

                Widget:
                    id: language_button
                    size_hint: None, None
                    size: 1, 1
                    pos: 0, 0

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
'''


class Tab(MDFloatLayout, MDTabsBase):
    title = StringProperty("")
    icon = StringProperty("")


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty([1, 1, 1, 1])

    def on_release(self):
        app = MDApp.get_running_app()

        if self.text in [app.tr("dark_light"), "Dark/Light", "Тема", "Ашық/Қараңғы"]:
            app.toggle_theme()

        elif self.text in [app.tr("language"), "Language", "Язык", "Тіл"]:
            app.open_language_menu()

        self.parent.set_color_item(self)


class DrawerList(MDList):
    def set_color_item(self, instance_item):
        app = MDApp.get_running_app()
        for item in self.children:
            item.text_color = app.theme_cls.text_color
        instance_item.text_color = app.theme_cls.primary_color


class MortgageCalculatorApp(MDApp):
    title = "Mortgage Calculator"
    by_who = "author Aliev Batyrkhann"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self.language_menu = None
        self.screen = None
        self.table_widget = None
        self.graph_data = []
        self.chart_interest_total = 0.0
        self.chart_principal_total = 0.0
        self.current_language = "kz"

        self.translations = {
            "en": {
                "title": "Mortgage Calculator",
                "author": "author Aliev Batyrkhann",
                "input": "Input",
                "table": "Table",
                "graph": "Graph",
                "chart": "Chart",
                "sum": "Sum",
                "start_date": "Start date",
                "loan": "Loan",
                "months": "Months",
                "interest": "Interest, %",
                "payment_type": "Payment type",
                "calc": "Calc",
                "graph_payments": "Graph payments",
                "chart_payments": "Chart payments",
                "total_amount": "Total amount of payments",
                "overpayment": "Overpayment loan",
                "effective_rate": "Effective interest rate",
                "about_author": "About author",
                "my_youtube": "My YouTube",
                "donate_author": "Donate author",
                "source_code": "Source code",
                "share_app": "Share app",
                "dark_light": "Dark/Light",
                "language": "Language",
                "monthly_payment": "Monthly payment",
                "first_payment": "First payment",
                "fill_all_fields": "Fill all fields",
                "wrong_numbers": "Wrong numbers",
                "values_invalid": "Values must be valid",
                "interest_legend": "Interest",
                "principal_legend": "Principal",
                "payment_type_annuity": "annuity",
                "payment_type_diff": "differentiated",
            },
            "ru": {
                "title": "Ипотечный калькулятор",
                "author": "автор Алиев Батырхан",
                "input": "Ввод",
                "table": "Таблица",
                "graph": "График",
                "chart": "Диаграмма",
                "sum": "Итог",
                "start_date": "Дата начала",
                "loan": "Сумма кредита",
                "months": "Месяцы",
                "interest": "Процент, %",
                "payment_type": "Тип платежа",
                "calc": "Рассчитать",
                "graph_payments": "График платежей",
                "chart_payments": "Диаграмма платежей",
                "total_amount": "Общая сумма выплат",
                "overpayment": "Переплата",
                "effective_rate": "Эффективная ставка",
                "about_author": "Об авторе",
                "my_youtube": "Мой YouTube",
                "donate_author": "Поддержать автора",
                "source_code": "Исходный код",
                "share_app": "Поделиться",
                "dark_light": "Тема",
                "language": "Язык",
                "monthly_payment": "Ежемесячный платеж",
                "first_payment": "Первый платеж",
                "fill_all_fields": "Заполните все поля",
                "wrong_numbers": "Неверные числа",
                "values_invalid": "Некорректные значения",
                "interest_legend": "Проценты",
                "principal_legend": "Основной долг",
                "payment_type_annuity": "аннуитет",
                "payment_type_diff": "дифференцированный",
            },
            "kz": {
                "title": "Ипотекалық калькулятор",
                "author": "автор Алиев Батырхан",
                "input": "Енгізу",
                "table": "Кесте",
                "graph": "График",
                "chart": "Диаграмма",
                "sum": "Қорытынды",
                "start_date": "Басталу күні",
                "loan": "Несие сомасы",
                "months": "Ай саны",
                "interest": "Пайыз, %",
                "payment_type": "Төлем түрі",
                "calc": "Есептеу",
                "graph_payments": "Төлем графигі",
                "chart_payments": "Төлем диаграммасы",
                "total_amount": "Жалпы төлем сомасы",
                "overpayment": "Артық төлем",
                "effective_rate": "Тиімді мөлшерлеме",
                "about_author": "Автор туралы",
                "my_youtube": "Менің YouTube арнам",
                "donate_author": "Авторды қолдау",
                "source_code": "Бастапқы код",
                "share_app": "Қосымшамен бөлісу",
                "dark_light": "Ашық/Қараңғы",
                "language": "Тіл",
                "monthly_payment": "Ай сайынғы төлем",
                "first_payment": "Бірінші төлем",
                "fill_all_fields": "Барлық өрістерді толтырыңыз",
                "wrong_numbers": "Қате сандар",
                "values_invalid": "Мәндер қате",
                "interest_legend": "Пайыз",
                "principal_legend": "Негізгі қарыз",
                "payment_type_annuity": "аннуитет",
                "payment_type_diff": "сараланған",
            },
        }

    def tr(self, key):
        return self.translations.get(self.current_language, {}).get(key, key)

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        self.screen = Builder.load_string(KV)
        Clock.schedule_once(self.setup_menu, 0.2)
        Clock.schedule_once(self.setup_language_menu, 0.2)
        Clock.schedule_once(self.refresh_ui_colors, 0.2)
        Clock.schedule_once(self.bind_graph_widget, 0.3)
        Clock.schedule_once(self.bind_chart_widget, 0.3)
        return self.screen

    def bind_graph_widget(self, *args):
        graph_widget = self.screen.ids.graph_widget
        graph_widget.bind(pos=lambda *x: self.draw_graph())
        graph_widget.bind(size=lambda *x: self.draw_graph())

    def bind_chart_widget(self, *args):
        chart_widget = self.screen.ids.chart_widget
        chart_widget.bind(pos=lambda *x: self.draw_chart())
        chart_widget.bind(size=lambda *x: self.draw_chart())

    def setup_menu(self, *args):
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.payment_type,
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": self.tr("payment_type_annuity"),
                    "on_release": lambda: self.set_payment_type("annuity"),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": self.tr("payment_type_diff"),
                    "on_release": lambda: self.set_payment_type("differentiated"),
                },
            ],
            width_mult=4,
        )

    def refresh_payment_menu(self):
        if self.menu:
            self.menu.dismiss()

        self.menu = MDDropdownMenu(
            caller=self.screen.ids.payment_type,
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": self.tr("payment_type_annuity"),
                    "on_release": lambda: self.set_payment_type("annuity"),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": self.tr("payment_type_diff"),
                    "on_release": lambda: self.set_payment_type("differentiated"),
                },
            ],
            width_mult=4,
        )

    def setup_language_menu(self, *args):
        self.language_menu = MDDropdownMenu(
            caller=self.screen.ids.language_button,
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": "English",
                    "on_release": lambda: self.set_language("en"),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Русский",
                    "on_release": lambda: self.set_language("ru"),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "Қазақша",
                    "on_release": lambda: self.set_language("kz"),
                },
            ],
            width_mult=4,
        )

    def open_language_menu(self):
        if self.language_menu:
            self.language_menu.caller = self.screen.ids.language_button
            self.language_menu.open()

    def set_language(self, lang_code):
        self.current_language = lang_code
        if self.language_menu:
            self.language_menu.dismiss()
        self.apply_language()

    def open_payment_menu(self):
        if self.menu:
            self.menu.caller = self.screen.ids.payment_type
            self.menu.open()

    def set_payment_type(self, value):
        self.screen.ids.payment_type.text = self.tr("payment_type_annuity") if value == "annuity" else self.tr("payment_type_diff")
        self.screen.ids.payment_type.focus = False
        self.screen.ids.payment_type._payment_type_value = value
        if self.menu:
            self.menu.dismiss()

    def get_payment_type_value(self):
        if hasattr(self.screen.ids.payment_type, "_payment_type_value"):
            return self.screen.ids.payment_type._payment_type_value
        return "annuity"

    def rebuild_drawer(self):
        md_list = self.screen.ids.content_drawer.ids.md_list
        md_list.clear_widgets()

        menu_items = {
            "account-cowboy-hat": self.tr("about_author"),
            "youtube": self.tr("my_youtube"),
            "coffee": self.tr("donate_author"),
            "github": self.tr("source_code"),
            "share-variant": self.tr("share_app"),
            "shield-sun": self.tr("dark_light"),
            "translate": self.tr("language"),
        }

        for icon_name, item_text in menu_items.items():
            md_list.add_widget(ItemDrawer(icon=icon_name, text=item_text))

    def apply_language(self):
        self.title = self.tr("title")
        self.by_who = self.tr("author")

        self.screen.ids.toolbar.title = self.tr("title")
        self.screen.ids.content_drawer.ids.app_title_label.text = self.tr("title")
        self.screen.ids.content_drawer.ids.app_author_label.text = self.tr("author")

        self.screen.ids.start_date.hint_text = self.tr("start_date")
        self.screen.ids.loan.hint_text = self.tr("loan")
        self.screen.ids.months.hint_text = self.tr("months")
        self.screen.ids.interest.hint_text = self.tr("interest")
        self.screen.ids.payment_type.hint_text = self.tr("payment_type")
        self.screen.ids.calc_button.text = self.tr("calc")

        self.screen.ids.table_label.text = self.tr("table")
        self.screen.ids.graph_label.text = self.tr("graph_payments")
        self.screen.ids.chart_label.text = self.tr("chart_payments")
        self.screen.ids.sum_label.text = self.tr("sum")

        self.screen.ids.total_amount_label.text = f"{self.tr('total_amount')}: "
        self.screen.ids.overpayment_label.text = f"{self.tr('overpayment')}: "
        self.screen.ids.effective_rate_label.text = f"{self.tr('effective_rate')}: "

        self.screen.ids.graph_interest_legend.text = f"[color=0000ff]■[/color] {self.tr('interest_legend')}"
        self.screen.ids.graph_principal_legend.text = f"[color=ff0000]■[/color] {self.tr('principal_legend')}"
        self.screen.ids.chart_interest_legend.text = f"[color=0000ff]■[/color] {self.tr('interest_legend')}"
        self.screen.ids.chart_principal_legend.text = f"[color=ff0000]■[/color] {self.tr('principal_legend')}"

        tabs = self.screen.ids.tabs.get_tab_list()
        if len(tabs) >= 5:
            tabs[4].text = self.tr("sum")
            tabs[3].text = self.tr("chart")
            tabs[2].text = self.tr("graph")
            tabs[1].text = self.tr("table")
            tabs[0].text = self.tr("input")

        current_type = self.get_payment_type_value()
        self.refresh_payment_menu()
        self.set_payment_type(current_type)
        self.rebuild_drawer()

    def on_start(self):
        self.screen.ids.start_date.text = datetime.date.today().strftime("%d-%m-%Y")
        self.screen.ids.loan.text = "5000000"
        self.screen.ids.months.text = "120"
        self.screen.ids.interest.text = "9.5"
        self.screen.ids.payment_type._payment_type_value = "annuity"
        self.apply_language()
        Clock.schedule_once(self.refresh_ui_colors, 0.2)

    def get_date(self, date_obj):
        self.screen.ids.start_date.text = date_obj.strftime("%d-%m-%Y")

    def on_save(self, instance, value, date_range):
        self.get_date(value)

    def on_cancel(self, instance, value):
        print("Date picker canceled")

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def set_textfield_colors(self, field, text_c, hint_c, line_c):
        field.text_color = text_c
        field.line_color_normal = line_c
        field.line_color_focus = line_c
        field.current_hint_text_color = hint_c
        field.hint_text_color_normal = hint_c

    def refresh_ui_colors(self, *args):
        toolbar = self.screen.ids.toolbar
        tabs = self.screen.ids.tabs
        drawer = self.screen.ids.content_drawer

        if self.theme_cls.theme_style == "Dark":
            bg_tabs = [0.10, 0.10, 0.10, 1]
            fg_main = [1, 1, 1, 1]
            fg_soft = [1, 1, 1, 0.7]
            field_line = [0.35, 0.35, 0.35, 1]
        else:
            bg_tabs = [0.95, 0.95, 0.95, 1]
            fg_main = [0, 0, 0, 1]
            fg_soft = [0, 0, 0, 0.7]
            field_line = [0.25, 0.25, 0.25, 1]

        toolbar.md_bg_color = [0, 0, 0, 1] if self.theme_cls.theme_style == "Dark" else [1, 1, 1, 1]
        toolbar.specific_text_color = fg_main

        tabs.background_color = bg_tabs
        tabs.text_color_normal = fg_soft
        tabs.text_color_active = fg_main

        for lbl in tabs.get_tab_list():
            lbl.text_color_normal = fg_soft
            lbl.text_color_active = fg_main
            lbl.color = fg_soft

        drawer.ids.app_title_label.text_color = fg_main
        drawer.ids.app_author_label.text_color = fg_soft

        self.screen.ids.table_label.text_color = fg_main
        self.screen.ids.graph_label.text_color = fg_main
        self.screen.ids.chart_label.text_color = fg_main
        self.screen.ids.sum_label.text_color = fg_main
        self.screen.ids.result_label.text_color = fg_main
        self.screen.ids.total_amount_label.text_color = fg_main
        self.screen.ids.overpayment_label.text_color = fg_main
        self.screen.ids.effective_rate_label.text_color = fg_main

        for icon_id in ("icon_date", "icon_loan", "icon_months", "icon_interest"):
            self.screen.ids[icon_id].text_color = fg_main

        self.set_textfield_colors(self.screen.ids.start_date, fg_main, fg_soft, field_line)
        self.set_textfield_colors(self.screen.ids.loan, fg_main, fg_soft, field_line)
        self.set_textfield_colors(self.screen.ids.months, fg_main, fg_soft, field_line)
        self.set_textfield_colors(self.screen.ids.interest, fg_main, fg_soft, field_line)
        self.set_textfield_colors(self.screen.ids.payment_type, fg_main, fg_soft, field_line)

    def toggle_theme(self):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        Clock.schedule_once(self.refresh_ui_colors, 0.1)
        Clock.schedule_once(lambda dt: self.draw_graph(), 0.15)
        Clock.schedule_once(lambda dt: self.draw_chart(), 0.15)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if self.theme_cls.theme_style == "Dark":
            normal = [1, 1, 1, 0.7]
            active = [1, 1, 1, 1]
        else:
            normal = [0, 0, 0, 0.7]
            active = [0, 0, 0, 1]

        for lbl in instance_tabs.get_tab_list():
            lbl.color = normal

        instance_tab_label.color = active

        if tab_text in ["Graph", "График"]:
            Clock.schedule_once(lambda dt: self.draw_graph(), 0.05)

        if tab_text in ["Chart", "Диаграмма"]:
            Clock.schedule_once(lambda dt: self.draw_chart(), 0.05)

    def add_months(self, source_date, months):
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def show_table(self, rows):
        table_box = self.screen.ids.table_box
        table_box.clear_widgets()

        self.table_widget = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            rows_num=10,
            check=False,
            column_data=[
                ("№", dp(15)),
                ("Date", dp(25)),
                ("Payment", dp(25)),
                ("Interest", dp(25)),
                ("Loan body", dp(25)),
                ("Debt", dp(25)),
            ],
            row_data=rows,
        )
        table_box.add_widget(self.table_widget)

    def draw_graph(self):
        graph_widget = self.screen.ids.graph_widget
        graph_widget.canvas.after.clear()

        if not self.graph_data:
            return

        x = graph_widget.x
        y = graph_widget.y
        w = graph_widget.width
        h = graph_widget.height

        if w <= 0 or h <= 0:
            return

        left_pad = dp(10)
        right_pad = dp(10)
        top_pad = dp(10)
        bottom_pad = dp(10)

        chart_x = x + left_pad
        chart_y = y + bottom_pad
        chart_w = w - left_pad - right_pad
        chart_h = h - top_pad - bottom_pad

        if chart_w <= 0 or chart_h <= 0:
            return

        max_total = max(item["principal"] + item["interest"] for item in self.graph_data)
        if max_total <= 0:
            return

        count = len(self.graph_data)
        gap = dp(2)
        bar_w = max((chart_w - gap * (count - 1)) / count, 1)

        axis_color = (1, 1, 1, 1) if self.theme_cls.theme_style == "Dark" else (0, 0, 0, 1)

        with graph_widget.canvas.after:
            Color(*axis_color)
            Line(points=[chart_x, chart_y, chart_x, chart_y + chart_h], width=1.2)
            Line(points=[chart_x, chart_y, chart_x + chart_w, chart_y], width=1.2)

            current_x = chart_x
            for item in self.graph_data:
                principal = item["principal"]
                interest = item["interest"]

                principal_h = (principal / max_total) * chart_h
                interest_h = (interest / max_total) * chart_h

                Color(1, 0, 0, 1)
                Rectangle(pos=(current_x, chart_y), size=(bar_w, principal_h))

                Color(0, 0, 1, 1)
                Rectangle(pos=(current_x, chart_y + principal_h), size=(bar_w, interest_h))

                current_x += bar_w + gap

    def draw_chart(self):
        chart_widget = self.screen.ids.chart_widget
        chart_widget.canvas.after.clear()

        interest = self.chart_interest_total
        principal = self.chart_principal_total
        total = interest + principal

        if total <= 0:
            return

        x = chart_widget.x
        y = chart_widget.y
        w = chart_widget.width
        h = chart_widget.height

        if w <= 0 or h <= 0:
            return

        size = min(w, h) * 0.9
        pie_x = x + (w - size) / 2
        pie_y = y + (h - size) / 2

        interest_angle = 360 * (interest / total)
        principal_angle = 360 - interest_angle

        with chart_widget.canvas.after:
            Color(1, 0, 0, 1)
            Ellipse(
                pos=(pie_x, pie_y),
                size=(size, size),
                angle_start=0,
                angle_end=principal_angle,
            )

            Color(0, 0, 1, 1)
            Ellipse(
                pos=(pie_x, pie_y),
                size=(size, size),
                angle_start=principal_angle,
                angle_end=360,
            )

    def calculate(self):
        loan_text = self.screen.ids.loan.text.strip()
        months_text = self.screen.ids.months.text.strip()
        interest_text = self.screen.ids.interest.text.strip()
        start_date_text = self.screen.ids.start_date.text.strip()
        payment_type = self.get_payment_type_value()

        if not loan_text or not months_text or not interest_text or not start_date_text:
            self.screen.ids.result_label.text = self.tr("fill_all_fields")
            return

        try:
            loan = float(loan_text)
            months = int(months_text)
            interest = float(interest_text)
            start_date = datetime.datetime.strptime(start_date_text, "%d-%m-%Y").date()
        except ValueError:
            self.screen.ids.result_label.text = self.tr("wrong_numbers")
            return

        if loan <= 0 or months <= 0 or interest < 0:
            self.screen.ids.result_label.text = self.tr("values_invalid")
            return

        monthly_rate = interest / 100 / 12

        rows = []
        graph_data = []
        debt = loan
        total_amount_of_payments = 0.0
        total_interest = 0.0
        total_principal = 0.0

        if payment_type == "annuity":
            if monthly_rate == 0:
                monthly_payment = loan / months
            else:
                monthly_payment = loan * (
                    monthly_rate / (1 - ((1 + monthly_rate) ** (-months)))
                )

            for i in range(months):
                pay_date = self.add_months(start_date, i)
                repayment_of_interest = debt * monthly_rate
                repayment_of_loan_body = monthly_payment - repayment_of_interest
                debt = debt - repayment_of_loan_body

                if debt < 0:
                    repayment_of_loan_body += debt
                    debt = 0

                total_amount_of_payments += monthly_payment
                total_interest += repayment_of_interest
                total_principal += repayment_of_loan_body

                rows.append((
                    str(i + 1),
                    pay_date.strftime("%d-%m-%Y"),
                    f"{monthly_payment:.2f}",
                    f"{repayment_of_interest:.2f}",
                    f"{repayment_of_loan_body:.2f}",
                    f"{debt:.2f}",
                ))

                graph_data.append({
                    "month": i + 1,
                    "interest": repayment_of_interest,
                    "principal": repayment_of_loan_body,
                })

            self.screen.ids.result_label.text = f"{self.tr('monthly_payment')}: {monthly_payment:.2f}"

        else:
            repayment_of_loan_body_const = loan / months

            for i in range(months):
                pay_date = self.add_months(start_date, i)
                repayment_of_interest = debt * monthly_rate
                monthly_payment = repayment_of_loan_body_const + repayment_of_interest
                debt = debt - repayment_of_loan_body_const

                if debt < 0:
                    debt = 0

                total_amount_of_payments += monthly_payment
                total_interest += repayment_of_interest
                total_principal += repayment_of_loan_body_const

                rows.append((
                    str(i + 1),
                    pay_date.strftime("%d-%m-%Y"),
                    f"{monthly_payment:.2f}",
                    f"{repayment_of_interest:.2f}",
                    f"{repayment_of_loan_body_const:.2f}",
                    f"{debt:.2f}",
                ))

                graph_data.append({
                    "month": i + 1,
                    "interest": repayment_of_interest,
                    "principal": repayment_of_loan_body_const,
                })

            self.screen.ids.result_label.text = f"{self.tr('first_payment')}: {rows[0][2]}"

        overpayment_loan = total_amount_of_payments - loan
        effective_interest_rate = (total_amount_of_payments / loan - 1) * 100

        self.screen.ids.total_amount_label.text = f"{self.tr('total_amount')}: {total_amount_of_payments:.2f}"
        self.screen.ids.overpayment_label.text = f"{self.tr('overpayment')}: {overpayment_loan:.2f}"
        self.screen.ids.effective_rate_label.text = f"{self.tr('effective_rate')}: {effective_interest_rate:.2f}%"

        self.graph_data = graph_data
        self.chart_interest_total = total_interest
        self.chart_principal_total = total_principal

        self.show_table(rows)
        Clock.schedule_once(lambda dt: self.draw_graph(), 0.05)
        Clock.schedule_once(lambda dt: self.draw_chart(), 0.05)

    def on_star_click(self):
        print("star clicked!")


MortgageCalculatorApp().run()