from tabulate import tabulate    
import datetime as dt

while True:
    nomor_hp = input("Silahkan masukan nomor HP: ")
    if nomor_hp.isdigit() and (len(nomor_hp) == 12 or len(nomor_hp)== 13) :
        #print("aman")
        break
    else:
        print("Nomor HP tidak valid!")

while True:
    email = input("Silahkan masukan email: ")
    if email == "":
        print("Email masih kosong")
    else:
        break

while True:
    nama = input("Silahkan masukan nama: ")
    if nama == "" or nama[0].isdigit() :
        print("Input tidak valid")
    else:
        break

nickname = input("Tambahkan nickname pada kontak (optional): ")
        
while True:
    print("1. Laki-laki")
    print("2. Perempuan")
    jenis_kelamin = input("Silahkan pilih kelamin :")
    if jenis_kelamin.lower() == "1" or jenis_kelamin == "2":
        
        if jenis_kelamin == "1":
            jenis_kelamin = "Laki-laki"
        elif jenis_kelamin == "2":
            jenis_kelamin = "Perempuan"
        #print("aman")
        break
    else:
        print("Input tidak valid!")

while True:
    provinsi = input("Silahkan masukan provinsi: ")
    if provinsi == "":
        print("Provinsi masih kosong")
    else:
        break

while True:
    kota = input("Silahkan masukan kota: ")
    if kota == "":
        print("Kota masih kosong")
    else:
        break

alamat = input("Silahkan masukan alamat lengkap (optional): ")

while True:
        print("Kategori Kontak :")
        print("1. Keluarga")
        print("2. Teman Kerja")
        print("3. Teman Kuliah")
        print("4. Teman SMA")
        print("5. Teman SMP")
        print("6. Teman SD")
        print("7. Teman Main")
        print("")
        list_kategori = ["Keluarga","Teman Kerja","Teman Kuliah","Teman SMA","Teman SMP","Teman SD","Teman Main"]

        kategori = input("Silahkan pilih kategori : ")
        try:
            kategori = int(kategori)
            if kategori in range(1,8):
                kategori = list_kategori[kategori-1]
                break
            else:
                print("Silahkan masukan angka 1-7")
                continue
        except:
            print("Silahkan masukan angka 1-7")

catatan = input("Tambahkan catatan pada kontak(optional): ")
facebook = input("Tambahkan facebook pada kontak(optional): ")
instagram = input("Tambahkan instagram pada kontak(optional): ")
twitter = input("Tambahkan twitter pada kontak(optional): ")

last_update = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

inputed_data = {"phone_number": nomor_hp,
                "email": email,
                "full_name": nama,
                "nickname": nickname,
                "gender": jenis_kelamin,
                "state":provinsi,
                "city": kota,
                "address":alamat,
                "contact_category":kategori,
                "notes":catatan,
                "facebook":facebook,
                "instagram":instagram,
                "twitter":twitter,
                "last_update": last_update} 
print(tabulate([inputed_data], headers="keys", tablefmt="pipe"))