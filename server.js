const express = require('express');
const path = require('path');
const app = express();

// Lê a porta da nuvem (Render) ou usa a 3000 no computador/celular
const PORT = process.env.PORT || 3000;

// Servir os arquivos estáticos da pasta public
app.use(express.static(path.join(__dirname, 'public')));

// Dados de exemplo dos projetos
const projetos = [
    { id: 1, name: 'Projeto Eterno-World', platform: 'Ativo - Web' },
    { id: 2, name: 'Mapeamento de Mídia', platform: 'Em Desenvolvimento' },
    { id: 3, name: 'Sistema de Automação', platform: 'Concluído' }
];

// Rota da API
app.get('/api/projects', (req, res) => {
    res.json(projetos);
});

app.listen(PORT, () => {
    console.log(`Servidor ativo na porta ${PORT}`);
});
