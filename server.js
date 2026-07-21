const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Configuração para desativar a cache no navegador e garantir atualização instantânea
app.use(express.static(path.join(__dirname, 'public'), {
    etag: false,
    maxAge: 0,
    setHeaders: (res) => {
        res.set('Cache-Control', 'no-store, no-cache, must-revalidate, private');
    }
}));

const projetos = [
    { id: 1, name: 'Projeto Eterno-World', platform: 'Ativo - Web' },
    { id: 2, name: 'Mapeamento de Mídia', platform: 'Em Desenvolvimento' },
    { id: 3, name: 'Sistema de Automação', platform: 'Concluído' }
];

app.get('/api/projects', (req, res) => {
    res.json(projetos);
});

app.listen(PORT, () => {
    console.log(`Servidor ativo na porta ${PORT}`);
});
