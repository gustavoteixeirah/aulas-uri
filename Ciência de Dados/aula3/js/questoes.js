/* =========================================================
   Aula 03 — banco de questões (múltipla escolha)
   Cada questão vira 2 slides: enunciado + resposta comentada.
   O campo `grupo` casa com <div data-quiz="..."> no index.html.

   Três questões curtas, todas conferidas rodando no NumPy.
   ========================================================= */
window.QUESTOES = [

  {
    grupo: 'fim', tema: 'Lista × array',
    texto: 'O que cada linha imprime?',
    codigo: 'print([1, 2, 3] * 2)\nprint(np.array([1, 2, 3]) * 2)',
    alts: [
      '<code>[2, 4, 6]</code> · <code>[2 4 6]</code>',
      '<code>[1, 2, 3, 1, 2, 3]</code> · <code>[2 4 6]</code>',
      '<code>[1, 2, 3, 1, 2, 3]</code> · <code>[1 2 3 1 2 3]</code>',
      'Erro na primeira linha'
    ],
    correta: 1,
    porque: 'Na lista, <code>* 2</code> quer dizer <b>repita a lista</b>. No array, <b>multiplique cada valor</b>. É a aula inteira num exemplo.'
  },
  {
    grupo: 'fim', tema: 'Filtrar',
    texto: 'O que sai aqui?',
    codigo: 'tarifa = np.array([12, 45, 8, 60])\n\nprint(tarifa[tarifa &gt; 30])',
    alts: [
      '<code>[False True False True]</code>',
      '<code>[45 60]</code>',
      '<code>2</code>',
      '<code>[12 8]</code>'
    ],
    correta: 1,
    porque: 'Sai <b>[45 60]</b> — os valores que passaram. Sozinho, <code>tarifa &gt; 30</code> devolve <code>True</code>/<code>False</code>; dentro dos colchetes, vira <b>filtro</b>.'
  },
  {
    grupo: 'fim', tema: 'Contar',
    texto: 'Quanto vale <code>n</code>?',
    codigo: 'tarifa = np.array([12, 45, 8, 60])\n\nn = (tarifa &gt; 30).sum()',
    alts: ['<code>2</code>', '<code>105</code>', '<code>True</code>', '<code>[45 60]</code>'],
    correta: 0,
    porque: '<b>2</b>. <code>True</code> vale 1 e <code>False</code> vale 0 — <b>somar é contar</b>. Com <code>.mean()</code> no lugar, vem a <b>proporção</b>: 0,5.'
  }
];
