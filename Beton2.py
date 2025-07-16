import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math

def calculate_all():
    try:
        # Get input values from GUI
        tp_dak = float(entry_tp_dak.get())
        tp_lantai = float(entry_tp_lantai.get())
        balok_dak_b = float(entry_balok_dak_b.get())
        balok_dak_h = float(entry_balok_dak_h.get())
        balok_lantai_b = float(entry_balok_lantai_b.get())
        balok_lantai_h = float(entry_balok_lantai_h.get())
        kolom_b = float(entry_kolom_b.get())
        kolom_h = float(entry_kolom_h.get())
        L_kolom_atas = float(entry_L_kolom_atas.get())
        L_kolom_bawah = float(entry_L_kolom_bawah.get())
        fc_prime = float(entry_fc_prime.get())
        # fy = float(entry_fy.get()) # fy is not used in stiffness calculation directly

        # Span lengths from the image
        L_span_long = float(entry_L_span_long.get()) # cm
        L_span_short = float(entry_L_span_short.get()) # cm
        Lp = float(entry_Lp.get())# cm (Lp from the image, typically represents the width of the slab strip considered for T-beam)

        # Clear previous results
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)

        # --- Define Text Tags for Formatting ---
        output_text.tag_configure("header1", font=("Helvetica", 14, "bold"), foreground="navy")
        output_text.tag_configure("header2", font=("Helvetica", 12, "bold"), foreground="darkgreen")
        output_text.tag_configure("subheader", font=("Helvetica", 11, "bold"), foreground="darkblue")
        output_text.tag_configure("formula", font=("Consolas", 10, "italic"), foreground="purple")
        output_text.tag_configure("calculation", font=("Consolas", 10), foreground="black")
        output_text.tag_configure("result", font=("Helvetica", 11, "bold"), foreground="red")
        output_text.tag_configure("explanation", font=("Helvetica", 9, "italic"), foreground="gray40")
        output_text.tag_configure("bold", font=("Helvetica", 10, "bold"))
        output_text.tag_configure("value", font=("Consolas", 10, "bold"), foreground="blue")


        output_text.insert(tk.END, "===== Hasil Perhitungan Kekakuan Struktur Portal Ekuivalen =====\n\n", "header1")

        # 1. Calculate Modulus of Elasticity of Concrete (Ec)
        output_text.insert(tk.END, "--- 1. Perhitungan Modulus Elastisitas Beton (Ec) ---\n", "header2")
        output_text.insert(tk.END, "  Modulus elastisitas beton (Ec) dihitung berdasarkan mutu beton (fc').\n", "explanation")
        Ec_calc = 4700 * math.sqrt(fc_prime) # MPa
        output_text.insert(tk.END, f"  Formula: ", "formula")
        output_text.insert(tk.END, f"Ec = 4700 * sqrt(fc')\n", "calculation")
        output_text.insert(tk.END, f"  Perhitungan: ", "calculation")
        output_text.insert(tk.END, f"Ec = 4700 * sqrt({fc_prime:.2f}) = ", "calculation")
        output_text.insert(tk.END, f"{Ec_calc:.3f} MPa\n", "value")
        output_text.insert(tk.END, f"  Nilai Ec: ", "result")
        output_text.insert(tk.END, f"{Ec_calc:.3f} MPa (Akan ditulis dalam bentuk 'Ec')\n\n", "value")

        output_text.insert(tk.END, "===== B.1. Kekakuan Balok Ekuivalen ====="+"\n\n", "header1")

        # LANTAI I (Floor)
        output_text.insert(tk.END, "--- LANTAI I (Lantai Beton) ---\n", "header2")
        output_text.insert(tk.END, "  Analisis balok sebagai T-Beam dengan memperhitungkan plat lantai.\n", "explanation")
        output_text.insert(tk.END, "  Tipe Balok: ", "bold")
        output_text.insert(tk.END, "T-Beam (Balok Lantai 30x50 cm + Plat Lantai 15 cm)\n", "calculation")
        output_text.insert(tk.END, f"  Lebar efektif plat (bt): ", "bold")
        output_text.insert(tk.END, f"{Lp:.1f} cm\n", "calculation")
        output_text.insert(tk.END, f"  Tebal plat (hf): ", "bold")
        output_text.insert(tk.END, f"{tp_lantai:.1f} cm\n", "calculation")
        output_text.insert(tk.END, f"  Lebar badan balok (bw): ", "bold")
        output_text.insert(tk.END, f"{balok_lantai_b:.1f} cm\n", "calculation")
        output_text.insert(tk.END, f"  Tinggi total balok (H_total): ", "bold")
        output_text.insert(tk.END, f"{balok_lantai_h:.1f} cm\n", "calculation")
        h_w_lantai = balok_lantai_h - tp_lantai
        output_text.insert(tk.END, f"  Tinggi badan balok (hw): ", "bold")
        output_text.insert(tk.END, f"{balok_lantai_h} - {tp_lantai} = {h_w_lantai:.1f} cm\n\n", "calculation")

        # Calculate neutral axis for T-beam (Lantai I)
        output_text.insert(tk.END, "  *Perhitungan Letak Garis Netral (yt)*:\n", "subheader")
        output_text.insert(tk.END, "  Menentukan pusat gravitasi penampang komposit (T-Beam).\n", "explanation")
        A1_lantai = Lp * tp_lantai
        y1_bar_lantai = tp_lantai / 2
        A2_lantai = balok_lantai_b * h_w_lantai
        y2_bar_lantai = tp_lantai + (h_w_lantai / 2)
        output_text.insert(tk.END, f"    Luas Bagian 1 (Plat): A1 = {Lp} x {tp_lantai} = ", "calculation")
        output_text.insert(tk.END, f"{A1_lantai:.1f} cm^2\n", "value")
        output_text.insert(tk.END, f"    Jarak centroid Bagian 1 dari sisi atas (y1_bar): {tp_lantai} / 2 = ", "calculation")
        output_text.insert(tk.END, f"{y1_bar_lantai:.1f} cm\n", "value")
        output_text.insert(tk.END, f"    Luas Bagian 2 (Badan Balok): A2 = {balok_lantai_b} x {h_w_lantai} = ", "calculation")
        output_text.insert(tk.END, f"{A2_lantai:.1f} cm^2\n", "value")
        output_text.insert(tk.END, f"    Jarak centroid Bagian 2 dari sisi atas (y2_bar): {tp_lantai} + ({h_w_lantai} / 2) = ", "calculation")
        output_text.insert(tk.END, f"{y2_bar_lantai:.1f} cm\n", "value")

        yt_numerator_lantai = (A1_lantai * y1_bar_lantai) + (A2_lantai * y2_bar_lantai)
        yt_denominator_lantai = A1_lantai + A2_lantai
        yt_lantai_calc = yt_numerator_lantai / yt_denominator_lantai
        output_text.insert(tk.END, f"    Formula yt: ", "formula")
        output_text.insert(tk.END, f"(A1*y1_bar + A2*y2_bar) / (A1 + A2)\n", "calculation")
        output_text.insert(tk.END, f"    Perhitungan yt: ", "calculation")
        output_text.insert(tk.END, f"({A1_lantai:.1f} * {y1_bar_lantai:.1f} + {A2_lantai:.1f} * {y2_bar_lantai:.1f}) / ({A1_lantai:.1f} + {A2_lantai:.1f}) = ", "calculation")
        output_text.insert(tk.END, f"{yt_lantai_calc:.3f} cm\n", "value")
        output_text.insert(tk.END, f"  Letak garis netral terhadap sisi atas (yt) LANTAI I: ", "result")
        output_text.insert(tk.END, f"{yt_lantai_calc:.3f} cm\n", "value")

        yb_lantai_calc = balok_lantai_h - yt_lantai_calc
        output_text.insert(tk.END, f"  Letak garis netral terhadap sisi bawah (yb) LANTAI I: {balok_lantai_h} - {yt_lantai_calc:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{yb_lantai_calc:.3f} cm\n\n", "value")

        # Moment of Inertia of Balok T (Lantai I)
        output_text.insert(tk.END, "  *Perhitungan Momen Inersia Balok T (Ib+p)*:\n", "subheader")
        output_text.insert(tk.END, "  Menggunakan Teorema Sumbu Sejajar untuk penampang T-Beam.\n", "explanation")
        I_flange_lantai = (1/12) * Lp * tp_lantai**3 + A1_lantai * (yt_lantai_calc - y1_bar_lantai)**2
        I_web_lantai = (1/12) * balok_lantai_b * h_w_lantai**3 + A2_lantai * (y2_bar_lantai - yt_lantai_calc)**2
        Ib_p_lantai = I_flange_lantai + I_web_lantai
        output_text.insert(tk.END, f"    Momen Inersia Plat (I_flange): ", "calculation")
        output_text.insert(tk.END, f"(1/12) * {Lp} * {tp_lantai}^3 + {A1_lantai:.1f} * ({yt_lantai_calc:.3f} - {y1_bar_lantai:.1f})^2 = {I_flange_lantai:.3f} cm^4\n", "value")
        output_text.insert(tk.END, f"    Momen Inersia Badan Balok (I_web): ", "calculation")
        output_text.insert(tk.END, f"(1/12) * {balok_lantai_b} * {h_w_lantai}^3 + {A2_lantai:.1f} * ({y2_bar_lantai:.1f} - {yt_lantai_calc:.3f})^2 = {I_web_lantai:.3f} cm^4\n", "value")
        output_text.insert(tk.END, f"    Total Momen Inersia (Ib+p): {I_flange_lantai:.3f} + {I_web_lantai:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Ib_p_lantai:.3f} cm^4\n", "value")
        output_text.insert(tk.END, f"  Momen Inersia Balok T (Ib+p) LANTAI I: ", "result")
        output_text.insert(tk.END, f"{Ib_p_lantai:.3f} cm^4\n\n", "value")

        # Kekakuan Balok Ekuivalen (Kbe) for LANTAI I
        output_text.insert(tk.END, "  *Perhitungan Kekakuan Balok Ekuivalen (Kbe)*:\n", "subheader")
        output_text.insert(tk.END, "  Kekakuan balok dihitung sebagai 4EI/L.\n", "explanation")
        output_text.insert(tk.END, "    Formula: ", "formula")
        output_text.insert(tk.END, f"Kbe = (4 * Ec * Ib+p) / L\n", "calculation")
        Kbe_A1B1 = (4 * Ib_p_lantai) / L_span_long
        output_text.insert(tk.END, f"    Bentang A1-B1 (L={L_span_long:.1f} cm): Kbe = (4 * {Ib_p_lantai:.3f}) / {L_span_long} = ", "calculation")
        output_text.insert(tk.END, f"{Kbe_A1B1:.3f} Ec\n", "value")
        Kbe_B1C1 = (4 * Ib_p_lantai) / L_span_short
        output_text.insert(tk.END, f"    Bentang B1-C1 (L={L_span_short:.1f} cm): Kbe = (4 * {Ib_p_lantai:.3f}) / {L_span_short} = ", "calculation")
        output_text.insert(tk.END, f"{Kbe_B1C1:.3f} Ec\n", "value")
        Kbe_C1D1 = (4 * Ib_p_lantai) / L_span_long
        output_text.insert(tk.END, f"    Bentang C1-D1 (L={L_span_long:.1f} cm): Kbe = (4 * {Ib_p_lantai:.3f}) / {L_span_long} = ", "calculation")
        output_text.insert(tk.END, f"{Kbe_C1D1:.3f} Ec\n\n", "value")

        # LANTAI II (Roof)
        output_text.insert(tk.END, "--- LANTAI II (Pelat Dak) ---\n", "header2")
        output_text.insert(tk.END, "  Analisis balok sebagai T-Beam untuk plat dak.\n", "explanation")
        output_text.insert(tk.END, "  Tipe Balok: ", "bold")
        output_text.insert(tk.END, "T-Beam (Balok Dak 30x30 cm + Plat Dak 10 cm)\n", "calculation")
        output_text.insert(tk.END, f"  Lebar efektif plat (bt): ", "bold")
        output_text.insert(tk.END, f"{Lp:.1f} cm\n", "calculation")
        output_text.insert(tk.END, f"  Tebal plat (hf): ", "bold")
        output_text.insert(tk.END, f"{tp_dak:.1f} cm\n", "calculation")
        output_text.insert(tk.END, f"  Lebar badan balok (bw): ", "bold")
        output_text.insert(tk.END, f"{balok_dak_b:.1f} cm\n", "calculation")
        output_text.insert(tk.END, f"  Tinggi total balok (H_total): ", "bold")
        output_text.insert(tk.END, f"{balok_dak_h:.1f} cm\n", "calculation")
        h_w_dak = balok_dak_h - tp_dak
        output_text.insert(tk.END, f"  Tinggi badan balok (hw): ", "bold")
        output_text.insert(tk.END, f"{balok_dak_h} - {tp_dak} = {h_w_dak:.1f} cm\n\n", "calculation")

        # Calculate neutral axis for T-beam (Lantai II)
        output_text.insert(tk.END, "  *Perhitungan Letak Garis Netral (yt)*:\n", "subheader")
        output_text.insert(tk.END, "  Menentukan pusat gravitasi penampang komposit (T-Beam) untuk dak.\n", "explanation")
        A1_dak = Lp * tp_dak
        y1_bar_dak = tp_dak / 2
        A2_dak = balok_dak_b * h_w_dak
        y2_bar_dak = tp_dak + (h_w_dak / 2)
        output_text.insert(tk.END, f"    Luas Bagian 1 (Plat): A1 = {Lp} x {tp_dak} = ", "calculation")
        output_text.insert(tk.END, f"{A1_dak:.1f} cm^2\n", "value")
        output_text.insert(tk.END, f"    Jarak centroid Bagian 1 dari sisi atas (y1_bar): {tp_dak} / 2 = ", "calculation")
        output_text.insert(tk.END, f"{y1_bar_dak:.1f} cm\n", "value")
        output_text.insert(tk.END, f"    Luas Bagian 2 (Badan Balok): A2 = {balok_dak_b} x {h_w_dak} = ", "calculation")
        output_text.insert(tk.END, f"{A2_dak:.1f} cm^2\n", "value")
        output_text.insert(tk.END, f"    Jarak centroid Bagian 2 dari sisi atas (y2_bar): {tp_dak} + ({h_w_dak} / 2) = ", "calculation")
        output_text.insert(tk.END, f"{y2_bar_dak:.1f} cm\n\n", "value")

        yt_numerator_dak = (A1_dak * y1_bar_dak) + (A2_dak * y2_bar_dak)
        yt_denominator_dak = A1_dak + A2_dak
        yt_dak_calc = yt_numerator_dak / yt_denominator_dak
        output_text.insert(tk.END, f"    Formula yt: ", "formula")
        output_text.insert(tk.END, f"(A1*y1_bar + A2*y2_bar) / (A1 + A2)\n", "calculation")
        output_text.insert(tk.END, f"    Perhitungan yt: ", "calculation")
        output_text.insert(tk.END, f"({A1_dak:.1f} * {y1_bar_dak:.1f} + {A2_dak:.1f} * {y2_bar_dak:.1f}) / ({A1_dak:.1f} + {A2_dak:.1f}) = ", "calculation")
        output_text.insert(tk.END, f"{yt_dak_calc:.3f} cm\n", "value")
        output_text.insert(tk.END, f"  Letak garis netral terhadap sisi atas (yt) LANTAI II: ", "result")
        output_text.insert(tk.END, f"{yt_dak_calc:.3f} cm\n", "value")

        yb_dak_calc = balok_dak_h - yt_dak_calc
        output_text.insert(tk.END, f"  Letak garis netral terhadap sisi bawah (yb) LANTAI II: {balok_dak_h} - {yt_dak_calc:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{yb_dak_calc:.3f} cm\n\n", "value")

        # Moment of Inertia of Balok T (Lantai II)
        output_text.insert(tk.END, "  *Perhitungan Momen Inersia Balok T (Ib+p)*:\n", "subheader")
        output_text.insert(tk.END, "  Menggunakan Teorema Sumbu Sejajar untuk penampang T-Beam dak.\n", "explanation")
        I_flange_dak = (1/12) * Lp * tp_dak**3 + A1_dak * (yt_dak_calc - y1_bar_dak)**2
        I_web_dak = (1/12) * balok_dak_b * h_w_dak**3 + A2_dak * (y2_bar_dak - yt_dak_calc)**2
        Ib_p_dak = I_flange_dak + I_web_dak
        output_text.insert(tk.END, f"    Momen Inersia Plat (I_flange): ", "calculation")
        output_text.insert(tk.END, f"(1/12) * {Lp} * {tp_dak}^3 + {A1_dak:.1f} * ({yt_dak_calc:.3f} - {y1_bar_dak:.1f})^2 = {I_flange_dak:.3f} cm^4\n", "value")
        output_text.insert(tk.END, f"    Momen Inersia Badan Balok (I_web): ", "calculation")
        output_text.insert(tk.END, f"(1/12) * {balok_dak_b} * {h_w_dak}^3 + {A2_dak:.1f} * ({y2_bar_dak:.1f} - {yt_dak_calc:.3f})^2 = {I_web_dak:.3f} cm^4\n", "value")
        output_text.insert(tk.END, f"    Total Momen Inersia (Ib+p): {I_flange_dak:.3f} + {I_web_dak:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Ib_p_dak:.3f} cm^4\n", "value")
        output_text.insert(tk.END, f"  Momen Inersia Balok T (Ib+p) LANTAI II: ", "result")
        output_text.insert(tk.END, f"{Ib_p_dak:.3f} cm^4\n\n", "value")

        # Kekakuan Balok Ekuivalen (Kbe) for LANTAI II
        output_text.insert(tk.END, "  *Perhitungan Kekakuan Balok Ekuivalen (Kbe)*:\n", "subheader")
        output_text.insert(tk.END, "  Kekakuan balok dak dihitung sebagai 4EI/L.\n", "explanation")
        output_text.insert(tk.END, "    Formula: ", "formula")
        output_text.insert(tk.END, f"Kbe = (4 * Ec * Ib+p) / L\n", "calculation")
        Kbe_A2B2 = (4 * Ib_p_dak) / L_span_long
        output_text.insert(tk.END, f"    Bentang A2-B2 (L={L_span_long:.1f} cm): Kbe = (4 * {Ib_p_dak:.3f}) / {L_span_long} = ", "calculation")
        output_text.insert(tk.END, f"{Kbe_A2B2:.3f} Ec\n", "value")
        Kbe_B2C2 = (4 * Ib_p_dak) / L_span_short
        output_text.insert(tk.END, f"    Bentang B2-C2 (L={L_span_short:.1f} cm): Kbe = (4 * {Ib_p_dak:.3f}) / {L_span_short} = ", "calculation")
        output_text.insert(tk.END, f"{Kbe_B2C2:.3f} Ec\n", "value")
        Kbe_C2D2 = (4 * Ib_p_dak) / L_span_long
        output_text.insert(tk.END, f"    Bentang C2-D2 (L={L_span_long:.1f} cm): Kbe = (4 * {Ib_p_dak:.3f}) / {L_span_long} = ", "calculation")
        output_text.insert(tk.END, f"{Kbe_C2D2:.3f} Ec\n\n", "value")

        output_text.insert(tk.END, "===== B.2. Kekakuan Kolom Ekuivalen ====="+"\n\n", "header1")

        # B.2.1. Ditinjau Titik Joint pada Pelat Lantai (Floor)
        output_text.insert(tk.END, "--- B.2.1. Ditinjau Titik Joint pada Pelat Lantai ---\n", "header2")

        # Kolom Tepi (Edge Column)
        output_text.insert(tk.END, "\n  *Kolom Tepi (Lantai I)*\n", "subheader")
        output_text.insert(tk.END, "  Perhitungan untuk kolom pada tepi struktur lantai.\n", "explanation")
        # Lebar Efektif Balok Penahan Torsi (be)
        output_text.insert(tk.END, "    *Perhitungan Lebar Efektif Balok Penahan Torsi (be)*:\n", "subheader")
        output_text.insert(tk.END, "    Lebar efektif (be) ditentukan dari nilai terkecil dari dua kriteria.\n", "explanation")
        be1_lantai_edge = balok_lantai_b + (balok_lantai_h - tp_lantai)
        be2_lantai_edge = balok_lantai_b + 4 * tp_lantai
        be_lantai_edge = min(be1_lantai_edge, be2_lantai_edge)
        output_text.insert(tk.END, f"      Nilai terkecil dari:\n", "calculation")
        output_text.insert(tk.END, f"        be = bw + (h - tp) = {balok_lantai_b} + ({balok_lantai_h} - {tp_lantai}) = ", "calculation")
        output_text.insert(tk.END, f"{be1_lantai_edge:.1f} cm\n", "value")
        output_text.insert(tk.END, f"        be = bw + 4 * tp = {balok_lantai_b} + 4 * {tp_lantai} = ", "calculation")
        output_text.insert(tk.END, f"{be2_lantai_edge:.1f} cm\n", "value")
        output_text.insert(tk.END, f"    Lebar Efektif Balok Penahan Torsi (be) Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{be_lantai_edge:.3f} cm (Digunakan)\n\n", "value")

        # Momen Inersia Balok Penahan Torsi (C) (L-shaped section)
        output_text.insert(tk.END, "    *Perhitungan Momen Inersia Balok Penahan Torsi (C) (L-shaped)*:\n", "subheader")
        output_text.insert(tk.END, "    Konstanta torsional C dihitung dengan membagi penampang menjadi persegi panjang.\n", "explanation")
        # Section 1 (web): 30 x 50
        dim1_part1_lantai_edge = balok_lantai_b # 30
        dim2_part1_lantai_edge = balok_lantai_h # 50
        # Section 2 (flange): 35 x 15
        dim1_part2_lantai_edge = be_lantai_edge - balok_lantai_b # 65 - 30 = 35
        dim2_part2_lantai_edge = tp_lantai # 15

        # Ensure x is always the shorter side and y is the longer side for the ratio in C formula
        x1_lantai_edge_val = min(dim1_part1_lantai_edge, dim2_part1_lantai_edge)
        y1_lantai_edge_val = max(dim1_part1_lantai_edge, dim2_part1_lantai_edge)
        x2_lantai_edge_val = min(dim1_part2_lantai_edge, dim2_part2_lantai_edge)
        y2_lantai_edge_val = max(dim1_part2_lantai_edge, dim2_part2_lantai_edge)

        ratio1_lantai_edge = x1_lantai_edge_val / y1_lantai_edge_val
        ratio2_lantai_edge = x2_lantai_edge_val / y2_lantai_edge_val

        term1_val_lantai_edge = x1_lantai_edge_val**3 * y1_lantai_edge_val / 3
        term2_val_lantai_edge = x2_lantai_edge_val**3 * y2_lantai_edge_val / 3

        C_lantai_edge_part1 = (1 - 0.63 * ratio1_lantai_edge) * term1_val_lantai_edge
        C_lantai_edge_part2 = (1 - 0.63 * ratio2_lantai_edge) * term2_val_lantai_edge
        C_lantai_edge = C_lantai_edge_part1 + C_lantai_edge_part2
        
        output_text.insert(tk.END, f"      Formula C: ", "formula")
        output_text.insert(tk.END, f"(1 - 0.63 * x1/y1) * (x1^3 * y1 / 3) + (1 - 0.63 * x2/y2) * (x2^3 * y2 / 3)\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan C:\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x1_lantai_edge_val:.1f}/{y1_lantai_edge_val:.1f}) * ({x1_lantai_edge_val:.1f}^3 * {y1_lantai_edge_val:.1f} / 3) +\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x2_lantai_edge_val:.1f}/{y2_lantai_edge_val:.1f}) * ({x2_lantai_edge_val:.1f}^3 * {y2_lantai_edge_val:.1f} / 3)\n", "calculation")
        output_text.insert(tk.END, f"      C = ", "calculation")
        output_text.insert(tk.END, f"({1 - 0.63 * ratio1_lantai_edge:.3f}) * ({term1_val_lantai_edge:.3f}) + ({1 - 0.63 * ratio2_lantai_edge:.3f}) * ({term2_val_lantai_edge:.3f})\n", "value")
        output_text.insert(tk.END, f"      C = ", "result")
        output_text.insert(tk.END, f"{C_lantai_edge:.3f} cm^4\n\n", "value")
        output_text.insert(tk.END, f"    Total Momen Inersia Balok Penahan Torsi (C) Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{C_lantai_edge:.3f} cm^4\n\n", "value")

        # Kekakuan Balok Penahan Torsi (Kt)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Balok Penahan Torsi (Kt)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan torsi balok penahan torsi.\n", "explanation")
        L2_kt_lantai_edge = Lp
        C2_kt_lantai_edge = kolom_b
        Kt_lantai_edge_term1 = (9 * C_lantai_edge) / (L2_kt_lantai_edge * (1 - C2_kt_lantai_edge / L2_kt_lantai_edge)**3)
        Kt_lantai_edge_term2 = (9 * C_lantai_edge) / (L2_kt_lantai_edge * (1 - C2_kt_lantai_edge / L2_kt_lantai_edge)**3)
        Kt_lantai_edge = Kt_lantai_edge_term1 + Kt_lantai_edge_term2
        output_text.insert(tk.END, f"      Formula Kt: ", "formula")
        output_text.insert(tk.END, f"(9 * Ec * C) / (L2 * (1-C2/L2)^3) + (9 * Ec * C) / (L2 * (1-C2/L2)^3)\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt = 2 * (9 * {C_lantai_edge:.3f}) / ({L2_kt_lantai_edge} * (1 - {C2_kt_lantai_edge}/{L2_kt_lantai_edge})^3) = ", "calculation")
        output_text.insert(tk.END, f"{Kt_lantai_edge:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi (Kt) Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{Kt_lantai_edge:.3f} Ec\n\n", "value")

        # Koreksi Kt menjadi Kt'
        output_text.insert(tk.END, "\n    *Koreksi Kekakuan Balok Penahan Torsi menjadi Kt'*:\n", "subheader")
        output_text.insert(tk.END, "    Koreksi ini memperhitungkan efek lentur dari plat.\n", "explanation")
        Ip_lantai_edge = (1/12) * Lp * tp_lantai**3
        output_text.insert(tk.END, f"      Ip (Momen Inersia Plat): (1/12) * {Lp} * {tp_lantai}^3 = ", "calculation")
        output_text.insert(tk.END, f"{Ip_lantai_edge:.3f} cm^4\n", "value")
        Kt_prime_lantai_edge_calc = (Ib_p_lantai / Ip_lantai_edge) * Kt_lantai_edge
        output_text.insert(tk.END, f"      Formula Kt': ", "formula")
        output_text.insert(tk.END, f"(Ib+p / Ip) * Kt\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt' = ({Ib_p_lantai:.3f} / {Ip_lantai_edge:.3f}) * {Kt_lantai_edge:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kt_prime_lantai_edge_calc:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi yang telah dikoreksi (Kt') Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{Kt_prime_lantai_edge_calc:.3f} Ec\n\n", "value")

        # Kekakuan Kolom (Sigma Kk)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom (Sigma Kk)*:\n", "subheader")
        output_text.insert(tk.END, "    Jumlah kekakuan kolom di atas dan di bawah joint.\n", "explanation")
        I_kolom = (1/12) * kolom_b * kolom_h**3
        K_kolom_bawah_val = (4 * I_kolom) / L_kolom_bawah
        K_kolom_atas_val = (4 * I_kolom) / L_kolom_atas
        Sigma_Kk_lantai_edge = K_kolom_bawah_val + K_kolom_atas_val
        output_text.insert(tk.END, f"      Momen Inersia Kolom (I_kolom): (1/12) * {kolom_b} * {kolom_h}^3 = ", "calculation")
        output_text.insert(tk.END, f"{I_kolom:.3f} cm^4\n", "value")
        output_text.insert(tk.END, f"      Kekakuan Kolom Bawah (K_bawah): (4 * {I_kolom:.3f}) / {L_kolom_bawah} = ", "calculation")
        output_text.insert(tk.END, f"{K_kolom_bawah_val:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"      Kekakuan Kolom Atas (K_atas): (4 * {I_kolom:.3f}) / {L_kolom_atas} = ", "calculation")
        output_text.insert(tk.END, f"{K_kolom_atas_val:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"      Sigma Kk = K_bawah + K_atas = {K_kolom_bawah_val:.3f} Ec + {K_kolom_atas_val:.3f} Ec = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kk_lantai_edge:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Sigma Kk Kolom Tepi (Lantai I): ", "result")
        output_text.insert(tk.END, f"{Sigma_Kk_lantai_edge:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen (Sigma Kke)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen (Sigma Kke)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan ekuivalen kolom yang memperhitungkan balok penahan torsi.\n", "explanation")
        Sigma_Kke_lantai_edge = 1 / ((1 / Sigma_Kk_lantai_edge) + (1 / Kt_prime_lantai_edge_calc))
        output_text.insert(tk.END, f"      Formula 1/Sigma Kke = 1/Sigma Kk + 1/Kt'\n", "formula")
        output_text.insert(tk.END, f"      Perhitungan 1/Sigma Kke = 1/{Sigma_Kk_lantai_edge:.3f} Ec + 1/{Kt_prime_lantai_edge_calc:.3f} Ec\n", "calculation")
        output_text.insert(tk.END, f"      Sigma Kke = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kke_lantai_edge:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Sigma Kke Kolom Tepi (Lantai I): ", "result")
        output_text.insert(tk.END, f"{Sigma_Kke_lantai_edge:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Biasa Ao-A1 dan A1-A2
        output_text.insert(tk.END, "\n    *Kekakuan Kolom Biasa Ao-A1 dan A1-A2*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan individual segmen kolom.\n", "explanation")
        K_AoA1_val = (4 * I_kolom) / L_kolom_bawah
        K_A1A2_val = (4 * I_kolom) / L_kolom_atas
        output_text.insert(tk.END, f"      K_AoA1 = (4 * {I_kolom:.3f}) / {L_kolom_bawah} = ", "calculation")
        output_text.insert(tk.END, f"{K_AoA1_val:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"      K_A1A2 = (4 * {I_kolom:.3f}) / {L_kolom_atas} = ", "calculation")
        output_text.insert(tk.END, f"{K_A1A2_val:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen Ao-A1
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen Ao-A1*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan kolom ekuivalen untuk segmen Ao-A1.\n", "explanation")
        Kke_AoA1 = (K_AoA1_val / Sigma_Kk_lantai_edge) * Sigma_Kke_lantai_edge
        output_text.insert(tk.END, f"      Formula Kke(AoA1) = ", "formula")
        output_text.insert(tk.END, f"(K_AoA1 / Sigma Kk) * Sigma Kke\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kke(AoA1) = ({K_AoA1_val:.3f} / {Sigma_Kk_lantai_edge:.3f}) * {Sigma_Kke_lantai_edge:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kke_AoA1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Kolom Ekuivalen Ao-A1: ", "result")
        output_text.insert(tk.END, f"{Kke_AoA1:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen A1-A2
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen A1-A2*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan kolom ekuivalen untuk segmen A1-A2.\n", "explanation")
        Kke_A1A2 = (K_A1A2_val / Sigma_Kk_lantai_edge) * Sigma_Kke_lantai_edge
        output_text.insert(tk.END, f"      Formula Kke(A1A2) = ", "formula")
        output_text.insert(tk.END, f"(K_A1A2 / Sigma Kk) * Sigma Kke\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kke(A1A2) = ({K_A1A2_val:.3f} / {Sigma_Kk_lantai_edge:.3f}) * {Sigma_Kke_lantai_edge:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kke_A1A2:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Kolom Ekuivalen A1-A2: ", "result")
        output_text.insert(tk.END, f"{Kke_A1A2:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen Do-D1 dan D1-D2 (same as Ao-A1 and A1-A2 due to symmetry)
        output_text.insert(tk.END, "\n    *Kekakuan Kolom Ekuivalen Do-D1 dan D1-D2 (Simetris)*:\n", "subheader")
        Kke_DoD1 = Kke_AoA1
        Kke_D1D2 = Kke_A1A2
        output_text.insert(tk.END, f"      Kke(DoD1) = Kke(AoA1) = ", "calculation")
        output_text.insert(tk.END, f"{Kke_DoD1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"      Kke(D1D2) = Kke(A1A2) = ", "calculation")
        output_text.insert(tk.END, f"{Kke_D1D2:.3f} Ec\n\n", "value")

        # Kolom Tengah (Middle Column)
        output_text.insert(tk.END, "\n  *Kolom Tengah (Lantai I)*\n", "subheader")
        output_text.insert(tk.END, "  Perhitungan untuk kolom pada bagian tengah struktur lantai.\n", "explanation")
        # Lebar Efektif Balok Penahan Torsi (be)
        output_text.insert(tk.END, "    *Perhitungan Lebar Efektif Balok Penahan Torsi (be)*:\n", "subheader")
        output_text.insert(tk.END, "    Lebar efektif (be) ditentukan dari nilai terkecil dari dua kriteria untuk kolom tengah.\n", "explanation")
        be1_lantai_middle = balok_lantai_b + 2 * (balok_lantai_h - tp_lantai)
        be2_lantai_middle = balok_lantai_b + 8 * tp_lantai
        be_lantai_middle = min(be1_lantai_middle, be2_lantai_middle)
        output_text.insert(tk.END, f"      Nilai terkecil dari:\n", "calculation")
        output_text.insert(tk.END, f"        be = bw + 2*(h - tp) = {balok_lantai_b} + 2 * ({balok_lantai_h} - {tp_lantai}) = ", "calculation")
        output_text.insert(tk.END, f"{be1_lantai_middle:.1f} cm\n", "value")
        output_text.insert(tk.END, f"        be = bw + 8 * tp = {balok_lantai_b} + 8 * {tp_lantai} = ", "calculation")
        output_text.insert(tk.END, f"{be2_lantai_middle:.1f} cm\n", "value")
        output_text.insert(tk.END, f"    Lebar Efektif Balok Penahan Torsi (be) Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{be_lantai_middle:.3f} cm (Digunakan)\n\n", "value")

        # Momen Inersia Balok Penahan Torsi (C) (T-shaped section)
        output_text.insert(tk.END, "    *Perhitungan Momen Inersia Balok Penahan Torsi (C) (T-shaped)*:\n", "subheader")
        output_text.insert(tk.END, "    Konstanta torsional C dihitung dengan membagi penampang menjadi persegi panjang.\n", "explanation")
        # Section 1 (flange left):
        dim1_part1_lantai_middle = (be_lantai_middle - balok_lantai_b) / 2
        dim2_part1_lantai_middle = tp_lantai
        # Section 2 (flange right):
        dim1_part2_lantai_middle = dim1_part1_lantai_middle
        dim2_part2_lantai_middle = dim2_part1_lantai_middle
        # Section 3 (web):
        dim1_part3_lantai_middle = balok_lantai_b
        dim2_part3_lantai_middle = balok_lantai_h

        x1_lantai_middle_val = min(dim1_part1_lantai_middle, dim2_part1_lantai_middle)
        y1_lantai_middle_val = max(dim1_part1_lantai_middle, dim2_part1_lantai_middle)
        x2_lantai_middle_val = min(dim1_part2_lantai_middle, dim2_part2_lantai_middle)
        y2_lantai_middle_val = max(dim1_part2_lantai_middle, dim2_part2_lantai_middle)
        x3_lantai_middle_val = min(dim1_part3_lantai_middle, dim2_part3_lantai_middle)
        y3_lantai_middle_val = max(dim1_part3_lantai_middle, dim2_part3_lantai_middle)

        ratio1_lantai_middle = x1_lantai_middle_val / y1_lantai_middle_val
        ratio2_lantai_middle = x2_lantai_middle_val / y2_lantai_middle_val
        ratio3_lantai_middle = x3_lantai_middle_val / y3_lantai_middle_val

        term1_val_lantai_middle = x1_lantai_middle_val**3 * y1_lantai_middle_val / 3
        term2_val_lantai_middle = x2_lantai_middle_val**3 * y2_lantai_middle_val / 3
        term3_val_lantai_middle = x3_lantai_middle_val**3 * y3_lantai_middle_val / 3

        C_lantai_middle = (1 - 0.63 * ratio1_lantai_middle) * term1_val_lantai_middle + \
                       (1 - 0.63 * ratio2_lantai_middle) * term2_val_lantai_middle + \
                       (1 - 0.63 * ratio3_lantai_middle) * term3_val_lantai_middle
        
        output_text.insert(tk.END, f"      Formula C: ", "formula")
        output_text.insert(tk.END, f"(1 - 0.63 * x1/y1) * (x1^3 * y1 / 3) + ...\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan C:\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x1_lantai_middle_val:.1f}/{y1_lantai_middle_val:.1f}) * ({x1_lantai_middle_val:.1f}^3 * {y1_lantai_middle_val:.1f} / 3) +\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x2_lantai_middle_val:.1f}/{y2_lantai_middle_val:.1f}) * ({x2_lantai_middle_val:.1f}^3 * {y2_lantai_middle_val:.1f} / 3) +\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x3_lantai_middle_val:.1f}/{y3_lantai_middle_val:.1f})) * ({x3_lantai_middle_val:.1f}^3 * {y3_lantai_middle_val:.1f} / 3)\n", "calculation")
        output_text.insert(tk.END, f"      C = ", "calculation")
        output_text.insert(tk.END, f"{C_lantai_middle:.3f} cm^4\n\n", "value")
        output_text.insert(tk.END, f"    Total Momen Inersia Balok Penahan Torsi (C) Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{C_lantai_middle:.3f} cm^4\n\n", "value")

        # Kekakuan Balok Penahan Torsi (Kt)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Balok Penahan Torsi (Kt)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan torsi balok penahan torsi untuk kolom tengah.\n", "explanation")
        L2_kt_lantai_middle = Lp
        C2_kt_lantai_middle = kolom_b
        Kt_lantai_middle_term1 = (9 * C_lantai_middle) / (L2_kt_lantai_middle * (1 - C2_kt_lantai_middle / L2_kt_lantai_middle)**3)
        Kt_lantai_middle_term2 = (9 * C_lantai_middle) / (L2_kt_lantai_middle * (1 - C2_kt_lantai_middle / L2_kt_lantai_middle)**3)
        Kt_lantai_middle = Kt_lantai_middle_term1 + Kt_lantai_middle_term2
        output_text.insert(tk.END, f"      Formula Kt: ", "formula")
        output_text.insert(tk.END, f"(9 * Ec * C) / (L2 * (1-C2/L2)^3) + (9 * Ec * C) / (L2 * (1-C2/L2)^3)\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt = 2 * (9 * {C_lantai_middle:.3f}) / ({L2_kt_lantai_middle} * (1 - {C2_kt_lantai_middle}/{L2_kt_lantai_middle})^3) = ", "calculation")
        output_text.insert(tk.END, f"{Kt_lantai_middle:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi (Kt) Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{Kt_lantai_middle:.3f} Ec\n\n", "value")

        # Koreksi Kt menjadi Kt'
        output_text.insert(tk.END, "\n    *Koreksi Kekakuan Balok Penahan Torsi menjadi Kt'*:\n", "subheader")
        output_text.insert(tk.END, "    Koreksi ini memperhitungkan efek lentur dari plat pada kolom tengah.\n", "explanation")
        # Ip_lantai_middle = (1/12) * Lp * tp_lantai**3 # Same Ip as edge column
        Kt_prime_lantai_middle_calc = (Ib_p_lantai / Ip_lantai_edge) * Kt_lantai_middle
        output_text.insert(tk.END, f"      Formula Kt': ", "formula")
        output_text.insert(tk.END, f"(Ib+p / Ip) * Kt\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt' = ({Ib_p_lantai:.3f} / {Ip_lantai_edge:.3f}) * {Kt_lantai_middle:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kt_prime_lantai_middle_calc:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi yang telah dikoreksi (Kt') Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{Kt_prime_lantai_middle_calc:.3f} Ec\n\n", "value")

        # Kekakuan Kolom (Sigma Kk) (Same as edge column as column dimensions are the same)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom (Sigma Kk)*:\n", "subheader")
        output_text.insert(tk.END, "    Jumlah kekakuan kolom di atas dan di bawah joint untuk kolom tengah.\n", "explanation")
        output_text.insert(tk.END, f"      Sigma Kk Kolom Tengah (Lantai I) = Sigma Kk Kolom Tepi = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kk_lantai_edge:.3f} Ec\n\n", "value")
        Sigma_Kk_lantai_middle = Sigma_Kk_lantai_edge

        # Kekakuan Kolom Ekuivalen (Sigma Kke)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen (Sigma Kke)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan ekuivalen kolom yang memperhitungkan balok penahan torsi untuk kolom tengah.\n", "explanation")
        Sigma_Kke_lantai_middle = 1 / ((1 / Sigma_Kk_lantai_middle) + (1 / Kt_prime_lantai_middle_calc))
        output_text.insert(tk.END, f"      Formula 1/Sigma Kke = 1/Sigma Kk + 1/Kt'\n", "formula")
        output_text.insert(tk.END, f"      Perhitungan 1/Sigma Kke = 1/{Sigma_Kk_lantai_middle:.3f} Ec + 1/{Kt_prime_lantai_middle_calc:.3f} Ec\n", "calculation")
        output_text.insert(tk.END, f"      Sigma Kke = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kke_lantai_middle:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Sigma Kke Kolom Tengah (Lantai I): ", "result")
        output_text.insert(tk.END, f"{Sigma_Kke_lantai_middle:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Biasa Bo-B1 dan B1-B2
        output_text.insert(tk.END, "\n    *Kekakuan Kolom Biasa Bo-B1 dan B1-B2*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan individual segmen kolom tengah.\n", "explanation")
        K_BoB1_val = K_AoA1_val # Same as Ao-A1
        K_B1B2_val = K_A1A2_val # Same as A1-A2
        output_text.insert(tk.END, f"      K_BoB1 = ", "calculation")
        output_text.insert(tk.END, f"{K_BoB1_val:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"      K_B1B2 = ", "calculation")
        output_text.insert(tk.END, f"{K_B1B2_val:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen Bo-B1
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen Bo-B1*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan kolom ekuivalen untuk segmen Bo-B1.\n", "explanation")
        Kke_BoB1 = (K_BoB1_val / Sigma_Kk_lantai_middle) * Sigma_Kke_lantai_middle
        output_text.insert(tk.END, f"      Formula Kke(BoB1) = ", "formula")
        output_text.insert(tk.END, f"(K_BoB1 / Sigma Kk) * Sigma Kke\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kke(BoB1) = ({K_BoB1_val:.3f} / {Sigma_Kk_lantai_middle:.3f}) * {Sigma_Kke_lantai_middle:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kke_BoB1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Kolom Ekuivalen Bo-B1: ", "result")
        output_text.insert(tk.END, f"{Kke_BoB1:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen B1-B2
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen B1-B2*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan kolom ekuivalen untuk segmen B1-B2.\n", "explanation")
        Kke_B1B2 = (K_B1B2_val / Sigma_Kk_lantai_middle) * Sigma_Kke_lantai_middle
        output_text.insert(tk.END, f"      Formula Kke(B1B2) = ", "formula")
        output_text.insert(tk.END, f"(K_B1B2 / Sigma Kk) * Sigma Kke\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kke(B1B2) = ({K_B1B2_val:.3f} / {Sigma_Kk_lantai_middle:.3f}) * {Sigma_Kke_lantai_middle:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kke_B1B2:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Kolom Ekuivalen B1-B2: ", "result")
        output_text.insert(tk.END, f"{Kke_B1B2:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen Co-C1 dan C1-C2 (same as Bo-B1 and B1-B2 due to symmetry)
        output_text.insert(tk.END, "\n    *Kekakuan Kolom Ekuivalen Co-C1 dan C1-C2 (Simetris)*:\n", "subheader")
        Kke_CoC1 = Kke_BoB1
        Kke_C1C2 = Kke_B1B2
        output_text.insert(tk.END, f"      Kke(CoC1) = Kke(BoB1) = ", "calculation")
        output_text.insert(tk.END, f"{Kke_CoC1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"      Kke(C1C2) = Kke(B1B2) = ", "calculation")
        output_text.insert(tk.END, f"{Kke_C1C2:.3f} Ec\n\n", "value")


        # B.2.2. Ditinjau Titik Joint pada Pelat Dak (Roof)
        output_text.insert(tk.END, "\n\n--- B.2.2. Ditinjau Titik Joint pada Pelat Dak ---\n", "header2")

        # Kolom Tepi (Edge Column)
        output_text.insert(tk.END, "\n  *Kolom Tepi (Lantai II - Dak)*\n", "subheader")
        output_text.insert(tk.END, "  Perhitungan untuk kolom pada tepi struktur dak.\n", "explanation")
        # Lebar Efektif Balok Penahan Torsi (be)
        output_text.insert(tk.END, "    *Perhitungan Lebar Efektif Balok Penahan Torsi (be)*:\n", "subheader")
        output_text.insert(tk.END, "    Lebar efektif (be) ditentukan dari nilai terkecil dari dua kriteria untuk dak.\n", "explanation")
        be1_dak_edge = balok_dak_b + (balok_dak_h - tp_dak)
        be2_dak_edge = balok_dak_b + 4 * tp_dak
        be_dak_edge = min(be1_dak_edge, be2_dak_edge)
        output_text.insert(tk.END, f"      Nilai terkecil dari:\n", "calculation")
        output_text.insert(tk.END, f"        be = bw + (h - tp) = {balok_dak_b} + ({balok_dak_h} - {tp_dak}) = ", "calculation")
        output_text.insert(tk.END, f"{be1_dak_edge:.1f} cm\n", "value")
        output_text.insert(tk.END, f"        be = bw + 4 * tp = {balok_dak_b} + 4 * {tp_dak} = ", "calculation")
        output_text.insert(tk.END, f"{be2_dak_edge:.1f} cm\n", "value")
        output_text.insert(tk.END, f"    Lebar Efektif Balok Penahan Torsi (be) Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{be_dak_edge:.3f} cm (Digunakan)\n\n", "value")

        # Momen Inersia Balok Penahan Torsi (C) (L-shaped section)
        output_text.insert(tk.END, "\n    *Perhitungan Momen Inersia Balok Penahan Torsi (C) (L-shaped)*:\n", "subheader")
        output_text.insert(tk.END, "    Konstanta torsional C dihitung dengan membagi penampang menjadi persegi panjang.\n", "explanation")
        # Section 1 (web): 30 x 30
        dim1_part1_dak_edge = balok_dak_b
        dim2_part1_dak_edge = balok_dak_h
        # Section 2 (flange): 20 x 10
        dim1_part2_dak_edge = be_dak_edge - balok_dak_b
        dim2_part2_dak_edge = tp_dak

        x1_dak_edge_val = min(dim1_part1_dak_edge, dim2_part1_dak_edge)
        y1_dak_edge_val = max(dim1_part1_dak_edge, dim2_part1_dak_edge)
        x2_dak_edge_val = min(dim1_part2_dak_edge, dim2_part2_dak_edge)
        y2_dak_edge_val = max(dim1_part2_dak_edge, dim2_part2_dak_edge)

        ratio1_dak_edge = x1_dak_edge_val / y1_dak_edge_val
        ratio2_dak_edge = x2_dak_edge_val / y2_dak_edge_val

        term1_val_dak_edge = x1_dak_edge_val**3 * y1_dak_edge_val / 3
        term2_val_dak_edge = x2_dak_edge_val**3 * y2_dak_edge_val / 3

        C_dak_edge = (1 - 0.63 * ratio1_dak_edge) * term1_val_dak_edge + \
                     (1 - 0.63 * ratio2_dak_edge) * term2_val_dak_edge
        
        output_text.insert(tk.END, f"      Formula C: ", "formula")
        output_text.insert(tk.END, f"(1 - 0.63 * x1/y1) * (x1^3 * y1 / 3) + (1 - 0.63 * x2/y2) * (x2^3 * y2 / 3)\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan C:\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x1_dak_edge_val:.1f}/{y1_dak_edge_val:.1f}) * ({x1_dak_edge_val:.1f}^3 * {y1_dak_edge_val:.1f} / 3) +\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x2_dak_edge_val:.1f}/{y2_dak_edge_val:.1f}) * ({x2_dak_edge_val:.1f}^3 * {y2_dak_edge_val:.1f} / 3)\n", "calculation")
        output_text.insert(tk.END, f"      C = ", "calculation")
        output_text.insert(tk.END, f"{C_dak_edge:.3f} cm^4\n\n", "value")
        output_text.insert(tk.END, f"    Total Momen Inersia Balok Penahan Torsi (C) Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{C_dak_edge:.3f} cm^4\n\n", "value")

        # Kekakuan Balok Penahan Torsi (Kt)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Balok Penahan Torsi (Kt)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan torsi balok penahan torsi untuk dak.\n", "explanation")
        L2_kt_dak_edge = Lp
        C2_kt_dak_edge = kolom_b
        Kt_dak_edge_term1 = (9 * C_dak_edge) / (L2_kt_dak_edge * (1 - C2_kt_dak_edge / L2_kt_dak_edge)**3)
        Kt_dak_edge_term2 = (9 * C_dak_edge) / (L2_kt_dak_edge * (1 - C2_kt_dak_edge / L2_kt_dak_edge)**3)
        Kt_dak_edge = Kt_dak_edge_term1 + Kt_dak_edge_term2
        output_text.insert(tk.END, f"      Formula Kt: ", "formula")
        output_text.insert(tk.END, f"(9 * Ec * C) / (L2 * (1-C2/L2)^3) + (9 * Ec * C) / (L2 * (1-C2/L2)^3)\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt = 2 * (9 * {C_dak_edge:.3f}) / ({L2_kt_dak_edge} * (1 - {C2_kt_dak_edge}/{L2_kt_dak_edge})^3) = ", "calculation")
        output_text.insert(tk.END, f"{Kt_dak_edge:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi (Kt) Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{Kt_dak_edge:.3f} Ec\n\n", "value")

        # Koreksi Kt menjadi Kt'
        output_text.insert(tk.END, "\n    *Koreksi Kekakuan Balok Penahan Torsi menjadi Kt'*:\n", "subheader")
        output_text.insert(tk.END, "    Koreksi ini memperhitungkan efek lentur dari plat pada dak.\n", "explanation")
        Ip_dak_edge_calc = (1/12) * Lp * tp_dak**3
        output_text.insert(tk.END, f"      Ip (Momen Inersia Plat): (1/12) * {Lp} * {tp_dak}^3 = ", "calculation")
        output_text.insert(tk.END, f"{Ip_dak_edge_calc:.3f} cm^4\n", "value")
        Kt_prime_dak_edge_calc = (Ib_p_dak / Ip_dak_edge_calc) * Kt_dak_edge
        output_text.insert(tk.END, f"      Formula Kt': ", "formula")
        output_text.insert(tk.END, f"(Ib+p / Ip) * Kt\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt' = ({Ib_p_dak:.3f} / {Ip_dak_edge_calc:.3f}) * {Kt_dak_edge:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kt_prime_dak_edge_calc:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi yang telah dikoreksi (Kt') Kolom Tepi: ", "result")
        output_text.insert(tk.END, f"{Kt_prime_dak_edge_calc:.3f} Ec\n\n", "value")

        # Kekakuan Kolom (Sigma Kk) (Only the column below this level)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom (Sigma Kk)*:\n", "subheader")
        output_text.insert(tk.END, "    Jumlah kekakuan kolom di bawah dak.\n", "explanation")
        output_text.insert(tk.END, f"      Kolom di bawah pelat dak adalah A1-A2 (atas)\n", "calculation")
        Sigma_Kk_dak_edge = K_A1A2_val # Only column A1-A2 contributes here for the roof
        output_text.insert(tk.END, f"      Sigma Kk = K_A1A2 = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kk_dak_edge:.3f} Ec\n\n", "value")
        output_text.insert(tk.END, f"    Sigma Kk Kolom Tepi (Lantai II): ", "result")
        output_text.insert(tk.END, f"{Sigma_Kk_dak_edge:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen (Sigma Kke)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen (Sigma Kke)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan ekuivalen kolom yang memperhitungkan balok penahan torsi untuk dak.\n", "explanation")
        Sigma_Kke_dak_edge = 1 / ((1 / Sigma_Kk_dak_edge) + (1 / Kt_prime_dak_edge_calc))
        output_text.insert(tk.END, f"      Formula 1/Sigma Kke = 1/Sigma Kk + 1/Kt'\n", "formula")
        output_text.insert(tk.END, f"      Perhitungan 1/Sigma Kke = 1/{Sigma_Kk_dak_edge:.3f} Ec + 1/{Kt_prime_dak_edge_calc:.3f} Ec\n", "calculation")
        output_text.insert(tk.END, f"      Sigma Kke = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kke_dak_edge:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Sigma Kke Kolom Tepi (Lantai II): ", "result")
        output_text.insert(tk.END, f"{Sigma_Kke_dak_edge:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen A1-A2
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen A1-A2*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan kolom ekuivalen untuk segmen A1-A2 pada dak.\n", "explanation")
        Kke_A1A2_dak = Sigma_Kke_dak_edge
        output_text.insert(tk.END, f"      Kke(A1A2) = Sigma Kke = ", "calculation")
        output_text.insert(tk.END, f"{Kke_A1A2_dak:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Kolom Ekuivalen A1-A2 (Dak): ", "result")
        output_text.insert(tk.END, f"{Kke_A1A2_dak:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen D1-D2 (same as A1-A2 due to symmetry)
        output_text.insert(tk.END, "\n    *Kekakuan Kolom Ekuivalen D1-D2 (Simetris)*:\n", "subheader")
        Kke_D1D2_dak = Kke_A1A2_dak
        output_text.insert(tk.END, f"      Kke(D1D2) = Kke(A1A2) = ", "calculation")
        output_text.insert(tk.END, f"{Kke_D1D2_dak:.3f} Ec\n\n", "value")


        # Kolom Tengah (Middle Column)
        output_text.insert(tk.END, "\n  *Kolom Tengah (Lantai II - Dak)*\n", "subheader")
        output_text.insert(tk.END, "  Perhitungan untuk kolom pada bagian tengah struktur dak.\n", "explanation")
        # Lebar Efektif Balok Penahan Torsi (be)
        output_text.insert(tk.END, "    *Perhitungan Lebar Efektif Balok Penahan Torsi (be)*:\n", "subheader")
        output_text.insert(tk.END, "    Lebar efektif (be) ditentukan dari nilai terkecil dari dua kriteria untuk kolom tengah dak.\n", "explanation")
        be1_dak_middle = balok_dak_b + 2 * (balok_dak_h - tp_dak)
        be2_dak_middle = balok_dak_b + 8 * tp_dak
        be_dak_middle = min(be1_dak_middle, be2_dak_middle)
        output_text.insert(tk.END, f"      Nilai terkecil dari:\n", "calculation")
        output_text.insert(tk.END, f"        be = bw + 2*(h - tp) = {balok_dak_b} + 2 * ({balok_dak_h} - {tp_dak}) = ", "calculation")
        output_text.insert(tk.END, f"{be1_dak_middle:.1f} cm\n", "value")
        output_text.insert(tk.END, f"        be = bw + 8 * tp = {balok_dak_b} + 8 * {tp_dak} = ", "calculation")
        output_text.insert(tk.END, f"{be2_dak_middle:.1f} cm\n", "value")
        output_text.insert(tk.END, f"    Lebar Efektif Balok Penahan Torsi (be) Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{be_dak_middle:.3f} cm (Digunakan)\n\n", "value")

        # Momen Inersia Balok Penahan Torsi (C) (T-shaped section)
        output_text.insert(tk.END, "\n    *Perhitungan Momen Inersia Balok Penahan Torsi (C) (T-shaped)*:\n", "subheader")
        output_text.insert(tk.END, "    Konstanta torsional C dihitung dengan membagi penampang menjadi persegi panjang.\n", "explanation")
        # Section 1 (flange left):
        dim1_part1_dak_middle = (be_dak_middle - balok_dak_b) / 2
        dim2_part1_dak_middle = tp_dak
        # Section 2 (flange right):
        dim1_part2_dak_middle = dim1_part1_dak_middle
        dim2_part2_dak_middle = dim2_part1_dak_middle
        # Section 3 (web):
        dim1_part3_dak_middle = balok_dak_b
        dim2_part3_dak_middle = balok_dak_h

        x1_dak_middle_val = min(dim1_part1_dak_middle, dim2_part1_dak_middle)
        y1_dak_middle_val = max(dim1_part1_dak_middle, dim2_part1_dak_middle)
        x2_dak_middle_val = min(dim1_part2_dak_middle, dim2_part2_dak_middle)
        y2_dak_middle_val = max(dim1_part2_dak_middle, dim2_part2_dak_middle)
        x3_dak_middle_val = min(dim1_part3_dak_middle, dim2_part3_dak_middle)
        y3_dak_middle_val = max(dim1_part3_dak_middle, dim2_part3_dak_middle)

        ratio1_dak_middle = x1_dak_middle_val / y1_dak_middle_val
        ratio2_dak_middle = x2_dak_middle_val / y2_dak_middle_val
        ratio3_dak_middle = x3_dak_middle_val / y3_dak_middle_val

        term1_val_dak_middle = x1_dak_middle_val**3 * y1_dak_middle_val / 3
        term2_val_dak_middle = x2_dak_middle_val**3 * y2_dak_middle_val / 3
        term3_val_dak_middle = x3_dak_middle_val**3 * y3_dak_middle_val / 3

        C_dak_middle = (1 - 0.63 * ratio1_dak_middle) * term1_val_dak_middle + \
                       (1 - 0.63 * ratio2_dak_middle) * term2_val_dak_middle + \
                       (1 - 0.63 * ratio3_dak_middle) * term3_val_dak_middle
        
        output_text.insert(tk.END, f"      Formula C: ", "formula")
        output_text.insert(tk.END, f"(1 - 0.63 * x1/y1) * (x1^3 * y1 / 3) + ...\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan C:\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x1_dak_middle_val:.1f}/{y1_dak_middle_val:.1f}) * ({x1_dak_middle_val:.1f}^3 * {y1_dak_middle_val:.1f} / 3) +\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x2_dak_middle_val:.1f}/{y2_dak_middle_val:.1f}) * ({x2_dak_middle_val:.1f}^3 * {y2_dak_middle_val:.1f} / 3) +\n", "calculation")
        output_text.insert(tk.END, f"        (1 - 0.63 * {x3_dak_middle_val:.1f}/{y3_dak_middle_val:.1f})) * ({x3_dak_middle_val:.1f}^3 * {y3_dak_middle_val:.1f} / 3)\n", "calculation")
        output_text.insert(tk.END, f"      C = ", "calculation")
        output_text.insert(tk.END, f"{C_dak_middle:.3f} cm^4\n\n", "value")
        output_text.insert(tk.END, f"    Total Momen Inersia Balok Penahan Torsi (C) Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{C_dak_middle:.3f} cm^4\n\n", "value")

        # Kekakuan Balok Penahan Torsi (Kt)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Balok Penahan Torsi (Kt)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan torsi balok penahan torsi untuk kolom tengah dak.\n", "explanation")
        L2_kt_dak_middle = Lp
        C2_kt_dak_middle = kolom_b
        Kt_dak_middle_term1 = (9 * C_dak_middle) / (L2_kt_dak_middle * (1 - C2_kt_dak_middle / L2_kt_dak_middle)**3)
        Kt_dak_middle_term2 = (9 * C_dak_middle) / (L2_kt_dak_middle * (1 - C2_kt_dak_middle / L2_kt_dak_middle)**3)
        Kt_dak_middle = Kt_dak_middle_term1 + Kt_dak_middle_term2
        output_text.insert(tk.END, f"      Formula Kt: ", "formula")
        output_text.insert(tk.END, f"(9 * Ec * C) / (L2 * (1-C2/L2)^3) + (9 * Ec * C) / (L2 * (1-C2/L2)^3)\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt = 2 * (9 * {C_dak_middle:.3f}) / ({L2_kt_dak_middle} * (1 - {C2_kt_dak_middle}/{L2_kt_dak_middle})^3) = ", "calculation")
        output_text.insert(tk.END, f"{Kt_dak_middle:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi (Kt) Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{Kt_dak_middle:.3f} Ec\n\n", "value")

        # Koreksi Kt menjadi Kt'
        output_text.insert(tk.END, "\n    *Koreksi Kekakuan Balok Penahan Torsi menjadi Kt'*:\n", "subheader")
        output_text.insert(tk.END, "    Koreksi ini memperhitungkan efek lentur dari plat pada kolom tengah dak.\n", "explanation")
        # Ip_dak_middle = (1/12) * Lp * tp_dak**3 # Same Ip as edge column
        Kt_prime_dak_middle_calc = (Ib_p_dak / Ip_dak_edge_calc) * Kt_dak_middle
        output_text.insert(tk.END, f"      Formula Kt': ", "formula")
        output_text.insert(tk.END, f"(Ib+p / Ip) * Kt\n", "calculation")
        output_text.insert(tk.END, f"      Perhitungan Kt' = ({Ib_p_dak:.3f} / {Ip_dak_edge_calc:.3f}) * {Kt_dak_middle:.3f} = ", "calculation")
        output_text.insert(tk.END, f"{Kt_prime_dak_middle_calc:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Balok Penahan Torsi yang telah dikoreksi (Kt') Kolom Tengah: ", "result")
        output_text.insert(tk.END, f"{Kt_prime_dak_middle_calc:.3f} Ec\n\n", "value")

        # Kekakuan Kolom (Sigma Kk) (Only the column below this level)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom (Sigma Kk)*:\n", "subheader")
        output_text.insert(tk.END, "    Jumlah kekakuan kolom di bawah dak untuk kolom tengah.\n", "explanation")
        output_text.insert(tk.END, f"      Kolom di bawah pelat dak adalah B1-B2 (atas)\n", "calculation")
        Sigma_Kk_dak_middle = K_B1B2_val # Only column B1-B2 contributes here for the roof
        output_text.insert(tk.END, f"      Sigma Kk = K_B1B2 = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kk_dak_middle:.3f} Ec\n\n", "value")
        output_text.insert(tk.END, f"    Sigma Kk Kolom Tengah (Lantai II): ", "result")
        output_text.insert(tk.END, f"{Sigma_Kk_dak_middle:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen (Sigma Kke)
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen (Sigma Kke)*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan ekuivalen kolom yang memperhitungkan balok penahan torsi untuk kolom tengah dak.\n", "explanation")
        Sigma_Kke_dak_middle = 1 / ((1 / Sigma_Kk_dak_middle) + (1 / Kt_prime_dak_middle_calc))
        output_text.insert(tk.END, f"      Formula 1/Sigma Kke = 1/Sigma Kk + 1/Kt'\n", "formula")
        output_text.insert(tk.END, f"      Perhitungan 1/Sigma Kke = 1/{Sigma_Kk_dak_middle:.3f} Ec + 1/{Kt_prime_dak_middle_calc:.3f} Ec\n", "calculation")
        output_text.insert(tk.END, f"      Sigma Kke = ", "calculation")
        output_text.insert(tk.END, f"{Sigma_Kke_dak_middle:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Sigma Kke Kolom Tengah (Lantai II): ", "result")
        output_text.insert(tk.END, f"{Sigma_Kke_dak_middle:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen B1-B2
        output_text.insert(tk.END, "\n    *Perhitungan Kekakuan Kolom Ekuivalen B1-B2*:\n", "subheader")
        output_text.insert(tk.END, "    Kekakuan kolom ekuivalen untuk segmen B1-B2 pada dak.\n", "explanation")
        Kke_B1B2_dak = Sigma_Kke_dak_middle
        output_text.insert(tk.END, f"      Kke(B1B2) = Sigma Kke = ", "calculation")
        output_text.insert(tk.END, f"{Kke_B1B2_dak:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    Kekakuan Kolom Ekuivalen B1-B2 (Dak): ", "result")
        output_text.insert(tk.END, f"{Kke_B1B2_dak:.3f} Ec\n\n", "value")

        # Kekakuan Kolom Ekuivalen C1-C2 (same as B1-B2 due to symmetry)
        output_text.insert(tk.END, "\n    *Kekakuan Kolom Ekuivalen C1-C2 (Simetris)*:\n", "subheader")
        Kke_C1C2_dak = Kke_B1B2_dak
        output_text.insert(tk.END, f"      Kke(C1C2) = Kke(B1B2) = ", "calculation")
        output_text.insert(tk.END, f"{Kke_C1C2_dak:.3f} Ec\n\n", "value")


        output_text.insert(tk.END, "\n\n===== Rekapitulasi Kekakuan Struktur Portal Ekuivalen ====="+"\n", "header1")
        output_text.insert(tk.END, "  Berikut adalah ringkasan hasil kekakuan untuk setiap elemen struktur.\n\n", "explanation")
        output_text.insert(tk.END, "  **Kekakuan Balok Ekuivalen (Lantai I):**\n", "bold")
        output_text.insert(tk.END, f"    *Bentang A1-B1*: ", "bold")
        output_text.insert(tk.END, f"{Kbe_A1B1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Bentang B1-C1*: ", "bold")
        output_text.insert(tk.END, f"{Kbe_B1C1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Bentang C1-D1*: ", "bold")
        output_text.insert(tk.END, f"{Kbe_C1D1:.3f} Ec\n\n", "value")
        output_text.insert(tk.END, "  **Kekakuan Balok Ekuivalen (Lantai II - Dak):**\n", "bold")
        output_text.insert(tk.END, f"    *Bentang A2-B2*: ", "bold")
        output_text.insert(tk.END, f"{Kbe_A2B2:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Bentang B2-C2*: ", "bold")
        output_text.insert(tk.END, f"{Kbe_B2C2:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Bentang C2-D2*: ", "bold")
        output_text.insert(tk.END, f"{Kbe_C2D2:.3f} Ec\n\n", "value")

        output_text.insert(tk.END, "  **Kekakuan Kolom Ekuivalen (Lantai I):**\n", "bold")
        output_text.insert(tk.END, f"    *Kolom Tepi (Ao-A1)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_AoA1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tepi (A1-A2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_A1A2:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tepi (Do-D1)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_DoD1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tepi (D1-D2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_D1D2:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tengah (Bo-B1)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_BoB1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tengah (B1-B2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_B1B2:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tengah (Co-C1)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_CoC1:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tengah (C1-C2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_C1C2:.3f} Ec\n\n", "value")

        output_text.insert(tk.END, "  **Kekakuan Kolom Ekuivalen (Lantai II - Dak):**\n", "bold")
        output_text.insert(tk.END, f"    *Kolom Tepi (A1-A2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_A1A2_dak:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tepi (D1-D2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_D1D2_dak:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tengah (B1-B2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_B1B2_dak:.3f} Ec\n", "value")
        output_text.insert(tk.END, f"    *Kolom Tengah (C1-C2)*: ", "bold")
        output_text.insert(tk.END, f"{Kke_C1C2_dak:.3f} Ec\n\n", "value")


    except ValueError:
        messagebox.showerror("Input Error", "Mohon masukkan nilai numerik yang valid untuk semua input.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    finally:
        output_text.config(state=tk.DISABLED)


# --- GUI Setup ---
root = tk.Tk()
root.title("Aplikasi Perhitungan Kekakuan Struktur Portal Ekuivalen")
root.geometry("1400x800")

# Apply a modern style
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10, "bold"))
style.configure("TEntry", font=("Helvetica", 10))
style.configure("TLabelFrame", font=("Helvetica", 12, "bold"))

# Main Frames
input_frame = ttk.LabelFrame(root, text="Data Input Proyek", padding="15")
input_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

output_frame = ttk.LabelFrame(root, text="Langkah dan Hasil Perhitungan", padding="15")
output_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

# Configure grid for main window to expand
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# Configure grid for input_frame
input_frame.columnconfigure(1, weight=1)

# Input fields
labels_data = [
    ("Tebal plat dak (cm):", "tp_dak", "10"),
    ("Tebal plat lantai (cm):", "tp_lantai", "15"),
    ("Ukuran Balok dak - lebar (cm):", "balok_dak_b", "30"),
    ("Ukuran Balok dak - tinggi (cm):", "balok_dak_h", "30"),
    ("Ukuran Balok lantai - lebar (cm):", "balok_lantai_b", "30"),
    ("Ukuran Balok lantai - tinggi (cm):", "balok_lantai_h", "50"),
    ("Ukuran Kolom - lebar (cm):", "kolom_b", "40"),
    ("Ukuran Kolom - tinggi (cm):", "kolom_h", "40"),
    ("Panjang kolom atas (cm):", "L_kolom_atas", "450"),
    ("Panjang kolom bawah (cm):", "L_kolom_bawah", "700"),
    ("Mutu beton fc' (MPa):", "fc_prime", "18"),
    ("Mutu baja fy (MPa):", "fy", "400"),
    ("Panjang Bentang Pendek:", "L_Pendek", "400"),
    ("Panjang Bentang panjang:", "L_Panjang", "400"),
    ("Panjang Jalur:", "LP", "400")
]

entries = {}
row_idx = 0

for label_text, key, default_value in labels_data:
    ttk.Label(input_frame, text=label_text).grid(row=row_idx, column=0, sticky="w", pady=4, padx=5)
    entry = ttk.Entry(input_frame, width=20)
    entry.grid(row=row_idx, column=1, sticky="ew", pady=4, padx=5)
    entry.insert(0, default_value)
    entries[key] = entry
    row_idx += 1

# Assign specific entry widgets for easier access
entry_tp_dak = entries["tp_dak"]
entry_tp_lantai = entries["tp_lantai"]
entry_balok_dak_b = entries["balok_dak_b"]
entry_balok_dak_h = entries["balok_dak_h"]
entry_balok_lantai_b = entries["balok_lantai_b"]
entry_balok_lantai_h = entries["balok_lantai_h"]
entry_kolom_b = entries["kolom_b"]
entry_kolom_h = entries["kolom_h"]
entry_L_kolom_atas = entries["L_kolom_atas"]
entry_L_kolom_bawah = entries["L_kolom_bawah"]
entry_fc_prime = entries["fc_prime"]
entry_fy = entries["fy"]
entry_L_span_long = entries["L_Panjang"]
entry_L_span_short = entries["L_Pendek"]
entry_Lp = entries["LP"]


# Calculation Button
calculate_button = ttk.Button(input_frame, text="Hitung Kekakuan Struktur", command=calculate_all, cursor="hand2")
calculate_button.grid(row=row_idx, column=0, columnspan=2, pady=15, padx=5)

# Output Text Area
output_frame.columnconfigure(0, weight=1)
output_frame.rowconfigure(0, weight=1)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=100, height=35, font=("Consolas", 9), relief="flat", bg="#f0f0f0")
output_text.grid(row=0, column=0, sticky="nsew")
output_text.config(state=tk.DISABLED)

root.mainloop()