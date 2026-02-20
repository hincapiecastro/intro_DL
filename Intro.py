import streamlit as st

st.title("app de prueba") 
import math

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Calculadora", page_icon="⬡", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

/* ── Reset & root ── */
:root {
    --bg:       #0a0a0f;
    --surface:  #12121a;
    --panel:    #1a1a26;
    --accent:   #00ffe5;
    --accent2:  #ff3cac;
    --text:     #e0e0f0;
    --muted:    #555577;
    --btn-num:  #1e1e2e;
    --btn-op:   #1a1a36;
    --btn-eq:   #00ffe5;
    --radius:   12px;
    --shadow:   0 0 24px rgba(0,255,229,0.12);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--text) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stMain"] > div { padding-top: 2rem; }
.block-container { max-width: 460px !important; padding: 0 1rem !important; }

/* ── Title ── */
.calc-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 900;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent);
    text-align: center;
    margin-bottom: 1.6rem;
    text-shadow: 0 0 12px rgba(0,255,229,0.5);
}

/* ── Display ── */
.display-wrap {
    background: var(--surface);
    border: 1px solid rgba(0,255,229,0.18);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem 1rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}
.display-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
}
.display-history {
    font-size: 0.75rem;
    color: var(--muted);
    text-align: right;
    min-height: 1.1rem;
    letter-spacing: 0.05em;
}
.display-main {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    text-align: right;
    color: var(--text);
    word-break: break-all;
    line-height: 1.15;
    text-shadow: 0 0 8px rgba(224,224,240,0.25);
}
.display-main.error {
    color: var(--accent2);
    font-size: 1.5rem;
    text-shadow: 0 0 8px rgba(255,60,172,0.4);
}

/* ── Button grid ── */
.btn-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}
.btn {
    padding: 0;
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.1rem;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.12s ease;
    position: relative;
    overflow: hidden;
}
.btn::after {
    content: '';
    position: absolute;
    inset: 0;
    background: white;
    opacity: 0;
    transition: opacity 0.1s;
}
.btn:active::after { opacity: 0.07; }

.btn-num {
    background: var(--btn-num);
    color: var(--text);
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
}
.btn-num:hover { background: #252535; border-color: rgba(0,255,229,0.2); }

.btn-op {
    background: var(--btn-op);
    color: var(--accent);
    border: 1px solid rgba(0,255,229,0.2);
    font-size: 1.3rem;
}
.btn-op:hover { background: #222240; box-shadow: 0 0 10px rgba(0,255,229,0.15); }

.btn-fn {
    background: #1e1a2e;
    color: var(--accent2);
    border: 1px solid rgba(255,60,172,0.18);
    font-size: 0.9rem;
    letter-spacing: 0.05em;
}
.btn-fn:hover { background: #251a36; box-shadow: 0 0 10px rgba(255,60,172,0.15); }

.btn-clear {
    background: #2a1a1a;
    color: #ff6b6b;
    border: 1px solid rgba(255,107,107,0.2);
}
.btn-clear:hover { background: #331a1a; }

.btn-eq {
    background: var(--btn-eq);
    color: #0a0a0f;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    font-size: 1.3rem;
    grid-column: span 2;
    box-shadow: 0 0 18px rgba(0,255,229,0.3);
    border: none;
}
.btn-eq:hover { background: #33fff0; box-shadow: 0 0 28px rgba(0,255,229,0.5); }

.btn-zero { grid-column: span 2; }

/* ── Mode toggle ── */
.mode-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 1rem;
}
.mode-btn {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    padding: 6px 18px;
    border-radius: 999px;
    cursor: pointer;
    border: 1px solid var(--muted);
    background: transparent;
    color: var(--muted);
    transition: all 0.15s;
}
.mode-btn.active {
    border-color: var(--accent);
    color: var(--accent);
    box-shadow: 0 0 10px rgba(0,255,229,0.2);
}

/* ── Sci grid ── */
.btn-grid-sci {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 10px;
}

/* ── Streamlit button overrides ── */
div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── State init ────────────────────────────────────────────────────────────────
def init():
    defaults = {
        "current": "0",
        "history": "",
        "operator": None,
        "prev": None,
        "fresh": True,     # next digit replaces display
        "mode": "basic",   # basic | sci
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()
s = st.session_state

# ── Logic helpers ─────────────────────────────────────────────────────────────
def push_digit(d: str):
    if s.fresh:
        s.current = d
        s.fresh = False
    else:
        if s.current == "0" and d != ".":
            s.current = d
        elif "." in s.current and d == ".":
            pass
        else:
            if len(s.current.lstrip("-")) < 15:
                s.current += d

def push_op(op: str):
    try:
        val = float(s.current)
    except:
        return
    if s.operator and not s.fresh:
        val = compute(s.prev, val, s.operator)
        s.current = fmt(val)
    s.prev = float(s.current)
    s.operator = op
    s.history = f"{s.current} {op}"
    s.fresh = True

def fmt(n):
    if n == int(n) and abs(n) < 1e12:
        return str(int(n))
    return f"{n:.10g}"

def compute(a, b, op):
    if op == "+": return a + b
    if op == "−": return a - b
    if op == "×": return a * b
    if op == "÷":
        if b == 0: raise ZeroDivisionError
        return a / b
    if op == "%": return a % b
    if op == "^": return a ** b
    return b

def do_equals():
    try:
        val = float(s.current)
        if s.operator:
            result = compute(s.prev, val, s.operator)
            s.history = f"{fmt(s.prev)} {s.operator} {fmt(val)} ="
            s.current = fmt(result)
        s.operator = None
        s.prev = None
        s.fresh = True
    except ZeroDivisionError:
        s.current = "ERROR: ÷0"
        s.operator = None; s.prev = None; s.fresh = True
    except:
        s.current = "ERROR"
        s.operator = None; s.prev = None; s.fresh = True

def do_sci(fn: str):
    try:
        val = float(s.current)
        ops = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "√":   lambda x: math.sqrt(x),
            "log": lambda x: math.log10(x),
            "ln":  lambda x: math.log(x),
            "x²":  lambda x: x**2,
            "1/x": lambda x: 1/x,
            "π":   lambda x: math.pi,
            "e":   lambda x: math.e,
            "|x|": lambda x: abs(x),
            "!":   lambda x: float(math.factorial(int(x))),
        }
        result = ops[fn](val)
        s.history = f"{fn}({fmt(val)}) ="
        s.current = fmt(result)
        s.fresh = True
    except:
        s.current = "ERROR"
        s.fresh = True

def do_clear():
    s.current = "0"; s.history = ""; s.operator = None; s.prev = None; s.fresh = True

def do_backspace():
    if s.fresh or len(s.current) <= 1 or s.current in ("0",):
        s.current = "0"; s.fresh = True
    else:
        s.current = s.current[:-1]
        if s.current == "-": s.current = "0"

def do_sign():
    try:
        v = float(s.current)
        s.current = fmt(-v)
    except: pass

# ── Render ────────────────────────────────────────────────────────────────────
st.markdown('<div class="calc-title">⬡ CALC·OS ⬡</div>', unsafe_allow_html=True)

# Mode toggle (radio)
mode = st.radio("", ["BASIC", "SCI"], horizontal=True,
                index=0 if s.mode == "basic" else 1,
                label_visibility="collapsed")
s.mode = "basic" if mode == "BASIC" else "sci"

# Display
is_err = "ERROR" in s.current
display_class = "display-main error" if is_err else "display-main"
st.markdown(f"""
<div class="display-wrap">
  <div class="display-history">{s.history or "&nbsp;"}</div>
  <div class="{display_class}">{s.current}</div>
</div>
""", unsafe_allow_html=True)

# ── Button factory ─────────────────────────────────────────────────────────────
def btn(label, key, cols, style="num"):
    with cols:
        if st.button(label, key=key, use_container_width=True):
            return True
    return False

# ── Scientific row ─────────────────────────────────────────────────────────────
if s.mode == "sci":
    sci_rows = [
        ["sin", "cos", "tan", "x²"],
        ["√",   "log", "ln",  "1/x"],
        ["π",   "e",   "|x|", "!"],
    ]
    for row in sci_rows:
        cols = st.columns(4)
        for i, fn in enumerate(row):
            if cols[i].button(fn, key=f"sci_{fn}", use_container_width=True):
                if fn in ("π", "e"):
                    do_sci(fn)
                    s.current = fmt(math.pi if fn == "π" else math.e)
                    s.fresh = True
                else:
                    do_sci(fn)
        st.write("")  # small gap
    st.divider()

# ── Main keypad ───────────────────────────────────────────────────────────────
rows = [
    [("AC","clear"), ("±","sign"), ("%","pct"), ("÷","op_div")],
    [("7","d7"),("8","d8"),("9","d9"),("×","op_mul")],
    [("4","d4"),("5","d5"),("6","d6"),("−","op_sub")],
    [("1","d1"),("2","d2"),("3","d3"),("+","op_add")],
    [("0","d0","span2"),(".","dot"),("=","eq","span2")],
]

for row in rows:
    # Determine column widths
    weights = []
    for item in row:
        if len(item) == 3 and item[2] == "span2":
            weights.append(2)
        else:
            weights.append(1)
    cols = st.columns(weights)
    for i, item in enumerate(row):
        label = item[0]
        key   = item[1]
        with cols[i]:
            if st.button(label, key=key, use_container_width=True):
                if label in "0123456789":
                    push_digit(label)
                elif label == ".":
                    push_digit(".")
                elif label == "AC":
                    do_clear()
                elif label == "⌫":
                    do_backspace()
                elif label == "±":
                    do_sign()
                elif label in ("+", "−", "×", "÷", "^"):
                    push_op(label)
                elif label == "%":
                    push_op("%")
                elif label == "=":
                    do_equals()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#333355;font-size:0.65rem;
            letter-spacing:0.15em;margin-top:1.5rem;">
CALC·OS v2.0 · POWERED BY STREAMLIT
</div>
""", unsafe_allow_html=True)
