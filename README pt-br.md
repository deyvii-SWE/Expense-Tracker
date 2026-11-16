# Expense Tracker 0.5

## Como Funciona

Este é um programa desenvolvido para ajudar você a gerenciar suas finanças pessoais. É possível registrar despesas, consultar o total e a média dos gastos, alterar a moeda e muito mais.

O programa oferece suporte a uma grande variedade de moedas, que podem ser selecionadas nas configurações. Quando um novo mês começa, um novo arquivo é criado para ele. Mas não se preocupe, você ainda poderá acessar os meses anteriores e suas estatísticas pelas configurações (essa funcionalidade ainda não foi implementada).

## Sobre o Código

Dessa vez, o projeto foi um pouco mais complexo, então decidi separar algumas classes do código principal. Agora temos três classes: `Config`, `Storage` e `Interface`, cada uma com suas próprias responsabilidades.

Também tentei ao máximo garantir que, caso alguma pasta ou arquivo seja deletado por algum motivo, o programa consiga recriá-lo. Por isso, ele já começa com algumas verificações.

Para o `match`, decidi criar funções separadas para cada opção, mantendo os blocos de código organizados e independentes.

Na interface e nas outras funções, também tentei deixar tudo mais flexível e reutilizável, mantendo eficiência e facilidade de manutenção em mente.

Uma das partes mais divertidas foi criar a Page Interface! Temos páginas nas configurações, ao alterar moedas, e também na lista de despesas, onde podemos navegar por tudo. Cada página possui 10 itens, e você pode avançar, voltar, editar despesas e muito mais.

Pelo menos os dados são persistentes!

Você pode fazer alterações, adicionar despesas, editar configurações e, quando abrir o programa novamente, tudo continuará lá, salvo em JSON.

Eu poderia ter reduzido bastante coisa e feito algumas partes funcionarem melhor, mas decidi manter o código mais direto e simples para entender melhor como as coisas funcionam.

No geral, foi uma ótima oportunidade para aprender como várias coisas funcionam por trás dos panos, melhorar minha organização e lógica, além de expandir meu conhecimento. Também aprendi sobre Babel, JSON, datetime e várias outras bibliotecas.

Esse é atualmente meu maior projeto de programação, e estou realmente orgulhoso de como ele ficou!
