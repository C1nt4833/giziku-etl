def transform_akg_data(raw_data):
    """
    LOGIKA TRANSFORM AKG DATA - CRITICAL BUSINESS LOGIC!
    
    Tahapan transform:
    1. Hitung total gizi untuk Hamil/Menyusui (Nilai Dasar + Tambahan)
    2. Hapus kolom yang tidak relevan (Gula, Kolesterol, Waktu_Makan)
    3. Standardize nama kolom untuk output
    
    PENTING:
    - base_ref (Perempuan 19-29 tahun) adalah REFERENCE untuk hamil/menyusui
    - Jika data hamil/menyusui hilang di input, calculate_total akan gunakan base
    - Jika base_ref tidak ada -> return None untuk item tersebut (safety)
    - Output columns harus KONSISTEN dengan sheet definition
    """
    
    # CRITICAL: Cari reference dasar (Perempuan 19-29) untuk penjumlahan hamil/menyusui
    # Jika tidak ada -> None, dan calculate_total akan handle gracefully
    base_ref = next(
        (item for item in raw_data if item['label'] == "19-29 tahun" and item['kategori'] == "Perempuan"), 
        None
    )

    transformed_data = []

    for item in raw_data:
        # LOGIC: Hamil/Menyusui ada nilai TAMBAHAN, bukan nilai final
        # Nilai final = Base (Perempuan 19-29) + Tambahan (dari web)
        is_additional = item['kategori'] in ["Hamil", "Menyusui"]
        
        def calculate_total(key):
            """
            Helper untuk hitung nutrisi dengan atau tanpa penjumlahan base.
            
            Untuk Hamil/Menyusui:
            - return base_ref[key] + item[key] (Dasar + Tambahan)
            
            Untuk kategori normal:
            - return item[key] (nilai langsung dari web)
            """
            val = item.get(key, 0.0)
            if is_additional and base_ref:
                # Hamil/Menyusui: tambahkan ke base reference
                return base_ref.get(key, 0.0) + val
            return val

        # Standardize column names untuk output
        refined_item = {
            "Kategori": item['kategori'],
            "Label_Umur_Kondisi": item['label'],
            "Energi (kkal)": calculate_total("energi"),
            "Protein (g)": calculate_total("protein"),
            "Karbohidrat (g)": calculate_total("karbohidrat"),
            "Lemak (g)": calculate_total("lemak"),
            "Serat (g)": calculate_total("serat"),
            "Natrium (mg)": calculate_total("natrium"),
            "Air (ml)": calculate_total("air")
        }
        
        transformed_data.append(refined_item)
    
    return transformed_data

