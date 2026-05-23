import streamlit as st
import streamlit.components.v1 as components
from collections import deque

# Set konfig halaman Streamlit agar mendukung layout luas
st.set_page_config(layout="wide", page_title="8-Sliding Puzzle 3x3 - BFS Solver")

# ==========================================
# 1. STYLE CSS RESPONSIF (TETAP SEPERTI SEMULA)
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
    st.session_state.status_text_1 = "Gunakan D-Pad di layar, Arrow Keys, atau tombol WASD untuk bermain!"
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

# Fungsi pemicu kembalian dari deteksi tombol kustom internal
if "internal_move" in st.session_state and st.session_state.internal_move != "":
    arah_aksi = st.session_state.internal_move
    st.session_state.internal_move = ""
    geser_manual(arah_aksi)

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
# 5. RENDER LAYOUT UTAMA (TIDAK BERUBAH)
# ==========================================
st.title("🧩 8-Puzzle BFS Solver")
st.write("---")

col1, col2 = st.columns([1, 1], gap="large")

# KELOMPOK KONTROL MANUAL (KIRI)
with col1:
    # ----------------------------------------------------
    # TAMPILAN MURNI D-PAD SILANG (HTML / SVG)
    # ----------------------------------------------------
    # Rahasianya: Menggunakan form tersembunyi berukuran 0px di dalam iframe D-Pad.
    # Tidak akan merusak visual halaman luar Anda sedikit pun.
    components.html(f"""
    <div class="dpad-wrapper">
        <div class="dpad-container">
            <button class="dpad-btn up" id="ui-up" title="Atas">
                <svg viewBox="0 0 24 24"><path d="M12 4l-8 8h6v8h4v-8h6z"/></svg>
            </button>
            <button class="dpad-btn left" id="ui-left" title="Kiri">
                <svg viewBox="0 0 24 24"><path d="M4 12l8-8v6h8v4h-8v6z"/></svg>
            </button>
            <div class="dpad-center"></div>
            <button class="dpad-btn right" id="ui-right" title="Kanan">
                <svg viewBox="0 0 24 24"><path d="M20 12l-8-8v6h-8v4h8v6z"/></svg>
            </button>
            <button class="dpad-btn down" id="ui-down" title="Bawah">
                <svg viewBox="0 0 24 24"><path d="M12 20l8-8h-6v-8h-4v8h-6z"/></svg>
            </button>
        </div>
    </div>

    <form id="hidden-form" style="display:none;">
        <input type="text" id="dir-input" name="internal_move">
    </form>

    <style>
    .dpad-wrapper { display: flex; justify-content: center; align-items: center; margin: 15px auto; }
    .dpad-container {
        display: grid; grid-template-columns: repeat(3, 75px); grid-template-rows: repeat(3, 75px); gap: 2px;
        background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 50%; box-shadow: inset 0 2px 5px rgba(0,0,0,0.5), 0 10px 20px rgba(0,0,0,0.3);
    }
    .dpad-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border: 2px solid #1d4ed8;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.4), 0 4px 6px rgba(0,0,0,0.3); cursor: pointer;
        display: flex; align-items: center; justify-content: center; transition: all 0.1s ease;
    }
    .dpad-btn svg { width: 40px; height: 40px; fill: #f8fafc; filter: drop-shadow(0 2px 2px rgba(0,0,0,0.3)); }
    .up { grid-column: 2; grid-row: 1; border-radius: 12px 12px 0 0; position: relative;}
    .left { grid-column: 1; grid-row: 2; border-radius: 12px 0 0 12px; position: relative;}
    .right { grid-column: 3; grid-row: 2; border-radius: 0 12px 12px 0; position: relative;}
    .down { grid-column: 2; grid-row: 3; border-radius: 0 0 12px 12px; position: relative;}
    .dpad-center { grid-column: 2; grid-row: 2; background: #1e293b; border: none; }
    .dpad-btn:active { background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%); transform: scale(0.95); }
    </style>

    <script>
    const executeMove = (direction) => {
        window.parent.postMessage({
            type: 'streamlit:set_widget_value',
            key: 'internal_move',
            value: direction
        }, '*');
        
        // Memaksa Streamlit mendeteksi perubahan input dengan menargetkan tombol acak di halaman luar luar secara aman
        const anyBtn = window.parent.document.querySelector('button');
        if(anyBtn) { anyBtn.focus(); anyBtn.blur(); }
    };

    document.getElementById('ui-up').onclick = () => executeMove('Atas');
    document.getElementById('ui-left').onclick = () => executeMove('Kiri');
    document.getElementById('ui-right').onclick = () => executeMove('Kanan');
    document.getElementById('ui-down').onclick = () => executeMove('Bawah');

    // Menangkap kontrol keyboard WASD / Arrow Key Desktop asli
    window.parent.document.onkeydown = function(e) {
        let key = e.key.toLowerCase();
        if (key === 'arrowup' || key === 'w') { e.preventDefault(); executeMove('Atas'); }
        else if (key === 'arrowdown' || key === 's') { e.preventDefault(); executeMove('Bawah'); }
        else if (key === 'arrowleft' || key === 'a') { e.preventDefault(); executeMove('Kiri'); }
        else if (key === 'arrowright' || key === 'd') { e.preventDefault(); executeMove('Kanan'); }
    };
    </script>
    """, height=290)

    st.write("---")
    cc_bt1, cc_bt2 = st.columns(2)
    with cc_bt1: st.button("🔄 RESET GAME", on_click=aksi_tekan_Reset, use_container_width=True, key="btn_dt_reset")
    with cc_bt2: st.button("🤖 JALANKAN AI BFS SOLVER", on_click=aksi_tekan_BFS, type="primary", use_container_width=True, key="btn_dt_bfs")

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

# Menyiapkan variabel penampung state pemicu
st.session_state["internal_move"] = st.session_state.get("internal_move", "")

# ==========================================
# 6. STATUS BAWAH
# ==========================================
st.write("---")
st.markdown(f"<p class='status-cyan'>{st.session_state.status_text_1}</p>", unsafe_allow_html=True)
if st.session_state.status_text_2:
    st.markdown(f"<p class='status-sub'>{st.session_state.status_text_2}</p>", unsafe_allow_html=True)