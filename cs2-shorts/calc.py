#!/usr/bin/env python3
"""Сколько месяцев Shorts по CS2 копят на 2 ПВЗ Ozon.

Все цифры ниже — ДОПУЩЕНИЯ-заглушки. Замените их реальными:
ставки партнёрок и цены интеграций — из чата по партнёркам,
просмотры — из YouTube Studio, стоимость точки — по конкретному помещению.

    python3 calc.py
"""

# --- цель ---------------------------------------------------------------
PVZ_COUNT = 2
PVZ_COST = 1_000_000          # ₽ на открытие одной точки (уточнить!)
RESERVE = 300_000             # ₽ подушка на первые месяцы работы
TAX = 0.06                    # самозанятый, платежи от юрлиц

# --- канал: стартовые значения и рост -----------------------------------
SHORTS_PER_MONTH = 60
VIEWS_MONTH_1 = 300_000       # суммарные просмотры за первый месяц
VIEWS_GROWTH = 1.5            # во сколько раз растут просмотры каждый месяц
VIEWS_CAP = 30_000_000        # потолок просмотров в месяц

# --- доходы -------------------------------------------------------------
AFFILIATE_PER_1K_VIEWS = 15   # ₽ партнёрок на 1 000 просмотров Shorts (заглушка)
VK_DZEN_PER_1K_VIEWS = 5      # ₽ с дублей на VK Клипы / Дзен на 1 000 просмотров YouTube (заглушка)
INTEGRATION_PRICE = 15_000    # ₽ за одну интеграцию (заглушка, из чата по партнёркам)
INTEGRATIONS_START_VIEWS = 3_000_000  # с какого охвата в месяц приходят рекламодатели
INTEGRATIONS_PER_MONTH = 3
PRODUCT_MONTHLY = 0           # ₽ в месяц со своего продукта (гайд, конфиг, тренировки)
PRODUCT_START_MONTH = 4

MAX_MONTHS = 36


def main():
    goal = PVZ_COUNT * PVZ_COST + RESERVE
    total, views = 0.0, VIEWS_MONTH_1
    print(f"Цель: {PVZ_COUNT} ПВЗ × {PVZ_COST:,} + подушка {RESERVE:,} = {goal:,} ₽\n".replace(",", " "))
    print(f"{'мес':>3} {'просмотры':>12} {'партнёрки':>10} {'VK/Дзен':>9} {'интегр.':>9} {'продукт':>9} {'за месяц':>10} {'накоплено':>11}")
    first_pvz = None
    for m in range(1, MAX_MONTHS + 1):
        aff = views / 1000 * AFFILIATE_PER_1K_VIEWS
        vk = views / 1000 * VK_DZEN_PER_1K_VIEWS
        integ = INTEGRATION_PRICE * INTEGRATIONS_PER_MONTH if views >= INTEGRATIONS_START_VIEWS else 0
        prod = PRODUCT_MONTHLY if m >= PRODUCT_START_MONTH else 0
        month = (aff + vk + integ + prod) * (1 - TAX)
        total += month
        print(f"{m:>3} {int(views):>12,} {int(aff):>10,} {int(vk):>9,} {int(integ):>9,} {int(prod):>9,} {int(month):>10,} {int(total):>11,}".replace(",", " "))
        if first_pvz is None and total >= PVZ_COST + RESERVE / PVZ_COUNT:
            first_pvz = m
        if total >= goal:
            print(f"\nПВЗ №1 — месяц {first_pvz}, цель на 2 ПВЗ — месяц {m}.")
            return
        views = min(views * VIEWS_GROWTH, VIEWS_CAP)
    print(f"\nЗа {MAX_MONTHS} мес. цель не набирается при этих допущениях — нужны интеграции дороже, свой продукт или больше охвата.")


if __name__ == "__main__":
    main()
