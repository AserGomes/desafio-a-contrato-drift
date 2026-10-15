# Desafio A — Contrato de Dados e Bloqueio Preventivo de Data Drift

## Problema de Negócio

Um dashboard executivo de vendas passou a mostrar números errados após mudanças silenciosas na fonte de dados. O time de dados precisava de uma forma de detectar e bloquear dados corrompidos antes que chegassem ao dashboard.

## Solução

Implementação de um contrato de dados versionado e um validador que executa antes de qualquer publicação. Se o dado violar o contrato, o pipeline é bloqueado e o time é alertado.
