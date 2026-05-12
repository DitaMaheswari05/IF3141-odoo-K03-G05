import random
from datetime import date, timedelta

# Konfigurasi
TOTAL_PRODUK = 100
TOTAL_PROMO = 100
TOTAL_TRANSAKSI = 100
TOTAL_LAPORAN = 100
TOTAL_REKAP = 100

START_DATE = date(2026, 1, 1)

def write_xml(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<odoo>\n    <data noupdate="1">\n\n')
        f.write(content)
        f.write('\n    </data>\n</odoo>')
    print(f"File {filename} berhasil dibuat!")

# ==========================================
# 1. GENERATE PRODUK (100 Data)
# ==========================================
produk_xml = ""
for i in range(1, TOTAL_PRODUK + 1):
    divisi = "bar" if i <= 50 else "kitchen"
    tipe_nama = "Minuman" if divisi == "bar" else "Makanan"
    harga_jual = random.randint(15, 60) * 1000
    hpp = int(harga_jual * random.uniform(0.3, 0.5))
    
    produk_xml += f"""
        <record id="produk_demo_{i}" model="plumeria.produk">
            <field name="nama_produk">{tipe_nama} Spesial {i}</field>
            <field name="divisi">{divisi}</field>
            <field name="harga_jual">{harga_jual}</field>
            <field name="hpp">{hpp}</field>
            <field name="status_aktif">True</field>
        </record>"""
write_xml("demo_produk.xml", produk_xml)

# ==========================================
# 2. GENERATE PROMO (100 Data)
# ==========================================
promo_xml = ""
for i in range(1, TOTAL_PROMO + 1):
    jenis = random.choice(['persentase', 'nominal'])
    nilai = random.randint(5, 30) if jenis == 'persentase' else random.randint(5, 20) * 1000
    p_mulai = START_DATE + timedelta(days=random.randint(0, 100))
    p_selesai = p_mulai + timedelta(days=random.randint(5, 30))
    
    # Pilih 3 produk acak untuk promo ini
    prod_ids = random.sample(range(1, TOTAL_PRODUK + 1), 3)
    eval_str = f"[(4, ref('produk_demo_{prod_ids[0]}')), (4, ref('produk_demo_{prod_ids[1]}')), (4, ref('produk_demo_{prod_ids[2]}'))]"
    
    promo_xml += f"""
        <record id="promo_demo_{i}" model="plumeria.promo">
            <field name="nama_promo">Promo Meriah {i}</field>
            <field name="kode_promo">PROMO{i:03d}</field>
            <field name="periode_mulai">{p_mulai}</field>
            <field name="periode_selesai">{p_selesai}</field>
            <field name="jenis_diskon">{jenis}</field>
            <field name="nilai_diskon">{nilai}</field>
            <field name="aktif">True</field>
            <field name="produk_ids" eval="{eval_str}"/>
        </record>"""
write_xml("demo_promo.xml", promo_xml)

# ==========================================
# 3. GENERATE TRANSAKSI POS (100 Data)
# ==========================================
transaksi_xml = ""
metode = ['tunai', 'qris', 'debit']
for i in range(1, TOTAL_TRANSAKSI + 1):
    divisi = random.choice(['bar', 'kitchen'])
    tgl_trx = START_DATE + timedelta(days=i%30, hours=random.randint(8, 20), minutes=random.randint(0, 59))
    met = random.choice(metode)
    
    transaksi_xml += f"""
        <record id="trx_demo_{i}" model="plumeria.transaksi.pos">
            <field name="id_transaksi">POS-DEMO-{2026000+i}</field>
            <field name="waktu_transaksi">{tgl_trx.strftime('%Y-%m-%d %H:%M:%S')}</field>
            <field name="divisi">{divisi}</field>
            <field name="metode_pembayaran">{met}</field>
        </record>"""
    
    # Generate 2 Detail Transaksi per POS
    for j in range(1, 3):
        # Sesuaikan rentang produk dengan divisi
        prod_id = random.randint(1, 50) if divisi == 'bar' else random.randint(51, 100)
        qty = random.randint(1, 4)
        harga = random.randint(15, 60) * 1000
        
        transaksi_xml += f"""
        <record id="det_trx_{i}_{j}" model="plumeria.detail.transaksi">
            <field name="transaksi_id" ref="trx_demo_{i}"/>
            <field name="produk_id" ref="produk_demo_{prod_id}"/>
            <field name="jumlah">{qty}</field>
            <field name="harga_satuan">{harga}</field>
        </record>"""
write_xml("demo_transaksi.xml", transaksi_xml)

# ==========================================
# 4. GENERATE LAPORAN OPERASIONAL (100 Data)
# ==========================================
laporan_xml = ""
states = ['draft', 'submitted', 'approved', 'archived']
for i in range(1, TOTAL_LAPORAN + 1):
    divisi = "bar" if i % 2 == 0 else "kitchen"
    tgl_lap = START_DATE + timedelta(days=i//2)
    pendapatan = random.randint(300, 1500) * 1000
    hpp = int(pendapatan * random.uniform(0.3, 0.4))
    beban = random.randint(30, 100) * 1000
    met = random.choice(['tunai', 'qris', 'debit', 'campuran'])
    st = random.choice(states)
    
    laporan_xml += f"""
        <record id="lap_demo_{i}" model="plumeria.laporan.operasional">
            <field name="nomor_referensi">LAP/DEMO/{i:04d}</field>
            <field name="tanggal">{tgl_lap}</field>
            <field name="divisi">{divisi}</field>
            <field name="total_pendapatan">{pendapatan}</field>
            <field name="jumlah_transaksi">{random.randint(10, 50)}</field>
            <field name="metode_pembayaran">{met}</field>
            <field name="hpp">{hpp}</field>
            <field name="beban_operasional">{beban}</field>
            <field name="catatan_kendala">Operasional berjalan lancar (Seeder {i})</field>
            <field name="state">{st}</field>
        </record>"""
write_xml("demo_laporan.xml", laporan_xml)

# ==========================================
# 5. GENERATE REKAP KEUANGAN (100 Data)
# ==========================================
rekap_xml = ""
for i in range(1, TOTAL_REKAP + 1):
    divisi = "bar" if i % 2 == 0 else "kitchen"
    tgl_rekap = START_DATE + timedelta(days=i//2)
    total_kas = random.randint(300, 1500) * 1000
    
    # Sengaja membuat 20% data memiliki selisih untuk testing
    ada_selisih = random.random() < 0.2
    total_pos = total_kas + (random.choice([-15000, 20000]) if ada_selisih else 0)
    catatan = "Ada selisih kas" if ada_selisih else "Sesuai."
    
    laporan_ref = f"lap_demo_{i}"
    
    rekap_xml += f"""
        <record id="rekap_demo_{i}" model="plumeria.rekap.keuangan">
            <field name="tanggal">{tgl_rekap}</field>
            <field name="divisi">{divisi}</field>
            <field name="total_kas">{total_kas}</field>
            <field name="total_pos">{total_pos}</field>
            <field name="catatan">{catatan}</field>
            <field name="laporan_ids" eval="[(4, ref('{laporan_ref}'))]"/>
        </record>"""
write_xml("demo_rekap.xml", rekap_xml)