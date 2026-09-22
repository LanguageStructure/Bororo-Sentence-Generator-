# Bororo Sentence Generator

Gerador experimental de sentenças em **Boe-Bororo** baseado em evidência linguística do **CorBo — Corpus da Língua Bororo**.

O projeto investiga até que ponto um corpus de tamanho limitado, combinado com anotação morfossintática e regras linguísticas explícitas, permite gerar novas sentenças de maneira controlada, rastreável e reproduzível.

## Princípios

O gerador não trata a saída de um modelo de linguagem como evidência gramatical. O **CorBo é a fonte de dados**; regras e padrões derivados do corpus controlam a geração.

Cada saída deverá ser classificada como:

- **attested** — sentença efetivamente documentada no CorBo;
- **recombined** — nova combinação lexical em uma estrutura atestada;
- **generated** — sentença nova licenciada por regras explícitas.

Toda sentença gerada deverá, sempre que possível, registrar sua proveniência: padrão sintático, formas utilizadas, regras aplicadas e sentenças do corpus que sustentam a construção.

## Arquitetura inicial

```text
Bororo-Sentence-Generator/
├── data/
│   └── corbo/
├── rules/
│   ├── syntax.yaml
│   ├── morphology.yaml
│   └── valency.yaml
├── src/
│   ├── corpus.py
│   ├── patterns.py
│   ├── lexicon.py
│   ├── morphology.py
│   ├── generator.py
│   ├── validator.py
│   └── provenance.py
├── tests/
└── docs/
```

## Etapas

1. Ler o CoNLL-U do CorBo.
2. Extrair padrões sintáticos recorrentes.
3. Identificar os padrões mais frequentes e produtivos.
4. Construir um léxico a partir das formas e lemas atestados.
5. Acrescentar restrições de valência e morfologia.
6. Gerar recombinações conservadoras.
7. Validar as saídas contra regras explícitas e evidência do corpus.
8. Introduzir, posteriormente, componentes de IA apenas onde acrescentem valor.

## Complexidade

A interface deverá permitir geração em diferentes níveis de complexidade, desde predicações mínimas até construções com complementação, modificação e subordinação. Os níveis serão definidos empiricamente a partir das estruturas encontradas no CorBo.

## Fonte dos dados

CorBo — Corpus da Língua Bororo, versão 0.7.  
DOI: 10.5281/zenodo.12110451

Os dados do CorBo permanecem em seu próprio repositório. Este projeto os consome como fonte externa e não substitui nem modifica a documentação original.

## Estado

Protótipo experimental em desenvolvimento.
