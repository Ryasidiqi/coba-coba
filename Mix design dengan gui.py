import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

# --- Definisi Tabel-Tabel SNI (Sama seperti sebelumnya) ---
# ... (Definisi tabel-tabel SNI yang sudah ada di program sebelumnya bisa dimasukkan di sini) ...
# Tabel 4.1 & 4.2 (Nilai Deviasi Standar) - Disederhanakan
def hitung_f_cr(f_c_rencana, S_s):
    if f_c_rencana <= 35:
        f_cr_1_calc = f_c_rencana + 1.34 * S_s
        f_cr_2_calc = f_c_rencana + 2.33 * S_s - 3.5
        return max(f_cr_1_calc, f_cr_2_calc), f_cr_1_calc, f_cr_2_calc
    else:
        f_cr_1_calc = f_c_rencana + 1.34 * S_s
        f_cr_2_calc = 0.90 * f_c_rencana + 2.33 * S_s
        return max(f_cr_1_calc, f_cr_2_calc), f_cr_1_calc, f_cr_2_calc

tabel_kebutuhan_air_udara = {
    9.5: {(25, 50): (207, 3.0), (75, 100): (228, 3.0), (150, 175): (243, 3.0)},
    12.7: {(25, 50): (199, 2.5), (75, 100): (216, 2.5), (150, 175): (228, 2.5)},
    19: {(25, 50): (190, 2.0), (75, 100): (205, 2.0), (150, 175): (216, 2.0)},
    25: {(25, 50): (179, 1.5), (75, 100): (193, 1.5), (150, 175): (202, 1.5)},
    37.5: {(25, 50): (166, 1.0), (75, 100): (181, 1.0), (150, 175): (190, 1.0)},
    50: {(25, 50): (154, 0.5), (75, 100): (169, 0.5), (150, 175): (178, 0.5)},
    75: {(25, 50): (130, 0.3), (75, 100): (145, 0.3), (150, 175): (160, 0.3)},
    150: {(25, 50): (113, 0.2), (75, 100): (124, 0.2)}
}
tabel_fas = {
    40: 0.42, 35: 0.47, 30: 0.54, 25: 0.61, 20: 0.69, 15: 0.79
}
tabel_volume_ag_kasar = {
    9.5: {2.4: 0.50, 2.6: 0.48, 2.8: 0.46, 3.0: 0.44},
    12.5: {2.4: 0.59, 2.6: 0.57, 2.8: 0.55, 3.0: 0.53},
    19: {2.4: 0.66, 2.6: 0.64, 2.8: 0.62, 3.0: 0.60},
    25: {2.4: 0.71, 2.6: 0.69, 2.8: 0.67, 3.0: 0.65},
    37.5: {2.4: 0.75, 2.6: 0.73, 2.8: 0.71, 3.0: 0.69},
    50: {2.4: 0.78, 2.6: 0.76, 2.8: 0.74, 3.0: 0.72},
    75: {2.4: 0.82, 2.6: 0.80, 2.8: 0.78, 3.0: 0.76},
    150: {2.4: 0.87, 2.6: 0.85, 2.8: 0.83, 3.0: 0.81}
}
tabel_berat_beton_segar = {
    9.5: 2280, 12.5: 2310, 19: 2345, 25: 2380, 37.5: 2410,
    50: 2445, 75: 2490, 150: 2530
}

def format_equation_natural(y_target_name, y1_val, x_target_val, x1_val, y2_val, y1_val_2, x2_val, x1_val_2):
    """Helper untuk memformat persamaan interpolasi secara natural."""
    numerator_val = (y2_val - y1_val_2)
    denominator_val = (x2_val - x1_val_2)
    fraction_val = numerator_val / denominator_val if denominator_val != 0 else 0
    
    lines = []
    lines.append(f"  {y_target_name} = y1 + ( (x_target - x1) / (x2 - x1) ) * (y2 - y1)")
    lines.append(f"      = {y1_val:.4f} + ( ({x_target_val:.2f} - {x1_val:.2f}) / ({x2_val:.2f} - {x1_val:.2f}) ) * ({y2_val:.4f} - {y1_val_2:.4f})")
    lines.append(f"      = {y1_val:.4f} + ( {x_target_val - x1_val:.2f} / {x2_val - x1_val:.2f} ) * ({numerator_val:.4f})")
    if denominator_val != 0:
        lines.append(f"      = {y1_val:.4f} + ( {(x_target_val - x1_val) / denominator_val:.4f} ) * ({numerator_val:.4f})")
        lines.append(f"      = {y1_val:.4f} + {((x_target_val - x1_val) / denominator_val) * numerator_val:.4f}")
    else:
        lines.append(f"      = {y1_val:.4f} + (Pembagian dengan nol dihindari)")
    return lines

def interpolasi_ekstrapolasi_natural(x_target, x_data, y_data, var_name_x="x", var_name_y="y", output_text_area=None):
    def log_message_natural(message, indent_level=1, tag=None):
        indent = "  " * indent_level # 2 spasi per indent
        if output_text_area:
            output_text_area.insert(tk.END, indent + message + "\n", tag)
            output_text_area.see(tk.END)
        else:
            print(indent + message)

    log_message_natural(f"Proses interpolasi/ekstrapolasi untuk {var_name_y} pada {var_name_x} = {x_target:.2f}", 0, "subheader_calc")

    if len(x_data) < 2 or len(y_data) < 2 or len(x_data) != len(y_data):
        log_message_natural("Error: Data tidak cukup atau tidak konsisten.", 1)
        raise ValueError("Data untuk interpolasi/ekstrapolasi tidak cukup atau tidak konsisten.")

    for i, xi in enumerate(x_data):
        if xi == x_target:
            log_message_natural(f"Nilai {x_target:.2f} ditemukan langsung, {var_name_y} = {y_data[i]:.4f}", 1)
            return y_data[i]

    # Tentukan titik data untuk interpolasi/ekstrapolasi
    x1_calc, y1_calc, x2_calc, y2_calc = 0,0,0,0
    operation_type = ""

    # Urutkan data untuk memudahkan pencarian titik
    sorted_pairs = sorted(zip(x_data, y_data))
    x_s = [p[0] for p in sorted_pairs]
    y_s = [p[1] for p in sorted_pairs]

    found_interpolate = False
    for i in range(len(x_s) - 1):
        if x_s[i] <= x_target <= x_s[i+1]:
            x1_calc, y1_calc = x_s[i], y_s[i]
            x2_calc, y2_calc = x_s[i+1], y_s[i+1]
            operation_type = "Interpolasi"
            found_interpolate = True
            break
    
    if not found_interpolate: # Ekstrapolasi
        if x_target < x_s[0]:
            x1_calc, y1_calc = x_s[0], y_s[0]
            x2_calc, y2_calc = x_s[1], y_s[1]
            operation_type = "Ekstrapolasi ke kiri"
        elif x_target > x_s[-1]:
            x1_calc, y1_calc = x_s[-2], y_s[-2]
            x2_calc, y2_calc = x_s[-1], y_s[-1]
            operation_type = "Ekstrapolasi ke kanan"
        else: # Seharusnya tidak terjadi jika data terurut
            log_message_natural("Error: Logika penentuan titik ekstrapolasi gagal.", 1)
            raise Exception("Logika penentuan titik ekstrapolasi gagal.")

    log_message_natural(f"{operation_type} antara/menggunakan titik ({x1_calc:.2f}, {y1_calc:.4f}) dan ({x2_calc:.2f}, {y2_calc:.4f})", 1)
    
    if x1_calc == x2_calc:
        log_message_natural(f"Hasil (x1=x2): {y1_calc:.4f}", 2)
        return y1_calc
    
    # Tampilkan proses perhitungan dengan format natural
    equation_lines = format_equation_natural(var_name_y, y1_calc, x_target, x1_calc, y2_calc, y1_calc, x2_calc, x1_calc)
    for line in equation_lines:
        log_message_natural(line, 2, "equation_detail") # Tag baru untuk detail rumus

    hasil_calc = y1_calc + (x_target - x1_calc) * (y2_calc - y1_calc) / (x2_calc - x1_calc)
    log_message_natural(f"Hasil {operation_type.lower()}: {hasil_calc:.4f}", 1, "result_value_calc")
    return hasil_calc


class MixDesignAppNormalGUI_Natural:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Perhitungan Mix Design Beton Normal (Format Natural)")
        self.root.geometry("1000x800") 

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("TEntry", font=("Arial", 11), padding=5)
        self.style.configure("TButton", font=("Arial", 11, "bold"), padding=5)
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold", "underline"), padding=(0,10)) # Lebih besar
        self.style.configure("SubHeader.TLabel", font=("Arial", 13, "bold"), padding=(0,5)) # Lebih besar
        self.style.configure("Result.TLabel", font=("Arial", 12, "bold"), foreground="blue") # Lebih besar
        self.style.configure("EquationStep.TLabel", font=("Consolas", 12, "italic"), foreground="#333333") # Font untuk rumus
        self.style.configure("FinalHeader.TLabel", font=("Arial", 14, "bold"), justify='center', spacing3=10, padding=(0,10))
        self.style.configure("FinalKomposisi.TLabel", font=("Consolas", 12, "bold"))


        main_canvas = tk.Canvas(root_window)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(root_window, orient=tk.VERTICAL, command=main_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.configure(yscrollcommand=scrollbar.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion = main_canvas.bbox("all")))
        self.scrollable_frame = ttk.Frame(main_canvas, style="Background.TFrame") # Tambah style jika perlu
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        input_frame = ttk.LabelFrame(self.scrollable_frame, text="Input Data Desain Beton Normal", padding=(15, 10))
        input_frame.pack(padx=10, pady=10, fill="x")

        self.entries = {}
        input_fields_normal = [
            ("Kuat Tekan Beton Rencana (f_c') (MPa)", "23"), ("Deviasi Standar (S_s) (MPa)", "7.0"),
            ("Slump Rencana Minimum (mm)", "25"), ("Slump Rencana Maksimum (mm)", "50"),
            ("Ukuran Agregat Maksimum (mm)", "20"), ("MHB Agregat Halus", "2.03"),
            ("Berat Volume Ag. Kasar Padat (kg/m³)", "1440"), ("SG Semen", "3.15"),
            ("SG Agregat Kasar", "2.75"), ("SG Agregat Halus", "2.35"),
            ("Kadar Air Ag. Kasar (%)", "0.997"), ("Kadar Air Ag. Halus (%)", "4.39"),
            ("Absorpsi Air Ag. Kasar (%)", "0.30"), ("Absorpsi Air Ag. Halus (%)", "4.16")
        ]

        for i, (text, default_val) in enumerate(input_fields_normal):
            row, col = divmod(i, 4) # Ubah jadi 4 kolom input agar lebih ringkas
            ttk.Label(input_frame, text=text + ":").grid(row=row, column=col*2, padx=5, pady=6, sticky="w")
            entry = ttk.Entry(input_frame, width=10) # Lebar entry
            entry.insert(0, default_val)
            entry.grid(row=row, column=col*2 + 1, padx=5, pady=6, sticky="ew")
            self.entries[text.split(" (")[0]] = entry

        calculate_button = ttk.Button(self.scrollable_frame, text="HITUNG MIX DESIGN NORMAL", command=self.calculate_mix_design_normal_gui)
        calculate_button.pack(pady=15, ipady=5) # Tombol lebih besar

        output_frame = ttk.LabelFrame(self.scrollable_frame, text="Hasil dan Proses Perhitungan Beton Normal", padding=(15, 10))
        output_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 12), height=20, relief=tk.SOLID, borderwidth=1)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Define tags untuk styling
        self.output_text.tag_configure("header_main", font=("Arial", 16, "bold", "underline"), justify='center', spacing1=10, spacing3=10)
        self.output_text.tag_configure("subheader_step", font=("Arial", 13, "bold", "underline"), spacing1=5, spacing3=5)
        self.output_text.tag_configure("equation_general", font=("Consolas", 12, "italic"), foreground="#000080", lmargin1="20p", lmargin2="20p") # Biru tua
        self.output_text.tag_configure("equation_detail", font=("Consolas", 12), lmargin1="30p", lmargin2="30p", spacing1=2)
        self.output_text.tag_configure("result_value_step", font=("Consolas", 12, "bold"), foreground="darkgreen", lmargin1="20p", lmargin2="20p")
        self.output_text.tag_configure("final_header_summary", font=("Arial", 14, "bold"), justify='center', spacing1=10, spacing3=10, foreground="#006400") # Hijau tua
        self.output_text.tag_configure("final_komposisi_summary", font=("Consolas", 12, "bold"), lmargin1="20p", lmargin2="20p", spacing1=3)


    def log_to_gui_styled(self, message, tag=None, indent_level=0):
        indent = "  " * indent_level
        self.output_text.insert(tk.END, indent + message + "\n", tag)
        self.output_text.see(tk.END)
        self.output_text.update_idletasks()

    def get_float_entry(self, name, is_percentage=False):
        try:
            val_str = self.entries[name].get()
            if not val_str: # Handle empty entry
                 messagebox.showerror("Input Error", f"Nilai untuk '{name}' tidak boleh kosong.")
                 return None
            val = float(val_str)
            return val / 100 if is_percentage else val
        except ValueError:
            messagebox.showerror("Input Error", f"Nilai tidak valid untuk '{name}'. Harap masukkan angka.")
            return None
        except KeyError:
            messagebox.showerror("Input Error", f"Field '{name}' tidak ditemukan.")
            return None
            
    def log_equation_natural_format(self, title, var_name, formula_parts, values, result, unit=""):
        self.log_to_gui_styled(f"{title}:", "subheader_calc", 1)
        
        # Tampilkan rumus umum
        formula_str = f"{var_name} = "
        for part in formula_parts:
            formula_str += str(part) + " "
        self.log_to_gui_styled(formula_str.strip(), "equation_general", 2)

        # Tampilkan substitusi nilai
        subst_str = f"{var_name} = "
        for val_part in values:
            if isinstance(val_part, (int,float)):
                subst_str += f"{val_part:.2f} "
            else:
                subst_str += str(val_part) + " "
        subst_str += f"= {result:.2f} {unit}" # Tampilkan hasil akhir di baris substitusi
        self.log_to_gui_styled(subst_str.strip(), "equation_detail", 2)


    def calculate_mix_design_normal_gui(self):
        self.output_text.delete(1.0, tk.END)
        
        try:
            # ... (Pengambilan input sama seperti sebelumnya, panggil get_float_entry) ...
            f_c_rencana = self.get_float_entry("Kuat Tekan Beton Rencana")
            S_s = self.get_float_entry("Deviasi Standar")
            slump_min = self.get_float_entry("Slump Rencana Minimum")
            slump_maks = self.get_float_entry("Slump Rencana Maksimum")
            ukuran_agregat_maks = self.get_float_entry("Ukuran Agregat Maksimum")
            mhb_ag_halus = self.get_float_entry("MHB Agregat Halus")
            berat_volume_ag_kasar_padat = self.get_float_entry("Berat Volume Ag. Kasar Padat")
            # ... (Lanjutkan untuk semua input)
            sg_semen = self.get_float_entry("SG Semen")
            sg_ag_kasar = self.get_float_entry("SG Agregat Kasar")
            sg_ag_halus = self.get_float_entry("SG Agregat Halus")
            kadar_air_ag_kasar = self.get_float_entry("Kadar Air Ag. Kasar", True)
            kadar_air_ag_halus = self.get_float_entry("Kadar Air Ag. Halus", True)
            absorpsi_ag_kasar = self.get_float_entry("Absorpsi Air Ag. Kasar", True)
            absorpsi_ag_halus = self.get_float_entry("Absorpsi Air Ag. Halus", True)


            if None in [f_c_rencana, S_s, slump_min, slump_maks, ukuran_agregat_maks, mhb_ag_halus, 
                         berat_volume_ag_kasar_padat, sg_semen, sg_ag_kasar, sg_ag_halus,
                         kadar_air_ag_kasar, kadar_air_ag_halus, absorpsi_ag_kasar, absorpsi_ag_halus]:
                return

            slump_pilih_tengah = (slump_min + slump_maks) / 2
            self.log_to_gui_styled("--- MULAI PERHITUNGAN MIX DESIGN BETON NORMAL ---", "header_main")
            
            # Langkah 1 & 2
            self.log_to_gui_styled("LANGKAH 1 & 2: INPUT DATA AWAL", "subheader_step", 0)
            self.log_to_gui_styled(f"1. Kuat tekan beton rencana (f_c'): {f_c_rencana} MPa", indent_level=1)
            self.log_to_gui_styled(f"2. Deviasi standar (S_s): {S_s} MPa", indent_level=1)

            # Langkah 3
            self.log_to_gui_styled("LANGKAH 3: Menghitung Kuat Tekan Beton Rata-rata (f_cr')", "subheader_step", 0)
            f_cr_rencana, f_cr_1_val, f_cr_2_val = hitung_f_cr(f_c_rencana, S_s)
            self.log_equation_natural_format("Formula 1", "f_cr'(1)", ["f_c'", "+", "1.34", "*", "S_s"],
                                             [f_c_rencana, "+", 1.34, "*", S_s], f_cr_1_val, "MPa")
            self.log_equation_natural_format("Formula 2", "f_cr'(2)", ["f_c'", "+", "2.33", "*", "S_s", "-", "3.5"],
                                             [f_c_rencana, "+", 2.33, "*", S_s, "-", 3.5], f_cr_2_val, "MPa")
            self.log_to_gui_styled(f"Digunakan f_cr' terbesar = {f_cr_rencana:.2f} MPa", "result_value_step", 1)


            # Langkah 4 & 5
            self.log_to_gui_styled(f"LANGKAH 4: Nilai slump rencana: {slump_min:.0f}-{slump_maks:.0f} mm", "subheader_step", 0)
            self.log_to_gui_styled(f"LANGKAH 5: Ukuran agregat maksimum: {ukuran_agregat_maks} mm", "subheader_step", 0)
            
            # Langkah 6: Air dan Udara
            self.log_to_gui_styled("LANGKAH 6: Perkiraan Air Pencampur dan Kandungan Udara", "subheader_step", 0)
            # ... (Proses interpolasi/ekstrapolasi dengan logging detail menggunakan fungsi baru)
            slump_key_pilihan = None
            for slump_range_key_iter in tabel_kebutuhan_air_udara[19].keys(): 
                if slump_range_key_iter[0] <= slump_pilih_tengah <= slump_range_key_iter[1]:
                    slump_key_pilihan = slump_range_key_iter
                    break
            if slump_key_pilihan is None: slump_key_pilihan = (25,50) 
            self.log_to_gui_styled(f"Menggunakan data slump untuk rentang: {slump_key_pilihan} mm", indent_level=1)
            ukuran_agg_data_air_udara = sorted(tabel_kebutuhan_air_udara.keys())
            air_data_untuk_slump_list = [tabel_kebutuhan_air_udara[k][slump_key_pilihan][0] for k in ukuran_agg_data_air_udara if slump_key_pilihan in tabel_kebutuhan_air_udara[k]]
            udara_data_untuk_slump_list = [tabel_kebutuhan_air_udara[k][slump_key_pilihan][1] for k in ukuran_agg_data_air_udara if slump_key_pilihan in tabel_kebutuhan_air_udara[k]]
            ukuran_agg_data_air_udara_filtered_list = [k for k in ukuran_agg_data_air_udara if slump_key_pilihan in tabel_kebutuhan_air_udara[k]]
            air_pencampur = interpolasi_ekstrapolasi_natural(ukuran_agregat_maks, ukuran_agg_data_air_udara_filtered_list, air_data_untuk_slump_list, "Ukuran Agregat", "Air Pencampur", self.output_text)
            kandungan_udara = interpolasi_ekstrapolasi_natural(ukuran_agregat_maks, ukuran_agg_data_air_udara_filtered_list, udara_data_untuk_slump_list, "Ukuran Agregat", "Kandungan Udara", self.output_text)
            air_pencampur = round(air_pencampur, 2)
            kandungan_udara = round(kandungan_udara, 2)
            self.log_to_gui_styled(f"Hasil: Banyaknya air pencampur = {air_pencampur} kg/m³", "result_value_step", 1)
            self.log_to_gui_styled(f"Hasil: Banyaknya udara dalam beton = {kandungan_udara}%", "result_value_step", 1)

            # Langkah 7: FAS
            self.log_to_gui_styled("LANGKAH 7: Menetapkan Nilai Faktor Air Semen (FAS)", "subheader_step", 0)
            fcr_data_fas_list = sorted(tabel_fas.keys()) 
            fas_data_sorted_list = [tabel_fas[k] for k in fcr_data_fas_list] 
            fas_calc = interpolasi_ekstrapolasi_natural(f_cr_rencana, fcr_data_fas_list, fas_data_sorted_list, "f_cr'", "FAS", self.output_text)
            fas_calc = round(fas_calc, 2)
            self.log_to_gui_styled(f"Hasil: Faktor Air Semen (FAS) = {fas_calc}", "result_value_step", 1)


            # Langkah 8: Kebutuhan Semen
            self.log_to_gui_styled("LANGKAH 8: Menghitung Kebutuhan Semen", "subheader_step", 0)
            kebutuhan_semen_total = air_pencampur / fas_calc
            self.log_equation_natural_format("Perhitungan", "Kebutuhan Semen", ["Air Pencampur", "/", "FAS"],
                                             [air_pencampur, "/", fas_calc], kebutuhan_semen_total, "kg/m³")
            kebutuhan_semen_total = round(kebutuhan_semen_total, 2)
            self.log_to_gui_styled(f"Hasil: Kebutuhan semen = {kebutuhan_semen_total} kg/m³", "result_value_step", 1)


            # Langkah 9: Agregat Kasar
            self.log_to_gui_styled("LANGKAH 9: Menentukan Kebutuhan Agregat Kasar", "subheader_step", 0)
            # ... (Logika interpolasi Agregat Kasar dengan logging detail)
            ukuran_agg_data_vol_list = sorted(tabel_volume_ag_kasar.keys())
            mhb_data_vol_list = sorted(tabel_volume_ag_kasar[ukuran_agg_data_vol_list[0]].keys())
            self.log_to_gui_styled(f"Proses Interpolasi Volume Agregat Kasar:", "equation_general", 1)
            vol_prop_interp_mhb_list = []
            for mhb_val_iter in mhb_data_vol_list:
                y_values_for_mhb_list = [tabel_volume_ag_kasar[k_agg][mhb_val_iter] for k_agg in ukuran_agg_data_vol_list]
                self.log_to_gui_styled(f"  Untuk MHB {mhb_val_iter}:", "equation_general", 2)
                interp_val = interpolasi_ekstrapolasi_natural(ukuran_agregat_maks, ukuran_agg_data_vol_list, y_values_for_mhb_list, "Ukuran Agregat", f"Vol. Prop. @MHB {mhb_val_iter}", self.output_text)
                vol_prop_interp_mhb_list.append(interp_val)
            self.log_to_gui_styled(f"  Nilai Vol. Prop. terinterpolasi untuk ukuran agregat {ukuran_agregat_maks}mm pada berbagai MHB: { [round(v,4) for v in vol_prop_interp_mhb_list] }", "equation_general", 1)
            self.log_to_gui_styled(f"  Interpolasi akhir untuk MHB aktual ({mhb_ag_halus}):", "equation_general", 1)
            volume_ag_kasar_kering_prop_calc = interpolasi_ekstrapolasi_natural(mhb_ag_halus, mhb_data_vol_list, vol_prop_interp_mhb_list, "MHB Ag. Halus", "Volume Ag. Kasar Prop.", self.output_text)
            volume_ag_kasar_kering_prop_calc = round(volume_ag_kasar_kering_prop_calc, 3)
            self.log_to_gui_styled(f"Hasil: Volume agregat kasar kering per satuan volume beton = {volume_ag_kasar_kering_prop_calc} m³", "result_value_step", 1)
            berat_ag_kasar_kering_calc = volume_ag_kasar_kering_prop_calc * berat_volume_ag_kasar_padat
            self.log_equation_natural_format("Perhitungan Berat Ag. Kasar Kering", "Berat Ag.Kasar Kering", ["Volume Proporsi", "*", "Berat Volume Padat"],
                                             [volume_ag_kasar_kering_prop_calc, "*", berat_volume_ag_kasar_padat], berat_ag_kasar_kering_calc, "kg/m³")
            berat_ag_kasar_kering_calc = round(berat_ag_kasar_kering_calc, 2)
            self.log_to_gui_styled(f"Hasil: Berat kering agregat kasar = {berat_ag_kasar_kering_calc} kg/m³", "result_value_step", 1)


            # Langkah 10: Agregat Halus
            self.log_to_gui_styled("LANGKAH 10: Menentukan Kebutuhan Agregat Halus (Metode Perkiraan Berat Beton)", "subheader_step", 0)
             # ... (Logika interpolasi Berat Beton Segar dengan logging detail)
            ukuran_agg_data_berat_list = sorted(tabel_berat_beton_segar.keys())
            berat_beton_data_list = [tabel_berat_beton_segar[k] for k in ukuran_agg_data_berat_list]
            perkiraan_berat_beton_calc = interpolasi_ekstrapolasi_natural(ukuran_agregat_maks, ukuran_agg_data_berat_list, berat_beton_data_list, "Ukuran Agregat", "Perkiraan Berat Beton", self.output_text)
            perkiraan_berat_beton_calc = round(perkiraan_berat_beton_calc, 1)
            self.log_to_gui_styled(f"Hasil: Perkiraan berat beton segar = {perkiraan_berat_beton_calc} kg/m³", "result_value_step", 1)
            berat_total_non_ag_halus_calc = air_pencampur + kebutuhan_semen_total + berat_ag_kasar_kering_calc
            berat_total_non_ag_halus_calc = round(berat_total_non_ag_halus_calc, 2)
            self.log_equation_natural_format("Perhitungan Berat Total (Non Ag. Halus)", "Berat Total Non Ag.Halus", ["Air", "+", "Semen", "+", "Ag. Kasar Kering"],
                                             [air_pencampur, "+", kebutuhan_semen_total, "+", berat_ag_kasar_kering_calc], berat_total_non_ag_halus_calc, "kg")
            berat_ag_halus_kering_calc = perkiraan_berat_beton_calc - berat_total_non_ag_halus_calc
            self.log_equation_natural_format("Perhitungan Massa Ag. Halus Kering", "Massa Ag.Halus Kering", ["Perk. Berat Beton", "-", "Berat Total Non Ag.Halus"],
                                             [perkiraan_berat_beton_calc, "-", berat_total_non_ag_halus_calc], berat_ag_halus_kering_calc, "kg/m³")
            berat_ag_halus_kering_calc = round(berat_ag_halus_kering_calc, 2)
            self.log_to_gui_styled(f"Hasil: Massa (berat) agregat halus kering = {berat_ag_halus_kering_calc} kg/m³", "result_value_step", 1)

            # Langkah 11: Koreksi
            self.log_to_gui_styled("LANGKAH 11: Koreksi terhadap Kondisi Bahan (Beton Normal)", "subheader_step", 0)
            # ... (Perhitungan dan log detail untuk Langkah 11 tanpa substitusi)
            berat_ag_kasar_basah_calc = round(berat_ag_kasar_kering_calc * (1 + kadar_air_ag_kasar), 2)
            self.log_equation_natural_format("Perhitungan Ag. Kasar Basah", "Ag.Kasar Basah", ["Berat Kering AK", "*", "(1 + Kadar Air AK)"],
                                             [berat_ag_kasar_kering_calc, "*", f"(1 + {kadar_air_ag_kasar:.4f})"], berat_ag_kasar_basah_calc, "kg")
            
            berat_ag_halus_basah_calc_normal = round(berat_ag_halus_kering_calc * (1 + kadar_air_ag_halus), 2) 
            self.log_equation_natural_format("Perhitungan Ag. Halus Basah", "Ag.Halus Basah", ["Berat Kering AH", "*", "(1 + Kadar Air AH)"],
                                             [berat_ag_halus_kering_calc, "*", f"(1 + {kadar_air_ag_halus:.4f})"], berat_ag_halus_basah_calc_normal, "kg")

            air_permukaan_ag_kasar_persen_calc = kadar_air_ag_kasar - absorpsi_ag_kasar
            air_permukaan_ag_halus_persen_calc = kadar_air_ag_halus - absorpsi_ag_halus
            self.log_equation_natural_format("Perhitungan Air Permukaan Ag. Kasar", "Air Perm. AK (%)", ["Kadar Air AK", "-", "Absorpsi AK"],
                                             [kadar_air_ag_kasar*100, "-", absorpsi_ag_kasar*100], air_permukaan_ag_kasar_persen_calc*100, "%")
            self.log_equation_natural_format("Perhitungan Air Permukaan Ag. Halus", "Air Perm. AH (%)", ["Kadar Air AH", "-", "Absorpsi AH"],
                                             [kadar_air_ag_halus*100, "-", absorpsi_ag_halus*100], air_permukaan_ag_halus_persen_calc*100, "%")

            koreksi_air_ag_kasar_calc = berat_ag_kasar_kering_calc * air_permukaan_ag_kasar_persen_calc
            koreksi_air_ag_halus_calc = berat_ag_halus_kering_calc * air_permukaan_ag_halus_persen_calc
            
            air_awal_koreksi_calc = air_pencampur 
            air_ditambahkan_dikoreksi_normal_calc = air_awal_koreksi_calc - koreksi_air_ag_kasar_calc - koreksi_air_ag_halus_calc
            self.log_to_gui_styled("  Perhitungan Air Ditambahkan (Dikoreksi):", "subheader_calc",1)
            self.log_to_gui_styled(f"    Air Ditambahkan = Air Awal - (Berat AK Kering * Air Perm. AK) - (Berat AH Kering * Air Perm. AH)", "equation_general", 2)
            self.log_to_gui_styled(f"                    = {air_awal_koreksi_calc:.2f} - ({berat_ag_kasar_kering_calc:.2f} * {air_permukaan_ag_kasar_persen_calc:.5f}) - ({berat_ag_halus_kering_calc:.2f} * {air_permukaan_ag_halus_persen_calc:.5f})", "equation_detail", 2)
            self.log_to_gui_styled(f"                    = {air_awal_koreksi_calc:.2f} - {koreksi_air_ag_kasar_calc:.4f} - {koreksi_air_ag_halus_calc:.4f} = {air_ditambahkan_dikoreksi_normal_calc:.4f} kg", "equation_detail", 2)
            air_ditambahkan_dikoreksi_normal_calc = round(air_ditambahkan_dikoreksi_normal_calc, 2)
            self.log_to_gui_styled(f"Hasil: Kebutuhan air ditambahkan (dikoreksi) = {air_ditambahkan_dikoreksi_normal_calc} kg", "result_value_step",1)
            

            # Komposisi Akhir Beton Normal
            self.log_to_gui_styled("----------------------------------------------------------------------", "final_header_summary")
            self.log_to_gui_styled(f"KOMPOSISI BAHAN UNTUK 1 m³ BETON NORMAL (TARGET f_c'={f_c_rencana} MPa)", "final_header_summary")
            self.log_to_gui_styled("----------------------------------------------------------------------", "final_header_summary")
            self.log_to_gui_styled(f"{'Air':<25}: {air_ditambahkan_dikoreksi_normal_calc:>10.2f} kg", "final_komposisi_summary")
            self.log_to_gui_styled(f"{'Semen':<25}: {kebutuhan_semen_total:>10.2f} kg", "final_komposisi_summary")
            self.log_to_gui_styled(f"{'Agregat Kasar (Basah)':<25}: {berat_ag_kasar_basah_calc:>10.2f} kg", "final_komposisi_summary")
            self.log_to_gui_styled(f"{'Agregat Halus (Basah)':<25}: {berat_ag_halus_basah_calc_normal:>10.2f} kg", "final_komposisi_summary")
            total_final_normal = air_ditambahkan_dikoreksi_normal_calc + kebutuhan_semen_total + \
                                 berat_ag_kasar_basah_calc + berat_ag_halus_basah_calc_normal
            self.log_to_gui_styled("----------------------------------------------------", "final_komposisi_summary")
            self.log_to_gui_styled(f"{'TOTAL':<25}: {round(total_final_normal, 2):>10.2f} kg", "final_komposisi_summary")
            self.log_to_gui_styled("----------------------------------------------------", "final_komposisi_summary")
            self.log_to_gui_styled("\nPerhitungan Beton Normal Selesai.")

        except ValueError as e:
            messagebox.showerror("Error Perhitungan", str(e))
            self.log_to_gui_styled(f"Error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error Tak Terduga", f"Terjadi kesalahan: {str(e)}")
            self.log_to_gui_styled(f"Error tak terduga: {str(e)}")


if __name__ == '__main__':
    main_root_normal_gui_natural = tk.Tk()
    app_normal_gui_natural = MixDesignAppNormalGUI_Natural(main_root_normal_gui_natural)
    main_root_normal_gui_natural.mainloop()