# Код анализа: Кредитный лимит, кто проиграет (STAT.DATATHON-2026, Data to Policy)

Python 3.9+, pandas, numpy, statsmodels (`pip install -r requirements.txt`).

Полный прогон из корня репозитория, около 20 секунд:

    bash run_all.sh <путь_к_synthetic_microdata_2021-2024_20260921> out

По шагам (тоже из корня репозитория):

| Шаг | Команда | Результат |
|---|---|---|
| 1 | `python3 code/build_panel.py <данные> out` | `out/hh_quarter.pkl`: панель домохозяйство-квартал (96 000 строк) |
| 2 | `python3 code/analyze.py out/hh_quarter.pkl out` | `out/results.json` (дескриптивы, гипотезы Г1-Г4, симуляция лимитов 30-50%), `out/reg_new.pkl` (4 284 новых займа банков и МФО) |
| 3 | `python3 code/extra.py <данные> out` | добавляет в `results.json` региональную занятость из T-001 и сетку лимитов 20-70% |
| 4 | `python3 code/scenarios.py out/reg_new.pkl` | печатает сценарии: действующий 50%, единый 30%, адресный, адресный + соцзащита |
| 5 | `python3 code/export_sim_data.py out/reg_new.pkl out/sim_data.json` | массивы займов, встроенные в `simulator/simulator.html` (`const D`); с флагом `--inject simulator/simulator.html` обновляет симулятор |

Входные данные: d004 (2023, 2024), d008, d002, t001/2024. Подробнее в `data/README.md`.

`code/results.json` здесь сохранен как эталон: прогон на тех же данных воспроизводит его один в один, а `out/sim_data.json` совпадает с данными симулятора.

## Допущения

- Коды KODNU 2.1.1.4.1 и 2.1.1.4.2 в kv_vopr12 приняты за погашение займов, 59-62 за полученные займы. Требуют сверки с кодовой книгой.
- Доход = сумма GR1-GR23 в kv_vopr11 без GR17 (редкие экстремальные значения, вероятно продажа имущества).
- Без весов обследования; симуляция статическая.

Все определения, числа и ограничения: `docs/FINDINGS.md`.

`_early_versions/`: первые черновики `build_panel.py` и `analyze.py`, оставлены для истории.
