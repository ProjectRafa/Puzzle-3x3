import streamlit as st
import streamlit.components.v1 as components
from collections import deque
import time

# Set konfig halaman Streamlit agar mendukung layout luas
st.set_page_config(layout="wide", page_title="8-Sliding Puzzle 3x3 - BFS Solver")

# ==========================================
# 1. STYLE CSS RESPONSIF (ADAPTIF HP & DESKTOP)
# ==========================================
st.markdown("""
    <style>
    /* Mengurangi padding bawaan streamlit di HP agar hemat ruang */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    /* Grid container menggunakan max-width agar tidak terlalu raksasa di desktop */
    .tile-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-gap: 8px;
        justify-content: center;
        background-color: #0F172A;
        padding: 10px;
        border-radius: 10px;
        max-width: 340px;
        margin: 0 auto; /* Supaya posisi puzzle pas di tengah-tengah layar */
    }
    /* Menggunakan aspect-ratio agar ubin selalu kotak sempurna di perangkat apapun */
    .tile {
        aspect-ratio: 1 / 1;
        background-color: #3B82F6;
        color: #F8FAFC;
        font-size: 2rem; /* Menggunakan rem agar ukuran font proporsional */
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .tile-empty {
        aspect-ratio: 1 / 1;
        background-color: #1E293B;
        border-radius: 8px;
    }
    .status-cyan {
        color: #22D3EE;
        font-weight: bold;
        font-size: 1.1rem;
        text-align: center;
    }
    .status-sub {
        color: #E2E8F0;
        font-size: 0.9rem;
        text-align: center;
        word-break: break-word; /* Mencegah teks rute meluber di layar HP */
    }
    /* Penyesuaian khusus tombol agar lebih tebal & mudah di-tap jari di HP */
    .stButton>button {
        padding: 0.5rem 0.2rem !important;
        font-weight: bold !important;
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
    st.session_state.status_text_1 = "Gunakan tombol layar, Arrow Keys (Panah), atau tombol WASD di keyboard Anda!"
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
# 4. HANDLER BUTTON
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
        st.session_state.current_state = GOAL_STATE 
    else:
        st.session_state.status_text_1 = "Sistem Error: State puzzle ini tidak dapat diselesaikan!"
        st.session_state.status_text_2 = ""

# ==========================================
# 5. RENDER LAYOUT UTAMA (RESPONSIVE COLUMN BINDING)
# ==========================================
st.title("🧩 8-Puzzle BFS Solver")
st.write("---")

# Menginisialisasi dua kolom (Kiri untuk tombol kontrol, Kanan untuk visual matriks di Desktop)
col1, col2 = st.columns([1, 1], gap="large")

# --- SEKARANG DIRENDER PERTAMA: MATRIKS GRAFIS PUZZLE ---
# (Di Desktop berada di kanan, di HP otomatis naik ke posisi paling atas)
with col2:
    st.markdown("<h3 style='text-align: center; margin-bottom: 15px;'>TAMPILAN PUZZLE</h3>", unsafe_allow_html=True)
    
    html_matriks = "<div class='tile-container'>"
    for angka in st.session_state.current_state:
        if angka == 0:
            html_matriks += "<div class='tile-empty'></div>"
        else:
            html_matriks += f"<div class='tile'>{angka}</div>"
    html_matriks += "</div>"
    
    st.markdown(html_matriks, unsafe_allow_html=True)
    st.write("")

# --- DIRENDER KEDUA: PANDUAN & KONTROL MANUAL ---
# (Di Desktop berada di kiri, di HP otomatis turun di bawah Puzzle)
with col1:
    with st.expander("ℹ️ Lihat Panduan Kontrol Game", expanded=False):
        st.markdown("### KONTROL GAME:")
        st.markdown("• **Tombol Keyboard:** Gunakan **Panah (Arrow Keys)** atau **W, A, S, D**")
        st.markdown("• Tombol **[ 🔼 Atas / W ]** : Geser Kosong ke Atas")
        st.markdown("• Tombol **[ 🔽 Bawah / S ]** : Geser Kosong ke Bawah")
        st.markdown("• Tombol **[ ◀️ Kiri / A ]** : Geser Kosong ke Kiri")
        st.markdown("• Tombol **[ ▶️ Kanan / D ]** : Geser Kosong ke Kanan")
    
    st.write("")
    
    # Grid Tombol Navigasi Manual
    cc1, cc2, cc3 = st.columns([1,1,1])
    with cc2: st.button("🔼 Atas", on_click=tekan_Atas, use_container_width=True, key="btn_atas")
    
    cc4, cc5, cc6 = st.columns([1,1,1])
    with cc4: st.button("◀️ Kiri", on_click=tekan_Kiri, use_container_width=True, key="btn_kiri")
    with cc5: st.button("🔄 Reset", on_click=aksi_tekan_Reset, use_container_width=True, key="btn_reset")
    with cc6: st.button("▶️ Kanan", on_click=tekan_Kanan, use_container_width=True, key="btn_kanan")
    
    cc7, cc8, cc9 = st.columns([1,1,1])
    with cc8: st.button("🔽 Bawah", on_click=tekan_Bawah, use_container_width=True, key="btn_bawah")
    
    st.write("---")
    st.button("🤖 JALANKAN AI BFS SOLVER", on_click=aksi_tekan_BFS, type="primary", use_container_width=True)

# ==========================================
# 6. STATUS BAWAH
# ==========================================
st.write("---")
st.markdown(f"<p class='status-cyan'>{st.session_state.status_text_1}</p>", unsafe_allow_html=True)
if st.session_state.status_text_2:
    st.markdown(f"<p class='status-sub'>{st.session_state.status_text_2}</p>", unsafe_allow_html=True)

# ==========================================
# 7. JAVASCRIPT KEYBOARD LISTENER (EMBEDDED)
# ==========================================
components.html("""
<script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        let key = e.key.toLowerCase();
        let targetButton = null;

        if (key === 'arrowup' || key === 'w') {
            targetButton = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('🔼 Atas'));
        } else if (key === 'arrowdown' || key === 's') {
            targetButton = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('🔽 Bawah'));
        } else if (key === 'arrowleft' || key === 'a') {
            targetButton = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('◀️ Kiri'));
        } else if (key === 'arrowright' || key === 'd') {
            targetButton = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('▶️ Kanan'));
        }

        if (targetButton) {
            e.preventDefault(); 
            targetButton.click();
        }
    });
</script>
""", height=0)