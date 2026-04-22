from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

import datetime
import calendar


KV = '''
#:import dp kivy.metrics.dp

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    MDLabel:
        text: "Mortgage Calculator"
        font_style: "H5"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        MDList:
            OneLineListItem:
                text: "Ипотечный калькулятор"

<Tab>:
    BoxLayout:
        orientation: "vertical"

MDScreen:
    MDNavigationLayout:

        MDScreenManager:
            MDScreen:

                MDBoxLayout:
                    orientation: "vertical"

                    MDTopAppBar:
                        title: "Mortgage Calculator"
                        elevation: 4
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                    MDTabs:
                        id: tabs
                        on_tab_switch: app.on_tab_switch(*args)

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            ContentNavigationDrawer:
                id: content_drawer

<TabInput>:
    name: "input"

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            padding: dp(15)
            spacing: dp(15)

            MDTextField:
                id: loan
                hint_text: "Loan"
                helper_text: "Enter loan amount"
                helper_text_mode: "on_focus"
                icon_right: "cash"
                input_filter: "float"

            MDTextField:
                id: interest
                hint_text: "Interest"
                helper_text: "Enter annual interest rate"
                helper_text_mode: "on_focus"
                icon_right: "percent"
                input_filter: "float"

            MDTextField:
                id: months
                hint_text: "Months"
                helper_text: "Enter months"
                helper_text_mode: "on_focus"
                icon_right: "calendar-month"
                input_filter: "int"

            MDTextField:
                id: start_date
                hint_text: "Start date"
                helper_text: "Select start date"
                helper_text_mode: "on_focus"
                icon_right: "calendar"
                readonly: True
                on_focus:
                    if self.focus: app.show_date_picker()

            MDTextField:
                id: payment_type
                hint_text: "Payment type"
                helper_text: "Select payment type"
                helper_text_mode: "on_focus"
                icon_right: "menu-down"
                readonly: True
                on_focus:
                    if self.focus: app.menu.open()

            MDBoxLayout:
                adaptive_height: True
                spacing: dp(10)

                MDRaisedButton:
                    text: "Reset"
                    on_release: app.reset_fields()

                MDRaisedButton:
                    text: "Calc"
                    on_release: app.calc_table()

<TabTable>:
    name: "table"

    MDBoxLayout:
        id: table_box
        orientation: "vertical"
        padding: dp(10)

        MDLabel:
            text: "Payment table will appear here"
            halign: "center"

<TabGraph>:
    name: "graph"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)

        MDLabel:
            text: "Graph"
            halign: "center"

<TabChart>:
    name: "chart"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)

        MDLabel:
            text: "Chart"
            halign: "center"

<TabSum>:
    name: "sum"

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            padding: dp(15)
            spacing: dp(15)

            MDTextField:
                id: total_amount
                hint_text: "Total amount of payments"
                readonly: True

            MDTextField:
                id: overpayment
                hint_text: "Overpayment loan"
                readonly: True

            MDTextField:
                id: effective_rate
                hint_text: "Effective interest rate"
                readonly: True
'''


class ContentNavigationDrawer(BoxLayout):
    pass


class Tab(FloatLayout, MDTabsBase):
    title = StringProperty("")


class TabInput(Tab):
    pass


class TabTable(Tab):
    pass


class TabGraph(Tab):
    pass


class TabChart(Tab):
    pass


class TabSum(Tab):
    pass


class MortgageCalculatorApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        screen = Builder.load_string(KV)

        self.tab_input = TabInput(title="Input", icon="calculator")
        self.tab_table = TabTable(title="Table", icon="table")
        self.tab_graph = TabGraph(title="Graph", icon="chart-line")
        self.tab_chart = TabChart(title="Chart", icon="chart-pie")
        self.tab_sum = TabSum(title="Sum", icon="cash-multiple")

        screen.ids.tabs.add_widget(self.tab_input)
        screen.ids.tabs.add_widget(self.tab_table)
        screen.ids.tabs.add_widget(self.tab_graph)
        screen.ids.tabs.add_widget(self.tab_chart)
        screen.ids.tabs.add_widget(self.tab_sum)

        menu_items = [
            {
                "text": "annuity",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="annuity": self.set_payment_type(x),
            },
            {
                "text": "differentiated",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="differentiated": self.set_payment_type(x),
            },
        ]

        self.menu = MDDropdownMenu(
            caller=self.tab_input.ids.payment_type,
            items=menu_items,
            width_mult=4,
        )

        return screen

    def on_start(self):
        today = datetime.date.today()
        self.tab_input.ids.start_date.text = today.strftime("%d-%m-%Y")
        self.tab_input.ids.payment_type.text = "annuity"

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        print(f"tab clicked [{instance_tab}]")

    def set_payment_type(self, value):
        self.tab_input.ids.payment_type.text = value
        self.menu.dismiss()

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    def on_save_date(self, instance, value, date_range):
        self.tab_input.ids.start_date.text = value.strftime("%d-%m-%Y")

    def reset_fields(self):
        self.tab_input.ids.loan.text = ""
        self.tab_input.ids.interest.text = ""
        self.tab_input.ids.months.text = ""
        self.tab_input.ids.start_date.text = datetime.date.today().strftime("%d-%m-%Y")
        self.tab_input.ids.payment_type.text = "annuity"

        self.tab_sum.ids.total_amount.text = ""
        self.tab_sum.ids.overpayment.text = ""
        self.tab_sum.ids.effective_rate.text = ""

        self.clear_table()

    def show_error(self, text):
        self.dialog = MDDialog(
            title="Error",
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def clear_table(self):
        box = self.tab_table.ids.table_box
        box.clear_widgets()
        from kivy.uix.label import Label
        box.add_widget(Label(text="Payment table will appear here"))

    def add_months(self, source_date, months):
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def calc_table(self):
        try:
            start_date = self.tab_input.ids.start_date.text
            loan = self.tab_input.ids.loan.text
            months = self.tab_input.ids.months.text
            interest = self.tab_input.ids.interest.text
            payment_type = self.tab_input.ids.payment_type.text

            if not loan or not months or not interest or not start_date or not payment_type:
                self.show_error("Fill in all fields.")
                return

            start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
            loan = float(loan)
            months = int(months)
            interest = float(interest)

            if loan <= 0 or months <= 0 or interest < 0:
                self.show_error("Values must be valid and greater than zero.")
                return

            percent = interest / 100 / 12

            rows = []

            debt_end_month = loan
            total_amount_of_payments = 0.0

            if payment_type == "annuity":
                if percent == 0:
                    monthly_payment = loan / months
                else:
                    monthly_payment = loan * (
                        percent / (1 - ((1 + percent) ** (-months)))
                    )

                print(int(monthly_payment), monthly_payment)

                for i in range(months):
                    pay_date = self.add_months(start_date, i)
                    repayment_of_interest = debt_end_month * percent
                    repayment_of_loan_body = monthly_payment - repayment_of_interest
                    debt_end_month = debt_end_month - repayment_of_loan_body

                    if debt_end_month < 0:
                        repayment_of_loan_body += debt_end_month
                        debt_end_month = 0

                    total_amount_of_payments += monthly_payment

                    rows.append((
                        str(i + 1),
                        pay_date.strftime("%d-%m-%Y"),
                        f"{monthly_payment:.2f}",
                        f"{repayment_of_interest:.2f}",
                        f"{repayment_of_loan_body:.2f}",
                        f"{debt_end_month:.2f}",
                    ))

            else:  # differentiated
                repayment_of_loan_body_const = loan / months

                for i in range(months):
                    pay_date = self.add_months(start_date, i)
                    repayment_of_interest = debt_end_month * percent
                    monthly_payment = repayment_of_loan_body_const + repayment_of_interest
                    debt_end_month = debt_end_month - repayment_of_loan_body_const

                    if debt_end_month < 0:
                        debt_end_month = 0

                    total_amount_of_payments += monthly_payment

                    rows.append((
                        str(i + 1),
                        pay_date.strftime("%d-%m-%Y"),
                        f"{monthly_payment:.2f}",
                        f"{repayment_of_interest:.2f}",
                        f"{repayment_of_loan_body_const:.2f}",
                        f"{debt_end_month:.2f}",
                    ))

            overpayment_loan = total_amount_of_payments - loan
            effective_interest_rate = (total_amount_of_payments / loan - 1) * 100

            self.tab_sum.ids.total_amount.text = f"{total_amount_of_payments:.2f}"
            self.tab_sum.ids.overpayment.text = f"{overpayment_loan:.2f}"
            self.tab_sum.ids.effective_rate.text = f"{effective_interest_rate:.2f} %"

            self.show_table(rows)

        except Exception as e:
            self.show_error(str(e))

    def show_table(self, rows):
        box = self.tab_table.ids.table_box
        box.clear_widgets()

        table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            rows_num=10,
            check=False,
            column_data=[
                ("№", dp(18)),
                ("Date", dp(28)),
                ("Payment", dp(28)),
                ("Interest", dp(28)),
                ("Loan body", dp(30)),
                ("Debt", dp(28)),
            ],
            row_data=rows,
        )

        box.add_widget(table)


MortgageCalculatorApp().run()