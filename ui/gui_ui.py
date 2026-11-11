#
#
# GUI
#
#


"""
Graphical interface for the Personal Finance Manager, built with FreeSimpleGUI.

Exactly like the Console UI, this module only builds windows, reads user
input and shows popups. Every action is delegated to the shared
FinanceManager so both front-ends behave identically.
"""

"""
FreeSimpleGUI was used as intended. 
Everything in the GUI (windows, buttons, tables, combos, images, charts) is built with FreeSimpleGUI (import FreeSimpleGUI as sg).

tkinter.ttk only shows up as a small supporting import in ui/gui_ui.py — FreeSimpleGUI is itself
built on top of tkinter, and its own API doesn’t expose enough control 
over ttk’s button/combobox styling (removing borders, custom padding, custom combo colors). 
So _style_buttons()/_style_combos() reach into ttk.Style() directly, purely to fine-tune the look 
of the FreeSimpleGUI-created widgets after the window is built. No windows or widgets are 
created with raw tkinter/ttk — sg.Window/sg.Button/etc. are the only things actually constructing UI.

I also verified your edits to console_ui.py, file_manager.py, and finance_manager.py still 
compile cleanly and the full test suite still passes (43/43), so nothing’s broken by the reformatting.

"""

#
# Imports
#


import os
import tkinter.ttk as ttk
from datetime import datetime
from decimal import Decimal

import FreeSimpleGUI as sg

from core.exceptions import FinanceManagerError

# --- Fixed, non-dark-mode-aware theme so text/backgrounds never flip to
# an unreadable white-on-white (or white-on-light) combination. ---
sg.theme("LightGrey1")

# Verdana 14 is the single font used everywhere in the GUI.
FONT = ("Verdana", 14)
FONT_BOLD = ("Verdana", 14, "bold")
sg.set_options(font=FONT)

# Font used only for the top nav buttons (Admin / Create / Edit / Erase /
# Dashboard), ~15% bigger than FONT so their icons read more clearly.
NAV_FONT = ("Verdana", 16)

# Default theme button color is white-on-blue ("#0079d3"); the About button
# uses a ~10% lighter shade of that same blue.
ABOUT_BUTTON_COLOR = ("#FFFFFF", "#1A86D7")

# "clam" is a pure-Tk ttk theme (unlike "aqua" on macOS) which means every
# color/border/padding we configure below is actually honored, instead of
# being silently ignored in favor of the native OS control appearance.
sg.set_options(use_ttk_buttons=True, ttk_theme="clam")

# --- Visual palette (approximating a clean, card-based dashboard look) ---
BG_PAGE = "#f4f6f8"
BG_SIDEBAR = "#cacdd0"  # ~15% darker than the original #eef1f5
BG_WHITE = "#ffffff"
TEXT_DARK = "#1c1f26"
TEXT_MUTED = "#5a6472"
INCOME_BG, INCOME_FG = "#e9f9ef", "#1e7e34"
EXPENSE_BG, EXPENSE_FG = "#fdecee", "#c0392b"
NET_BG, NET_FG = "#eaf2fd", "#1f6feb"
DOT_COLORS = ["#4C8BF5", "#F2994A", "#9B51E0", "#27AE60", "#EB5757", "#17A2B8", "#8395A7", "#F1C40F"]

# Dark "pill" style used for every dropdown (Period / Category / Type filters).
DROPDOWN_BG = "#334155"
DROPDOWN_FG = "#ffffff"

PERIOD_ALL = "All Time"
PERIOD_MONTH = "Last 30 Days"
PERIOD_TWO_WEEKS = "Last 2 Weeks"
PERIOD_WEEK = "Last Week"
PERIOD_YESTERDAY = "Yesterday"
PERIOD_TODAY = "Today"
PERIOD_CUSTOM = "Custom Range..."
PERIOD_OPTIONS = [
    PERIOD_ALL, PERIOD_MONTH, PERIOD_TWO_WEEKS, PERIOD_WEEK,
    PERIOD_YESTERDAY, PERIOD_TODAY, PERIOD_CUSTOM,
]

MAX_CATEGORY_ROWS = 8

# External spacing (pixels) kept *between* buttons/elements.
BTN_PAD = (10, 8)
# Internal ttk style padding: (5, 8) keeps the same horizontal size as the
# theme default (5px/side) while growing the vertical size ~20% (5px -> 8px
# per side), i.e. taller buttons without making them any wider.
BTN_STYLE_PADDING = (5, 8)


def _style_buttons(window: sg.Window) -> None:
    """Strip the default ttk border and apply the taller (height-only) padding
    to every button in `window`. Must be called after the window is finalized."""
    style = ttk.Style()
    for element in window.element_list():
        if isinstance(element, sg.Button) and hasattr(element, "ttk_style_name"):
            style.configure(
                element.ttk_style_name,
                borderwidth=0,
                relief="flat",
                padding=BTN_STYLE_PADDING,
            )


def _style_combos(window: sg.Window) -> None:
    """Force every dropdown to the dark/white 'pill' look with no border,
    regardless of what it was constructed with. Must be called after the
    window is finalized."""
    style = ttk.Style()
    for element in window.element_list():
        if isinstance(element, sg.Combo) and hasattr(element, "ttk_style_name"):
            style_name = element.ttk_style_name
            style.configure(
                style_name,
                foreground=DROPDOWN_FG,
                fieldbackground=DROPDOWN_BG,
                background=DROPDOWN_BG,
                bordercolor=DROPDOWN_BG,
                lightcolor=DROPDOWN_BG,
                arrowcolor=DROPDOWN_FG,
                borderwidth=0,
            )
            style.map(
                style_name,
                fieldbackground=[("readonly", DROPDOWN_BG)],
                foreground=[("readonly", DROPDOWN_FG)],
            )


def _money(value: Decimal) -> str:
    """Format a Decimal as a dollar amount with thousands separators."""
    return f"${value:,.2f}"


class GUIUI:
    """FreeSimpleGUI front-end driving a FinanceManager instance."""

    def __init__(self, finance_manager):
        self.finance_manager = finance_manager
        self._period_label = PERIOD_ALL
        self._period_bounds = (None, None)
        self._table_transaction_ids = []

    # ------------------------------------------------------------------ #
    # Main dashboard window
    # ------------------------------------------------------------------ #
    def run(self) -> None:
        window = self._build_main_window()

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "Exit"):
                break
            elif event == "Admin":
                self._admin_window()
                self._refresh_main_window(window)
            elif event == "About":
                self._show_about_window()
            elif event == "CSV File":
                self._show_csv_paths()
            elif event in ("Add Income", "Add Expense"):
                preset_name = "Income" if event == "Add Income" else "Expense"
                self._transaction_window(preset_type_name=preset_name)
                self._refresh_main_window(window)
            elif event == "Add Transaction":
                self._transaction_window()
                self._refresh_main_window(window)
            elif event == "Edit Transaction":
                selected_rows = values.get("-TABLE-")
                if not selected_rows:
                    sg.popup("Please select a transaction from the table first.", title="No Selection", font=FONT)
                else:
                    transaction_id = self._table_transaction_ids[selected_rows[0]]
                    self._transaction_window(transaction_id=transaction_id)
                    self._refresh_main_window(window)
            elif event == "Erase Transaction":
                selected_rows = values.get("-TABLE-")
                if not selected_rows:
                    sg.popup("Please select a transaction from the table first.", title="No Selection", font=FONT)
                else:
                    transaction_id = self._table_transaction_ids[selected_rows[0]]
                    self._erase_transaction(transaction_id)
                    self._refresh_main_window(window)
            elif event == "Dashboard":
                self._refresh_main_window(window)
                self._show_dashboard_charts(window)
            elif event == "-PERIOD-":
                self._handle_period_change(window, values["-PERIOD-"])
            elif event in ("-CATEGORY-FILTER-", "-TYPE-FILTER-"):
                self._refresh_main_window(window)

        window.close()

    def _show_csv_paths(self) -> None:
        paths = self.finance_manager.get_data_file_paths()
        message = (
            f"Transactions:\n{paths['transactions']}\n\n"
            f"Categories:\n{paths['categories']}\n\n"
            f"Types:\n{paths['types']}"
        )
        sg.popup(message, title="CSV File", font=FONT)

    def _erase_transaction(self, transaction_id: int) -> None:
        """Confirm with the user, then delete a single transaction."""
        confirm = sg.popup_yes_no(
            f"This will permanently erase transaction ID {transaction_id}.\n\n"
            "Are you sure you want to continue?",
            title="Erase Transaction",
            font=FONT,
        )
        if confirm != "Yes":
            return
        try:
            self.finance_manager.delete_transaction(transaction_id)
            sg.popup(f"Transaction ID {transaction_id} was erased.", title="Erase Transaction", font=FONT)
        except FinanceManagerError as error:
            sg.popup_error(str(error), title="Error", font=FONT)

    def _show_about_window(self) -> None:
        """Display the About window with the app badge image."""
        image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "about_badge.png")
        layout = [
            [sg.Image(filename=image_path)],
            [sg.Button("Close", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        window = sg.Window("About Personal Finance Manager", layout, modal=True, finalize=True, element_justification="center")
        _style_buttons(window)
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "Close"):
                break
        window.close()

    # ------------------------------------------------------------------ #
    # Dashboard charts (bar: Income vs Expenses, pie: by Category)
    # ------------------------------------------------------------------ #
    def _current_filter_selection(self, window: sg.Window):
        """Resolve the Category/Type filter combos' current text selections
        back into IDs, so chart data matches exactly what's on screen."""
        category_name = window["-CATEGORY-FILTER-"].get() or "All"
        type_name = window["-TYPE-FILTER-"].get() or "All"

        category_id = None
        if category_name not in ("All", "", None):
            match = next((c for c in self.finance_manager.get_categories() if c.name == category_name), None)
            category_id = match.category_id if match else None

        type_id = None
        if type_name not in ("All", "", None):
            match = next((t for t in self.finance_manager.get_types() if t["name"] == type_name), None)
            type_id = match["id"] if match else None

        return category_id, category_name, type_id, type_name

    def _show_dashboard_charts(self, window: sg.Window) -> None:
        category_id, category_name, type_id, type_name = self._current_filter_selection(window)
        start, end = self._period_bounds

        summary = self.finance_manager.dashboard_summary(
            start=start, end=end, category_id=category_id, type_id=type_id
        )
        category_totals = self.finance_manager.category_totals_abs(
            start=start, end=end, category_id=category_id, type_id=type_id
        )

        ranked_all = sorted(category_totals.items(), key=lambda kv: kv[1], reverse=True)
        total_categorized = sum(category_totals.values()) if category_totals else Decimal("0.00")
        if len(ranked_all) > MAX_CATEGORY_ROWS:
            ranked = ranked_all[:MAX_CATEGORY_ROWS - 1]
            other_total = sum(amount for _, amount in ranked_all[MAX_CATEGORY_ROWS - 1:])
            ranked = ranked + [(None, other_total)]
        else:
            ranked = ranked_all

        legend_rows = []
        for i, (cat_id, amount) in enumerate(ranked):
            color = DOT_COLORS[i % len(DOT_COLORS)]
            if cat_id is None:
                name = "Other"
            else:
                try:
                    name = self.finance_manager.get_category_by_id(cat_id).name
                except FinanceManagerError:
                    name = f"(deleted #{cat_id})"
            pct = (amount / total_categorized * 100) if total_categorized else Decimal("0")
            legend_rows.append([
                sg.Text("●", text_color=color, background_color=BG_WHITE),
                sg.Text(name, size=(14, 1), background_color=BG_WHITE, text_color=TEXT_DARK),
                sg.Text(f"{_money(amount)} ({pct:.1f}%)", background_color=BG_WHITE, text_color=TEXT_DARK),
            ])
        if not legend_rows:
            legend_rows = [[sg.Text("No data for this view.", background_color=BG_WHITE, text_color=TEXT_MUTED)]]

        subtitle = f"{self._period_label}  ·  Category: {category_name}  ·  Type: {type_name}"
        stats_line = (
            f"Transactions: {summary['transaction_count']}    "
            f"Net Balance: {_money(summary['net_balance'])}    "
            f"Total Categorized: {_money(total_categorized)}"
        )

        bar_graph = sg.Graph(canvas_size=(320, 300), graph_bottom_left=(0, 0), graph_top_right=(320, 300),
                              background_color=BG_WHITE, key="-BAR-GRAPH-")
        pie_graph = sg.Graph(canvas_size=(300, 300), graph_bottom_left=(0, 0), graph_top_right=(300, 300),
                              background_color=BG_WHITE, key="-PIE-GRAPH-")

        layout = [
            [sg.Text("Dashboard", font=("Verdana", 16, "bold"), background_color=BG_WHITE, text_color=TEXT_DARK)],
            [sg.Text(subtitle, background_color=BG_WHITE, text_color=TEXT_MUTED)],
            [sg.Text(stats_line, background_color=BG_WHITE, text_color=TEXT_DARK)],
            [sg.Column([[sg.Text("Income vs Expenses", font=FONT_BOLD,
                                  background_color=BG_WHITE, text_color=TEXT_DARK)], [bar_graph]],
                       background_color=BG_WHITE, vertical_alignment="top"),
             sg.Column([[sg.Text("By Category", font=FONT_BOLD,
                                  background_color=BG_WHITE, text_color=TEXT_DARK)], [pie_graph]],
                       background_color=BG_WHITE, vertical_alignment="top"),
             sg.Column(legend_rows, background_color=BG_WHITE, vertical_alignment="top")],
            [sg.Button("Close", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        chart_window = sg.Window("Dashboard", layout, modal=True, finalize=True, background_color=BG_WHITE)
        _style_buttons(chart_window)

        self._draw_bar_chart(chart_window["-BAR-GRAPH-"], summary["total_income"], summary["total_expenses"])
        self._draw_pie_chart(chart_window["-PIE-GRAPH-"], ranked, total_categorized)

        while True:
            event, _ = chart_window.read()
            if event in (sg.WIN_CLOSED, "Close"):
                break
        chart_window.close()

    def _draw_bar_chart(self, graph: sg.Graph, income: Decimal, expense: Decimal) -> None:
        graph.erase()
        margin_bottom, margin_top = 40, 30
        max_val = max(float(income), float(expense), 0.01)
        usable_height = 300 - margin_top - margin_bottom
        scale = usable_height / max_val
        bar_width, gap, x_start = 80, 40, 40

        for i, (label, value, color) in enumerate([
            ("Income", income, INCOME_FG), ("Expenses", expense, EXPENSE_FG)
        ]):
            x1 = x_start + i * (bar_width + gap)
            x2 = x1 + bar_width
            bar_height = float(value) * scale
            graph.draw_rectangle((x1, margin_bottom), (x2, margin_bottom + bar_height),
                                  fill_color=color, line_color=color)
            graph.draw_text(_money(value), (x1 + bar_width / 2, margin_bottom + bar_height + 15),
                             color=TEXT_DARK, font=FONT)
            graph.draw_text(label, (x1 + bar_width / 2, margin_bottom - 15), color=TEXT_DARK, font=FONT)

        graph.draw_line((20, margin_bottom), (300, margin_bottom), color=TEXT_MUTED)

    def _draw_pie_chart(self, graph: sg.Graph, ranked: list, total: Decimal) -> None:
        graph.erase()
        if not ranked or total == 0:
            graph.draw_text("No data for this view", (150, 150), color=TEXT_MUTED, font=FONT)
            return

        cx, cy, r = 150, 150, 120
        start_angle = 0.0
        for i, (_, amount) in enumerate(ranked):
            extent = 360 * float(amount) / float(total)
            color = DOT_COLORS[i % len(DOT_COLORS)]
            graph.draw_arc((cx - r, cy + r), (cx + r, cy - r), extent, start_angle,
                            style="pieslice", fill_color=color, arc_color=BG_WHITE, line_width=2)
            start_angle += extent

    # --- Layout builders -------------------------------------------------
    def _stat_card(self, title: str, key: str, bg: str, fg: str, icon: str) -> sg.Frame:
        return sg.Frame(
            "",
            [
                [sg.Text(f"{icon}  {title}", font=FONT, background_color=bg, text_color=fg)],
                [sg.Text("$0.00", key=key, font=FONT_BOLD, background_color=bg, text_color=fg)],
            ],
            background_color=bg, pad=(8, 8), border_width=0, expand_x=True, relief=sg.RELIEF_FLAT,
        )

    def _build_main_window(self) -> sg.Window:
        header = [
            # Icon is ~30% bigger than body text (14 -> 18); title is ~20% bigger (14 -> 17).
            sg.Text("💰", font=("Verdana", 18), background_color=BG_PAGE, text_color=TEXT_DARK),
            sg.Text("Personal Finance Manager", font=("Verdana", 17, "bold"),
                    background_color=BG_PAGE, text_color=TEXT_DARK),
            sg.Push(background_color=BG_PAGE),
            sg.Button("ℹ  About Personal Finance Manager", key="About", size=(30, 1), pad=BTN_PAD,
                      font=FONT, button_color=ABOUT_BUTTON_COLOR),
        ]
        nav = [
            sg.Button("⚙  Admin", key="Admin", size=(17, 1), pad=BTN_PAD, font=NAV_FONT),
            sg.Button("➕  Create Transaction", key="Add Transaction", size=(24, 1), pad=BTN_PAD, font=NAV_FONT),
            sg.Button("✎  Edit Transaction", key="Edit Transaction", size=(22, 1), pad=BTN_PAD, font=NAV_FONT),
            sg.Button("🗑  Erase Transaction", key="Erase Transaction", size=(22, 1), pad=BTN_PAD, font=NAV_FONT),
            sg.Button("📊  Dashboard", key="Dashboard", size=(24, 1), pad=BTN_PAD, font=NAV_FONT),
        ]
        cards = [
            self._stat_card("Total Income", "-INCOME-", INCOME_BG, INCOME_FG, "💰"),
            self._stat_card("Total Expenses", "-EXPENSES-", EXPENSE_BG, EXPENSE_FG, "💳"),
            self._stat_card("Net Balance", "-NET-", NET_BG, NET_FG, "⚖"),
        ]

        sidebar_rows = [
            [sg.Text("Quick Actions", font=FONT_BOLD, background_color=BG_SIDEBAR, text_color=TEXT_DARK)],
            [sg.Button("📄  CSV File", key="CSV File", size=(29, 1), pad=BTN_PAD, font=FONT)],
            [sg.Button("➖  Add Expense", key="Add Expense", size=(29, 1), pad=BTN_PAD, font=FONT)],
            [sg.Button("➕  Add Income", key="Add Income", size=(29, 1), pad=BTN_PAD, font=FONT)],
            [sg.HorizontalSeparator()],
            [sg.Text("Summary", font=FONT_BOLD, background_color=BG_SIDEBAR, text_color=TEXT_DARK)],
            [sg.Text("Current Balance", size=(16, 1), background_color=BG_SIDEBAR, text_color=TEXT_DARK),
             sg.Text("$0.00", key="-BALANCE-", font=FONT_BOLD, background_color=BG_SIDEBAR, text_color=TEXT_DARK)],
            [sg.Text("Income (Period)", size=(16, 1), background_color=BG_SIDEBAR, text_color=TEXT_DARK),
             sg.Text("$0.00", key="-SIDE-INCOME-", background_color=BG_SIDEBAR, text_color=INCOME_FG)],
            [sg.Text("Expenses (Period)", size=(16, 1), background_color=BG_SIDEBAR, text_color=TEXT_DARK),
             sg.Text("$0.00", key="-SIDE-EXPENSES-", background_color=BG_SIDEBAR, text_color=EXPENSE_FG)],
            [sg.Text("Net (Period)", size=(16, 1), background_color=BG_SIDEBAR, text_color=TEXT_DARK),
             sg.Text("$0.00", key="-SIDE-NET-", font=FONT_BOLD, background_color=BG_SIDEBAR, text_color=TEXT_DARK)],
            [sg.HorizontalSeparator()],
            [sg.Text("Categories (Expenses)", font=FONT_BOLD, background_color=BG_SIDEBAR, text_color=TEXT_DARK)],
        ]
        for i in range(MAX_CATEGORY_ROWS):
            sidebar_rows.append([
                sg.Text("", key=f"-CAT-DOT-{i}-", background_color=BG_SIDEBAR),
                sg.Text("", key=f"-CAT-NAME-{i}-", size=(16, 1),
                        background_color=BG_SIDEBAR, text_color=TEXT_DARK),
                sg.Text("", key=f"-CAT-AMT-{i}-", size=(10, 1), justification="right",
                        background_color=BG_SIDEBAR, text_color=TEXT_DARK),
            ])

        sidebar = sg.Column(sidebar_rows, background_color=BG_SIDEBAR, pad=(10, 10),
                             size=(320, 600), vertical_alignment="top")

        main_rows = [
            [sg.Text("☰ Transactions", font=FONT_BOLD, background_color=BG_PAGE, text_color=TEXT_DARK),
             sg.Text("   Category:", background_color=BG_PAGE, text_color=TEXT_DARK),
             sg.Combo([], key="-CATEGORY-FILTER-", enable_events=True, readonly=True,
                      font=FONT, background_color=BG_WHITE, text_color=TEXT_DARK, size=(16, 1)),
             sg.Text("Type:", background_color=BG_PAGE, text_color=TEXT_DARK),
             sg.Combo([], key="-TYPE-FILTER-", enable_events=True, readonly=True,
                      font=FONT, background_color=BG_WHITE, text_color=TEXT_DARK, size=(16, 1)),
             sg.Text("Period:", background_color=BG_PAGE, text_color=TEXT_DARK),
             sg.Combo(PERIOD_OPTIONS, default_value=PERIOD_ALL, key="-PERIOD-",
                      enable_events=True, readonly=True, font=FONT,
                      background_color=BG_WHITE, text_color=TEXT_DARK, size=(16, 1))],
            [sg.Table(
                values=[], headings=["ID", "TimeStamp", "Category", "Type", "Amount"],
                key="-TABLE-", enable_events=True, auto_size_columns=False,
                col_widths=[10, 19, 16, 11, 11], justification="left", num_rows=18,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE, font=FONT, header_font=FONT_BOLD,
                expand_x=True, expand_y=True, background_color=BG_WHITE,
                alternating_row_color="#f0f3f7", text_color=TEXT_DARK,
            )],
            [sg.Text("", key="-COUNT-", background_color=BG_PAGE, text_color=TEXT_MUTED),
             sg.Text("", key="-FOOTER-", background_color=BG_PAGE, text_color=TEXT_DARK,
                     justification="right", expand_x=True)],
        ]
        main_panel = sg.Column(main_rows, pad=(10, 10), background_color=BG_PAGE,
                                expand_x=True, expand_y=True)

        layout = [
            header,
            nav,
            cards,
            [sidebar, main_panel],
            [sg.Button("Exit", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        # The filter row now also holds the Period dropdown (moved out of the
        # stat-cards row), so the window needs ~200px of extra width to fit
        # everything on one line without crowding the table beneath it.
        window = sg.Window("Personal Finance Manager", layout, finalize=True,
                            resizable=True, background_color=BG_PAGE, size=(1300, 760))
        _style_buttons(window)
        _style_combos(window)
        self._refresh_main_window(window)
        return window

    # --- Period handling ---------------------------------------------------
    def _handle_period_change(self, window: sg.Window, selected: str) -> None:
        if selected == PERIOD_ALL:
            self._period_label, self._period_bounds = PERIOD_ALL, (None, None)
        elif selected == PERIOD_MONTH:
            self._period_label = PERIOD_MONTH
            self._period_bounds = self.finance_manager.last_n_days_bounds(30)
        elif selected == PERIOD_TWO_WEEKS:
            self._period_label = PERIOD_TWO_WEEKS
            self._period_bounds = self.finance_manager.last_n_days_bounds(14)
        elif selected == PERIOD_WEEK:
            self._period_label = PERIOD_WEEK
            self._period_bounds = self.finance_manager.last_n_days_bounds(7)
        elif selected == PERIOD_YESTERDAY:
            self._period_label = PERIOD_YESTERDAY
            self._period_bounds = self.finance_manager.day_bounds(1)
        elif selected == PERIOD_TODAY:
            self._period_label = PERIOD_TODAY
            self._period_bounds = self.finance_manager.day_bounds(0)
        elif selected == PERIOD_CUSTOM:
            bounds, label = self._ask_custom_range()
            if bounds is None:
                # User cancelled: revert the dropdown to the previous period.
                window["-PERIOD-"].update(value=self._period_label)
                return
            self._period_label, self._period_bounds = label, bounds

        self._refresh_main_window(window)

    def _ask_custom_range(self):
        layout = [
            [sg.Text("Custom Date Range", font=FONT_BOLD)],
            [sg.Text("Start date (YYYY-MM-DD):"), sg.Input(key="-START-", size=(14, 1), font=FONT)],
            [sg.Text("End date (YYYY-MM-DD):  "), sg.Input(key="-END-", size=(14, 1), font=FONT)],
            [sg.Button("Apply", size=(12, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Cancel", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        window = sg.Window("Custom Range", layout, modal=True, finalize=True)
        _style_buttons(window)

        result = None
        label = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            if event == "Apply":
                try:
                    bounds = self.finance_manager.parse_date_range(values["-START-"], values["-END-"])
                    result = bounds
                    label = f"{values['-START-'].strip()} to {values['-END-'].strip()}"
                    break
                except FinanceManagerError as error:
                    sg.popup_error(str(error), title="Invalid Date Range", font=FONT)

        window.close()
        return result, label

    # --- Refresh ------------------------------------------------------------
    def _refresh_main_window(self, window: sg.Window) -> None:
        start, end = self._period_bounds
        summary = self.finance_manager.dashboard_summary(start=start, end=end)
        all_time_summary = self.finance_manager.dashboard_summary()

        window["-INCOME-"].update(_money(summary["total_income"]))
        window["-EXPENSES-"].update(_money(summary["total_expenses"]))
        window["-NET-"].update(_money(summary["net_balance"]))

        window["-BALANCE-"].update(_money(all_time_summary["net_balance"]))
        window["-SIDE-INCOME-"].update(_money(summary["total_income"]))
        window["-SIDE-EXPENSES-"].update(_money(summary["total_expenses"]))
        window["-SIDE-NET-"].update(_money(summary["net_balance"]))

        self._refresh_category_breakdown(window, start, end)

        # Remember what the user had selected *before* touching `values=`,
        # since Combo.update(values=...) without an explicit value= blanks
        # the current selection. Only fall back to "All" if the previous
        # selection is gone (e.g. its category/type was deleted) or this is
        # the very first refresh.
        previous_category = window["-CATEGORY-FILTER-"].get() or "All"
        previous_type = window["-TYPE-FILTER-"].get() or "All"

        category_options = ["All"] + [c.name for c in self.finance_manager.get_categories()]
        type_options = ["All"] + [t["name"] for t in self.finance_manager.get_types()]

        category_filter = previous_category if previous_category in category_options else "All"
        type_filter = previous_type if previous_type in type_options else "All"

        window["-CATEGORY-FILTER-"].update(values=category_options, value=category_filter)
        window["-TYPE-FILTER-"].update(values=type_options, value=type_filter)

        rows = []
        self._table_transaction_ids = []
        for transaction in self.finance_manager.get_transactions(start=start, end=end):
            try:
                category_name = self.finance_manager.get_category_by_id(transaction.category_id).name
            except FinanceManagerError:
                category_name = "(deleted)"
            try:
                type_name = self.finance_manager.get_type_name(transaction.type_id)
            except FinanceManagerError:
                type_name = "(deleted)"

            if category_filter not in ("All", "", None) and category_name != category_filter:
                continue
            if type_filter not in ("All", "", None) and type_name != type_filter:
                continue

            rows.append([transaction.transaction_id, transaction.timestamp,
                         category_name, type_name, str(transaction.amount)])
            self._table_transaction_ids.append(transaction.transaction_id)

        window["-TABLE-"].update(values=rows)
        window["-COUNT-"].update(f"Showing {len(rows)} transactions  ·  {self._period_label}")
        window["-FOOTER-"].update(
            f"Total Income: {_money(summary['total_income'])}    "
            f"Total Expenses: {_money(summary['total_expenses'])}    "
            f"Net: {_money(summary['net_balance'])}"
        )

    def _refresh_category_breakdown(self, window: sg.Window, start, end) -> None:
        totals = self.finance_manager.expenses_by_category(start=start, end=end)
        ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)

        for i in range(MAX_CATEGORY_ROWS):
            if i < len(ranked):
                category_id, amount = ranked[i]
                try:
                    name = self.finance_manager.get_category_by_id(category_id).name
                except FinanceManagerError:
                    name = f"(deleted #{category_id})"
                color = DOT_COLORS[i % len(DOT_COLORS)]
                window[f"-CAT-DOT-{i}-"].update("●", text_color=color)
                window[f"-CAT-NAME-{i}-"].update(name)
                window[f"-CAT-AMT-{i}-"].update(_money(amount))
            else:
                window[f"-CAT-DOT-{i}-"].update("")
                window[f"-CAT-NAME-{i}-"].update("")
                window[f"-CAT-AMT-{i}-"].update("")

    # ------------------------------------------------------------------ #
    # Admin
    # ------------------------------------------------------------------ #
    def _admin_window(self) -> None:
        admin_btn_size = (30, 1)
        # Lighter blue (~200% lighter than NET_FG "#1f6feb") used only for Leave Admin.
        leave_admin_color = (TEXT_DARK, "#cfe2ff")
        layout = [
            [sg.Text("Admin", font=FONT_BOLD)],
            [sg.Button("Manage Categories", size=admin_btn_size, pad=BTN_PAD, font=FONT)],
            [sg.Button("Manage Types", size=admin_btn_size, pad=BTN_PAD, font=FONT)],
            [sg.Button("Initialize Transaction File", size=admin_btn_size, pad=BTN_PAD, font=FONT)],
            [sg.Button("Upload CSV File", size=admin_btn_size, pad=BTN_PAD, font=FONT)],
            [sg.Column([[]], size=(1, 200), pad=(0, 0))],
            [sg.Button("Leave Admin", size=admin_btn_size, pad=BTN_PAD, font=FONT, button_color=leave_admin_color)],
        ]
        window = sg.Window("Admin", layout, modal=True, finalize=True)
        _style_buttons(window)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Leave Admin"):
                break
            elif event == "Manage Categories":
                self._category_admin_window()
            elif event == "Manage Types":
                self._type_admin_window()
            elif event == "Initialize Transaction File":
                self._erase_transactions_dialog()
            elif event == "Upload CSV File":
                self._upload_csv_dialog()

        window.close()

    def _erase_transactions_dialog(self) -> None:
        count = len(self.finance_manager.get_transactions())
        if count == 0:
            sg.popup("There are no transactions to erase.", title="Nothing to Erase", font=FONT)
            return

        confirmed = sg.popup_yes_no(
            f"This will erase all {count} transactions and save a backup to "
            "transaction_backup.csv.\n\nContinue?",
            title="Confirm Erase", font=FONT,
        )
        if confirmed != "Yes":
            return

        try:
            backup_path = self.finance_manager.erase_transactions()
            sg.popup(f"All transactions erased.\nBackup saved to:\n{backup_path}", title="Done", font=FONT)
        except FinanceManagerError as error:
            sg.popup_error(str(error), title="Error", font=FONT)

    def _upload_csv_dialog(self) -> None:
        current_dir = os.path.dirname(self.finance_manager.get_data_file_paths()["transactions"])

        source_path = sg.popup_get_file(
            "Select a transactions CSV file to upload:",
            title="Upload CSV File",
            initial_folder=current_dir,
            file_types=(("CSV Files", "*.csv"), ("All Files", "*.*")),
            font=FONT,
        )
        if not source_path:
            return

        if not os.path.isfile(source_path):
            sg.popup_error(f"File not found: {source_path}", title="Error", font=FONT)
            return

        confirmed = sg.popup_yes_no(
            "The current transactions.csv will be backed up to transaction_backup.csv "
            "before it is replaced.\n\nDo you want to continue?",
            title="Confirm Upload", font=FONT,
        )
        if confirmed != "Yes":
            return

        try:
            backup_path = self.finance_manager.replace_transactions_file(source_path)
            sg.popup(
                f"transactions.csv replaced successfully.\nPrevious data backed up to:\n{backup_path}",
                title="Done", font=FONT,
            )
        except FinanceManagerError as error:
            sg.popup_error(str(error), title="Error", font=FONT)

    # --- Category administration ---------------------------------------
    def _category_admin_window(self) -> None:
        def build_rows():
            return [[c.category_id, c.name] for c in self.finance_manager.get_categories()]

        layout = [
            [sg.Text("Manage Categories", font=FONT_BOLD)],
            [sg.Table(
                values=build_rows(), headings=["ID", "Category"], key="-CAT-TABLE-",
                auto_size_columns=False, col_widths=[8, 40], justification="left", num_rows=10,
                font=FONT, header_font=FONT_BOLD, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                enable_events=True, expand_x=True,
            )],
            [sg.Button("Add Category", size=(16, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Edit Category", size=(16, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Delete Category", size=(16, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Close", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        window = sg.Window("Admin - Categories", layout, modal=True, finalize=True)
        _style_buttons(window)
        category_ids = [c.category_id for c in self.finance_manager.get_categories()]

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Close"):
                break

            selected_rows = values.get("-CAT-TABLE-")
            selected_id = category_ids[selected_rows[0]] if selected_rows else None

            # Only rebuild the table when the data actually changed. Rebuilding
            # it on every event (including the table's own selection event)
            # wiped out the row the user had just clicked, making it look like
            # selection/editing didn't work at all.
            data_changed = False

            if event == "Add Category":
                self._category_form_window()
                data_changed = True
            elif event == "Edit Category":
                if selected_id is None:
                    sg.popup("Please select a category first.", title="No Selection", font=FONT)
                else:
                    self._category_form_window(category_id=selected_id)
                    data_changed = True
            elif event == "Delete Category":
                if selected_id is None:
                    sg.popup("Please select a category first.", title="No Selection", font=FONT)
                else:
                    try:
                        self.finance_manager.delete_category(selected_id)
                    except FinanceManagerError as error:
                        sg.popup_error(str(error), title="Cannot Delete Category", font=FONT)
                    data_changed = True

            if data_changed:
                category_ids = [c.category_id for c in self.finance_manager.get_categories()]
                window["-CAT-TABLE-"].update(values=build_rows())

        window.close()

    def _category_form_window(self, category_id=None) -> None:
        editing = category_id is not None
        current_name = self.finance_manager.get_category_by_id(category_id).name if editing else ""

        layout = [
            [sg.Text("Edit Category" if editing else "Add Category", font=FONT_BOLD)],
            [sg.Text("Name:"), sg.Input(current_name, key="-NAME-", font=FONT, size=(24, 1))],
            [sg.Button("Save", size=(12, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Cancel", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        window = sg.Window("Category", layout, modal=True, finalize=True)
        _style_buttons(window)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            if event == "Save":
                try:
                    if editing:
                        self.finance_manager.edit_category(category_id, values["-NAME-"])
                    else:
                        self.finance_manager.add_category(values["-NAME-"])
                    break
                except FinanceManagerError as error:
                    sg.popup_error(str(error), title="Validation Error", font=FONT)

        window.close()

    # --- Type administration ---------------------------------------------
    def _type_admin_window(self) -> None:
        def build_rows():
            return [[t["id"], t["name"]] for t in self.finance_manager.get_types()]

        layout = [
            [sg.Text("Manage Types", font=FONT_BOLD)],
            [sg.Table(
                values=build_rows(), headings=["ID", "Type"], key="-TYPE-TABLE-",
                auto_size_columns=False, col_widths=[8, 40], justification="left", num_rows=10,
                font=FONT, header_font=FONT_BOLD, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                enable_events=True, expand_x=True,
            )],
            [sg.Button("Add Type", size=(16, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Edit Type", size=(16, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Delete Type", size=(16, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Close", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        window = sg.Window("Admin - Types", layout, modal=True, finalize=True)
        _style_buttons(window)
        type_ids = [t["id"] for t in self.finance_manager.get_types()]

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Close"):
                break

            selected_rows = values.get("-TYPE-TABLE-")
            selected_id = type_ids[selected_rows[0]] if selected_rows else None

            # See the matching comment in _category_admin_window: only rebuild
            # the table when the data actually changed, never on a plain
            # row-selection event, or the selection gets wiped immediately.
            data_changed = False

            if event == "Add Type":
                self._type_form_window()
                data_changed = True
            elif event == "Edit Type":
                if selected_id is None:
                    sg.popup("Please select a type first.", title="No Selection", font=FONT)
                else:
                    self._type_form_window(type_id=selected_id)
                    data_changed = True
            elif event == "Delete Type":
                if selected_id is None:
                    sg.popup("Please select a type first.", title="No Selection", font=FONT)
                else:
                    try:
                        self.finance_manager.delete_type(selected_id)
                    except FinanceManagerError as error:
                        sg.popup_error(str(error), title="Cannot Delete Type", font=FONT)
                    data_changed = True

            if data_changed:
                type_ids = [t["id"] for t in self.finance_manager.get_types()]
                window["-TYPE-TABLE-"].update(values=build_rows())

        window.close()

    def _type_form_window(self, type_id=None) -> None:
        editing = type_id is not None
        current_name = self.finance_manager.get_type_name(type_id) if editing else ""

        layout = [
            [sg.Text("Edit Type" if editing else "Add Type", font=FONT_BOLD)],
            [sg.Text("Name:"), sg.Input(current_name, key="-NAME-", font=FONT, size=(24, 1))],
            [sg.Button("Save", size=(12, 1), pad=BTN_PAD, font=FONT),
             sg.Button("Cancel", size=(12, 1), pad=BTN_PAD, font=FONT)],
        ]
        window = sg.Window("Type", layout, modal=True, finalize=True)
        _style_buttons(window)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            if event == "Save":
                try:
                    if editing:
                        self.finance_manager.edit_type(type_id, values["-NAME-"])
                    else:
                        self.finance_manager.add_type(values["-NAME-"])
                    break
                except FinanceManagerError as error:
                    sg.popup_error(str(error), title="Validation Error", font=FONT)

        window.close()

    # ------------------------------------------------------------------ #
    # Add / Edit transaction
    # ------------------------------------------------------------------ #
    def _transaction_window(self, transaction_id=None, preset_type_name=None) -> None:
        if not self.finance_manager.get_categories():
            sg.popup("No categories are available. Please create a category before adding a transaction.",
                     title="No Categories", font=FONT)
            return
        if not self.finance_manager.get_types():
            sg.popup("No transaction types are available. Please create a type before adding a transaction.",
                     title="No Types", font=FONT)
            return

        editing = transaction_id is not None
        transaction = self.finance_manager.get_transaction_by_id(transaction_id) if editing else None

        types = self.finance_manager.get_types()
        type_names = [t["name"] for t in types]
        type_id_by_name = {t["name"]: t["id"] for t in types}
        type_name_by_id = {t["id"]: t["name"] for t in types}

        categories = self.finance_manager.get_categories()
        category_names = [c.name for c in categories]
        category_by_name = {c.name: c.category_id for c in categories}
        category_by_id = {c.category_id: c.name for c in categories}

        now = datetime.now()
        if editing:
            default_type = type_name_by_id.get(transaction.type_id, type_names[0])
            default_category = category_by_id.get(transaction.category_id, category_names[0])
            default_amount = str(abs(transaction.amount))
            existing_timestamp = datetime.strptime(transaction.timestamp, "%Y-%m-%d %H:%M:%S")
            default_date = existing_timestamp.strftime("%Y-%m-%d")
            default_time = existing_timestamp.strftime("%H:%M:%S")
        else:
            preset_match = next((n for n in type_names if n.lower() == (preset_type_name or "").lower()), None)
            default_type = preset_match or type_names[0]
            default_category = category_names[0]
            default_amount = ""
            default_date = now.strftime("%Y-%m-%d")
            default_time = now.strftime("%H:%M:%S")

        # ~20% bigger than the rest of the GUI (14 -> 17), with a fixed label
        # width so every input/dropdown starts at the same horizontal pixel.
        tx_font = ("Verdana", 17)
        tx_font_bold = ("Verdana", 17, "bold")
        label_size = (10, 1)
        input_size = (24, 1)
        label_pad = ((5, 10), (12, 12))
        input_pad = ((0, 5), (12, 12))

        layout = [
            [sg.Text("Edit Transaction" if editing else "Add Transaction", font=tx_font_bold,
                      pad=((5, 5), (15, 25)))],
            [sg.Text("Type:", size=label_size, font=tx_font, pad=label_pad),
             sg.Combo(type_names, default_value=default_type, key="-TYPE-",
                      readonly=True, font=tx_font, size=input_size, pad=input_pad)],
            [sg.Text("Category:", size=label_size, font=tx_font, pad=label_pad),
             sg.Combo(category_names, default_value=default_category,
                      key="-CATEGORY-", readonly=True, font=tx_font, size=input_size, pad=input_pad)],
            [sg.Text("Amount:", size=label_size, font=tx_font, pad=label_pad),
             sg.Input(default_amount, key="-AMOUNT-", font=tx_font, size=input_size, pad=input_pad)],
            [sg.Text("Date:", size=label_size, font=tx_font, pad=label_pad),
             sg.Input(default_date, key="-DATE-", font=tx_font, size=input_size, pad=input_pad),
             sg.CalendarButton("📅", target="-DATE-", format="%Y-%m-%d",
                                pad=((5, 5), (12, 12)), font=tx_font, no_titlebar=False)],
            [sg.Text("Time:", size=label_size, font=tx_font, pad=label_pad),
             sg.Input(default_time, key="-TIME-", font=tx_font, size=input_size, pad=input_pad)],
            [sg.Button("Save Transaction", size=(18, 1), pad=BTN_PAD, font=tx_font),
             sg.Button("Cancel", size=(12, 1), pad=BTN_PAD, font=tx_font)],
        ]
        window = sg.Window("Transaction", layout, modal=True, finalize=True)
        _style_buttons(window)
        _style_combos(window)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                break
            if event == "Save Transaction":
                type_id = type_id_by_name[values["-TYPE-"]]
                category_id = category_by_name[values["-CATEGORY-"]]
                try:
                    timestamp = self.finance_manager.combine_date_time(values["-DATE-"], values["-TIME-"])
                    if editing:
                        self.finance_manager.edit_transaction(
                            transaction_id, category_id=category_id,
                            amount=values["-AMOUNT-"], type_id=type_id, timestamp=timestamp,
                        )
                    else:
                        self.finance_manager.add_transaction(
                            type_id=type_id, category_id=category_id, amount=values["-AMOUNT-"],
                            timestamp=timestamp,
                        )
                    break
                except FinanceManagerError as error:
                    sg.popup_error(str(error), title="Validation Error", font=FONT)

        window.close()
