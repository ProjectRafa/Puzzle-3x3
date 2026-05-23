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
    
    /* TRICK UTAMA UNTUK HP: Memaksa susunan kolom Streamlit patuh dari atas ke bawah */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: column-reverse !important; 
        }
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
    /* Menggunakan aspect-ratio agar ubin selalu kotak sempurna */
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
    
    /* Menyembunyikan tombol bawaan Streamlit untuk di-bridge oleh D-Pad Kustom */
    .hidden-btn {
        display: none !important;
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
    st.session_state.status_text_1 = "Gunakan D-Pad di bawah, Arrow Keys, atau tombol WASD untuk bermain!"
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
# 5. RENDER LAYOUT UTAMA
# ==========================================
st.title("🧩 8-Puzzle BFS Solver")
st.write("---")

col1, col2 = st.columns([1, 1], gap="large")

# KELOMPOK KONTROL MANUAL & PANDUAN
with col1:
    with st.expander("ℹ️ Lihat Panduan Kontrol Game", expanded=False):
        st.markdown("### KONTROL GAME:")
        st.markdown("• **Tombol Keyboard:** Gunakan **Panah (Arrow Keys)** atau **W, A, S, D**")
        st.markdown("• **D-Pad Layar:** Gunakan controller panah biru di bawah.")
    
    # Tombol Python Asli Disembunyikan Menggunakan Div Ber-Class Khusus (Supaya Tetap Bisa Dipicu JS)
    st.markdown('<div class="hidden-btn">', unsafe_allow_html=True)
    st.button("🔼 Atas", on_click=tekan_Atas, key="real_up")
    st.button("◀️ Kiri", on_click=tekan_Kiri, key="real_left")
    st.button("🔄 Reset", on_click=aksi_tekan_Reset, key="real_reset")
    st.button("▶️ Kanan", on_click=tekan_Kanan, key="real_right")
    st.button("🔽 Bawah", on_click=tekan_Bawah, key="real_down")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==========================================
    # PEMBUATAN D-PAD GLOSSY KUSTOM (SESUAI GAMBAR)
    # ==========================================
    # HTML & CSS murni dipasang di sini untuk membentuk stick navigasi game silang transparan
    components.html("""
    <div class="dpad-wrapper">
        <div class="dpad-container">
            <button class="dpad-btn up" id="ui-up" title="Atas">
                <svg viewBox="0 0 24 24"><path d="M12 4l-8 8h6v8h4v-8h6z"/></svg>
            </button>
            <button class="dpad-btn left" id="ui-left" title="Kiri">
                <svg viewBox="0 0 24 24"><path d="M4 12l8-8v6h8v4h-8v6z"/></svg>
            </button>
            <button class="dpad-center" id="ui-reset" title="Reset">
                <div class="inner-reset"></div>
            </button>
            <button class="dpad-btn right" id="ui-right" title="Kanan">
                <svg viewBox="0 0 24 24"><path d="M20 12l-8-8v6h-8v4h8v6z"/></svg>
            </button>
            <button class="dpad-btn down" id="ui-down" title="Bawah">
                <svg viewBox="0 0 24 24"><path d="M12 20l8-8h-6v-8h-4v8h-6z"/></svg>
            </button>
        </div>
    </div>

    <style>
    .dpad-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px auto;
        padding: 10px;
    }
    /* Membentuk layout silang menggunakan grid 3x3 */
    .dpad-container {
        display: grid;
        grid-template-columns: repeat(3, 75px);
        grid-template-rows: repeat(3, 75px);
        gap: 2px;
        background: rgba(30, 41, 59, 0.5);
        padding: 12px;
        border-radius: 50%;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.5), 0 10px 20px rgba(0,0,0,0.3);
    }
    /* Style Tombol Panah (Sesuai dengan gambar gradasi biru mengkilap/glossy) */
    .dpad-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border: 2px solid #1d4ed8;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.4), 0 4px 6px rgba(0,0,0,0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.1s ease;
    }
    .dpad-btn svg {
        width: 40px;
        height: 40px;
        fill: #f8fafc;
        filter: drop-shadow(0 2px 2px rgba(0,0,0,0.3));
    }
    /* Efek glossy memantul di bagian atas/ujung tombol */
    .dpad-btn:after {
        content: '';
        position: absolute;
        top: 2px; left: 2px; right: 2px; height: 40%;
        background: linear-gradient(to bottom, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }
    /* Memposisikan tiap bagian ubin silang */
    .up { grid-column: 2; grid-row: 1; border-radius: 12px 12px 0 0; position: relative;}
    .left { grid-column: 1; grid-row: 2; border-radius: 12px 0 0 12px; position: relative;}
    .right { grid-column: 3; grid-row: 2; border-radius: 0 12px 12px 0; position: relative;}
    .down { grid-column: 2; grid-row: 3; border-radius: 0 0 12px 12px; position: relative;}
    
    /* Tombol Reset di Tengah Lingkaran */
    .dpad-center {
        grid-column: 2;
        grid-row: 2;
        background: #1e293b;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .inner-reset {
        width: 32px;
        height: 32px;
        border: 3px solid #64748b;
        border-radius: 50%;
        background: transparent;
        transition: all 0.2s;
    }
    /* Efek Interaksi saat tombol ditekan / active state */
    .dpad-btn:active {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: scale(0.95);
        box-shadow: inset 0 4px 6px rgba(0,0,0,0.6);
    }
    .dpad-center:active .inner-reset {
        border-color: #3b82f6;
        transform: scale(0.9);
    }
    </style>

    <script>
    // Menghubungkan klik D-pad Kustom ke tombol asli Streamlit di Parent Window
    const doc = window.parent.document;
    
    document.getElementById('ui-up').onclick = () => {
        const btn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('🔼 Atas'));
        if(btn) btn.click();
    };
    document.getElementById('ui-left').onclick = () => {
        const btn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('◀️ Kiri'));
        if(btn) btn.click();
    };
    document.getElementById('ui-right').onclick = () => {
        const btn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('▶️ Kanan'));
        if(btn) btn.click();
    };
    document.getElementById('ui-down').onclick = () => {
        const btn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('🔽 Bawah'));
        if(btn) btn.click();
    };
    document.getElementById('ui-reset').onclick = () => {
        const btn = Array.from(doc.querySelectorAll('button')).find(el => el.innerText.includes('🔄 Reset'));
        if(btn) btn.click();
    };
    </script>
    """, height=290)

    st.write("---")
    st.button("🤖 JALANKAN AI BFS SOLVER", on_click=aksi_tekan_BFS, type="primary", use_container_width=True)

# KELOMPOK VISUALISASI MATRIKS PUZZLE
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