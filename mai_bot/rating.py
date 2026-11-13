from decimal import Decimal, InvalidOperation, ROUND_FLOOR

MAX_ACHIEVEMENT = Decimal("101.0000")
RATING_ACHIEVEMENT_CAP = Decimal("100.5")
AP_BONUS = 1

# (最低達成率, 評級, 係數)，由高到低
RANK_TABLE = [
    (Decimal("100.5"), "SSS+", Decimal("22.4")),
    (Decimal("100.4999"), "SSS", Decimal("22.2")),
    (Decimal("100.0"), "SSS", Decimal("21.6")),
    (Decimal("99.9999"), "SS+", Decimal("21.4")),
    (Decimal("99.5"), "SS+", Decimal("21.1")),
    (Decimal("99.0"), "SS", Decimal("20.8")),
    (Decimal("98.0"), "S+", Decimal("20.3")),
    (Decimal("97.0"), "S", Decimal("20.0")),
    (Decimal("94.0"), "AAA", Decimal("16.8")),
    (Decimal("90.0"), "AA", Decimal("15.2")),
    (Decimal("80.0"), "A", Decimal("13.6")),
    (Decimal("75.0"), "BBB", Decimal("12.0")),
    (Decimal("70.0"), "BB", Decimal("11.2")),
    (Decimal("60.0"), "B", Decimal("9.6")),
    (Decimal("50.0"), "C", Decimal("8.0")),
    (Decimal("40.0"), "D", Decimal("6.4")),
    (Decimal("30.0"), "D", Decimal("4.8")),
    (Decimal("20.0"), "D", Decimal("3.2")),
    (Decimal("10.0"), "D", Decimal("1.6")),
    (Decimal("0"), "D", Decimal("0")),
]


def get_rank(achievement: Decimal) -> tuple[str, Decimal]:
    for threshold, rank, factor in RANK_TABLE:
        if achievement >= threshold:
            return rank, factor
    return "D", Decimal("0")


def calc_rating(ds: Decimal, achievement: Decimal) -> int:
    _, factor = get_rank(achievement)
    capped = min(achievement, RATING_ACHIEVEMENT_CAP)
    value = (ds * capped * factor / 100).to_integral_value(rounding=ROUND_FLOOR)
    rating = int(value)
    if achievement == MAX_ACHIEVEMENT:
        rating += AP_BONUS
    return rating


def rating_message(keyword: str) -> str:
    usage = "用法：`!rating <定數> <達成率>`，例如 `!rating 14.0 100.5`"
    parts = keyword.replace("%", "").split()
    if len(parts) != 2:
        return usage

    try:
        ds = Decimal(parts[0])
        achievement = Decimal(parts[1])
    except InvalidOperation:
        return usage

    if not (Decimal("1.0") <= ds <= Decimal("15.0")):
        return "定數需介於 1.0 ~ 15.0"
    if not (Decimal("0") <= achievement <= MAX_ACHIEVEMENT):
        return "達成率需介於 0 ~ 101.0000"

    rank, _ = get_rank(achievement)
    rating = calc_rating(ds, achievement)
    ap_note = f"（含 AP +{AP_BONUS}）" if achievement == MAX_ACHIEVEMENT else ""
    return f"定數 {ds:.1f} / {achievement:.4f}% ({rank}) → **{rating}**{ap_note}"
