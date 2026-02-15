from flask import Flask, render_template_string, abort, url_for

app = Flask(__name__)

WHATS = "5515996344228"
EMAIL_CONTATO = "fabiolirya.contato@gmail.com"
ENDERECO = "📍 Sitio Lirya, Bairro Aquinos Itaberá - SP (CEP: 18449-899)"
MENSAGEM_END = "Venha negociar conosco pessoalmente."

PRODUTOS = {
    "quiabo-aaa": {
        "nome": "Quiabo (AAA)",
        "preco": "R$ 90,00 / Caixa 16Kg",
        "imagem": "https://69910180681c79fa0bcd3223.imgix.net/quiabo%20top/quiabo%20top.jpg",
        "descricao": "Quiabo fresquinho, selecionado, qualidade AAA.",
        "origem": "Colhido no dia",
        "embalagem": "Caixa / a combinar",
    },
    "pepino-japones-aaa": {
        "nome": "Pepino Japonês (AAA)",
        "preco": "R$ 75,00 / Caixa 22Kg",
        "imagem": "https://69910180681c79fa0bcd3223.imgix.net/pepino%20top/pepino%20top.jpeg",
        "descricao": "Pepino japonês crocante e firme, ótimo para saladas e conservas.",
        "origem": "Colhido no dia",
        "embalagem": "Caixa / a combinar",
    },
    "maracuja-aaa": {
        "nome": "Maracujá (AAA)",
        "preco": "R$ 120,00 / Caixa 20Kg",
        "imagem": "https://69910180681c79fa0bcd3223.imgix.net/maracuja/maracu.jpg",
        "descricao": "Maracujá selecionado, bem maduro e perfumado.",
        "origem": "Colhido no dia",
        "embalagem": "Unidade / a combinar",
    },
}

# Lista pedida (somente texto) na página /produtos
LISTA_PRODUTOS_TEXTO = ["Quiabo", "Pepino Japonês", "Pimentão", "Abobrinha", "Maracujá"]

# ===== Galeria 3 imagens do Quiabo =====
# Troque IMG_2 e IMG_3 pelos links que você quiser (podem ser do Imgix também).
QUIABO_IMAGENS = [
    "https://69910180681c79fa0bcd3223.imgix.net/quiabo%20top/quiabo%20top.jpg",
    "https://69910180681c79fa0bcd3223.imgix.net/quiabo1223/20260208_111352.jpg",
    "https://69910180681c79fa0bcd3223.imgix.net/quiabo1223/20260208_144314.jpg",
]

BASE_CSS = r"""
<style>
/* ===== Tema (variáveis) ===== */
:root{
  --bg: #f9f9f9;
  --text: #333;
  --card: #ffffff;
  --muted: #444;
  --shadow: rgba(0,0,0,.08);
  --navbg: rgba(255,255,255,0.78);
  --navhover: rgba(0,0,0,0.08);
  --btn: #111;
  --btnText: #fff;
  --preco: #e67e22;
  --title: #2d5a27;
  --border: #eee;
}

body.dark{
  --bg: #0f1115;
  --text: #e7e7ea;
  --card: #161a22;
  --muted: #c9c9d1;
  --shadow: rgba(0,0,0,.45);
  --navbg: rgba(18,20,26,0.72);
  --navhover: rgba(255,255,255,0.10);
  --btn: #f2f2f2;
  --btnText: #0f1115;
  --preco: #ffb25c;
  --title: #b9f0b2;
  --border: rgba(255,255,255,0.12);
}

/* ===== Base ===== */
body{
  font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;
  margin:0;padding:0;
  background:var(--bg);
  color:var(--text);
}

header{
  background-image:url("https://69910180681c79fa0bcd3223.imgix.net/backgroundhorti/essatop.png");
  background-size:cover;background-position:center;background-repeat:no-repeat;
  padding:60px 20px;text-align:center; position: relative;
}
header h1{color:#000;margin:0}
.subtitulo{color:#000;font-size:18px;font-weight:400;margin-top:10px}

.container{max-width:1000px;margin:20px auto;padding:0 15px}

.vitrine{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}
.produto-card{
  background:var(--card);
  border-radius:12px;
  overflow:hidden;
  box-shadow:0 4px 8px rgba(0,0,0,.1);
  text-align:center;transition:.3s
}
.produto-card:hover{transform:translateY(-5px)}
.produto-img{
  width:100%;
  height:200px;
  object-fit:cover;
  cursor:zoom-in;
  transition:transform .3s ease,filter .25s ease;
}
.produto-img:hover{transform:scale(1.03);filter:brightness(.95)}

.info{padding:15px}
.info h3{margin:10px 0;color:var(--title)}
.preco{font-size:1.2em;font-weight:700;color:var(--preco);margin-bottom:15px}

.btn{display:inline-block;padding:10px 18px;border-radius:25px;text-decoration:none;font-weight:700;transition:.25s}
.btn-detalhes{background:var(--btn);color:var(--btnText)}
.btn-detalhes:hover{transform:translateY(-1px);opacity:.92}

.footer{text-align:center;padding:40px;color:#777;font-size:.9em}

.breadcrumb a{color:var(--btn);text-decoration:none}
.breadcrumb a:hover{text-decoration:underline}

/* ===== Menu no topo (canto superior direito) ===== */
.nav-topo{
  position:absolute;
  top:14px;
  right:18px;
  display:flex;
  gap:14px;
  align-items:center;
  padding:10px 12px;
  border-radius:999px;
  background: var(--navbg);
  backdrop-filter: blur(6px);
  box-shadow: 0 10px 22px rgba(0,0,0,0.08);
}
.nav-topo a{
  color:var(--text);
  text-decoration:none;
  font-weight:700;
  font-size:14px;
  padding:6px 10px;
  border-radius:999px;
  transition: .2s;
}
.nav-topo a:hover{ background: var(--navhover); }
.nav-topo a.ativo{ background:var(--btn); color:var(--btnText); }

/* ===== Botão do tema ===== */
.theme-toggle{
  border:none;
  background: transparent;
  cursor:pointer;
  width:34px;
  height:34px;
  border-radius:999px;
  display:grid;
  place-items:center;
  transition:.2s;
}
.theme-toggle:hover{ background: var(--navhover); transform: translateY(-1px); }
.theme-toggle .sun{ display:none; }
body.dark .theme-toggle .sun{ display:inline; }
body.dark .theme-toggle .moon{ display:none; }

/* ===== Páginas simples ===== */
.page-title{margin:18px 0 6px 0}
.lista-produtos{
  background:var(--card);
  border-radius:16px;
  padding:16px 18px;
  box-shadow:0 10px 24px var(--shadow);
}
.lista-produtos ul{margin:0;padding-left:18px;line-height:2}
.lista-produtos a{color:var(--text);font-weight:700;text-decoration:none}
.lista-produtos a:hover{text-decoration:underline}

.card{
  background:var(--card);
  border-radius:16px;
  padding:18px 18px 22px;
  box-shadow:0 10px 24px var(--shadow);
}
.contato-linha{margin:10px 0;color:var(--muted)}
hr{ border:none; border-top:1px solid var(--border) !important; margin:16px 0; }

.whats-btn{
  display:inline-flex;align-items:center;gap:10px;
  background:#25d366;color:#fff;text-decoration:none;
  padding:12px 16px;border-radius:12px;font-weight:800;
  box-shadow:0 10px 20px rgba(0,0,0,0.12);
  transition:.2s;
}
.whats-btn:hover{background:#128c7e;transform:translateY(-1px)}
.whats-icone{width:22px;height:22px;display:inline-block}

/* ===== Título "Destaques" (preto, como você pediu) ===== */
.secao-destaques{
  text-align:center;
  margin: 10px 0 12px;
  font-size: 22px;
  font-weight: 800;
  color: #000;
}

/* ===== Galeria 3 imagens (Quiabo) ===== */
.galeria-3{
  display:grid;
  grid-template-columns:repeat(3, 1fr);
  gap:14px;
  margin: 12px 0 16px;
}
.galeria-3 .produto-img{
  height: 260px;          /* ajuste se quiser mais alto/baixo */
  border-radius: 16px;
}
@media (max-width: 820px){
  .galeria-3{ grid-template-columns: 1fr; }
  .galeria-3 .produto-img{ height: 220px; }
}
</style>
"""

# ===== Script do Tema (vale para todas as páginas) =====
THEME_SCRIPT = r"""
<script>
(function(){
  const KEY = "fh_theme";
  const apply = (mode) => {
    document.body.classList.toggle("dark", mode === "dark");
  };

  const saved = localStorage.getItem(KEY);
  if(saved){
    apply(saved);
  } else {
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    apply(prefersDark ? "dark" : "light");
  }

  document.querySelectorAll("[data-theme-toggle]").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const isDark = document.body.classList.toggle("dark");
      localStorage.setItem(KEY, isDark ? "dark" : "light");
    });
  });
})();
</script>
"""

# ===== Lightbox (modal) com zoom no scroll =====
LIGHTBOX_HTML = r"""
<div id="modalImagem">
  <div id="modalConteudo">
    <button id="btnFechar" onclick="fecharModal()">×</button>
    <div id="areaImagem" title="Use a rodinha do mouse para dar zoom">
      <img id="imagemGrande" alt="Imagem ampliada">
    </div>
    <div id="legendaImagem"></div>
    <div id="dicaZoom">Dica: use a rodinha do mouse para zoom • duplo clique para 2x</div>
  </div>
</div>

<style>
#modalImagem{position:fixed;inset:0;display:none;justify-content:center;align-items:center;background:rgba(0,0,0,.8);
backdrop-filter:blur(4px);z-index:9999;padding:20px}
#modalImagem.ativo{display:flex;animation:fadeIn .18s ease-out}
#modalConteudo{position:relative;max-width:min(1100px,92vw);width:100%;display:flex;flex-direction:column;align-items:center;gap:10px;animation:zoomIn .22s ease-out}
#areaImagem{max-width:100%;max-height:80vh;overflow:hidden;border-radius:12px;box-shadow:0 20px 50px rgba(0,0,0,.5);background:#111}
#imagemGrande{display:block;max-width:100%;max-height:80vh;transform:scale(1);transform-origin:center center;transition:transform .06s ease-out;cursor:zoom-in;user-select:none;-webkit-user-drag:none}
#legendaImagem{color:#fff;text-align:center;opacity:.95;font-size:14px}
#btnFechar{position:absolute;top:-15px;right:-15px;background:rgba(255,255,255,.95);border:none;width:42px;height:42px;border-radius:50%;font-size:24px;cursor:pointer;
box-shadow:0 10px 22px rgba(0,0,0,.25);transition:transform .15s ease}
#btnFechar:hover{transform:scale(1.06)}
#dicaZoom{color:rgba(255,255,255,.85);font-size:12px;text-align:center}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes zoomIn{from{transform:scale(.98);opacity:0}to{transform:scale(1);opacity:1}}
</style>

<script>
let zoomAtual = 1;
const ZOOM_MIN = 1, ZOOM_MAX = 4, ZOOM_STEP = 0.18;

const modal = document.getElementById("modalImagem");
const imgGrande = document.getElementById("imagemGrande");
const legenda = document.getElementById("legendaImagem");
const areaImagem = document.getElementById("areaImagem");

function aplicarZoom(){
  imgGrande.style.transform = `scale(${zoomAtual})`;
  imgGrande.style.cursor = zoomAtual > 1 ? "zoom-out" : "zoom-in";
}
function resetZoom(){
  zoomAtual = 1;
  imgGrande.style.transformOrigin = "center center";
  aplicarZoom();
}
function abrirModal(src, textoLegenda){
  imgGrande.src = src;
  legenda.textContent = textoLegenda || "";
  resetZoom();
  modal.classList.add("ativo");
  document.body.style.overflow = "hidden";
}
function fecharModal(){
  modal.classList.remove("ativo");
  document.body.style.overflow = "auto";
  setTimeout(() => { imgGrande.src = ""; }, 150);
}
modal.addEventListener("click", (e)=>{ if(e.target === modal) fecharModal(); });
document.addEventListener("keydown", (e)=>{ if(e.key === "Escape" && modal.classList.contains("ativo")) fecharModal(); });

areaImagem.addEventListener("wheel", (e)=>{
  if(!modal.classList.contains("ativo")) return;
  e.preventDefault();
  const rect = areaImagem.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  imgGrande.style.transformOrigin = `${x}% ${y}%`;

  if(e.deltaY < 0) zoomAtual = Math.min(ZOOM_MAX, zoomAtual + ZOOM_STEP);
  else zoomAtual = Math.max(ZOOM_MIN, zoomAtual - ZOOM_STEP);
  aplicarZoom();
},{passive:false});

areaImagem.addEventListener("dblclick", (e)=>{
  const rect = areaImagem.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  imgGrande.style.transformOrigin = `${x}% ${y}%`;
  zoomAtual = (zoomAtual === 1) ? 2 : 1;
  aplicarZoom();
});
</script>
"""

def header_nav(active: str):
    # active: "home" | "produtos" | "contato"
    return render_template_string(r"""
    <div class="nav-topo">
      <button type="button" class="theme-toggle" data-theme-toggle aria-label="Alternar tema" title="Alternar tema">
        <span class="sun" aria-hidden="true">☀️</span>
        <span class="moon" aria-hidden="true">🌙</span>
      </button>

      <a href="{{ url_for('home') }}" class="{{ 'ativo' if active=='home' else '' }}">Página Inicial</a>
      <a href="{{ url_for('produtos') }}" class="{{ 'ativo' if active=='produtos' else '' }}">Produtos</a>
      <a href="{{ url_for('contato') }}" class="{{ 'ativo' if active=='contato' else '' }}">Contato</a>
    </div>
    """, active=active)

# ======= PÁGINA EXCLUSIVA DO QUIABO =======
QUIABO_PAGE = r"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quiabo (AAA) - Fabio's Hortifruti</title>
""" + BASE_CSS + r"""
</head>
<body>

<header>
  {{ nav|safe }}
  <h1>🍎 Fabio's Hortifruti</h1>
  <h2 class="subtitulo">Quiabo (AAA)</h2>
</header>

<div class="container">
  <p class="breadcrumb"><a href="{{ url_for('home') }}">← Voltar para as ofertas</a></p>

  <div class="card">
    <h2 class="page-title">Quiabo (AAA)</h2>
    <p class="preco">R$ 90,00 / Caixa 16Kg</p>

    <!-- ===== Título no local marcado (amarelo) ===== -->
    <h3 class="secao-destaques">Destaques</h3>

    <!-- ===== Galeria 3 imagens (com mesmo efeito da home) ===== -->
    <div class="galeria-3">
      {% for img in imagens %}
        <img src="{{ img }}"
             alt="Quiabo (AAA) - Foto {{ loop.index }}"
             class="produto-img"
             onclick="abrirModal(this.src, this.alt)">
      {% endfor %}
    </div>

    <p class="contato-linha"><b>Descrição:</b> Quiabo fresquinho, selecionado, qualidade AAA.</p>
    <p class="contato-linha"><b>Origem:</b> Colhido no dia</p>
    <p class="contato-linha"><b>Embalagem:</b> Caixa / a combinar</p>

    <a class="whats-btn" target="_blank" rel="noopener"
       href="https://wa.me/{{ whats }}?text=Olá!%20Tenho%20interesse%20no%20Quiabo%20(AAA).">
      <svg class="whats-icone" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">
        <path d="M19.11 17.06c-.27-.14-1.58-.78-1.82-.87-.25-.09-.43-.14-.6.14-.18.27-.69.87-.85 1.05-.16.18-.31.2-.58.07-.27-.14-1.15-.42-2.19-1.34-.81-.72-1.35-1.6-1.51-1.87-.16-.27-.02-.41.12-.55.12-.12.27-.31.4-.47.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.47-.07-.14-.6-1.45-.82-1.98-.22-.53-.44-.46-.6-.47h-.51c-.18 0-.47.07-.71.34-.25.27-.93.91-.93 2.22 0 1.31.96 2.58 1.09 2.76.14.18 1.89 2.88 4.58 4.03.64.28 1.14.44 1.53.56.64.2 1.22.17 1.68.1.51-.08 1.58-.65 1.8-1.28.22-.63.22-1.17.16-1.28-.07-.11-.25-.18-.51-.31z"/>
        <path d="M26.62 5.38A12.89 12.89 0 0 0 16.02 1C8.95 1 3.2 6.75 3.2 13.82c0 2.26.59 4.47 1.71 6.43L3 31l10.96-1.87a12.78 12.78 0 0 0 6.11 1.56h.01c7.07 0 12.82-5.75 12.82-12.82 0-3.42-1.33-6.63-3.75-9.05zM20.08 28.36h-.01a10.6 10.6 0 0 1-5.4-1.48l-.39-.23-6.5 1.11 1.08-6.33-.25-.41a10.6 10.6 0 1 1 11.47 7.34z"/>
      </svg>
      Pedir no WhatsApp
    </a>
  </div>
</div>

<div class="footer">
  <p>🍎 &copy; 2026 Fabio Lirya - Todos Os Direitos Reservados.</p>
</div>

""" + LIGHTBOX_HTML + THEME_SCRIPT + r"""
</body>
</html>
"""

HOME_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fabio's Hortifruti - Frescor na sua Mesa</title>
<link rel="icon" type="image/svg+xml"
href="data:image/svg+xml,
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 100'>
<text x='10' y='85' font-size='90'>🍎</text>
</svg>">
""" + BASE_CSS + r"""
</head>
<body>

<header>
  {{ nav|safe }}
  <h1>🍎 Fabio's Hortifruti</h1>
  <h2 class="subtitulo">Produtos Fresquinhos</h2>
</header>

<div class="container">
  <h2 style="text-align:center; margin-bottom:30px;">Nossas Ofertas</h2>

  <div class="vitrine">
    {% for slug, p in produtos.items() %}
    <div class="produto-card">
      <img src="{{ p.imagem }}" alt="{{ p.nome }}" class="produto-img"
           onclick="abrirModal(this.src, this.alt)">
      <div class="info">
        <h3>{{ p.nome }}</h3>
        <p class="preco">{{ p.preco }}</p>

        {# ===== AQUI: Quiabo vai para /quiabo; outros continuam /produto/<slug> ===== #}
        {% if slug == 'quiabo-aaa' %}
          <a class="btn btn-detalhes" href="{{ url_for('quiabo') }}">Ver detalhes</a>
        {% else %}
          <a class="btn btn-detalhes" href="{{ url_for('produto', slug=slug) }}">Ver detalhes</a>
        {% endif %}

      </div>
    </div>
    {% endfor %}
  </div>
</div>

<div class="footer">
  <p>🍎 &copy; 2026 Fabio Lirya - Todos Os Direitos Reservados.</p>
</div>

""" + LIGHTBOX_HTML + THEME_SCRIPT + r"""
</body>
</html>
"""

PRODUTO_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ p.nome }} - Fabio's Hortifruti</title>
""" + BASE_CSS + r"""
</head>
<body>

<header>
  {{ nav|safe }}
  <h1>🍎 Fabio's Hortifruti</h1>
  <h2 class="subtitulo">Detalhes do produto</h2>
</header>

<div class="container">
  <p class="breadcrumb"><a href="{{ url_for('home') }}">← Voltar para as ofertas</a></p>

  <div class="card">
    <h2 class="page-title">{{ p.nome }}</h2>
    <p class="preco">{{ p.preco }}</p>
    <img src="{{ p.imagem }}" alt="{{ p.nome }}" style="width:100%;max-height:420px;object-fit:cover;border-radius:16px;cursor:zoom-in"
         onclick="abrirModal(this.src, this.alt)">
    <p class="contato-linha"><b>Descrição:</b> {{ p.descricao }}</p>
    <p class="contato-linha"><b>Origem:</b> {{ p.origem }}</p>
    <p class="contato-linha"><b>Embalagem:</b> {{ p.embalagem }}</p>

    <a class="whats-btn" target="_blank" rel="noopener"
       href="https://wa.me/{{ whats }}?text=Olá!%20Tenho%20interesse%20no%20{{ p.nome|urlencode }}.">
      <svg class="whats-icone" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">
        <path d="M19.11 17.06c-.27-.14-1.58-.78-1.82-.87-.25-.09-.43-.14-.6.14-.18.27-.69.87-.85 1.05-.16.18-.31.2-.58.07-.27-.14-1.15-.42-2.19-1.34-.81-.72-1.35-1.6-1.51-1.87-.16-.27-.02-.41.12-.55.12-.12.27-.31.4-.47.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.47-.07-.14-.6-1.45-.82-1.98-.22-.53-.44-.46-.6-.47h-.51c-.18 0-.47.07-.71.34-.25.27-.93.91-.93 2.22 0 1.31.96 2.58 1.09 2.76.14.18 1.89 2.88 4.58 4.03.64.28 1.14.44 1.53.56.64.20 1.22.17 1.68.10.51-.08 1.58-.65 1.8-1.28.22-.63.22-1.17.16-1.28-.07-.11-.25-.18-.51-.31z"/>
        <path d="M26.62 5.38A12.89 12.89 0 0 0 16.02 1C8.95 1 3.2 6.75 3.2 13.82c0 2.26.59 4.47 1.71 6.43L3 31l10.96-1.87a12.78 12.78 0 0 0 6.11 1.56h.01c7.07 0 12.82-5.75 12.82-12.82 0-3.42-1.33-6.63-3.75-9.05zM20.08 28.36h-.01a10.6 10.6 0 0 1-5.4-1.48l-.39-.23-6.5 1.11 1.08-6.33-.25-.41a10.6 10.6 0 1 1 11.47 7.34z"/>
      </svg>
      Pedir no WhatsApp
    </a>
  </div>
</div>

<div class="footer">
  <p>🍎 &copy; 2026 Fabio Lirya - Todos Os Direitos Reservados.</p>
</div>

""" + LIGHTBOX_HTML + THEME_SCRIPT + r"""
</body>
</html>
"""

PRODUTOS_PAGE = r"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Produtos - Fabio's Hortifruti</title>
""" + BASE_CSS + r"""
</head>
<body>

<header>
  {{ nav|safe }}
  <h1>🍎 Fabio's Hortifruti</h1>
  <h2 class="subtitulo">Lista de Produtos</h2>
</header>

<div class="container">
  <div class="lista-produtos">
    <h2 class="page-title">Produtos</h2>
    <ul>
      {% for item in lista %}
        {% if item == "Quiabo" %}
          <li><a href="{{ url_for('quiabo') }}">Quiabo</a></li>
        {% else %}
          <li>{{ item }}</li>
        {% endif %}
      {% endfor %}
    </ul>
  </div>
</div>

<div class="footer">
  <p>🍎 &copy; 2026 Fabio Lirya - Todos Os Direitos Reservados.</p>
</div>

""" + THEME_SCRIPT + r"""
</body>
</html>
"""

CONTATO_PAGE = r"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contato - Fabio's Hortifruti</title>
""" + BASE_CSS + r"""
</head>
<body>

<header>
  {{ nav|safe }}
  <h1>🍎 Fabio's Hortifruti</h1>
  <h2 class="subtitulo">Fale com a gente</h2>
</header>

<div class="container">
  <div class="card">
    <h2 class="page-title">Contato</h2>

    <a class="whats-btn" target="_blank" rel="noopener"
       href="https://wa.me/{{ whats }}">
      <svg class="whats-icone" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">
        <path d="M19.11 17.06c-.27-.14-1.58-.78-1.82-.87-.25-.09-.43-.14-.6.14-.18.27-.69.87-.85 1.05-.16.18-.31.2-.58.07-.27-.14-1.15-.42-2.19-1.34-.81-.72-1.35-1.6-1.51-1.87-.16-.27-.02-.41.12-.55.12-.12.27-.31.4-.47.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.47-.07-.14-.6-1.45-.82-1.98-.22-.53-.44-.46-.6-.47h-.51c-.18 0-.47.07-.71.34-.25.27-.93.91-.93 2.22 0 1.31.96 2.58 1.09 2.76.14.18 1.89 2.88 4.58 4.03.64.28 1.14.44 1.53.56.64.20 1.22.17 1.68.10.51-.08 1.58-.65 1.8-1.28.22-.63.22-1.17.16-1.28-.07-.11-.25-.18-.51-.31z"/>
        <path d="M26.62 5.38A12.89 12.89 0 0 0 16.02 1C8.95 1 3.2 6.75 3.2 13.82c0 2.26.59 4.47 1.71 6.43L3 31l10.96-1.87a12.78 12.78 0 0 0 6.11 1.56h.01c7.07 0 12.82-5.75 12.82-12.82 0-3.42-1.33-6.63-3.75-9.05zM20.08 28.36h-.01a10.6 10.6 0 0 1-5.4-1.48l-.39-.23-6.5 1.11 1.08-6.33-.25-.41a10.6 10.6 0 1 1 11.47 7.34z"/>
      </svg>
      WhatsApp: +55 15 99634-4228
    </a>

    <p class="contato-linha"><b>E-mail:</b> {{ email }}</p>

    <hr>

    <p class="contato-linha"><b>Endereço:</b> {{ endereco }}</p>
    <p class="contato-linha">{{ msg_end }}</p>
  </div>
</div>

<div class="footer">
  <p>🍎 &copy; 2026 Fabio Lirya - Todos Os Direitos Reservados.</p>
</div>

""" + THEME_SCRIPT + r"""
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HOME_TEMPLATE,
        produtos=PRODUTOS,
        nav=header_nav("home"),
    )

# ROTA EXCLUSIVA DO QUIABO
@app.route("/quiabo")
def quiabo():
    return render_template_string(
        QUIABO_PAGE,
        whats=WHATS,
        nav=header_nav("produtos"),
        imagens=QUIABO_IMAGENS,
    )

@app.route("/produto/<slug>")
def produto(slug):
    p = PRODUTOS.get(slug)
    if not p:
        abort(404)
    return render_template_string(
        PRODUTO_TEMPLATE,
        p=p,
        whats=WHATS,
        nav=header_nav("produtos"),
    )

@app.route("/produtos")
def produtos():
    return render_template_string(
        PRODUTOS_PAGE,
        lista=LISTA_PRODUTOS_TEXTO,
        nav=header_nav("produtos"),
    )

@app.route("/contato")
def contato():
    return render_template_string(
        CONTATO_PAGE,
        whats=WHATS,
        email=EMAIL_CONTATO,
        endereco=ENDERECO,
        msg_end=MENSAGEM_END,
        nav=header_nav("contato"),
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)