from typing import Dict, List
from django.db.models import QuerySet
from ads.models import Attribute

def apply_attribute_filters(qs: QuerySet, params: Dict[str, str]) -> QuerySet:
    """
    Застосовує динамічні фільтри за атрибутами.
    Підтримує:
      - attr_<slug>=a,b,c           (TEXT/CHOICE; OR по значеннях)
      - attr_<slug>_min / _max      (NUMBER)
      - attr_<slug>=true|false      (BOOLEAN)
    """
    # Збираємо всі ключі з префіксом attr_
    keys = [k for k in params.keys() if k.startswith("attr_")]
    # Групуємо по slug
    slugs = {k.split("_", 1)[1].split("_")[0] for k in keys}   # беремо перший сегмент після attr_

    for slug in slugs:
        try:
            attr = Attribute.objects.select_related("category").get(slug=slug)
        except Attribute.DoesNotExist:
            # невідомий атрибут — пропускаємо (або піднімаємо 400)
            continue

        if attr.type in (Attribute.TEXT, Attribute.CHOICE):
            raw = params.get(f"attr_{slug}")
            if not raw:
                continue
            values: List[str] = [v.strip() for v in raw.split(",") if v.strip()]
            if not values:
                continue
            # OR усередині атрибуту
            qs = qs.filter(attributes__attribute=attr).filter(
                (Q(attributes__value_text__in=values) | Q(attributes__option__value__in=values))
            )

        elif attr.type == Attribute.NUMBER:
            vmin = params.get(f"attr_{slug}_min")
            vmax = params.get(f"attr_{slug}_max")
            if vmin:
                qs = qs.filter(attributes__attribute=attr, attributes__value_number__gte=vmin)
            if vmax:
                qs = qs.filter(attributes__attribute=attr, attributes__value_number__lte=vmax)

        elif attr.type == Attribute.BOOLEAN:
            raw = params.get(f"attr_{slug}")
            if raw is None:
                continue
            val = str(raw).lower() in ("1", "true", "yes", "y", "on")
            qs = qs.filter(attributes__attribute=attr, attributes__value_bool=val)

    # Важливо: якщо ланцюжок фільтрів створює дублікати через JOIN — додай distinct()
    return qs.distinct()
