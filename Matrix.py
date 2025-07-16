n = int(input("Masukkan Ordo Matrix (n x n): "))
print("Masukkan elemen-elemen [X]:")
x = []
for i in range(n):
    row = list(map(int, input(f"Baris {i + 1}: ").split()))
    if len(row) != n:
        print(f"Setiap baris harus terdiri dari  {n} elemen.")
    x.append(row) 
print(f"Masukkan elemen-elemen matrik [Y]:")    
y = []
for i in range(n):
    row = list(map(int, input(f"Baris {i + 1}: ").split()))
    if len(row) != n:
        print(f"Setiap baris harus terdiri dari {n} elemen.")
    y.append(row) 

Pilih=input("1.Penjumlahan; 2.Perkalian  ")
if Pilih == "1":
    hasil = []
    for i in range(n):
        Baris=[]
        for j in range(n):
            Baris.append(x[i][j]+y[i][j])
        hasil.append(Baris)

    print("Penjumlahan Matrik:")
    for elemen in hasil:
        print(elemen)
elif Pilih == "2":
    hasil_kali = []
    for i in range(n):
        Baris = []
        for j in range(n):
            total = 0
            for k in range(n):
                total += x[i][k] * y[k][j]
            Baris.append(total)
        hasil_kali.append(Baris)

    print("Perkalian Matrik:")
    for elemen in hasil_kali:
        print(elemen)