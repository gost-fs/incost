# InCost — сайт incost.app

Цей репозиторій — **сайт** InCost (GitHub Pages, домен у `CNAME`) і місце для **релізів**
десктопної програми (`releases/latest/download/InCost-win.zip`). Самої програми
(Windows, Neutralino) тут немає — її код живе окремо. Оновлення для програми — у репозиторії `gost-fs/incost-updates`.

InCost — програма для розрахунку собівартості й ціни для технологів і інженерів:
листовий метал і DXF, розкрій (nesting), лазер, 3D-друк, мехобробка. Є Free і Pro (оплата через Freemius).
**Цільовий ринок — США.**

## Правила для тексту на сайті
- Основна мова сайту — англійська, американська (US English): `color`, `aluminum`, `optimize`.
- Для США спочатку імперські одиниці: in, lb, ga, $. Метричні йдуть поруч або перемикачем.
- Сайт перекладено на 5 мов: `en, uk, de, es, pl`. Якщо змінюєш текст англійською, онови всі 5 мов в одній зміні.
  - Статичний текст: атрибут `data-i="ключ"` в HTML, переклади зберігаються у словниках у скрипті `index.html` (`"ключ":"..."`).
  - Картки можливостей: `var MODS={en:[...],uk:[...],...}`, групи карток — `var FGK`.
- Пиши коротко й конкретно, мовою цеху: ціна деталі, час різання, грами, $/год. Без маркетингової «води».
  Цифри економії й точності мають бути чесними, бо їх читають технологи.
- Стиль у дусі Apple: багато повітря, один головний заклик на екран, системні шрифти (Segoe UI), змінні CSS з `:root`,
  обов'язково має працювати темна тема (`prefers-color-scheme`).

## Які файли генеруються (руками НЕ редагувати)
| Файл | Звідки | Команда |
|---|---|---|
| `features.html` | `index.html` + `tools/features_main.html` + `tools/features_parts/*` | `python3 tools/gen_features.py` |
| 4 калькулятори (`*-calculator.html`) | `tools/gen_calculators.py` (там і `TAIL` — лічильник візитів, beacon завантаження, обробка телефонів — спільний для всіх сторінок) | `python3 tools/gen_calculators.py .` |
| 8 сторінок-довідників (`*-chart.html`, `steel-grade-equivalents.html`) | `tools/charts-data.json` (таблиці з бібліотеки програми) + `tools/gen_charts.py` | `python3 tools/gen_charts.py`, потім `python3 tools/check_charts.py` |

Після будь-якої зміни в `index.html` треба перезапустити `gen_features.py`, а після зміни `gen_calculators.py` — і калькулятори, і довідники
(`gen_charts.py` бере з нього CSS, логотип і `TAIL`). Хук робить це сам.

## Аналітика й бекенд (не ламати)
- На кожній сторінці стоїть анонімний лічильник візитів: `https://api.incost.app/hit` (без cookies).
- Кожна кнопка завантаження — це `<a ... InCost-win.zip ... data-dl="звідки">`, і вона відправляє beacon на `api.incost.app/dl`.
- На головній є також `api.incost.app/contact`, `/send` і `/geo`. Ці адреси не змінюй і не видаляй.
- Оплата йде через Freemius (`freemius.com/js/v1/`). `thanks.html` — сторінка після покупки, `noindex`, її немає в sitemap.

## Нова сторінка
1. Додай `<link rel="canonical" href="https://incost.app/<файл>">`, title, description, og-теги, лічильник візитів.
2. Додай її в `sitemap.xml` (з `lastmod`).
3. Додай посилання з інших сторінок (блоки «tools» або «Reference charts»).
4. Запусти `python3 tools/check_site.py`.

## Перевірка перед push
```
python3 tools/check_site.py     # sitemap, посилання, canonical, аналітика, переклади, свіжість згенерованих сторінок
python3 tools/check_charts.py   # цифри в довідниках проти стандартів ISO/ANSI
```
Обидві команди мають пройти без FAIL. Якщо сторінка змінилася, онови її `lastmod` у `sitemap.xml`.

## Автоматика Claude Code (`.claude/`)
- Hooks (`.claude/hooks/incost_hook.py`):
  - блокують ручне редагування згенерованих сторінок;
  - після правок самі перегенеровують калькулятори, довідники й `features.html`;
  - перед завершенням роботи запускають `check_site.py`.
- Skills, які можна викликати як команди: `/site-check` (перевірка перед публікацією), `/add-feature` (нова картка можливості
  всіма 5 мовами), `/add-chart-page` (новий довідник).

## Git
- GitHub Pages публікує сайт з гілки `main`, тож push у `main` одразу потрапляє на живий сайт.
  Великі зміни роби в окремій гілці й через PR.
- Коміти пиши коротко англійською, як у тебе прийнято: `Site: shorter home page + features.html ...`.
