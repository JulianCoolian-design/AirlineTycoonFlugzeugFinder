import streamlit as st
from itertools import combinations_with_replacement

# Erweiterte Flugzeugdatenbank mit Preisen, Reichweiten, Verbrauch und Abnutzungskoeffizient[cite: 1, 2]
FLUGZEUGE = [
    {"name": "Il-96-300", "preis": 110000000, "reichweite": 11500, "sitze": 300, "verbrauch": 4.42, "abnutzung": 2.4},
    # [cite: 1, 2]
    {"name": "A318-100", "preis": 70100000, "reichweite": 6019, "sitze": 136, "verbrauch": 2.91, "abnutzung": 1.9},
    # [cite: 1, 2]
    {"name": "A320-200", "preis": 91500000, "reichweite": 6111, "sitze": 180, "verbrauch": 2.39, "abnutzung": 2.5},
    # [cite: 1, 2]
    {"name": "A321neo", "preis": 127000000, "reichweite": 6644, "sitze": 244, "verbrauch": 1.89, "abnutzung": 1.4},
    # [cite: 1, 2]
    {"name": "A350-1000", "preis": 335000000, "reichweite": 14750, "sitze": 522, "verbrauch": 2.06, "abnutzung": 1.4},
    # [cite: 1, 2]
    {"name": "A380-800", "preis": 403000000, "reichweite": 15556, "sitze": 853, "verbrauch": 2.44, "abnutzung": 1.7},
    # [cite: 1, 2]
    {"name": "737-900ER", "preis": 94600000, "reichweite": 6050, "sitze": 220, "verbrauch": 2.23, "abnutzung": 1.8},
    # [cite: 1, 2]
    {"name": "787-10", "preis": 257000000, "reichweite": 10067, "sitze": 440, "verbrauch": 2.07, "abnutzung": 1.4},
    # [cite: 1, 2]
    {"name": "787-8", "preis": 206800000, "reichweite": 15196, "sitze": 381, "verbrauch": 2.23, "abnutzung": 1.6},
    # [cite: 1, 2]
    {"name": "747-8I", "preis": 352800000, "reichweite": 14825, "sitze": 730, "verbrauch": 2.24, "abnutzung": 1.6},
    # [cite: 1, 2]
]

st.title("✈️ Airline Tycoon - Routen-Planer")

# Eingaben in der Seitenleiste
st.sidebar.header("Routen- und Nachfragedaten")
route_rw = st.sidebar.number_input("Reichweite der Strecke (km)", min_value=0.0, value=5000.0, step=100.0)
eco = st.sidebar.number_input("Nachfrage Economy-Sitze", min_value=0.0, value=500.0, step=10.0)
biz = st.sidebar.number_input("Nachfrage Business-Sitze", min_value=0.0, value=100.0, step=10.0)
first = st.sidebar.number_input("Nachfrage First-Class-Sitze", min_value=0.0, value=20.0, step=5.0)

if st.sidebar.button("Beste Optionen & Werte berechnen"):
    gesamt_nachfrage = (eco * 1.0) + (biz * 2.0) + (first * 4.0)

    st.write(f"**Berechnete Gesamtnachfrage:** {gesamt_nachfrage:.1f} Sitze")
    st.write(f"**Strecken-Reichweite:** {route_rw} km")
    st.markdown("---")

    gueltige_flugzeuge = [f for f in FLUGZEUGE if f["reichweite"] >= route_rw]

    if not gueltige_flugzeuge:
        st.warning("Kein Flugzeug in der Datenbank hat eine ausreichend große Reichweite für diese Route!")
    else:
        optionen = []
        for r in range(1, 8):
            for kombi in combinations_with_replacement(gueltige_flugzeuge, r):
                sitze = sum(f["sitze"] * 2 for f in kombi)
                preis = sum(f["preis"] for f in kombi)
                avg_verbrauch = sum(f["verbrauch"] for f in kombi) / len(kombi)
                avg_abnutzung = sum(f["abnutzung"] for f in kombi) / len(kombi)
                abweichung = abs(sitze - gesamt_nachfrage)

                if sitze <= gesamt_nachfrage + 10:
                    zaehlung = {}
                    for f in kombi:
                        zaehlung[f["name"]] = zaehlung.get(f["name"], 0) + 1
                    teile = [f"{anzahl}x {name}" for name, anzahl in zaehlung.items()]
                    name_str = " + ".join(teile)

                    optionen.append({
                        "text": name_str,
                        "sitze": sitze,
                        "preis": preis,
                        "verbrauch": avg_verbrauch,
                        "abnutzung": avg_abnutzung,
                        "abweichung": abweichung
                    })

        if not optionen:
            st.warning("Keine passenden Flugzeuge/Kombinationen im Rahmen der Toleranz gefunden.")
        else:
            optionen.sort(key=lambda x: x["abweichung"])

            einzigartige_optionen = []
            gesehene_texte = set()
            for opt in optionen:
                if opt["text"] not in gesehene_texte:
                    gesehene_texte.add(opt["text"])
                    einzigartige_optionen.append(opt)
                    if len(einzigartige_optionen) == 3:
                        break

            top_3 = einzigartige_optionen


            def get_ranks(key_func):
                sorted_indices = sorted(range(len(top_3)), key=lambda i: key_func(top_3[i]))
                mapped_tags = ["" for _ in range(len(top_3))]
                for rank, orig_idx in enumerate(sorted_indices):
                    if rank == 0:
                        mapped_tags[orig_idx] = "green"
                    elif rank == 1:
                        mapped_tags[orig_idx] = "orange"
                    else:
                        mapped_tags[orig_idx] = "red"
                return mapped_tags


            price_tags = get_ranks(lambda x: x['preis'])
            demand_tags = get_ranks(lambda x: x['abweichung'])
            verbrauch_tags = get_ranks(lambda x: x['verbrauch'])
            abnutzung_tags = get_ranks(lambda x: x['abnutzung'])

            for i, opt in enumerate(top_3, 1):
                preis_formatiert = f"{opt['preis']:,}".replace(",", ".")
                st.subheader(f"Option {i}: {opt['text']}")

                st.markdown(f"- **Gesamtkosten:** :{price_tags[i - 1]}[{preis_formatiert} $]")
                st.markdown(f"- **Abgedeckte Sitze:** :{demand_tags[i - 1]}[{opt['sitze']}]")
                st.markdown(f"- **Ø Verbrauch:** :{verbrauch_tags[i - 1]}[{opt['verbrauch']:.2f} Liter/pax/100km]")
                st.markdown(f"- **Ø Abnutzungskoeffizient:** :{abnutzung_tags[i - 1]}[{opt['abnutzung']:.2f}% / 100h]")

                differenz = gesamt_nachfrage - opt['sitze']
                if differenz < 0:
                    ueberschreitung = abs(differenz)
                    st.markdown(f"- :red[**Achtung:** Überschreitet Nachfrage um {ueberschreitung:.1f} Sitze!]")
                else:
                    st.markdown(f"- **Ungenutzte Nachfrage:** {differenz:.1f}")
                st.write("---")