const express = require('express');
const router = express.Router();
const pratoController = require('../controllers/pratoController');



// Definindo a rota para adicionar um prato
router.post('/', pratoController.adicionarPrato);

module.exports = router;
