import os
import sys
import getpass
import datetime
import random
import msvcrt
from tabulate import tabulate
import psycopg2
from colorama import Fore

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "finald", 
    "user": "postgres",
    "password": "DiegoVA86",  
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

def exec_fetchall(query, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def exec_fetchone(query, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def exec_commit(query, params=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

def format_rp(n):
    try:
        s = f"{int(n):,}".replace(",", ".")
        return f"Rp {s}"
    except:
        return str(n)

def pause():
    input("\nTekan ENTER untuk kembali...")

def get_password_with_cursor(prompt="Password : "):
    print(prompt, end='', flush=True)
    password = ''

    while True:
        ch = msvcrt.getch()
        if ch in [b'\r', b'\n']: 
            print()
            break
        elif ch == b'\x08':  
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        elif ch == b'\x03': 
            raise KeyboardInterrupt
        else:
            password += ch.decode('utf-8', errors='ignore')
            print('*', end='', flush=True)

    return password

def cover(b=107):
    garis = ("=" * b)
    print(garis)
    print(Fore.BLUE)
    print("       █████████     █████████  ███████████      ███████    █████   ████    ███████    ███████████  █████    ".center(b))
    print("      ███░░░░░███   ███░░░░░███░░███░░░░░███   ███░░░░░███ ░░███   ███░   ███░░░░░███ ░░███░░░░░███░░███     ".center(b))
    print("     ░███    ░███  ███     ░░░  ░███    ░███  ███     ░░███ ░███  ███    ███     ░░███ ░███    ░███ ░███     ".center(b)) 
    print("     ░███████████ ░███          ░██████████  ░███      ░███ ░███████    ░███      ░███ ░██████████  ░███     ".center(b))
    print("     ░███░░░░░███ ░███    █████ ░███░░░░░███ ░███      ░███ ░███░░███   ░███      ░███ ░███░░░░░░   ░███     ".center(b))
    print("     ░███    ░███ ░░███  ░░███  ░███    ░███ ░░███     ███  ░███ ░░███  ░░███     ███  ░███         ░███     ".center(b))
    print("     █████   █████ ░░█████████  █████   █████ ░░░███████░   █████ ░░████ ░░░███████░   █████        █████    ".center(b))
    print("     ░░░░░   ░░░░░   ░░░░░░░░░  ░░░░░   ░░░░░    ░░░░░░░    ░░░░░   ░░░░    ░░░░░░░    ░░░░░        ░░░░░    ".center(b))
    print(Fore.WHITE)
    print(garis)         

def register_user():
    while True:
        clear_screen()
        print("=== REGISTER (Pelanggan) ===\n")
     
        while True:
            nama = input("Nama lengkap : ").strip()
            if not nama:
                clear_screen()
                print("Nama lengkap tidak boleh kosong. Silakan isi Nama lengkap.")
                continue
            else:
                break
        
        while True:
            email = input("Email : ").strip()
            if '@' not in email or '.' not in email:
                clear_screen()
                print("Email tidak valid. Silakan masukkan email yang benar.")
                continue
            else:
                break
        
        while True:
            pw = get_password_with_cursor()
            if not pw:
                clear_screen()
                print("Password tidak boleh kosong.")
                continue
            else:
                break

        while True:
            no_telp = input("No. telp : ").strip()
            if not no_telp:
                clear_screen()
                print("Nomor Telepon tidak boleh kosong")
                continue
            else:
                break
        
        while True:
            nama_jalan = input("Nama Jalan: ").strip()
            if not nama_jalan:
                clear_screen()
                print("Nama Jalan Tidak Boleh Kosong")
                continue
            else:
                break
       
        rows = exec_fetchall("SELECT id_kecamatan, nama_kecamatan FROM kecamatan ORDER BY id_kecamatan")
        clear_screen()
        print("=== Pilih Kecamatan ===\n")
        if rows:
            print(tabulate(rows, headers=["ID", "Kecamatan"], tablefmt="psql"))
        else:
            print("Belum ada data kecamatan pada database.")
       
        print("\n+-----------------------------+")
        print("| 9  | Tambah Kecamatan Baru  |")
        print("| 0  | Lewati                 |")
        print("+-----------------------------+\n")
      
        while True:
            pilih_raw = input("Masukkan ID kecamatan (atau 9/0): ").strip()
            clear_screen()
            if not pilih_raw:
                print("Input tidak boleh kosong. Silakan masukkan angka.")
                if rows:
                    print(tabulate(rows, headers=["ID","Kecamatan"], tablefmt="psql"))
                print("\n+-----------------------------+")
                print("| 9  | Tambah Kecamatan Baru  |")
                print("| 0  | Lewati                 |")
                print("+-----------------------------+\n")
                continue
            if not pilih_raw.isdigit():
                print("Input harus angka. Silakan coba lagi.")
                if rows:
                    print(tabulate(rows, headers=["ID","Kecamatan"], tablefmt="psql"))
                print("\n+-----------------------------+")
                print("| 9  | Tambah Kecamatan Baru  |")
                print("| 0  | Lewati                 |")
                print("+-----------------------------+\n")
                continue
            pilih = int(pilih_raw)
           
            if pilih == 0:
                if rows:
                    id_kec = rows[0][0]  
                else:
                    
                    exec_commit("INSERT INTO kecamatan (nama_kecamatan, kabupaten_id_kabupaten) VALUES (%s,%s)", ("Default", 1))
                    row = exec_fetchone("SELECT id_kecamatan FROM kecamatan ORDER BY id_kecamatan DESC LIMIT 1")
                    id_kec = row[0] if row else 1
                clear_screen()
                print("Pengisian kecamatan dilewati — menggunakan kecamatan default.")
                break

            if pilih == 9:
                nama_kec = input("Nama kecamatan baru : ").strip()
                if not nama_kec:
                    nama_kec = "Default"
                try:
                    exec_commit("INSERT INTO kecamatan (nama_kecamatan, kabupaten_id_kabupaten) VALUES (%s,%s)", (nama_kec, 1))
                    row = exec_fetchone("SELECT id_kecamatan FROM kecamatan WHERE nama_kecamatan=%s ORDER BY id_kecamatan DESC LIMIT 1", (nama_kec,))
                    id_kec = row[0] if row else 1
                    clear_screen()
                    print(f"Kecamatan '{nama_kec}' berhasil ditambahkan dan dipilih.")
                    break
                except Exception:
                    clear_screen()
                    print("Gagal menambahkan kecamatan. Coba lagi atau hubungi admin.")
                    continue
         
            valid_ids = [r[0] for r in rows] if rows else []
            if pilih in valid_ids:
                id_kec = pilih
                clear_screen()
                print(f"Kecamatan dengan ID {pilih} dipilih.")
                break
            else:
                clear_screen()
                print("ID kecamatan tidak tersedia. Silakan masukkan kembali.")
                if rows:
                    print(tabulate(rows, headers=["ID","Kecamatan"], tablefmt="psql"))
                print("\n+-----------------------------+")
                print("| 9  | Tambah Kecamatan Baru  |")
                print("| 0  | Lewati                 |")
                print("+-----------------------------+\n")
                continue
       
        try:
            exec_commit("""
                INSERT INTO users (nama_lengkap, no_telp, email, password, role_id_role, nama_jalan, kecamatan_id_kecamatan)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (nama, no_telp or None, email, pw, 3, nama_jalan or "", id_kec))
            clear_screen()
            print("\nRegistrasi berhasil.")
        except Exception as e:
            clear_screen()
            print("\nRegistrasi gagal. Periksa kembali input Anda.")
            print("Error (singkat):", str(e))
        pause()
        return

def login():
    clear_screen()
    print("=== LOGIN ===\n")
    email = input("Email : ").strip()
    pw = get_password_with_cursor()
    row = exec_fetchone("SELECT id_user, nama_lengkap, role_id_role, password FROM users WHERE email=%s", (email,))
    if not row:
        print("Akun tidak ditemukan.")
        pause(); return None
    if pw != row[3]:
        print("Password salah.")
        pause(); return None
    user = {"id": row[0], "nama": row[1], "role": row[2], "email": email}
    clear_screen()
    print(f"Login berhasil : {user['nama']}")
    pause()
    return user

def list_products():
    clear_screen()
    rows = exec_fetchall("SELECT id_produk, nama_produk, harga, stok FROM produk ORDER BY id_produk")
    print("=== DAFTAR PRODUK ===\n")
    if rows:
        print(tabulate(rows, headers=["ID","Nama","Harga (Rp)","Stok"], tablefmt="psql"))
    else:
        print("Tidak ada produk.")
    pause()

def katalog_menu():
    while True:
        clear_screen()
        print("-- Edit Katalog Produk --")
        print("1. Lihat produk")
        print("2. Tambah produk")
        print("3. Ubah produk")
        print("4. Hapus produk")
        print("5. Kembali")
        ch = input("Pilih: ").strip()
        if ch == "1":
            list_products()

        elif ch == "2":
            
            while True:
                clear_screen()
                nama = input("Nama produk: ").strip()
                if not nama:
                    print("Nama produk tidak boleh kosong.")
                    pause()
                    continue
                break
          
            while True:
                clear_screen()
                harga_s = input("Harga (integer): ").strip()
                try:
                    harga = int(harga_s)
                    if harga < 0:
                        print("Harga tidak boleh bernilai negatif. Silakan masukkan angka yang valid.")
                        pause()
                        continue
                    break
                except:
                    print("Harga tidak valid. Masukkan angka bulat (integer).")
                    pause()

            while True:
                clear_screen()
                stok_s = input("Stok (integer): ").strip()
                try:
                    stok = int(stok_s)
                    if stok < 0:
                        print("Stok tidak boleh bernilai negatif. Silakan masukkan angka yang valid.")
                        pause()
                        continue
                    break
                except:
                    print("Stok tidak valid. Masukkan angka bulat (integer).")
                    pause()

            rows = exec_fetchall("SELECT id_jenis_produk, nama_jenis FROM jenis_produk ORDER BY id_jenis_produk")
            if rows:
                clear_screen()
                print(tabulate(rows, headers=["ID","Jenis"], tablefmt="psql"))
                try:
                    jid = int(input("Pilih ID jenis produk: ").strip())
                except:
                    jid = 1
            else:
                jid = 1

            exec_commit("INSERT INTO produk (nama_produk, harga, stok, deskripsi, jenis_produk_id_jenis_produk) VALUES (%s,%s,%s,%s,%s)",
                        (nama, harga, stok, "", jid))
            clear_screen()
            print("Produk berhasil ditambahkan.")
            pause()

        elif ch == "3":
            
            while True:
                clear_screen()
                rows = exec_fetchall("SELECT id_produk, nama_produk, harga, stok FROM produk ORDER BY id_produk")
                if not rows:
                    print("Tidak ada produk.")
                    pause(); break
                print(tabulate(rows, headers=["ID","Nama","Harga","Stok"], tablefmt="psql"))
                pid_raw = input("Pilih ID produk: ").strip()
                if not pid_raw:
                    print("Input tidak boleh kosong.")
                    pause(); continue
                try:
                    pid = int(pid_raw)
                except:
                    print("Input tidak valid.")
                    pause(); continue
                ids = [r[0] for r in rows]
                if pid not in ids:
                    print("Produk tidak ditemukan.")
                    pause(); continue
                break
            
            clear_screen()
            nama_baru = input("Nama baru (kosong = tetap): ").strip()
            if nama_baru:
                exec_commit("UPDATE produk SET nama_produk=%s WHERE id_produk=%s", (nama_baru, pid))
            
            while True:
                clear_screen()
                harga_s = input("Harga baru (kosong = tetap): ").strip()
                if not harga_s:
                    break
                try:
                    harga_val = int(harga_s)
                    if harga_val < 0:
                        print("Harga tidak boleh bernilai negatif. Silakan masukkan angka yang valid.")
                        pause()
                        continue
                    exec_commit("UPDATE produk SET harga=%s WHERE id_produk=%s", (harga_val, pid))
                    break
                except:
                    print("Harga tidak valid. Masukkan angka bulat (integer).")
                    pause()
           
            while True:
                clear_screen()
                stok_s = input("Stok baru (kosong = tetap): ").strip()
                if not stok_s:
                    break
                try:
                    stok_val = int(stok_s)
                    if stok_val < 0:
                        print("Stok tidak boleh bernilai negatif. Silakan masukkan angka yang valid.")
                        pause()
                        continue
                    exec_commit("UPDATE produk SET stok=%s WHERE id_produk=%s", (stok_val, pid))
                    break
                except:
                    print("Stok tidak valid. Masukkan angka bulat (integer).")
                    pause()

            clear_screen()
            print("Update produk selesai.")
            pause()

        elif ch == "4":
            clear_screen()
            rows = exec_fetchall("SELECT id_produk, nama_produk FROM produk ORDER BY id_produk")
            print(tabulate(rows, headers=["ID","Nama"], tablefmt="psql"))
            try:
                pid = int(input("ID produk dihapus: ").strip())
            except:
                print("Input invalid"); pause(); continue
            confirm = input(f"Yakin hapus produk ID {pid}? (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    exec_commit("DELETE FROM produk WHERE id_produk=%s",(pid,))
                    print("Produk dihapus.")
                except Exception:
                    print("Gagal menghapus produk.")
            pause()
        else:
            return

def choose_karyawan_loop():
    rows = exec_fetchall("SELECT id_user, nama_lengkap FROM users WHERE role_id_role = %s ORDER BY id_user", (2,))
    if not rows:
        return None
    while True:
        clear_screen()
        print("\n== Daftar Karyawan ==")
        print(tabulate(rows, headers=["ID","Nama"], tablefmt="psql"))
        raw = input("Pilih ID karyawan yang melayani (kosong=batalkan): ").strip()
        if not raw:
            return None
        try:
            kp = int(raw)
            valid_ids = [r[0] for r in rows]
            if kp in valid_ids:
                return kp
            else:
                print("ID tidak valid, coba lagi.")
                pause()
        except:
            print("Input tidak valid, coba lagi.")
            pause()

def create_transaction(user):
    clear_screen()
    if not user or user.get("role") != 3:
        print("Fitur ini hanya untuk pelanggan.")
        pause(); return

    basket = []
    while True:
        clear_screen()
        rows = exec_fetchall("SELECT id_produk, nama_produk, harga, stok FROM produk ORDER BY id_produk")
        if not rows:
            print("Tidak ada produk.")
            pause(); return
        print("\n=== PILIH PRODUK ===")
        print(tabulate(rows, headers=["ID","Nama","Harga (Rp)","Stok"], tablefmt="psql"))
        try:
            pid_raw = input("Pilih ID produk : ").strip()
            pid = int(pid_raw)
        except:
            print("Input salah."); pause(); continue

        ids = [r[0] for r in rows]
        if pid not in ids:
            print("Produk tidak ditemukan."); pause(); continue

        prod = next((r for r in rows if r[0]==pid), None)
        if not prod:
            print("Produk tidak ditemukan."); pause(); continue
    
        while True:
            try:
                gram_raw = input("Jumlah (satuan unit, misal gram/pcs): ").strip()
                gram = int(gram_raw)
                if gram <= 0:
                    print("Jumlah harus > 0."); pause(); continue
                if gram > prod[3]:
                    print(f"Stok tidak cukup (stok: {prod[3]})."); pause(); continue
                break
            except:
                print("Input salah, coba lagi."); pause()
        basket.append({"id": pid, "name": prod[1], "price": prod[2], "qty": gram})

        more = input("Tambah produk lain? (y/n): ").strip().lower()
        if more != "y":
            break

    karyawan_id = choose_karyawan_loop()
    if not karyawan_id:
        print("Tidak ada karyawan dipilih. Transaksi dibatalkan.")
        pause(); return

    row_k = exec_fetchone("SELECT nama_lengkap FROM users WHERE id_user=%s", (karyawan_id,))
    nama_karyawan = row_k[0] if row_k else "N/A"

    tanggal = datetime.date.today()
    total = sum(it["price"] * it["qty"] for it in basket)
    preview_status = random.choices(["Berhasil","Gagal"], weights=[90,10])[0]

    clear_screen()
    print("="*60)
    print(" " * 18 + "NOTA PEMBELIAN (PREVIEW)")
    print("="*60)
    print(f"Tanggal       : {tanggal}")
    print(f"Nama Pelanggan: {user.get('nama')}")
    print(f"Dilayani oleh : {nama_karyawan}")
    print("-"*60)
    for i,it in enumerate(basket, start=1):
        print(f"{i}. {it['name']} - {it['qty']} x {format_rp(it['price'])} = {format_rp(it['price']*it['qty'])}")
    print("-"*60)
    print(f"TOTAL         : {format_rp(total)}")
    print("-"*60)
    print(f"[Status Preview] : {preview_status}")
    print("="*60)
    ok = input("Konfirmasi & simpan transaksi? (y/n): ").strip().lower()
    if ok != "y":
        print("Transaksi dibatalkan.")
        pause(); return

    try:
        conn = get_conn()
        cur = conn.cursor()
       
        metode_row = exec_fetchone("SELECT id_metode_pembayaran FROM metode_pembayaran ORDER BY id_metode_pembayaran LIMIT 1")
        metode_id = metode_row[0] if metode_row else 1
        cur.execute("INSERT INTO pembayaran (jumlah_pembayaran, tanggal_pembayaran, status_pembayaran, metode_pembayaran_id_metode_pembayaran) VALUES (%s,%s,%s,%s) RETURNING id_pembayaran",
                    (total, tanggal, 'Lunas', metode_id))
        pay_id = cur.fetchone()[0]

        final_status = random.choices(["Berhasil","Gagal"], weights=[90,10])[0]
        status_id = 2 if final_status == "Berhasil" else 3

        cur.execute("""
            INSERT INTO transaksi (tanggal_transaksi, user_id_user, status_transaksi_id_status_transaksi, pembayaran_id_pembayaran)
            VALUES (%s,%s,%s,%s) RETURNING id_transaksi
        """, (tanggal, user['id'], status_id, pay_id))
        trx_id = cur.fetchone()[0]

        for it in basket:
            line_total = it['price'] * it['qty']
            cur.execute("INSERT INTO detail_transaksi (jumlah_produk, total_harga, transaksi_id_transaksi, produk_id_produk) VALUES (%s,%s,%s,%s)",
                        (it['qty'], line_total, trx_id, it['id']))
            cur.execute("UPDATE produk SET stok = stok - %s WHERE id_produk = %s", (it['qty'], it['id']))

        conn.commit()
        clear_screen()
        print("\nTransaksi tersimpan. NOTA FINAL:")
        print("="*60)
        print(f"ID Transaksi   : {trx_id}")
        print(f"Tanggal        : {tanggal}")
        print(f"Nama Pelanggan : {user.get('nama')}")
        print(f"Dilayani oleh  : {nama_karyawan}")
        print("-"*60)
        for i,it in enumerate(basket, start=1):
            print(f"{i}. {it['name']} - {it['qty']} x {format_rp(it['price'])} = {format_rp(it['price']*it['qty'])}")
        print("-"*60)
        print(f"TOTAL         : {format_rp(total)}")
        print(f"Status        : {final_status}")
        print("="*60)
    except Exception as e:
        try:
            conn.rollback()
        except:
            pass
        clear_screen()
        print("Gagal menyimpan transaksi. Periksa database atau koneksi.")
        print("Error (singkat):", str(e))
    finally:
        try:
            cur.close(); conn.close()
        except:
            pass
    pause()

def view_my_history(user):
    clear_screen()
    print("=== RIWAYAT PESANAN SAYA ===")
    t = input("Filter tanggal (YYYY-MM-DD) kosong = semua: ").strip()
    if t:
        try:
            tanggal = datetime.datetime.strptime(t, "%Y-%m-%d").date()
        except:
            print("Format tanggal salah.")
            pause(); return
        rows = exec_fetchall("""
            SELECT t.id_transaksi, t.tanggal_transaksi, p.jumlah_pembayaran, st.nama_status
            FROM transaksi t
            LEFT JOIN status_transaksi st ON st.id_status_transaksi = t.status_transaksi_id_status_transaksi
            LEFT JOIN pembayaran p ON p.id_pembayaran = t.pembayaran_id_pembayaran
            WHERE t.user_id_user=%s AND t.tanggal_transaksi=%s
            ORDER BY t.id_transaksi
        """, (user['id'], tanggal))
    else:
        rows = exec_fetchall("""
            SELECT t.id_transaksi, t.tanggal_transaksi, p.jumlah_pembayaran, st.nama_status
            FROM transaksi t
            LEFT JOIN status_transaksi st ON st.id_status_transaksi = t.status_transaksi_id_status_transaksi
            LEFT JOIN pembayaran p ON p.id_pembayaran = t.pembayaran_id_pembayaran
            WHERE t.user_id_user=%s
            ORDER BY t.id_transaksi
        """, (user['id'],))
    if not rows:
        print("Belum ada transaksi.")
        pause(); return
    print(tabulate(rows, headers=["ID","Tanggal","Total (Rp)","Status"], tablefmt="psql"))
    try:
        pick = input("Lihat detail transaksi ID (kosong untuk kembali): ").strip()
        if pick:
            tid = int(pick)
            dets = exec_fetchall("""
                SELECT pr.nama_produk, dt.jumlah_produk, dt.total_harga
                FROM detail_transaksi dt
                LEFT JOIN produk pr ON pr.id_produk=dt.produk_id_produk
                WHERE dt.transaksi_id_transaksi=%s
            """, (tid,))
            if dets:
                print(tabulate(dets, headers=["Produk","Jumlah","Harga/line (Rp)"], tablefmt="psql"))
            else:
                print("Tidak ada detail untuk transaksi ini.")
    except:
        pass
    pause()

def list_customers():
    clear_screen()
    rows = exec_fetchall("SELECT id_user, nama_lengkap, email FROM users WHERE role_id_role = %s ORDER BY id_user", (3,))
    print("=== DAFTAR PELANGGAN ===")
    if rows:
        print(tabulate(rows, headers=["ID","Nama","Email"], tablefmt="psql"))
    else:
        print("Tidak ada pelanggan.")
    pause()

def laporan_harian():
    clear_screen()
    print("=== LAPORAN HARIAN ===")
    tgl = input("Tanggal (YYYY-MM-DD): ").strip()
    try:
        tanggal = datetime.datetime.strptime(tgl, "%Y-%m-%d").date()
    except:
        print("Format tanggal salah.")
        pause(); return

    rows = exec_fetchall("""
        SELECT 
            t.id_transaksi,
            t.tanggal_transaksi,
            u.nama_lengkap,
            pr.nama_produk,
            dt.jumlah_produk,
            dt.total_harga,
            st.nama_status,
            mp.nama_metode_pembayaran
        FROM transaksi t
        LEFT JOIN detail_transaksi dt ON dt.transaksi_id_transaksi=t.id_transaksi
        LEFT JOIN produk pr ON pr.id_produk=dt.produk_id_produk
        LEFT JOIN users u ON u.id_user=t.user_id_user
        LEFT JOIN status_transaksi st ON st.id_status_transaksi=t.status_transaksi_id_status_transaksi
        LEFT JOIN pembayaran p ON p.id_pembayaran = t.pembayaran_id_pembayaran
        LEFT JOIN metode_pembayaran mp ON mp.id_metode_pembayaran = p.metode_pembayaran_id_metode_pembayaran
        WHERE t.tanggal_transaksi = %s
        ORDER BY t.id_transaksi
    """, (tanggal,))

    if not rows:
        print("Tidak ditemukan transaksi pada tanggal tersebut.")
    else:
        headers = ["ID","Tanggal","Pelanggan","Produk","Jumlah","Harga (Rp)","Status","Metode"]
        print(tabulate(rows, headers=headers, tablefmt="psql"))
    pause()

def menu_pelanggan(user):
    while True:
        clear_screen()
        print(f"=== Menu Pelanggan - {user['nama']} ===")
        print("1. Lihat produk")
        print("2. Buat transaksi")
        print("3. Lihat riwayat pesanan saya")
        print("4. Logout / Kembali")
        ch = input("Pilih: ").strip()
        if ch == "1":
            list_products()
        elif ch == "2":
            create_transaction(user)
        elif ch == "3":
            view_my_history(user)
        elif ch == "4":
            clear_screen()
            print("Log Out...")
            pause()
            return
        else:
            print("Pilihan tidak valid.")
            pause()

def menu_admin(user):
    while True:
        clear_screen()
        print(f"=== Menu Admin - {user['nama']} ===")
        print("1. Lihat daftar pelanggan")
        print("2. Edit katalog produk")
        print("3. Laporan harian")
        print("4. Logout / Kembali")
        ch = input("Pilih: ").strip()
        if ch == "1":
            list_customers()
        elif ch == "2":
            katalog_menu()
        elif ch == "3":
            laporan_harian()
        elif ch == "4":
            clear_screen()
            print("Log Out...")
            pause()
            return
        else:
            print("Pilihan tidak valid.")
            pause()

def menu_karyawan(user):
    while True:
        clear_screen()
        print(f"=== Menu Karyawan - {user['nama']} ===")
        print("1. Lihat daftar pelanggan")
        print("2. Edit katalog produk")
        print("3. Laporan harian")
        print("4. Logout / Kembali")
        ch = input("Pilih: ").strip()
        if ch == "1":
            list_customers()
        elif ch == "2":
            katalog_menu()
        elif ch == "3":
            laporan_harian()
        elif ch == "4":
            clear_screen()
            print("Log Out...")
            pause()
            return
        else:
            print("Pilihan tidak valid.")
            pause()

def main_menu():
    current_user = None
    while True:
        clear_screen()
        cover()
        print("=== AGROKOPI (CLI) ===")
        print("1. Register (pelanggan)")
        print("2. Login")
        print("0. Keluar")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            register_user()
        elif pilihan == "2":
            u = login()
            if u:
                current_user = u
                if current_user.get("role") == 1:
                    menu_admin(current_user)
                elif current_user.get("role") == 2:
                    menu_karyawan(current_user)
                elif current_user.get("role") == 3:
                    menu_pelanggan(current_user)
                else:
                    print("Role tidak dikenali.")
                    pause()
                current_user = None
        elif pilihan == "0":
            print("Out from Terminal..."); break
        else:
            print("Pilihan tidak diketahui (tidak valid).")
            pause()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nKeluar (CTRL+C).")
        sys.exit(0)
        

