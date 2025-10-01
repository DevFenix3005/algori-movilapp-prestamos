from functools import partial
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.factory import Factory

from kivy.uix.recycleboxlayout import RecycleBoxLayout

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.recycleview import MDRecycleView

from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTertiaryText,
)


# ---------- Viewclass personalizado para el RecycleView ----------
class RVListItem(MDListItem):
    headline = StringProperty("")
    supporting = StringProperty("")
    tertiary = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Composición de subwidgets (headline, supporting, leading, trailing)
        self._head = (
            MDListItemHeadlineText(text=self.headline)
            if self.headline
            else MDListItemHeadlineText(text="")
        )
        # supporting es opcional:
        self._supp = (
            MDListItemSupportingText(text=self.supporting) if self.supporting else None
        )

        self._tert = (
            MDListItemTertiaryText(text=self.tertiary) if self.tertiary else None
        )

        self.add_widget(self._head)
        if self._supp:
            self.add_widget(self._supp)
        if self._tert:
            self.add_widget(self._tert)

        # Bind para que si el RV recicla y cambia props, el item se actualice
        self.bind(
            headline=self._on_headline,
            supporting=self._on_supporting,
            tertiary=self._on_tertiary,
        )

    # Actualizaciones en caliente
    def _on_headline(self, _, value):
        if not self._head:
            self._head = MDListItemHeadlineText(text=value)
            # Inserta después del leading si existe
            idx = 1 if self._lead else 0
            self.add_widget(self._head, index=idx)
        else:
            self._head.text = value

    def _on_supporting(self, _, value):
        if value:
            if not self._supp:
                self._supp = MDListItemSupportingText(text=value)
                # Colocar antes del trailing si existe
                self.add_widget(self._supp)
            else:
                self._supp.text = value
        else:
            if self._supp and self._supp.parent:
                self.remove_widget(self._supp)
            self._supp = None

    def _on_tertiary(self, _, value):
        if value:
            if not self._tert:
                self._tert = MDListItemTertiaryText(text=value)
                # Colocar antes del trailing si existe
                self.add_widget(self._tert)
            else:
                self._tert.text = value
        else:
            if self._tert and self._tert.parent:
                self.remove_widget(self._tert)
            self._tert = None


# Registrar el viewclass para poder usarlo por nombre en el RV
Factory.register("RVListItem", cls=RVListItem)


# ---------- Pantalla con MDRecycleView usando RVListItem ----------
class AmortizacionScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "amortizacion"

        root = MDBoxLayout(orientation="vertical", spacing=dp(8))

        rv_layout = RecycleBoxLayout(
            default_size=(None, dp(72)),
            default_size_hint=(1, None),
            size_hint_y=None,
            orientation="vertical",
            spacing=dp(6),
        )
        rv_layout.bind(minimum_height=rv_layout.setter("height"))
        self.rv = MDRecycleView(rv_layout)
        self.rv.viewclass = "RVListItem"  # <- nuestro viewclass

        root.add_widget(self.rv)
        self.add_widget(root)

    def set_items(self, items):
        # Cada entrada SOLO usa props simples (nada de widgets):
        # headline, supporting, leading_icon, trailing_icon, on_release, etc.
        self.clear_items()
        for i, it in enumerate(items):
            d = {
                "headline": it.get("headline", ""),
                "supporting": it.get("supporting", ""),
                "tertiary": it.get("tertiary", ""),
                "on_release": partial(self.on_item_press, i),
                # Puedes agregar md_bg_color, ripple_behavior, etc.
            }
            self.rv.data.append(d)

    def on_item_press(self, index, *args):
        it = self.rv.data[index]
        print(f"[Tap] {it.get('headline')}")

    def clear_items(self):
        self.rv.data = []
