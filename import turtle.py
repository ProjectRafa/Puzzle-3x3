import turtle
from collections import deque

# ==========================================
# 1. SETUP LAYAR & CANVAS UTAMA (RESOLUSI BESAR)
# ==========================================
screen = turtle.Screen()
screen.setup(1200, 800)  # Resolusi diperbesar menjadi 1200 x 800
screen.title("8-Sliding Puzzle 3x3 - BFS Solver (Resolusi Besar HD)")
screen.bgcolor("#0F172A") # Background Slate 900
screen.tracer(0)          # Render instan tanpa delay

# ==========================================
# 2. KONFIGURASI STATE PUZZLE (ANGKA)
# ==========================================
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
INITIAL_STATE = (1, 3, 4, 8, 6, 2, 7, 0, 5)

current_state = INITIAL_STATE
status_text_1 = "Gunakan tombol PANAH untuk menggeser ubin, atau SPACEBAR untuk AI BFS!"
status_text_2 = ""

# ==========================================
# 3. SEPARASI OBJEK TURTLE (ANTI MENUMPUK)
# ==========================================
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.penup()

t_panduan = turtle.Turtle()
t_panduan.hideturtle()
t_panduan.penup()
t_panduan.color("#E2E8F0")

t_status = turtle.Turtle()
t_status.hideturtle()
t_status.penup()
t_status.color("#22D3EE") # Warna Cyan terang

# ==========================================
# 4. LOGIKA OPERATOR PERGESERAN
# ==========================================
def dapatkan_tetangga(state):
    neighbors = []
    idx = state.index(0)
    r, c = idx // 3, idx % 3
    moves = [(-1, 0, 'Atas'), (1, 0, 'Bawah'), (0, -1, 'Kiri'), (0, 1, 'Kanan')]
    
    for dr, dc, move in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            n_idx = nr * 3 + nc
            next_state = list(state)
            next_state[idx], next_state[n_idx] = next_state[n_idx], next_state[idx]
            neighbors.append((tuple(next_state), move))
    return neighbors

def geser_manual(arah):
    global current_state, status_text_1, status_text_2
    if current_state == GOAL_STATE:
        return
        
    for tetangga, move in dapatkan_tetangga(current_state):
        if move == arah:
            current_state = tetangga
            status_text_1 = f"Anda menggeser ubin kosong ke: {arah}"
            status_text_2 = ""
            if current_state == GOAL_STATE:
                status_text_1 = "🎉 GOAL STATE TERCAPAI! Puzzle Berhasil Disusun! 🎉"
            render_ulang_layar()
            return

def tekan_Atas():  geser_manual('Atas')
def tekan_Bawah(): geser_manual('Bawah')
def tekan_Kiri():  geser_manual('Kiri')
def tekan_Kanan(): geser_manual('Kanan')

# ==========================================
# 5. FUNGSI RENDER TAMPILAN GRAFIS (UKURAN DI-SCALE UP)
# ==========================================
def gambar_panduan_statis():
    """Menggambar menu instruksi di sisi kiri dengan layout resolusi besar"""
    t_panduan.clear()
    t_panduan.goto(-540, 260)  # Digeser lebih ke kiri mengikuti resolusi baru
    t_panduan.write("KONTROL MANUAL PUZZLE 3x3:", font=("Arial", 14, "bold"), align="left")
    t_panduan.goto(-540, 210)
    t_panduan.write("• Tekan [↑] : Geser Kosong ke Atas", font=("Arial", 12, "normal"), align="left")
    t_panduan.goto(-540, 170)
    t_panduan.write("• Tekan [↓] : Geser Kosong ke Bawah", font=("Arial", 12, "normal"), align="left")
    t_panduan.goto(-540, 130)
    t_panduan.write("• Tekan [←] : Geser Kosong ke Kiri", font=("Arial", 12, "normal"), align="left")
    t_panduan.goto(-540, 90)
    t_panduan.write("• Tekan [→] : Geser Kosong ke Kanan", font=("Arial", 12, "normal"), align="left")
    t_panduan.goto(-540, 40)
    t_panduan.write("• Tekan [SPACE] : Eksekusi AI BFS Solver", font=("Arial", 12, "normal"), align="left")
    t_panduan.goto(-540, 0)
    t_panduan.write("• Tekan [ESC] : Kembalikan ke Posisi Acak", font=("Arial", 12, "normal"), align="left")

def perbarui_status_bawah():
    """Membersihkan dan menulis status di bagian bawah layar resolusi besar"""
    t_status.clear()
    t_status.goto(0, -280)  # Diturunkan sedikit agar proporsional
    t_status.write(status_text_1, font=("Arial", 14, "bold"), align="center")
    if status_text_2:
        t_status.goto(0, -320)
        t_status.write(status_text_2, font=("Arial", 12, "normal"), align="center")

def render_ulang_layar():
    """Menggambar matriks ubin angka yang jauh lebih besar dan tebal"""
    drawer.clear()
    
    # Titik koordinat awal digeser agar pas di tengah (Center-Right Canvas)
    start_x, start_y = 60, 150  
    
    # Ukuran ubin dinaikkan menjadi 100x100 piksel (sebelumnya hanya 68x68)
    ukuran_ubin = 100
    jarak_antar_ubin = 110  # Ukuran + celah pembatas
    
    for idx, angka in enumerate(current_state):
        r, c = idx // 3, idx % 3
        x = start_x + c * jarak_antar_ubin
        y = start_y - r * jarak_antar_ubin
        
        drawer.goto(x, y)
        drawer.pendown()
        
        if angka == 0:
            drawer.fillcolor("#1E293B") # Warna ubin kosong
            drawer.begin_fill()
            for _ in range(4):
                drawer.forward(ukuran_ubin)
                drawer.right(90)
            drawer.end_fill()
        else:
            drawer.fillcolor("#3B82F6") # Warna ubin angka (Biru Premium)
            drawer.begin_fill()
            for _ in range(4):
                drawer.forward(ukuran_ubin)
                drawer.right(90)
            drawer.end_fill()
            
            # Tulis angka besar tepat di tengah-tengah ubin baru
            drawer.penup()
            drawer.goto(x + (ukuran_ubin // 2), y - (ukuran_ubin // 2) - 15)
            drawer.color("#F8FAFC")
            drawer.write(str(angka), font=("Arial", 32, "bold"), align="center") # Font diperbesar ke 32
            
        drawer.penup()
        
    perbarui_status_bawah()
    screen.update()

def aksi_tekan_Reset():
    global current_state, status_text_1, status_text_2
    current_state = INITIAL_STATE
    status_text_1 = "Game di-reset ke Kondisi Awal Acak PPT."
    status_text_2 = ""
    render_ulang_layar()

# ==========================================
# 6. LOGIKA INTELLIGENT AI BFS SOLVER
# ==========================================
def aksi_tekan_BFS():
    global status_text_1, status_text_2
    status_text_1 = "AI Sedang menghitung jalur solusi terpendek (BFS)..."
    status_text_2 = ""
    render_ulang_layar()
    
    queue = deque([(current_state, [])])
    visited = {current_state}
    rute_solusi = None
    
    while queue:
        curr, path = queue.popleft()
        if curr == GOAL_STATE:
            rute_solusi = path
            break
            
        for tetangga, move in dapatkan_tetangga(curr):
            if tetangga not in visited:
                visited.add(tetangga)
                queue.append((tetangga, path + [move]))
                
    if rute_solusi is not None:
        status_text_1 = "🎉 AI BFS BERHASIL MENEMUKAN SOLUSI TERPENDEK! 🎉"
        status_text_2 = f"Urutan Pergeseran Ubin: {' -> '.join(rute_solusi)}"
    else:
        status_text_1 = "Sistem Error: State puzzle ini tidak dapat diselesaikan!"
        status_text_2 = ""
    render_ulang_layar()

# ==========================================
# 7. MENJALANKAN ENGINE UTAMA GAME
# ==========================================
screen.listen()
screen.onkey(tekan_Atas, "Up")
screen.onkey(tekan_Bawah, "Down")
screen.onkey(tekan_Kiri, "Left")
screen.onkey(tekan_Kanan, "Right")
screen.onkey(aksi_tekan_Reset, "Escape")
screen.onkey(aksi_tekan_BFS, "space")

# Gambar komponen visual awal
gambar_panduan_statis()
render_ulang_layar()

screen.mainloop()