import streamlit as st
from collections import deque

# Set konfig halaman Streamlit agar mendukung layout luas
st.set_page_config(layout="wide", page_title="8-Sliding Puzzle 3x3 - BFS Solver")

# ==========================================
# 1. STYLE CSS RESPONSIF & MODEL D-PAD BARU
# ==========================================
st.markdown("""
    <style>
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
    
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: column-reverse !important;
        }
    }

    /* CONTAINER D-PAD MODEL BARU (CSS GRID) */
    .dpad-grid-container {
        display: grid;
        grid-template-columns: repeat(3, 75px);
        grid-template-rows: repeat(3, 75px);
        gap: 6px;
        justify-content: center;
        align-content: center;
        margin: 20px auto;
        background: rgba(30, 41, 59, 0.4);
        padding: 15px;
        border-radius: 50%;
        max-width: 260px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.5), 0 10px 20px rgba(0,0,0,0.3);
    }
    
    /* Memaksa Tombol Streamlit Menjadi Bagian dari D-Pad Silang */
    .dpad-grid-container div[data-testid="stButton"] {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 !important;
        padding: 0 !important;
    }
    .dpad-grid-container button {
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: #f8fafc !important;
        border: 2px solid #1d4ed8 !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.4), 0 4px 6px rgba(0,0,0,0.3) !important;
        transition: all 0.1s ease !important;
    }
    .dpad-grid-container button:active {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        transform: scale(0.95) !important;
    }
    
    /* Penempatan Grid Silang */
    .dpad-up { grid-column: 2; grid-row: 1; }
    .dpad-left { grid-column: 1; grid-row: 2; }
    .dpad-center-space { grid-column: 2; grid-row: 2; background: #1e293b; border-radius: 8px; }
    .dpad-right { grid-column: 3; grid-row: 2; }
    .dpad-down { grid-column: 2; grid-row: 3; }

    /* STYLE MATRIKS PUZZLE */
    .tile-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-gap: 8px;
        justify-content: center;
        background-color: #0F172A;
        padding: 10px;
        border-radius: 10px;
        max-width: 340px;
        margin: 0 auto;
    }
    .tile {
        aspect-ratio: 1 / 1;
        background-color: #3B82F6;
        color: #F8FAFC;
        font-size: 2rem; 
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
        word-break: break-word;
    }
    .bottom-controls button {
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
    st.session_state.status_text_1 = "Gunakan D-Pad asli di layar atau tekan tombol kontrol Anda!"
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
# 4. KONTROL DESKTOP KEYBOARD (WASD & ARROWS)
# ==========================================
# Script ultra-ringan khusus menangkap ketukan keyboard tanpa memakan resource halaman luar
st.components.v1.html("""
    <script>
    window.parent.document.onkeydown = function(e) {
        let key = e.key.toLowerCase();
        let targetBtn = null;
        
        if (key === 'arrowup' || key === 'w') targetBtn = "▲";
        else if (key === 'arrowdown' || key === 's') targetBtn = "▼";
        else if (key === 'arrowleft' || key === 'a') targetBtn = "◀";
        else if (key === 'arrowright' || key === 'd') targetBtn = "▶";
        
        if(targetBtn) {
            e.preventDefault();
            const btn = Array.from(window.parent.document.querySelectorAll('button')).find(el => el.innerText.trim() === targetBtn);
            if(btn) btn.click();
        }
    };
    </script>
""", height=0)

# ==========================================
# 5. RENDER LAYOUT UTAMA
# ==========================================
st.title("🧩 8-Puzzle BFS Solver")
st.write("---")

col1, col2 = st.columns([1, 1], gap="large")

# KELOMPOK KONTROL MANUAL (KIRI)
with col1:
    # ----------------------------------------------------
    # MODEL BARU: D-PAD NYATA BERBASIS TOMBOL PYTHON
    # ----------------------------------------------------
    # Struktur visual luar tidak berubah, namun tombol ini dijamin 100% responsif karena diproses murni oleh Python
    st.markdown('<div class="dpad-grid-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="dpad-up">', unsafe_allow_html=True)
    st.button("▲", on_click=geser_manual, args=('Atas',), key="btn_p_up")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dpad-left">', unsafe_allow_html=True)
    st.button("◀", on_click=geser_manual, args=('Kiri',), key="btn_p_left")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dpad-center-space"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dpad-right">', unsafe_allow_html=True)
    st.button("▶", on_click=geser_manual, args=('Kanan',), key="btn_p_right")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dpad-down">', unsafe_allow_html=True)
    st.button("▼", on_click=geser_manual, args=('Bawah',), key="btn_p_down")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown('<div class="bottom-controls">', unsafe_allow_html=True)
    cc_bt1, cc_bt2 = st.columns(2)
    with cc_bt1: st.button("🔄 RESET GAME", on_click=aksi_tekan_Reset, use_container_width=True, key="btn_dt_reset")
    with cc_bt2: st.button("🤖 JALANKAN AI BFS SOLVER", on_click=aksi_tekan_BFS, type="primary", use_container_width=True, key="btn_dt_bfs")
    st.markdown('</div>', unsafe_allow_html=True)

# KELOMPOK VISUALISASI MATRIKS PUZZLE & PANDUAN (KANAN)
with col2:
    with st.expander("ℹ️ Lihat Panduan Kontrol Game", expanded=False):
        st.markdown("### KONTROL GAME:")
        st.markdown("• **Tombol Keyboard:** Gunakan **Panah (Arrow Keys)** atau **W, A, S, D**")
        st.markdown("• **Layar Sentuh/Mouse:** Gunakan D-Pad murni di samping kiri.")
        
    st.write("")

    # Tampilan Ubin Matriks Puzzle
    html_matriks = "<div class='tile-container'>"
    for angka in st.session_state.current_state:
        if angka == 0:
            html_matriks += "<div class='tile-empty'></div>"
        else:
            html_matriks += f"<div class='tile'>{angka}</div>"
    html_matriks += "</div>"
    
    st.markdown(html_matriks, unsafe_allow_html=True)
    st.write("")

# ==========================================
# 6. STATUS BAWAH
# ==========================================
st.write("---")
st.markdown(f"<p class='status-cyan'>{st.session_state.status_text_1}</p>", unsafe_allow_html=True)
if st.session_state.status_text_2:
    st.markdown(f"<p class='status-sub'>{st.session_state.status_text_2}</p>", unsafe_allow_html=True)