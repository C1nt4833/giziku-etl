def transform_akg_data(raw_data):
    def get_base_ref(target_label="19-29 tahun"):
        return next(
            (item for item in raw_data if item['label'] == target_label and item['kategori'] == "Perempuan"), 
            None
        )

    transformed_data = []
    default_base = get_base_ref()

    for item in raw_data:
        is_additional = item['kategori'] in ["Hamil", "Menyusui"]
        
        def calculate_total(key):
            # Ambil nilai tambahan dari scraping (misal: 180.0 atau 0.5)
            val = item.get(key, 0.0)
            
            if is_additional and default_base:
                # Ambil nilai dasar perempuan dewasa (misal: 2250.0)
                base_val = default_base.get(key, 0.0)
                # Kembalikan hasil penjumlahan (2250 + 180 = 2430)
                return base_val + val
            return val

        refined_item = {
            "Kategori": item['kategori'],
            "Label_Umur_Kondisi": item['label'],
            "Energi (kkal)": calculate_total("energi"),
            "Protein (g)": calculate_total("protein"),
            "Lemak (g)": calculate_total("lemak"),
            "Lemak Omega 6 (g)": calculate_total("lemak_omega6"), 
            "Lemak Omega 3 (g)": calculate_total("lemak_omega3"), 
            "Karbohidrat (g)": calculate_total("karbohidrat"),
            "Serat (g)": calculate_total("serat"),
            "Natrium (mg)": calculate_total("natrium"),
            "Air (ml)": calculate_total("air"),
            "Is_Additional_Data": is_additional 
        }
        transformed_data.append(refined_item)
    
    return transformed_data
