// Controller para lidar com os pratos
const pratoController = {
  adicionarPrato: (req, res) => {
    const { nome, descricao, preco } = req.body;

    // Aqui você poderia adicionar lógica para validar os dados
    if (!nome || !descricao || !preco) {
      return res.status(400).json({ mensagem: 'Preencha todos os campos!' });
    }

    // Supondo que você tenha um banco de dados para salvar o prato
    // Aqui você pode fazer a lógica de salvar o prato no banco de dados

    // Exemplo de resposta de sucesso
    res.status(201).json({
      mensagem: 'Prato adicionado com sucesso!',
      prato: { nome, descricao, preco }
    });
  }
};

module.exports = pratoController;
