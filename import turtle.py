import streamlit as st
import streamlit.components.v1 as components
from collections import deque

# Set konfig halaman Streamlit agar mendukung layout luas
st.set_page_config(layout="wide", page_title="8-Sliding Puzzle 3x3 - BFS Solver")

# ==========================================
# 1. STYLE CSS RESPONSIF (POSISI PRESISI)
# ==========================================
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    
    /* DESKTOP: D-Pad di Kiri, Puzzle di Kanan */
    @media (min-width: 769px) {
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row-reverse !important; /* col2 (D-Pad) di kiri */
            align-items: center !important;
        }
    }

    /* HP/MOBILE: Puzzle di Atas, D-Pad di Bawah */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: column !important; /* col1 (Puzzle) di atas, col2 (D-Pad) di bawah */
        }
    }

    /* Sembunyikan tombol jembatan sistem secara total dari pandangan */
    .hidden-control-container {
        position: absolute;
        width: 0px;
        height: 0px;
        overflow: hidden;
        opacity: 0;
        pointer-events: none;
    }

    .tile-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-gap: 8px;
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
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .tile-empty {
        aspect-ratio: 1 / 1;
        background-color: #1E293B;
        border-radius: 8px;
    }
    .status-cyan {
        color: #22D3EE;
        font-weight: bold;
        text-align: center;
        font-size: 1.1rem;
    }
    .stButton>button {
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIKA & SESSION STATE
# ==========================================
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
INITIAL_STATE = (1, 3, 4, 8, 6, 2, 7, 0, 5)

if 'current_state' not in st.session_state:
    st.session_state.current_state = INITIAL_STATE
if 'status_text_1' not in st.session_state:
    st.session_state.status_text_1 = "Gunakan D-Pad bulat di layar atau tombol Keyboard!"

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
    if st.session_state.current_state == GOAL_STATE: return
    for tetangga, move in dapatkan_tetangga(st.session_state.current_state):
        if move == arah:
            st.session_state.current_state = tetangga
            st.session_state.status_text_1 = f"Geser: {arah}"
            if st.session_state.current_state == GOAL_STATE:
                st.session_state.status_text_1 = "🎉 PUZZLE SELESAI! 🎉"
            return

def aksi_tekan_Reset():
    st.session_state.current_state = INITIAL_STATE
    st.session_state.status_text_1 = "Game di-reset."

def aksi_tekan_BFS():
    queue = deque([(st.session_state.current_state, [])])
    visited = {st.session_state.current_state}
    while queue:
        curr, path = queue.popleft()
        if curr == GOAL_STATE:
            st.session_state.current_state = GOAL_STATE
            st.session_state.status_text_1 = "🎉 AI RAFA Berhasil Menemukan Solusi! 🎉"
            return
        for tetangga, move in dapatkan_tetangga(curr):
            if tetangga not in visited:
                visited.add(tetangga)
                queue.append((tetangga, path + [move]))

# ==========================================
# 3. RENDER LAYOUT UTAMA
# ==========================================
st.title("🧩 8-Puzzle BFS Solver")
st.write("---")

# Tombol jembatan kosong diidentifikasi via parameter key unik
st.markdown('<div class="hidden-control-container">', unsafe_allow_html=True)
st.button("", on_click=geser_manual, args=('Atas',), key="p_move_up")
st.button("", on_click=geser_manual, args=('Bawah',), key="p_move_down")
st.button("", on_click=geser_manual, args=('Kiri',), key="p_move_left")
st.button("", on_click=geser_manual, args=('Kanan',), key="p_move_right")
st.markdown('</div>', unsafe_allow_html=True)

# Urutan kolom: col1 (Puzzle), col2 (D-Pad)
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    # PUZZLE (Akan berada di ATAS pada layar HP)
    with st.expander("ℹ️ Panduan Kontrol", expanded=False):
        st.write("Desktop: **WASD** / Arrow Keys.")
        st.write("HP: Klik D-Pad di bawah.")
    
    st.write("")
    # Render Matriks Ubin
    html_matriks = "<div class='tile-container'>"
    for angka in st.session_state.current_state:
        if angka == 0: html_matriks += "<div class='tile-empty'></div>"
        else: html_matriks += f"<div class='tile'>{angka}</div>"
    html_matriks += "</div>"
    st.markdown(html_matriks, unsafe_allow_html=True)

with col2:
    # D-PAD (Akan berada di SAMPING KIRI pada Desktop, di BAWAH PUZZLE pada HP)
    components.html("""
    <div class="dpad-wrapper">
        <div class="dpad-container">
            <button class="dpad-btn up" id="ui-up"><svg viewBox="0 0 24 24"><path d="M12 4l-8 8h6v8h4v-8h6z"/></svg></button>
            <button class="dpad-btn left" id="ui-left"><svg viewBox="0 0 24 24"><path d="M4 12l8-8v6h8v4h-8v6z"/></svg></button>
            <div class="dpad-center"></div>
            <button class="dpad-btn right" id="ui-right"><svg viewBox="0 0 24 24"><path d="M20 12l-8-8v6h-8v4h8v6z"/></svg></button>
            <button class="dpad-btn down" id="ui-down"><svg viewBox="0 0 24 24"><path d="M12 20l8-8h-6v-8h-4v8h-6z"/></svg></button>
        </div>
    </div>
    <style>
        .dpad-wrapper { display: flex; justify-content: center; align-items: center; margin: 10px auto; }
        .dpad-container {
            display: grid; grid-template-columns: repeat(3, 70px); grid-template-rows: repeat(3, 70px); gap: 4px;
            background: rgba(30, 41, 59, 0.5); padding: 10px; border-radius: 50%;
        }
        .dpad-btn {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border: none; cursor: pointer;
            display: flex; align-items: center; justify-content: center; border-radius: 10px;
        }
        .dpad-btn svg { width: 35px; height: 35px; fill: white; }
        .up { grid-column: 2; grid-row: 1; }
        .left { grid-column: 1; grid-row: 2; }
        .right { grid-column: 3; grid-row: 2; }
        .down { grid-column: 2; grid-row: 3; }
        .dpad-center { grid-column: 2; grid-row: 2; background: transparent; }
        .dpad-btn:active { transform: scale(0.9); opacity: 0.8; }
    </style>
    <script>
        function pemicu(keyName) {
            const btn = window.parent.document.querySelector(`button[key="${keyName}"]`);
            if (btn) {
                btn.click();
            } else {
                const semuaTombol = window.parent.document.querySelectorAll('.hidden-control-container button');
                const urutan = {'p_move_up': 0, 'p_move_down': 1, 'p_move_left': 2, 'p_move_right': 3};
                if(semuaTombol.length > 0) semuaTombol[urutan[keyName]].click();
            }
        }
        
        document.getElementById('ui-up').onclick = () => pemicu('p_move_up');
        document.getElementById('ui-down').onclick = () => pemicu('p_move_down');
        document.getElementById('ui-left').onclick = () => pemicu('p_move_left');
        document.getElementById('ui-right').onclick = () => pemicu('p_move_right');
        
        window.parent.document.onkeydown = function(e) {
            let k = e.key.toLowerCase();
            if (k === 'arrowup' || k === 'w') { e.preventDefault(); pemicu('p_move_up'); }
            if (k === 'arrowdown' || k === 's') { e.preventDefault(); pemicu('p_move_down'); }
            if (k === 'arrowleft' || k === 'a') { e.preventDefault(); pemicu('p_move_left'); }
            if (k === 'arrowright' || k === 'd') { e.preventDefault(); pemicu('p_move_right'); }
        };
    </script>
    """, height=260)
    
    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.button("🔄 RESET", on_click=aksi_tekan_Reset, use_container_width=True)
    with c2: st.button("🤖 AI RAFA", on_click=aksi_tekan_BFS, type="primary", use_container_width=True)

# Status
st.write("---")
st.markdown(f"<p class='status-cyan'>{st.session_state.status_text_1}</p>", unsafe_allow_html=True)