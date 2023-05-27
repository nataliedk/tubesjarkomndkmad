# Mengimpor modul socket, sys, dan os yang akan digunakan dalam program.
from socket import *
import sys
import os

# Membangun serverSocket dengan menggunakan protokol AF_INET (IPv4) dan tipe soket SOCK_STREAM (TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Menyiapkan server socket
serverPort = 80  # Memasukkan server port
serverSocket.bind(('', serverPort)) # Mengikat (bind) soket ke alamat dan nomor port
serverSocket.listen(1) # Mendengarkan koneksi dengan menggunakan metode listen

while True:
    # Menerima koneksi
    print('Ready to serve...')
    # Mengembalikan objek soket connectionSocket dan alamat 'addr' yang terhubung
    connectionSocket, addr = serverSocket.accept() 
    try:
        # Menerima data dari klien melalui koneksi yang dibuat, lalu dikonversi ke string (decode)
        message = connectionSocket.recv(1024).decode()
        # Permintaan HTTP dipecah agar mendapatkan file name
        filename = message.split()[1]
        filepath = filename[1:]  # filepath adalah filename tanpa karakter '/' di depannya

        # Memeriksa apakah file ada menggunakan package OS
        if os.path.isfile(filepath):
            # Menentukan file ekstensi dari file yang diterima
            file_extension = os.path.splitext(filepath)[1]

            # Membuka file yang diminta menggunakan open() dengan mode baca biner ('rb')
            with open(filepath, 'rb') as file:
                outputdata = file.read()

            # Menentukan header content type berdasarkan file ekstensinya
            if file_extension == '.html':
                content_type = 'text/html'
            elif file_extension == '.jpg':
                content_type = 'image/jpeg'
            elif file_extension == '.png':
                content_type = 'image/png'
            elif file_extension == '.gif':
                content_type = 'image/gif'
            elif file_extension == '.txt':
                content_type = 'text/plain'
            else:
                # Content type diatur default yaitu biner
                content_type = 'application/octet-stream'

            # Membuat response HTTP
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
            # Mengirim response HTTP yang sudah di-encode
            connectionSocket.send(response.encode())

            # Mengirim konten file yang diminta ke klien
            connectionSocket.sendall(outputdata)
        else:
            # Mengirim response jika file tidak ada
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
            error_message = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
            # Mengirim response HTTP yang sudah di-encode
            connectionSocket.send(response.encode())
            connectionSocket.send(error_message.encode())

        # Koneksi dengan klien ditutup
        connectionSocket.close()

    except OSError:
        # Kirim response untuk kesalahan yang terjadi selama penanganan file
        response = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n"
        error_message = "<html><head></head><body><h1>500 Internal Server Error</h1></body></html>\r\n"
        # Mengirim response HTTP yang sudah di-encode
        connectionSocket.send(response.encode())
        connectionSocket.send(error_message.encode())
        # Koneksi dengan klien ditutup
        connectionSocket.close()

# Server Socket ditutup
serverSocket.close()
# Exit dari system
sys.exit()
