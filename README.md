# Bororo Sentence Generator

[![DOI](https://zenodo.org/badge/1382167262.svg)](https://doi.org/10.5281/zenodo.22941512)

Gerador experimental de sentenças em **Boe-Bororo**, desenvolvido a partir do **CorBo — Corpus da Língua Bororo**.

O projeto implementa uma arquitetura de **evidence-bounded generation**: evidência de corpus, análise linguística humana, licença gramatical, geração e atestação posterior são mantidas como camadas distintas. Uma forma encontrada no corpus não se torna automaticamente uma regra produtiva, e ausência no corpus não é interpretada como agramaticalidade.

## Princípio

O fluxo central é:

```text
CorBo
  → corpus evidence
  → human linguistic review
  → reviewed grammar
  → controlled generator
  → generated candidate
  → validation / corpus attestation
```

Somente análises explicitamente revisadas podem criar licenças de geração. Casos incertos permanecem incertos em vez de serem completados por analogia.

A interface experimental de linguagem natural acrescenta uma camada anterior ao gerador:

```text
Portuguese / English input
  → structured, language-neutral intent
  → deterministic licensing and validation
  → controlled Bororo realization
```

A camada de IA interpreta intenção; ela não cria morfologia Bororo, não inventa predicados Bororo e não concede novas licenças gramaticais.

## Componentes

A versão pública inclui:

- `src/bororo_generator/` — implementação do gerador e da avaliação;
- `scripts/` — utilitários de geração, diagnóstico, auditoria e avaliação;
- `tests/` — testes automatizados;
- `reports/grammar-v2-holdout-manifest.json` — manifest do split documental congelado;
- `reports/GRAMMAR_V2_HOLDOUT.md` — documentação da avaliação held-out;
- `docs/HUMAN_ADJUDICATION_PROTOCOL.md` — protocolo formal de adjudicação humana;
- `data/corbo/README.md` — documentação da relação com o CorBo;
- `docs/DATA_POLICY.md` — política de dados.

Dados documentais, análises linguísticas privadas, adjudicações humanas e dados gold experimentais não são distribuídos neste repositório.

## Gramática revisada

As licenças distinguem evidência lexical, morfológica e construcional. Entre outras coisas, o sistema mantém separados:

- paradigmas ou classes de radical explicitamente revisados;
- células de pessoa individualmente revisadas;
- quadros de valência;
- construções específicas;
- restrições morfotáticas;
- atestação de corpus.

A atestação posterior de uma forma gerada é evidência observacional, não uma atualização automática da gramática.

## Avaliação

A avaliação é decomposta porque os experimentos respondem a perguntas diferentes. **Functional correctness**, **coverage**, **compatibility** e **generalization** não são tratados como sinônimos.

| Componente | Material | O que testa | Escopo |
| --- | --- | --- | --- |
| Controlled baseline | casos licenciados | realização determinística das estruturas já revisadas | functional correctness dentro da gramática |
| Direct vs. evidence-bounded LLM | tarefas congeladas da grammar-v1 | efeito do gating baseado em evidência na configuração testada | comparação controlada, não avaliação geral de LLMs |
| Natural-language intent challenge | 30 casos PT/EN congelados | interpretação → intent → decisão determinística | agreement no challenge set, não accuracy irrestrita |
| Grammar boundary challenge | 84 casos: 28 positivos, 28 negativos, 28 boundary | limites de decisão e comportamento fail-closed | teste interno/regressão, não generalização independente |
| Source-group holdout | 157 sentenças; 194 predicate tokens | cobertura lexical e compatibilidade com licenças congeladas | evidência documental held-out condicionada à cobertura |

### Natural-language intent challenge

O challenge set congelado contém 30 casos: **15 positivos, 5 ambíguos e 10 boundary cases**. Na primeira execução completa registrada, houve:

- 30/30 decisões do validador esperadas;
- 20/20 intents com gold explícito;
- 16/16 realizações de sujeito com gold explícito;
- 5/5 casos ambíguos enviados para clarificação;
- 10/10 boundary cases tratados como esperado;
- 0 falhas de transporte.

Esses números descrevem concordância nesse conjunto controlado. Eles **não** constituem uma estimativa de accuracy para entradas arbitrárias em português/inglês nem de geração irrestrita em Bororo.

### Source-group holdout

O experimento grammar-v2 usa uma divisão congelada por grupo documental:

- 784 sentenças elegíveis;
- 627 na partição de desenvolvimento;
- 157 na partição held-out;
- grupos held-out: `ABE`, `BEBE` e `C.O.`;
- 194 predicate tokens (VERB/AUX) no teste;
- 28 licenças lexicais congeladas.

Dos 194 predicate tokens, **64 (33.0%)** estão dentro da cobertura lexical da grammar-v2 e **130** estão fora de cobertura. Entre os 64 cobertos, o resultado histórico registra **54 compatíveis, 8 conflitos e 2 não resolvidos**. Os oito conflitos correspondem a um único erro subjacente de licença lexical envolvendo `ro`.

Assim, **54/62 é compatibilidade entre tokens cobertos adjudicáveis**, não accuracy geral sobre Bororo não visto.

O teste é parcialmente unblinded: cinco exemplos das fontes held-out (3 ABE + 2 BEBE) haviam sido vistos anteriormente, mas não foram usados para adicionar ou revisar uma licença da grammar-v2. O manifest preserva essa condição explicitamente.

O CoNLL-U público atual não preserva informação suficiente para reconstruir de forma confiável o antigo mapeamento individual `ABE/BEBE/C.O. → sent_id`. Por isso, o resultado histórico e o desenho do split são preservados no manifest, sem inventar retrospectivamente uma reconstrução sentence-level.

## Adjudicação humana

A revisão dos casos held-out segue um protocolo fechado e versionado. Primeiro se determina cobertura lexical; somente tokens cobertos entram na avaliação de compatibilidade. Os rótulos são:

- `COVERED`, `OUT_OF_COVERAGE` ou `LEXICAL_IDENTITY_UNRESOLVED`;
- para casos cobertos: `COMPATIBLE`, `CONFLICT` ou `UNRESOLVED`.

Um conflito recebe ainda um locus primário (lexical frame, argument realization, morphology, construction, annotation mapping ou other) e uma nota de evidência. Possíveis objetos implícitos ou problemas de anotação não são convertidos automaticamente em erros gramaticais.

A adjudicação pode classificar resultados, mas **não pode alterar a gramática congelada do mesmo experimento**. Como a avaliação histórica foi realizada pelo autor da gramática, ela não constitui anotação independente e não se reporta inter-annotator agreement. O protocolo define também como uma futura segunda revisão independente deve ser conduzida.

Ver `docs/HUMAN_ADJUDICATION_PROTOCOL.md`.

## Reprodutibilidade e governança

Os artefatos públicos registram separadamente:

- a gramática congelada usada em cada experimento;
- o split documental;
- challenge sets congelados;
- decisões de cobertura;
- resultados de compatibilidade;
- limitações de proveniência;
- regras de adjudicação.

Observações obtidas durante um teste podem motivar uma versão posterior da gramática, mas não podem alterar retrospectivamente as licenças usadas para pontuar o mesmo experimento.

Uma reavaliação com corpus, anotação, gramática ou mapeamento de fontes modificados deve receber uma nova versão de manifest, preservando o resultado histórico.

## Uso

Instale o projeto em ambiente Python e execute os testes:

```bash
python3 -m pytest
```

Os utilitários em `scripts/` implementam as etapas públicas de geração, diagnóstico, auditoria e avaliação.

## Dados

**CorBo — Corpus da Língua Bororo**  
DOI: 10.5281/zenodo.12110451

Os dados documentais permanecem no repositório próprio do CorBo. Este projeto os utiliza como fonte externa e não substitui a documentação original.

## Citação do software

A versão citable atual é **v1.0.1**:

**Gerardi, Fabrício Ferraz. (2026). _Bororo Sentence Generator: Evidence-Bounded Generation for Boe-Bororo_ (v1.0.1). Zenodo. DOI: 10.5281/zenodo.22941512.**

## Estado

Projeto de pesquisa em desenvolvimento. As gramáticas experimentais, challenge sets e manifests são versionados e congelados por experimento para impedir que observações obtidas durante a avaliação alterem retrospectivamente as licenças usadas no mesmo teste.
