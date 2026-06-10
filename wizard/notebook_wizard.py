import time
from IPython.core.display_functions import display
from ipywidgets import widgets, HTML
from ipystream.voila.spinned_print_out import get_spinner_html, Spinned
from ipystream.voila.utils_tdqm import tqdm_out


# ── helpers ──────────────────────────────────────────────────────────────────

def _make_step_label(text: str) -> HTML:
    return HTML(f"<b style='font-size:14px'>{text}</b>")


def _make_buttons(*labels: str) -> list[widgets.Button]:
    buttons = []
    for label in labels:
        btn = widgets.Button(
            description=label,
            layout=widgets.Layout(width="220px"),
        )
        btn.layout.margin = "0 20px 0 0"
        buttons.append(btn)
    return buttons


def _make_nav_button(label: str, style: str = "info") -> widgets.Button:
    return widgets.Button(
        description=label,
        button_style=style,
        layout=widgets.Layout(width="120px", margin="0 10px 0 0"),
    )


# ── step panels ───────────────────────────────────────────────────────────────

def _build_step_a() -> tuple[widgets.VBox, list[widgets.Button]]:
    """Step A – pick a category."""
    label = _make_step_label("Step A  –  Choose a category")
    dropdown = widgets.Dropdown(
        description="Category:",
        options=["Alpha", "Beta", "Gamma"],
        layout=widgets.Layout(width="300px", margin="5px 0 10px 0"),
    )
    btn_load, btn_reset = _make_buttons("A) Load items", "A) Reset")
    box = widgets.VBox([label, dropdown, widgets.HBox([btn_load, btn_reset])])
    return box, [btn_load, btn_reset]


def _build_step_b() -> tuple[widgets.VBox, list[widgets.Button]]:
    """Step B – configure options."""
    label = _make_step_label("Step B  –  Configure options")
    slider = widgets.IntSlider(
        description="Count:",
        value=5, min=1, max=20,
        layout=widgets.Layout(width="350px", margin="5px 0 10px 0"),
    )
    chk = widgets.Checkbox(description="Enable feature X", value=False,
                           layout=widgets.Layout(margin="0 0 10px 0"))
    btn_apply, btn_preview = _make_buttons("B) Apply config", "B) Preview")
    box = widgets.VBox([label, slider, chk, widgets.HBox([btn_apply, btn_preview])])
    return box, [btn_apply, btn_preview]


def _build_step_c() -> tuple[widgets.VBox, list[widgets.Button]]:
    """Step C – review & validate."""
    label = _make_step_label("Step C  –  Review & validate")
    text_area = widgets.Textarea(
        placeholder="Add any notes here…",
        layout=widgets.Layout(width="400px", height="80px", margin="5px 0 10px 0"),
    )
    btn_validate, btn_clear = _make_buttons("C) Validate", "C) Clear notes")
    box = widgets.VBox([label, text_area, widgets.HBox([btn_validate, btn_clear])])
    return box, [btn_validate, btn_clear]


def _build_step_d() -> tuple[widgets.VBox, list[widgets.Button]]:
    """Step D – submit / finish."""
    label = _make_step_label("Step D  –  Submit")
    toggle = widgets.ToggleButton(
        description="I confirm",
        value=False,
        button_style="warning",
        layout=widgets.Layout(width="160px", margin="5px 0 10px 0"),
    )
    btn_submit, btn_dry_run = _make_buttons("D) Submit", "D) Dry run")
    box = widgets.VBox([label, toggle, widgets.HBox([btn_submit, btn_dry_run])])
    return box, [btn_submit, btn_dry_run]


# ── work functions (simulate real work) ──────────────────────────────────────

def _work_a_load(out):
    out.print("Loading items…")
    for i in tqdm_out(range(5), out):
        time.sleep(0.3)
    out.print("✓ 5 items loaded.")


def _work_a_reset(out):
    out.print("Resetting step A…")
    time.sleep(0.4)
    out.print("✓ Reset complete.")


def _work_b_apply(out):
    out.print("Applying configuration…")
    time.sleep(0.5)
    out.print("✓ Config applied.")


def _work_b_preview(out):
    out.print("Generating preview…")
    for i in tqdm_out(range(8), out):
        time.sleep(0.2)
    out.print("✓ Preview ready.")


def _work_c_validate(out):
    out.print("Validating data…")
    for i in tqdm_out(range(6), out):
        time.sleep(0.25)
    out.print("✓ Validation passed.")


def _work_c_clear(out):
    out.print("Notes cleared.")


def _work_d_submit(out):
    out.print("Submitting…")
    for i in tqdm_out(range(10), out):
        time.sleep(0.2)
    out.print("✓ Submitted successfully!")


def _work_d_dry_run(out):
    out.print("Dry-run only – nothing saved.")
    time.sleep(0.6)
    out.print("✓ Dry-run complete.")


# ── wizard shell ──────────────────────────────────────────────────────────────

def run():
    space = HTML("<br/>")

    # ── wizard header with step tabs ──────────────────────────────────────────
    step_labels = ["A  Choose", "B  Configure", "C  Review", "D  Submit"]
    step_tabs = widgets.ToggleButtons(
        options=step_labels,
        value=step_labels[0],
        layout=widgets.Layout(margin="0 0 10px 0"),
    )
    step_tabs.style.button_width = "140px"

    # ── build all four step panels ────────────────────────────────────────────
    panel_a, btns_a = _build_step_a()
    panel_b, btns_b = _build_step_b()
    panel_c, btns_c = _build_step_c()
    panel_d, btns_d = _build_step_d()

    panels = [panel_a, panel_b, panel_c, panel_d]
    all_buttons = btns_a + btns_b + btns_c + btns_d

    content_area = widgets.VBox([panel_a])  # show step A first

    # ── navigation row ────────────────────────────────────────────────────────
    btn_prev = _make_nav_button("◀  Back", "")
    btn_next = _make_nav_button("Next  ▶", "primary")
    nav_row = widgets.HBox([btn_prev, btn_next])

    # ── spinner / output area ─────────────────────────────────────────────────
    vbox = widgets.VBox()
    spinner_html = get_spinner_html()

    # ── assemble full wizard ──────────────────────────────────────────────────
    display(
        step_tabs,
        content_area,
        space,
        nav_row,
        space,
        spinner_html,
        vbox,
    )

    # ── step switching logic ──────────────────────────────────────────────────
    current_step = [0]  # mutable container so closures can write to it

    def _go_to(index: int):
        current_step[0] = index
        step_tabs.value = step_labels[index]
        content_area.children = [panels[index]]

    def _on_tab_change(change):
        if change["name"] == "value":
            _go_to(step_labels.index(change["new"]))

    step_tabs.observe(_on_tab_change)

    def _on_prev(_):
        if current_step[0] > 0:
            _go_to(current_step[0] - 1)

    def _on_next(_):
        if current_step[0] < len(panels) - 1:
            _go_to(current_step[0] + 1)

    btn_prev.on_click(_on_prev)
    btn_next.on_click(_on_next)

    # ── bind work functions to step buttons via Spinned ───────────────────────
    spinned = Spinned(vbox, spinner_html)

    work_map = {
        btns_a[0]: _work_a_load,
        btns_a[1]: _work_a_reset,
        btns_b[0]: _work_b_apply,
        btns_b[1]: _work_b_preview,
        btns_c[0]: _work_c_validate,
        btns_c[1]: _work_c_clear,
        btns_d[0]: _work_d_submit,
        btns_d[1]: _work_d_dry_run,
    }
    for btn, fn in work_map.items():
        spinned.bind(fn, btn)