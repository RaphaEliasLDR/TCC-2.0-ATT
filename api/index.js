const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { body, validationResult } = require('express-validator');
const morgan = require('morgan');

const app = express();
app.use(morgan('dev'));
const port = 3000;
const uploadDir = path.join(__dirname, 'uploads');

app.use(cors());
app.use(express.json());

if (!fs.existsSync(uploadDir)){
    fs.mkdirSync(uploadDir);
}

// Servir a pasta uploads como pública
app.use('/uploads', express.static(uploadDir));

// Configuração do multer com limites e filtro
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadDir);
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});


const upload = multer({
    storage: storage,
});

const { v4: uuidv4 } = require('uuid');

const pratos = [];
const funcionarios = [];

// PUT /pratos/:id - Atualização com validação
app.put('/pratos/:id',
    upload.single('imagem'),
    [
        body('nome').isLength({ min: 1 }).withMessage('Nome é obrigatório'),
        body('preco').isFloat({ gt: 0 }).withMessage('Preço deve ser um número positivo'),
        body('categoria').isLength({ min: 1 }).withMessage('Categoria é obrigatória')
    ],
    (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            if (req.file) {
                fs.unlinkSync(path.join(uploadDir, req.file.filename));
            }
            return res.status(400).json({ erros: errors.array() });
        }

        const { id } = req.params;
        const { nome, preco, categoria } = req.body;

        const pratoIndex = pratos.findIndex(p => p.id === id);
        if (pratoIndex === -1) {
            if (req.file) {
                fs.unlinkSync(path.join(uploadDir, req.file.filename));
            }
            return res.status(404).json({ erro: true, mensagem: 'Prato não encontrado' });
        }

        // Remover imagem antiga se nova imagem foi enviada
        if (req.file) {
            const imagemAntiga = pratos[pratoIndex].imagem;
            if (imagemAntiga) {
                const caminhoImagemAntiga = path.join(uploadDir, imagemAntiga);
                if (fs.existsSync(caminhoImagemAntiga)) {
                    fs.unlinkSync(caminhoImagemAntiga);
                }
            }
            pratos[pratoIndex].imagem = req.file.filename;
        }

        // Atualizar os dados
        pratos[pratoIndex] = {
            ...pratos[pratoIndex],
            nome,
            preco: parseFloat(preco),
            categoria
        };

        res.json({ mensagem: 'Prato atualizado', dados: pratos[pratoIndex] });
    }
);


app.post('/pratos', 
    // Middleware multer para upload e tratamento de erro do multer
    (req, res, next) => {
        upload.single('imagem')(req, res, function(err) {
            if (err instanceof multer.MulterError) {
                return res.status(400).json({ erro: true, mensagem: err.message });
            } else if (err) {
                return res.status(400).json({ erro: true, mensagem: err.message });
            }
            next();
        });
    },


    // Validação dos campos com express-validator
    [
        body('nome').isLength({ min: 1 }).withMessage('Nome é obrigatório'),
        body('preco').isFloat({ gt: 0 }).withMessage('Preço deve ser um número positivo'),
        body('categoria').isLength({ min: 1 }).withMessage('Categoria é obrigatória')
    ],
    (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            // Se tiver erros na validação, deleta o arquivo enviado para evitar lixo
            if (req.file) {
                fs.unlinkSync(path.join(uploadDir, req.file.filename));
            }
            return res.status(400).json({ erros: errors.array() });
        }

        if (!req.file) {
            return res.status(400).json({ erro: true, mensagem: 'Imagem é obrigatória' });
        }

        const { nome, preco, categoria } = req.body;
        const imagem = req.file.filename;

        const prato = {  id: uuidv4(), nome, preco, categoria, imagem };
        pratos.push(prato);

        return res.status(201).json({
            mensagem: 'Prato cadastrado com sucesso',
            dados: prato
        });
    }
);

app.delete('/pratos/:id', (req, res) => {
  const { id } = req.params;
  const pratoIndex = pratos.findIndex(p => p.id === id);

  if (pratoIndex === -1) {
    return res.status(404).json({ erro: true, mensagem: 'Prato não encontrado' });
  }

  // Remove imagem do prato, se existir
  const imagem = pratos[pratoIndex].imagem;
  if (imagem) {
    const caminhoImagem = path.join(uploadDir, imagem);
    if (fs.existsSync(caminhoImagem)) {
      fs.unlinkSync(caminhoImagem);
    }
  }

  // Remove o prato do array
  pratos.splice(pratoIndex, 1);

  res.json({ mensagem: 'Prato removido com sucesso' });
});


app.get('/pratos', (req, res) => {
    res.json(pratos);
});


// Validação básica para funcionários
const funcionarioValidation = [
  body('nome').isLength({ min: 1 }).withMessage('Nome é obrigatório'),
  body('cpf').isLength({ min: 11, max: 14 }).withMessage('CPF inválido'),
  body('cargo').isLength({ min: 1 }).withMessage('Cargo é obrigatório'),
  body('telefone').isLength({ min: 8 }).withMessage('Telefone inválido'),
];

// GET /funcionarios - Listar funcionários
app.get('/funcionarios', (req, res) => {
  res.json(funcionarios);
});

// POST /funcionarios - Criar funcionário
app.post('/funcionarios', funcionarioValidation, (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ erros: errors.array() });
  }

  const { nome, cpf, cargo, telefone } = req.body;

  const funcionario = {
    id: uuidv4(),
    nome,
    cpf,
    cargo,
    telefone
  };

  funcionarios.push(funcionario);

  res.status(201).json({
    mensagem: 'Funcionário cadastrado com sucesso',
    dados: funcionario
  });
});

// PUT /funcionarios/:id - Atualizar funcionário
app.put('/funcionarios/:id', funcionarioValidation, (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ erros: errors.array() });
  }

  const { id } = req.params;
  const { nome, cpf, cargo, telefone } = req.body;

  const funcionarioIndex = funcionarios.findIndex(f => f.id === id);
  if (funcionarioIndex === -1) {
    return res.status(404).json({ erro: true, mensagem: 'Funcionário não encontrado' });
  }

  funcionarios[funcionarioIndex] = {
    ...funcionarios[funcionarioIndex],
    nome,
    cpf,
    cargo,
    telefone
  };

  res.json({
    mensagem: 'Funcionário atualizado com sucesso',
    dados: funcionarios[funcionarioIndex]
  });
});

// DELETE /funcionarios/:id - Deletar funcionário
app.delete('/funcionarios/:id', (req, res) => {
  const { id } = req.params;

  const funcionarioIndex = funcionarios.findIndex(f => f.id === id);
  if (funcionarioIndex === -1) {
    return res.status(404).json({ erro: true, mensagem: 'Funcionário não encontrado' });
  }

  funcionarios.splice(funcionarioIndex, 1);

  res.json({ mensagem: 'Funcionário removido com sucesso' });
});



app.listen(port, () => {
    console.log(`API rodando em http://localhost:${port}`);
});

process.on('uncaughtException', (err) => {
  console.error('Erro não tratado:', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Promessa rejeitada não tratada:', reason);
});
