#!/usr/bin/env python3
"""GLAZE UI V1.2 Frosted Neutral GTK4 Linux native Candidate reference.

This is a bounded native desktop/System Shell reference. GTK4 provides the native
widget/rendering surface while compositor-wide backdrop blur remains an explicit
separate shell/compositor integration gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gio, GLib, Gtk  # noqa: E402

ROOT = Path(__file__).resolve().parent
CSS_PATH = ROOT / "glaze-v1.2-linux.css"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--appearance", choices=("light", "dark", "deep-dark"), default="light")
    parser.add_argument("--reduced-transparency", action="store_true")
    parser.add_argument("--touch-assistance", action="store_true")
    parser.add_argument("--large-text", action="store_true")
    parser.add_argument("--evidence-file")
    parser.add_argument("--auto-interact", action="store_true")
    return parser.parse_args()


class SettingTile(Gtk.Button):
    def __init__(self, name: str, state: str, active: bool) -> None:
        super().__init__()
        self.setting_name = name
        self.setting_state = state
        self.active = active
        self.add_css_class("setting-tile")
        self.set_hexpand(True)
        self.set_vexpand(False)
        self.set_can_focus(True)

        labels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        labels.set_halign(Gtk.Align.FILL)
        labels.set_valign(Gtk.Align.CENTER)

        title = Gtk.Label(label=name, xalign=0)
        title.add_css_class("setting-name")
        title.set_wrap(True)
        subtitle = Gtk.Label(label=state, xalign=0)
        subtitle.add_css_class("setting-state")
        subtitle.set_wrap(True)
        labels.append(title)
        labels.append(subtitle)
        self.set_child(labels)
        self._sync_state()
        self.connect("clicked", self._on_clicked)

    def _sync_state(self) -> None:
        if self.active:
            self.add_css_class("active")
        else:
            self.remove_css_class("active")
        self.set_tooltip_text(
            f"{self.setting_name}: {self.setting_state}; "
            + ("active accent state" if self.active else "inactive neutral state")
        )

    def _on_clicked(self, _button: Gtk.Button) -> None:
        self.active = not self.active
        self._sync_state()


class GlazeLinuxCandidate(Gtk.Application):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(application_id="com.goreecloud.glazeui.reference.v12.linux", flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.args = args
        self.window: Gtk.ApplicationWindow | None = None
        self.primary: Gtk.Button | None = None
        self.secondary: Gtk.Button | None = None
        self.search_entry: Gtk.SearchEntry | None = None
        self.interaction_state: Gtk.Label | None = None
        self.tiles: list[SettingTile] = []
        self.evidence_written = False

    def do_activate(self) -> None:
        if self.window is not None:
            self.window.present()
            return
        self._load_css()
        self.window = self._build_window()
        self.window.present()
        GLib.timeout_add(250, self._after_present)

    def _load_css(self) -> None:
        provider = Gtk.CssProvider()
        provider.load_from_path(str(CSS_PATH))
        display = Gdk.Display.get_default()
        if display is None:
            raise RuntimeError("GTK display is unavailable")
        Gtk.StyleContext.add_provider_for_display(display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _build_window(self) -> Gtk.ApplicationWindow:
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("GLAZE UI V1.2 — Frosted Neutral Linux Candidate")
        window.set_default_size(1180, 820)
        window.set_size_request(760, 620)
        window.add_css_class("glaze-shell")
        if self.args.appearance == "dark":
            window.add_css_class("dark")
        elif self.args.appearance == "deep-dark":
            window.add_css_class("deep-dark")
        if self.args.reduced_transparency:
            window.add_css_class("reduced-transparency")
        if self.args.touch_assistance:
            window.add_css_class("touch-assistance")
        if self.args.large_text:
            window.add_css_class("large-text")

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_propagate_natural_height(True)
        window.set_child(scroll)

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.set_margin_top(24)
        page.set_margin_bottom(28)
        page.set_margin_start(24)
        page.set_margin_end(24)
        scroll.set_child(page)

        shell_bar = self._build_shell_bar()
        page.append(shell_bar)

        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        main.set_homogeneous(False)
        page.append(main)

        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        left.set_hexpand(True)
        left.append(self._build_hero())
        left.append(self._build_search())
        left.append(self._build_critical_system())
        left.append(self._build_actions())
        main.append(left)

        control = self._build_control_center()
        control.set_size_request(390, -1)
        control.set_valign(Gtk.Align.START)
        main.append(control)

        boundary = Gtk.Label(
            label=(
                "Candidate boundary: native GTK rendering and headless Linux evidence do not establish "
                "Wayland/compositor-wide backdrop blur fidelity, production shell integration, distribution "
                "packaging, assistive-technology certification, downstream conformance, or V1.2 Stable promotion."
            ),
            xalign=0,
        )
        boundary.set_wrap(True)
        boundary.add_css_class("boundary")
        page.append(boundary)
        return window

    def _build_shell_bar(self) -> Gtk.Widget:
        bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        bar.add_css_class("glass-overlay")
        bar.add_css_class("material-card")

        brand = Gtk.Label(label="GoreeCloud", xalign=0)
        brand.add_css_class("section-title")
        bar.append(brand)

        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        bar.append(spacer)

        for label in ("Workspace", "Search", "Settings"):
            button = Gtk.Button(label=label)
            button.add_css_class("shell-button")
            button.set_can_focus(True)
            bar.append(button)

        status = Gtk.Label(label="V1.2 Candidate")
        status.add_css_class("status-pill")
        status.set_margin_start(4)
        status.set_margin_end(4)
        status.set_margin_top(6)
        status.set_margin_bottom(6)
        bar.append(status)
        return bar

    def _build_hero(self) -> Gtk.Widget:
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("glass-overlay")
        card.add_css_class("material-card")

        kicker = Gtk.Label(label="GOREECLOUD · GLAZE UI V1.2 CANDIDATE", xalign=0)
        kicker.add_css_class("kicker")
        card.append(kicker)

        title = Gtk.Label(label="Neutral glass is the material.", xalign=0)
        title.add_css_class("title")
        title.set_wrap(True)
        card.append(title)

        body = Gtk.Label(
            label=(
                "Frosty white and neutral translucent surfaces carry the desktop. Color remains purposeful—"
                "reserved for active controls, focus, selection, status, progress, and GoreeCloud identity."
            ),
            xalign=0,
        )
        body.set_wrap(True)
        body.add_css_class("secondary")
        card.append(body)

        chips = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        for text in ("Frosted", "White / neutral", "Translucent", "Accent-led color"):
            chip = Gtk.Label(label=text)
            chip.add_css_class("status-pill")
            chip.set_margin_top(5)
            chip.set_margin_bottom(5)
            chip.set_margin_start(8)
            chip.set_margin_end(8)
            chips.append(chip)
        card.append(chips)
        return card

    def _build_search(self) -> Gtk.Widget:
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("glass-base")
        card.add_css_class("material-card")

        heading = Gtk.Label(label="Universal Search", xalign=0)
        heading.add_css_class("section-title")
        card.append(heading)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search GoreeCloud")
        self.search_entry.add_css_class("search-entry")
        self.search_entry.set_can_focus(True)
        card.append(self.search_entry)

        note = Gtk.Label(label="Glaze entry + deeper neutral result surface; no nested blur authority.", xalign=0)
        note.set_wrap(True)
        note.add_css_class("secondary")
        card.append(note)
        return card

    def _build_control_center(self) -> Gtk.Widget:
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        panel.add_css_class("glass-panel")
        panel.add_css_class("control-center")

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title = Gtk.Label(label="Quick Settings", xalign=0)
        title.add_css_class("section-title")
        title.set_hexpand(True)
        header.append(title)
        battery = Gtk.Label(label="72%")
        battery.add_css_class("status-pill")
        battery.set_margin_top(4)
        battery.set_margin_bottom(4)
        battery.set_margin_start(8)
        battery.set_margin_end(8)
        header.append(battery)
        panel.append(header)

        note = Gtk.Label(label="Neutral panel · accent only on active state", xalign=0)
        note.add_css_class("secondary")
        note.set_wrap(True)
        panel.append(note)

        for name, value, percent in (("Volume", "64%", 0.64), ("Brightness", "78%", 0.78)):
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            label_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            label = Gtk.Label(label=name, xalign=0)
            label.set_hexpand(True)
            label.add_css_class("secondary")
            amount = Gtk.Label(label=value, xalign=1)
            amount.add_css_class("secondary")
            label_row.append(label)
            label_row.append(amount)
            row.append(label_row)
            scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
            scale.set_value(percent * 100)
            scale.set_draw_value(False)
            scale.set_can_focus(True)
            row.append(scale)
            panel.append(row)

        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        grid.set_column_homogeneous(True)
        settings = (
            ("Wi-Fi", "Connected", True),
            ("Bluetooth", "On", True),
            ("Night Light", "Off", False),
            ("Performance", "Balanced", True),
            ("Airplane Mode", "Off", False),
            ("Focus", "Available", False),
        )
        for index, (name, state, active) in enumerate(settings):
            tile = SettingTile(name, state, active)
            self.tiles.append(tile)
            grid.attach(tile, index % 2, index // 2, 1, 1)
        panel.append(grid)

        foot = Gtk.Label(
            label="The panel remains neutral. Accent identifies state instead of tinting the entire shell.",
            xalign=0,
        )
        foot.set_wrap(True)
        foot.add_css_class("secondary")
        panel.append(foot)
        return panel

    def _build_critical_system(self) -> Gtk.Widget:
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        card.add_css_class("critical-system")

        kicker = Gtk.Label(label="CRITICAL SYSTEM", xalign=0)
        kicker.add_css_class("kicker")
        card.append(kicker)
        title = Gtk.Label(label="High-opacity clarity stays separate.", xalign=0)
        title.add_css_class("section-title")
        title.set_wrap(True)
        card.append(title)
        body = Gtk.Label(
            label=(
                "Security, privacy, identity, recovery, and destructive confirmations never depend on "
                "translucency or compositor blur for legibility."
            ),
            xalign=0,
        )
        body.set_wrap(True)
        body.add_css_class("secondary")
        card.append(body)
        return card

    def _build_actions(self) -> Gtk.Widget:
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("glass-raised")
        card.add_css_class("material-card")

        title = Gtk.Label(label="Native interaction", xalign=0)
        title.add_css_class("section-title")
        card.append(title)
        self.interaction_state = Gtk.Label(label="Action: Ready", xalign=0)
        self.interaction_state.add_css_class("secondary")
        card.append(self.interaction_state)

        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.primary = Gtk.Button(label="Primary action")
        self.primary.add_css_class("action-primary")
        self.primary.set_hexpand(True)
        self.primary.set_can_focus(True)
        self.primary.connect("clicked", self._primary_clicked)
        actions.append(self.primary)

        self.secondary = Gtk.Button(label="Secondary action")
        self.secondary.add_css_class("action-secondary")
        self.secondary.set_hexpand(True)
        self.secondary.set_can_focus(True)
        self.secondary.connect("clicked", self._secondary_clicked)
        actions.append(self.secondary)
        card.append(actions)
        return card

    def _primary_clicked(self, _button: Gtk.Button) -> None:
        assert self.interaction_state is not None and self.primary is not None
        self.interaction_state.set_label("Action: Complete")
        self.primary.set_label("Complete")

    def _secondary_clicked(self, _button: Gtk.Button) -> None:
        assert self.interaction_state is not None
        self.interaction_state.set_label("Action: Secondary")

    def _after_present(self) -> bool:
        if self.args.auto_interact and self.primary is not None:
            self.primary.emit("clicked")
        GLib.timeout_add(250, self._emit_evidence)
        return GLib.SOURCE_REMOVE

    def _emit_evidence(self) -> bool:
        if self.evidence_written:
            return GLib.SOURCE_REMOVE
        assert self.window is not None
        assert self.primary is not None and self.secondary is not None and self.search_entry is not None
        assert self.interaction_state is not None

        data = {
            "schemaVersion": 1,
            "product": "GLAZE UI V1.2 Frosted Neutral",
            "lifecycle": "Candidate native evidence",
            "platform": "Linux GTK4",
            "gtkVersion": f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}",
            "appearance": self.args.appearance,
            "reducedTransparency": self.args.reduced_transparency,
            "touchAssistance": self.args.touch_assistance,
            "largeText": self.args.large_text,
            "window": {
                "width": self.window.get_width(),
                "height": self.window.get_height(),
            },
            "targets": {
                "primary": self.primary.get_allocated_height(),
                "secondary": self.secondary.get_allocated_height(),
                "search": self.search_entry.get_allocated_height(),
                "tiles": {tile.setting_name: tile.get_allocated_height() for tile in self.tiles},
            },
            "settings": {tile.setting_name: {"state": tile.setting_state, "active": tile.active} for tile in self.tiles},
            "interactionState": self.interaction_state.get_label(),
            "materialAuthority": "neutral substrate; color reserved for accent/state",
            "criticalSystem": "high-opacity; non-backdrop-dependent",
            "ready": True,
            "boundaries": [
                "not compositor-wide Wayland backdrop blur fidelity",
                "not production shell integration",
                "not distribution packaging acceptance",
                "not physical-display qualification",
                "not assistive-technology certification",
                "not downstream application conformance",
                "not V1.2 Stable promotion",
            ],
        }
        if self.args.evidence_file:
            path = Path(self.args.evidence_file)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        else:
            print(json.dumps(data, indent=2), flush=True)
        self.evidence_written = True
        return GLib.SOURCE_REMOVE


def main() -> int:
    args = parse_args()
    app = GlazeLinuxCandidate(args)
    return app.run([sys.argv[0]])


if __name__ == "__main__":
    raise SystemExit(main())
