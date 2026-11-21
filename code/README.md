# Кредитный лимит: кто проиграет (STAT.DATATHON-2026, Data to Policy)

Запуск (Python 3, pandas, numpy, statsmodels):

    python3 build_panel.py <путь_к_synthetic_microdata> out
    python3 analyze.py out/hh_quarter.pkl out
    python3 extra.py <путь_к_synthetic_microdata> out

Входные данные: d004 (2023, 2024), d008, d002, t001/2024.
Результаты: out/results.json (дескриптивы, гипотезы H1-H4, симуляция лимитов DSR 20-70%).

Допущения: коды KODNU 2.1.1.4.1 и 2.1.1.4.2 в kv_vopr12 приняты за погашение займов,
59-62 за полученные займы; доход = сумма GR1-GR23 kv_vopr11 без GR17. Требуют сверки с кодовой книгой.

    python3 scenarios.py out/reg_new.pkl   # единый vs адресный лимит

simulator.html: интерактивный симулятор (открывается в браузере, работает офлайн).

    python3 export_sim_data.py out/reg_new.pkl out/sim_data.json [--inject ../simulator/simulator.html]

export_sim_data.py: выгружает массивы займов, встроенные в simulator.html (const D). Добавлен 21.11.2026, совпадает с данными симулятора один в один.
