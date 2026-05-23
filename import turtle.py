import streamlit as st
from collections import deque
import time

# Set konfig halaman Streamlit agar mendukung layout luas (Resolusi Besar HD)
st.set_page_config(layout="wide", page_title="8-Sliding Puzzle 3x3 - BFS Solver")

# ==========================================
# 1. STYLE CSS (WARNA TEMA SLATE 900, CYAN, & BLUE PREMIUM)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    .tile-container {
        display: grid;
        grid-template-columns: repeat(3, 100px);
        grid-gap: 10px;
        justify-content: center;
        background-color: #0F172A;
        padding: 10px;
        border-radius: 10px;
    }
    .tile {
        width: 100px;
        height: 100px;
        background-color: #3B82F6;
        color: #F8FAFC;
        font-size: 32px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
    }
    .tile-empty {
        width: 100px;
        height: 100px;
        background-color: #1E293B;
        border-radius: 5px;
    }
    .status-cyan {
        color: #22D3EE;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
    }
    .status-sub {
        color: #E2E8F0;
        font-size: 14px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KONFIGURASI STATE PUZZLE & SESSION STATE
# ==========================================
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
INITIAL_STATE = (1, 3, 4, 8, 6, 2, 7, 0, 5)

if 'current_state' not in st.session_state:
    st.session_state.current_state = INITIAL_STATE
if 'status_text_1' not in st.session_state:
    st.session_state.status_text_1 = "Gunakan tombol kontrol di bawah untuk menggeser ubin, atau tombol AI BFS!"
if 'status_text_2' not in st.session_state:
    st.session_state.status_text_2 = ""

# ==========================================
# 3. LOGIKA OPERATOR PERGESERAN
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
    if st.session_state.current_state == GOAL_STATE:
        return
        
    for tetangga, move in dapatkan_tetangga(st.session_state.current_state):
        if move == arah:
            st.session_state.current_state = tetangga
            st.session_state.status_text_1 = f"Anda menggeser ubin kosong ke: {arah}"
            st.session_state.status_text_2 = ""
            if st.session_state.current_state == GOAL_STATE:
                st.session_state.status_text_1 = "🎉 GOAL STATE TERCAPAI! Puzzle Berhasil Disusun! 🎉"
            return

# ==========================================
# 4. HANDLER BUTTON (PENGGANTI KEYBINDING TURTLE)
# ==========================================
def tekan_Atas():  geser_manual('Atas')
def tekan_Bawah(): geser_manual('Bawah')
def tekan_Kiri():  geser_manual('Kiri')
def tekan_Kanan(): geser_manual('Kanan')

def aksi_tekan_Reset():
    st.session_state.current_state = INITIAL_STATE
    st.session_state.status_text_1 = "Game di-reset ke Kondisi Awal Acak PPT."
    st.session_state.status_text_2 = ""

def aksi_tekan_BFS():
    st.session_state.status_text_1 = "AI Sedang menghitung jalur solusi terpendek (BFS)..."
    st.session_state.status_text_2 = ""
    
    queue = deque([(st.session_state.current_state, [])])
    visited = {st.session_state.current_state}
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
        st.session_state.status_text_1 = "🎉 AI BFS BERHASIL MENEMUKAN SOLUSI TERPENDEK! 🎉"
        st.session_state.status_text_2 = f"Urutan Pergeseran Ubin: {' -> '.join(rute_solusi)}"
        
        # Animasi pergerakan otomatis (Simulasi visualisasi jalannya BFS)
        temp_state = st.session_state.current_state
        # Untuk streamlit, kita jalankan simulasi visualnya jika diinginkan, 
        # namun untuk menjaga kecocokan fungsi, kita langsung set ke GOAL setelah info rute didapat.
        st.session_state.current_state = GOAL_STATE 
    else:
        st.session_state.status_text_1 = "Sistem Error: State puzzle ini tidak dapat diselesaikan!"
        st.session_state.status_text_2 = ""

# ==========================================
# 5. RENDER LAYOUT UTAMA (RESOLUSI BESAR / SPLIT COLUMN)
# ==========================================
st.title("8-Sliding Puzzle 3x3 - BFS Solver (Streamlit Web Edition)")
st.write("---")

col1, col2 = st.columns([1, 1.2])

# --- SISI KIRI: PANDUAN & KONTROL ---
with col1:
    st.markdown("### KONTROL MANUAL PUZZLE 3x3:")
    st.markdown("• Klik tombol **[ ↑ ]** : Geser Kosong ke Atas")
    st.markdown("• Klik tombol **[ ↓ ]** : Geser Kosong ke Bawah")
    st.markdown("• Klik tombol **[ ← ]** : Geser Kosong ke Kiri")
    st.markdown("• Klik tombol **[ → ]** : Geser Kosong ke Kanan")
    st.markdown("• Klik tombol **[ AI BFS ]** : Eksekusi AI BFS Solver")
    st.markdown("• Klik tombol **[ RESET ]** : Kembalikan ke Posisi Acak")
    
    st.write("---")
    
    # Grid Tombol Navigasi Manual
    st.write("**Navigasi Manual Ubin:**")
    cc1, cc2, cc3 = st.columns([1,1,1])
    with cc2: st.button("🔼 Atas", on_click=tekan_Atas, use_container_width=True)
    
    cc4, cc5, cc6 = st.columns([1,1,1])
    with cc4: st.button("◀️ Kiri", on_click=tekan_Kiri, use_container_width=True)
    with cc5: st.button("🔄 Reset", on_click=aksi_tekan_Reset, use_container_width=True)
    with cc6: st.button("▶️ Kanan", on_click=tekan_Kanan, use_container_width=True)
    
    cc7, cc8, cc9 = st.columns([1,1,1])
    with cc8: st.button("🔽 Bawah", on_click=tekan_Bawah, use_container_width=True)
    
    st.write("")
    st.button("🤖 JALANKAN AI BFS SOLVER", on_click=aksi_tekan_BFS, type="primary", use_container_width=True)

# --- SISI KANAN: MATRIKS GRAFIS PUZZLE (RENDER ULANG INSTAN) ---
with col2:
    st.markdown("<h3 style='text-align: center;'>TAMPILAN PUZZLE</h3>", unsafe_allow_html=True)
    
    # Membangun elemen HTML Matriks 3x3 secara dinamis berdasarkan state saat ini
    html_matriks = "<div class='tile-container'>"
    for angka in st.session_state.current_state:
        if angka == 0:
            html_matriks += "<div class='tile-empty'></div>"
        else:
            html_matriks += f"<div class='tile'>{angka}</div>"
    html_matriks += "</div>"
    
    st.markdown(html_matriks, unsafe_allow_html=True)

# ==========================================
# 6. STATUS BAWAH (SAMA SEPERTI DI TURTLE)
# ==========================================
st.write("---")
st.markdown(f"<p class='status-cyan'>{st.session_state.status_text_1}</p>", unsafe_allow_html=True)
if st.session_state.status_text_2:
    st.markdown(f"<p class='status-sub'>{st.session_state.status_text_2}</p>", unsafe_allow_html=True)import streamlit as st
from collections import deque
import time

# Set konfig halaman Streamlit agar mendukung layout luas (Resolusi Besar HD)
st.set_page_config(layout="wide", page_title="8-Sliding Puzzle 3x3 - BFS Solver")

# ==========================================
# 1. STYLE CSS (WARNA TEMA SLATE 900, CYAN, & BLUE PREMIUM)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    .tile-container {
        display: grid;
        grid-template-columns: repeat(3, 100px);
        grid-gap: 10px;
        justify-content: center;
        background-color: #0F172A;
        padding: 10px;
        border-radius: 10px;
    }
    .tile {
        width: 100px;
        height: 100px;
        background-color: #3B82F6;
        color: #F8FAFC;
        font-size: 32px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
    }
    .tile-empty {
        width: 100px;
        height: 100px;
        background-color: #1E293B;
        border-radius: 5px;
    }
    .status-cyan {
        color: #22D3EE;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
    }
    .status-sub {
        color: #E2E8F0;
        font-size: 14px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KONFIGURASI STATE PUZZLE & SESSION STATE
# ==========================================
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
INITIAL_STATE = (1, 3, 4, 8, 6, 2, 7, 0, 5)

if 'current_state' not in st.session_state:
    st.session_state.current_state = INITIAL_STATE
if 'status_text_1' not in st.session_state:
    st.session_state.status_text_1 = "Gunakan tombol kontrol di bawah untuk menggeser ubin, atau tombol AI BFS!"
if 'status_text_2' not in st.session_state:
    st.session_state.status_text_2 = ""

# ==========================================
# 3. LOGIKA OPERATOR PERGESERAN
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
    if st.session_state.current_state == GOAL_STATE:
        return
        
    for tetangga, move in dapatkan_tetangga(st.session_state.current_state):
        if move == arah:
            st.session_state.current_state = tetangga
            st.session_state.status_text_1 = f"Anda menggeser ubin kosong ke: {arah}"
            st.session_state.status_text_2 = ""
            if st.session_state.current_state == GOAL_STATE:
                st.session_state.status_text_1 = "🎉 GOAL STATE TERCAPAI! Puzzle Berhasil Disusun! 🎉"
            return

# ==========================================
# 4. HANDLER BUTTON (PENGGANTI KEYBINDING TURTLE)
# ==========================================
def tekan_Atas():  geser_manual('Atas')
def tekan_Bawah(): geser_manual('Bawah')
def tekan_Kiri():  geser_manual('Kiri')
def tekan_Kanan(): geser_manual('Kanan')

def aksi_tekan_Reset():
    st.session_state.current_state = INITIAL_STATE
    st.session_state.status_text_1 = "Game di-reset ke Kondisi Awal Acak PPT."
    st.session_state.status_text_2 = ""

def aksi_tekan_BFS():
    st.session_state.status_text_1 = "AI Sedang menghitung jalur solusi terpendek (BFS)..."
    st.session_state.status_text_2 = ""
    
    queue = deque([(st.session_state.current_state, [])])
    visited = {st.session_state.current_state}
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
        st.session_state.status_text_1 = "🎉 AI BFS BERHASIL MENEMUKAN SOLUSI TERPENDEK! 🎉"
        st.session_state.status_text_2 = f"Urutan Pergeseran Ubin: {' -> '.join(rute_solusi)}"
        
        # Animasi pergerakan otomatis (Simulasi visualisasi jalannya BFS)
        temp_state = st.session_state.current_state
        # Untuk streamlit, kita jalankan simulasi visualnya jika diinginkan, 
        # namun untuk menjaga kecocokan fungsi, kita langsung set ke GOAL setelah info rute didapat.
        st.session_state.current_state = GOAL_STATE 
    else:
        st.session_state.status_text_1 = "Sistem Error: State puzzle ini tidak dapat diselesaikan!"
        st.session_state.status_text_2 = ""

# ==========================================
# 5. RENDER LAYOUT UTAMA (RESOLUSI BESAR / SPLIT COLUMN)
# ==========================================
st.title("8-Sliding Puzzle 3x3 - BFS Solver (Streamlit Web Edition)")
st.write("---")

col1, col2 = st.columns([1, 1.2])

# --- SISI KIRI: PANDUAN & KONTROL ---
with col1:
    st.markdown("### KONTROL MANUAL PUZZLE 3x3:")
    st.markdown("• Klik tombol **[ ↑ ]** : Geser Kosong ke Atas")
    st.markdown("• Klik tombol **[ ↓ ]** : Geser Kosong ke Bawah")
    st.markdown("• Klik tombol **[ ← ]** : Geser Kosong ke Kiri")
    st.markdown("• Klik tombol **[ → ]** : Geser Kosong ke Kanan")
    st.markdown("• Klik tombol **[ AI BFS ]** : Eksekusi AI BFS Solver")
    st.markdown("• Klik tombol **[ RESET ]** : Kembalikan ke Posisi Acak")
    
    st.write("---")
    
    # Grid Tombol Navigasi Manual
    st.write("**Navigasi Manual Ubin:**")
    cc1, cc2, cc3 = st.columns([1,1,1])
    with cc2: st.button("🔼 Atas", on_click=tekan_Atas, use_container_width=True)
    
    cc4, cc5, cc6 = st.columns([1,1,1])
    with cc4: st.button("◀️ Kiri", on_click=tekan_Kiri, use_container_width=True)
    with cc5: st.button("🔄 Reset", on_click=aksi_tekan_Reset, use_container_width=True)
    with cc6: st.button("▶️ Kanan", on_click=tekan_Kanan, use_container_width=True)
    
    cc7, cc8, cc9 = st.columns([1,1,1])
    with cc8: st.button("🔽 Bawah", on_click=tekan_Bawah, use_container_width=True)
    
    st.write("")
    st.button("🤖 JALANKAN AI BFS SOLVER", on_click=aksi_tekan_BFS, type="primary", use_container_width=True)

# --- SISI KANAN: MATRIKS GRAFIS PUZZLE (RENDER ULANG INSTAN) ---
with col2:
    st.markdown("<h3 style='text-align: center;'>TAMPILAN PUZZLE</h3>", unsafe_allow_html=True)
    
    # Membangun elemen HTML Matriks 3x3 secara dinamis berdasarkan state saat ini
    html_matriks = "<div class='tile-container'>"
    for angka in st.session_state.current_state:
        if angka == 0:
            html_matriks += "<div class='tile-empty'></div>"
        else:
            html_matriks += f"<div class='tile'>{angka}</div>"
    html_matriks += "</div>"
    
    st.markdown(html_matriks, unsafe_allow_html=True)

# ==========================================
# 6. STATUS BAWAH (SAMA SEPERTI DI TURTLE)
# ==========================================
st.write("---")
st.markdown(f"<p class='status-cyan'>{st.session_state.status_text_1}</p>", unsafe_allow_html=True)
if st.session_state.status_text_2:
    st.markdown(f"<p class='status-sub'>{st.session_state.status_text_2}</p>", unsafe_allow_html=True)import streamlit as st
from collections import deque
import time

# Set konfig halaman Streamlit agar mendukung layout luas (Resolusi Besar HD)
st.set_page_config(layout="wide", page_title="8-Sliding Puzzle 3x3 - BFS Solver")

# ==========================================
# 1. STYLE CSS (WARNA TEMA SLATE 900, CYAN, & BLUE PREMIUM)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    .tile-container {
        display: grid;
        grid-template-columns: repeat(3, 100px);
        grid-gap: 10px;
        justify-content: center;
        background-color: #0F172A;
        padding: 10px;
        border-radius: 10px;
    }
    .tile {
        width: 100px;
        height: 100px;
        background-color: #3B82F6;
        color: #F8FAFC;
        font-size: 32px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
    }
    .tile-empty {
        width: 100px;
        height: 100px;
        background-color: #1E293B;
        border-radius: 5px;
    }
    .status-cyan {
        color: #22D3EE;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
    }
    .status-sub {
        color: #E2E8F0;
        font-size: 14px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KONFIGURASI STATE PUZZLE & SESSION STATE
# ==========================================
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
INITIAL_STATE = (1, 3, 4, 8, 6, 2, 7, 0, 5)

if 'current_state' not in st.session_state:
    st.session_state.current_state = INITIAL_STATE
if 'status_text_1' not in st.session_state:
    st.session_state.status_text_1 = "Gunakan tombol kontrol di bawah untuk menggeser ubin, atau tombol AI BFS!"
if 'status_text_2' not in st.session_state:
    st.session_state.status_text_2 = ""

# ==========================================
# 3. LOGIKA OPERATOR PERGESERAN
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
    if st.session_state.current_state == GOAL_STATE:
        return
        
    for tetangga, move in dapatkan_tetangga(st.session_state.current_state):
        if move == arah:
            st.session_state.current_state = tetangga
            st.session_state.status_text_1 = f"Anda menggeser ubin kosong ke: {arah}"
            st.session_state.status_text_2 = ""
            if st.session_state.current_state == GOAL_STATE:
                st.session_state.status_text_1 = "🎉 GOAL STATE TERCAPAI! Puzzle Berhasil Disusun! 🎉"
            return

# ==========================================
# 4. HANDLER BUTTON (PENGGANTI KEYBINDING TURTLE)
# ==========================================
def tekan_Atas():  geser_manual('Atas')
def tekan_Bawah(): geser_manual('Bawah')
def tekan_Kiri():  geser_manual('Kiri')
def tekan_Kanan(): geser_manual('Kanan')

def aksi_tekan_Reset():
    st.session_state.current_state = INITIAL_STATE
    st.session_state.status_text_1 = "Game di-reset ke Kondisi Awal Acak PPT."
    st.session_state.status_text_2 = ""

def aksi_tekan_BFS():
    st.session_state.status_text_1 = "AI Sedang menghitung jalur solusi terpendek (BFS)..."
    st.session_state.status_text_2 = ""
    
    queue = deque([(st.session_state.current_state, [])])
    visited = {st.session_state.current_state}
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
        st.session_state.status_text_1 = "🎉 AI BFS BERHASIL MENEMUKAN SOLUSI TERPENDEK! 🎉"
        st.session_state.status_text_2 = f"Urutan Pergeseran Ubin: {' -> '.join(rute_solusi)}"
        
        # Animasi pergerakan otomatis (Simulasi visualisasi jalannya BFS)
        temp_state = st.session_state.current_state
        # Untuk streamlit, kita jalankan simulasi visualnya jika diinginkan, 
        # namun untuk menjaga kecocokan fungsi, kita langsung set ke GOAL setelah info rute didapat.
        st.session_state.current_state = GOAL_STATE 
    else:
        st.session_state.status_text_1 = "Sistem Error: State puzzle ini tidak dapat diselesaikan!"
        st.session_state.status_text_2 = ""

# ==========================================
# 5. RENDER LAYOUT UTAMA (RESOLUSI BESAR / SPLIT COLUMN)
# ==========================================
st.title("8-Sliding Puzzle 3x3 - BFS Solver (Streamlit Web Edition)")
st.write("---")

col1, col2 = st.columns([1, 1.2])

# --- SISI KIRI: PANDUAN & KONTROL ---
with col1:
    st.markdown("### KONTROL MANUAL PUZZLE 3x3:")
    st.markdown("• Klik tombol **[ ↑ ]** : Geser Kosong ke Atas")
    st.markdown("• Klik tombol **[ ↓ ]** : Geser Kosong ke Bawah")
    st.markdown("• Klik tombol **[ ← ]** : Geser Kosong ke Kiri")
    st.markdown("• Klik tombol **[ → ]** : Geser Kosong ke Kanan")
    st.markdown("• Klik tombol **[ AI BFS ]** : Eksekusi AI BFS Solver")
    st.markdown("• Klik tombol **[ RESET ]** : Kembalikan ke Posisi Acak")
    
    st.write("---")
    
    # Grid Tombol Navigasi Manual
    st.write("**Navigasi Manual Ubin:**")
    cc1, cc2, cc3 = st.columns([1,1,1])
    with cc2: st.button("🔼 Atas", on_click=tekan_Atas, use_container_width=True)
    
    cc4, cc5, cc6 = st.columns([1,1,1])
    with cc4: st.button("◀️ Kiri", on_click=tekan_Kiri, use_container_width=True)
    with cc5: st.button("🔄 Reset", on_click=aksi_tekan_Reset, use_container_width=True)
    with cc6: st.button("▶️ Kanan", on_click=tekan_Kanan, use_container_width=True)
    
    cc7, cc8, cc9 = st.columns([1,1,1])
    with cc8: st.button("🔽 Bawah", on_click=tekan_Bawah, use_container_width=True)
    
    st.write("")
    st.button("🤖 JALANKAN AI BFS SOLVER", on_click=aksi_tekan_BFS, type="primary", use_container_width=True)

# --- SISI KANAN: MATRIKS GRAFIS PUZZLE (RENDER ULANG INSTAN) ---
with col2:
    st.markdown("<h3 style='text-align: center;'>TAMPILAN PUZZLE</h3>", unsafe_allow_html=True)
    
    # Membangun elemen HTML Matriks 3x3 secara dinamis berdasarkan state saat ini
    html_matriks = "<div class='tile-container'>"
    for angka in st.session_state.current_state:
        if angka == 0:
            html_matriks += "<div class='tile-empty'></div>"
        else:
            html_matriks += f"<div class='tile'>{angka}</div>"
    html_matriks += "</div>"
    
    st.markdown(html_matriks, unsafe_allow_html=True)

# ==========================================
# 6. STATUS BAWAH (SAMA SEPERTI DI TURTLE)
# ==========================================
st.write("---")
st.markdown(f"<p class='status-cyan'>{st.session_state.status_text_1}</p>", unsafe_allow_html=True)
if st.session_state.status_text_2:
    st.markdown(f"<p class='status-sub'>{st.session_state.status_text_2}</p>", unsafe_allow_html=True)