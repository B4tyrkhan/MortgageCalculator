from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
import datetime

from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker

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
                        right_action_items: [["star-outline", lambda x: app.on_star_click()]]
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
                                    text: "Test Ok"
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

                                MDLabel:
                                    id: graph_label
                                    text: "Graph"
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

                                MDLabel:
                                    id: chart_label
                                    text: "Chart"
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

                                MDLabel:
                                    id: sum_label
                                    text: "Sum"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 1

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
        if self.text == "Dark/Light":
            app.toggle_theme()
        self.parent.set_color_item(self)


class DrawerList(MDList):
    def set_color_item(self, instance_item):
        app = MDApp.get_running_app()
        for item in self.children:
            item.text_color = app.theme_cls.text_color
        instance_item.text_color = app.theme_cls.primary_color


class MortgageCalculatorApp(MDApp):
    title = "Mortgage Calculator"
    by_who = "author Aliev Batyrkhan"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self.screen = None

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        self.screen = Builder.load_string(KV)
        Clock.schedule_once(self.setup_menu, 0.2)
        Clock.schedule_once(self.refresh_ui_colors, 0.2)
        return self.screen

    def setup_menu(self, *args):
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.payment_type,
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": "annuity",
                    "on_release": lambda: self.set_payment_type("annuity"),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "differentiated",
                    "on_release": lambda: self.set_payment_type("differentiated"),
                },
            ],
            width_mult=4,
        )

    def open_payment_menu(self):
        if self.menu:
            self.menu.caller = self.screen.ids.payment_type
            self.menu.open()

    def set_payment_type(self, value):
        self.screen.ids.payment_type.text = value
        self.screen.ids.payment_type.focus = False
        if self.menu:
            self.menu.dismiss()

    def on_start(self):
        menu_items = {
            "account-cowboy-hat": "About author",
            "youtube": "My YouTube",
            "coffee": "Donate author",
            "github": "Source code",
            "share-variant": "Share app",
            "shield-sun": "Dark/Light",
        }

        for icon_name, item_text in menu_items.items():
            self.screen.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=item_text)
            )

        self.screen.ids.start_date.text = datetime.date.today().strftime("%d-%m-%Y")
        self.screen.ids.loan.text = "5000000"
        self.screen.ids.months.text = "120"
        self.screen.ids.interest.text = "9.5"
        self.screen.ids.payment_type.text = "annuity"

        Clock.schedule_once(self.refresh_ui_colors, 0.2)

    def get_date(self, date_obj):
        print(date_obj)
        self.screen.ids.start_date.text = date_obj.strftime("%d-%m-%Y")

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
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

    def calculate(self):
        loan_text = self.screen.ids.loan.text.strip()
        months_text = self.screen.ids.months.text.strip()
        interest_text = self.screen.ids.interest.text.strip()
        payment_type = self.screen.ids.payment_type.text.strip()

        if not loan_text or not months_text or not interest_text:
            self.screen.ids.result_label.text = "Fill all fields"
            return

        try:
            loan = float(loan_text)
            months = int(months_text)
            interest = float(interest_text)
        except ValueError:
            self.screen.ids.result_label.text = "Wrong numbers"
            return

        if months <= 0:
            self.screen.ids.result_label.text = "Months must be > 0"
            return

        monthly_rate = interest / 100 / 12

        if payment_type == "annuity":
            if monthly_rate == 0:
                payment = loan / months
            else:
                payment = loan * (
                    monthly_rate * (1 + monthly_rate) ** months
                ) / ((1 + monthly_rate) ** months - 1)

            self.screen.ids.result_label.text = f"Monthly payment: {payment:.2f}"
        else:
            principal_payment = loan / months
            first_payment = principal_payment + loan * monthly_rate
            self.screen.ids.result_label.text = f"First payment: {first_payment:.2f}"

    def on_star_click(self):
        print("star clicked!")


MortgageCalculatorApp().run()