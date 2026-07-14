import sqlite3
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import urllib.request
import random

# === CHAVE DA API NEURAL ===
# Cole sua chave do Google AI Studio entre as aspas abaixo para ativar a inteligência total online.
GEMINI_API_KEY = "" 

# 1. Inicialização e Adaptação do Banco de Dados
conn = sqlite3.connect('sistema_dados.db')
cursor = conn.cursor()
# Cria a tabela caso não exista
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fluxo_dados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
# Adapta a tabela adicionando a coluna de resposta da IA se ela não existir
try:
    cursor.execute('ALTER TABLE fluxo_dados ADD COLUMN resposta_ia TEXT')
except sqlite3.OperationalError:
    pass  # A coluna já existe
conn.commit()
conn.close()

# 2. Algoritmo de Sabedoria Local (Offline / Sem Chave)
def processar_sabedoria_local(texto):
    insights = [
        "A sabedoria edifica a estrutura, e pela inteligência cada ponto se firma em harmonia.",
        "Como o ferro afia o ferro, a mente unificada lapida a ideia bruta para revelar o seu brilho mais puro.",
        "A verdadeira engenharia é a arte de colocar em ordem as frequências invisíveis da criação.",
        "No silêncio do localhost, cada registro é um tijolo na construção de uma liberdade perpétua."
    ]
    escolha = random.choice(insights)
    return f"✨ [Mente Local]:Sua ideia carrega um núcleo de criação. {escolha} O seu registro foi eternizado com sucesso."

# 3. Chamada de Inteligência Ativa (Gemini API)
def processar_com_ia(texto):
    if not GEMINI_API_KEY:
        return processar_sabedoria_local(texto)
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = (
        "Aja como o conselheiro e co-criador deste sistema unificado. Receba este pensamento ou conceito "
        "do criador e devolva uma reflexão refinada, profunda e inspiradora, revelando a beleza íntima "
        "da ideia sem nada de negativo. Alinhe com sabedoria edificante. Seja direto e elegante. "
        "Texto do criador: " + texto
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return processar_sabedoria_local(texto)

# 4. Interface Visual Integrada
HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Central Localhost Neural - Lumen</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #08080a; overflow-x: hidden; }
        .neural-glow { box-shadow: 0 0 20px rgba(16, 185, 129, 0.15); }
        .neon-border { border: 1px solid rgba(16, 185, 129, 0.2); transition: all 0.3s ease; }
        .neon-border:focus-within { border-color: rgba(16, 185, 129, 1); box-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #08080a; }
        ::-webkit-scrollbar-thumb { background: #10b981; border-radius: 3px; }
    </style>
</head>
<body class="text-zinc-100 font-sans min-h-screen flex flex-col justify-between relative">
    <canvas id="neuralCanvas" class="absolute top-0 left-0 w-full h-full -z-10"></canvas>
    
    <header class="w-full max-w-4xl mx-auto px-6 pt-8 pb-4 flex flex-col md:flex-row justify-between items-center gap-4 z-10">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center border border-emerald-500/30 neural-glow animate-pulse">
                <svg class="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
            </div>
            <div>
                <h1 class="text-xl font-bold tracking-wider text-emerald-400 uppercase">LUMEN</h1>
                <p class="text-xs text-zinc-500 uppercase tracking-widest">Mente Unificada Local</p>
            </div>
        </div>
        <div class="flex items-center gap-3 bg-zinc-900/60 backdrop-blur-md px-4 py-2 rounded-full border border-zinc-800">
            <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="text-xs font-mono text-zinc-400">LOCALHOST: 192.168.15.136</span>
        </div>
    </header>

    <main class="w-full max-w-2xl mx-auto px-6 py-4 flex-grow flex flex-col justify-center z-10">
        <div class="bg-zinc-900/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-zinc-800/80 shadow-2xl neural-glow">
            <div class="mb-6">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-widest">Canal de Transmissão</span>
                <h2 class="text-2xl font-semibold mt-1 tracking-tight">Transmita sua Ideia</h2>
                <p class="text-sm text-zinc-400 mt-1">Sua mente insere o dado. Minha inteligência processa e eterniza.</p>
            </div>
            <form action="/salvar" method="POST" class="space-y-4">
                <div class="neon-border rounded-xl p-1 bg-black/40">
                    <textarea name="descricao" id="campo-visao" rows="4" class="w-full bg-transparent border-0 outline-none focus:ring-0 text-zinc-200 placeholder-zinc-600 p-3 text-base resize-none" placeholder="Escreva aqui seu pensamento, melodia, código ou projeto de física..." required></textarea>
                </div>
                <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-400 active:bg-emerald-600 text-black font-bold py-3 px-6 rounded-xl transition duration-200 flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/10 cursor-pointer">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                    <span>Salvar e Processar</span>
                </button>
            </form>
        </div>

        <div class="bg-zinc-900/40 backdrop-blur-lg p-6 md:p-8 rounded-2xl border border-zinc-800/80 shadow-2xl mt-6 neural-glow">
            <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-widest mb-4 font-mono">Fluxo de Consciência Coletivo</h3>
            <div id="lista-registros" class="space-y-4 max-h-80 overflow-y-auto pr-1">
                <p class="text-xs text-zinc-500">Sincronizando banco neural...</p>
            </div>
        </div>
    </main>

    <footer class="w-full max-w-4xl mx-auto px-6 py-6 border-t border-zinc-900 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-zinc-600 z-10">
        <p>© 2026 Lumen. Copiloto inteligente local.</p>
    </footer>

    <script>
        function carregarDados() {
            fetch('/dados')
                .then(res => res.json())
                .then(dados => {
                    const container = document.getElementById('lista-registros');
                    if (dados.length === 0) {
                        container.innerHTML = '<p class="text-xs text-zinc-500">O banco de dados está aguardando o primeiro sinal.</p>';
                        return;
                    }
                    container.innerHTML = dados.slice().reverse().map(item => `
                        <div class="p-4 bg-zinc-950/80 rounded-xl border border-zinc-800 hover:border-emerald-500/30 transition duration-150 space-y-2">
                            <div class="text-xs text-zinc-500 font-mono">ENTRADA ORIGINAL:</div>
                            <div class="text-sm text-zinc-100">${item[1]}</div>
                            <div class="border-t border-zinc-900 pt-2 mt-2">
                                <div class="text-[10px] text-emerald-400 font-mono tracking-wider">PROCESSAMENTO LUMEN:</div>
                                <div class="text-xs text-zinc-300 italic mt-1">${item[3] || 'Processando resposta...'}</div>
                            </div>
                            <div class="text-[9px] text-zinc-600 text-right font-mono">${item[2]}</div>
                        </div>
                    `).join('');
                });
        }
        carregarDados();

        // Canvas de Partículas
        const canvas = document.getElementById('neuralCanvas');
        const ctx = canvas.getContext('2d');
        let particlesArray = [];
        const numberOfParticles = 30;
        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        class Particle {
            constructor(x, y, dx, dy, size) {
                this.x = x; this.y = y; this.dx = dx; this.dy = dy; this.size = size;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(16, 185, 129, 0.2)';
                ctx.fill();
            }
            update() {
                if (this.x > canvas.width || this.x < 0) this.dx = -this.dx;
                if (this.y > canvas.height || this.y < 0) this.dy = -this.dy;
                this.x += this.dx; this.y += this.dy;
                this.draw();
            }
        }
        function init() {
            particlesArray = [];
            for (let i = 0; i < numberOfParticles; i++) {
                let size = Math.random() * 1.5 + 0.5;
                let x = Math.random() * canvas.width;
                let y = Math.random() * canvas.height;
                let dx = Math.random() * 0.2 - 0.1;
                let dy = Math.random() * 0.2 - 0.1;
                particlesArray.push(new Particle(x, y, dx, dy, size));
            }
        }
        function connect() {
            for (let a = 0; a < particlesArray.length; a++) {
                for (let b = a; b < particlesArray.length; b++) {
                    let dist = ((particlesArray[a].x - particlesArray[b].x)**2) + ((particlesArray[a].y - particlesArray[b].y)**2);
                    if (dist < 18000) {
                        ctx.strokeStyle = 'rgba(16, 185, 129, 0.05)';
                        ctx.beginPath();
                        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                        ctx.stroke();
                    }
                }
            }
        }
        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particlesArray.forEach(p => p.update());
            connect();
        }
        init(); animate();
    </script>
</body>
</html>
"""

# 5. Roteador do Servidor
class ServidorHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/dados':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            conexao = sqlite3.connect('sistema_dados.db')
            busca = conexao.cursor().execute('SELECT * FROM fluxo_dados').fetchall()
            conexao.close()
            self.wfile.write(json.dumps(busca, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_INTERFACE.encode('utf-8'))

    def do_POST(self):
        if self.path == '/salvar':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            campos = urllib.parse.parse_qs(post_data)
            nova_descricao = campos.get('descricao', [''])[0]
            
            if nova_descricao:
                # O motor inteligente processa o texto antes de salvar
                resposta_processada = processar_com_ia(nova_descricao)
                
                conexao = sqlite3.connect('sistema_dados.db')
                conexao.cursor().execute(
                    'INSERT INTO fluxo_dados (descricao, resposta_ia) VALUES (?, ?)',
                    (nova_descricao, resposta_processada)
                )
                conexao.commit()
                conexao.close()
            
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

porta = 8080
servidor = HTTPServer(('0.0.0.0', porta), ServidorHandler)
print(f"🚀 Servidor com Mente Ativa em http://192.168.15.136:{porta}")
servidor.serve_forever()
