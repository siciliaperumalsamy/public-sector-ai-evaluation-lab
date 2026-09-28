# Public Sector AI Evaluation Lab

A Python prototype exploring how public-sector AI use cases can be evaluated against government AI assurance guidance using **semantic retrieval, Retrieval-Augmented Generation (RAG), structured LLM analysis and traceable source evidence**.

The application takes a proposed AI use case, retrieves relevant evidence from the **National Framework for the Assurance of Artificial Intelligence in Government**, provides that evidence to a language model for structured analysis, validates the model's source references, and generates a human-verifiable assessment report.

The project was developed iteratively:

- **V1** established a transparent keyword-based retrieval and rule-based assessment baseline.
- **V2** introduced local sentence embeddings and semantic retrieval after testing exposed limitations in keyword matching.
- **V3** introduced evidence-grounded LLM analysis, structured output, programmatic source validation and human-verifiable evidence attachment.

![Example AI assurance assessment](assets/western_power_assessment_preview.png)

## Why I Built This

AI teams working across government may encounter very different technical and assurance problems across agencies.

One engagement might involve evaluating an AI model, another may involve governance or technical documentation, while another may involve testing, deploying or integrating an AI solution.

I built this project to explore a practical question:

> How could a technical team rapidly perform an initial, evidence-grounded assessment of an unfamiliar public-sector AI use case while keeping AI-generated findings traceable to published government guidance?

Rather than attempting to automate an assurance or compliance decision, the prototype acts as an initial decision-support tool.

It combines automated retrieval and LLM-assisted analysis with explicit human-verification mechanisms.

## How This Was Built

I built this project with the help of AI coding assistants, which wrote most of the code. My role was to decide what the prototype should do, run and test each version, identify where it failed, and direct the changes described below. I can explain what each component does and why it is designed this way, and I am continuing to build my own coding skills.

## What the Prototype Does

The user provides:

- agency or organisation
- AI system or solution
- purpose of the AI system
- data used by the system
- known concerns or risks

The V3 pipeline then:

1. loads the government AI assurance framework
2. extracts and cleans the PDF text
3. splits the framework into overlapping, page-aware chunks
4. filters known non-substantive content such as contents and reference pages
5. converts policy chunks into local sentence embeddings
6. creates a semantic representation of the supplied AI use case
7. retrieves the most conceptually relevant framework evidence
8. supplies only the use case and retrieved evidence to an LLM
9. requests a structured evidence-grounded assessment
10. validates every LLM-generated source ID against the evidence actually retrieved
11. attaches the original policy text to each generated finding
12. generates an auditable Markdown assessment report

## V3 Architecture

```text
Government AI Assurance Framework
              |
              v
        PDF extraction
              |
              v
         Text cleaning
              |
              v
     Page-aware chunking
              |
              v
 Non-substantive content filter
              |
              v
      Sentence embeddings
              |
              |
              +-----------------------------+
                                            |
User-supplied AI use case                   |
              |                             |
              v                             |
       Semantic query                       |
              |                             |
              +-----------------------------+
                            |
                            v
                  Semantic retrieval
                            |
                            v
               Relevant policy evidence
                            |
                            +
                     AI use case
                            |
                            v
                Evidence-grounded LLM
                     analysis
                            |
                            v
                  Structured JSON
                            |
                            v
               Source-ID validation
                            |
                            v
             Original evidence attached
                            |
                            v
              Human-verifiable report
```

## Retrieval-Augmented Generation

V3 uses a Retrieval-Augmented Generation workflow.

Rather than asking a language model to assess an AI use case using unrestricted general knowledge, the application first retrieves relevant evidence from the government assurance framework.

The LLM receives:

```text
AI use case
     +
semantically retrieved government evidence
     ↓
evidence-grounded analysis
```

The prompt instructs the model to:

- use only the supplied framework evidence
- avoid inventing legal, policy or technical requirements
- avoid overstating obligations
- identify when further review is required
- return structured JSON
- cite only source IDs supplied by the retrieval system

The Python application then validates those source references before a report can be generated.

## Human-Verifiable Evidence

A valid-looking citation generated by an LLM is not automatically trustworthy.

V3 therefore separates two checks.

### 1. Source validation

Every retrieved policy chunk receives a source identifier such as:

```text
page_24_chunk_2
```

If the LLM references a source that was never retrieved and supplied to it, the application detects the invalid reference and stops report generation.

For example:

```text
LLM references:
page_99_chunk_7

Retrieved evidence:
page_24_chunk_2
page_28_chunk_3
...

Result:
SOURCE VALIDATION FAILED
```

### 2. Human verification

Even a valid source ID does not prove that the evidence supports the model's interpretation.

The application therefore attaches the **original retrieved framework text** beneath each generated finding.

A reviewer can inspect:

```text
Generated finding
      ↓
Why it matters
      ↓
Recommended action
      ↓
Original government evidence
      ↓
Page + chunk reference
```

This keeps human review explicitly inside the assessment workflow.

## Example: Western Power

One test scenario considers a fictional application of AI within Western Power.

**AI system**

An AI model predicting potential failures in electricity network assets.

**Purpose**

Identify assets at higher risk of failure to support maintenance planning.

**Data**

Historical asset condition, maintenance and failure data.

**Known concerns**

Safety, reliability, false predictions and human oversight.

The V3 RAG pipeline produced tailored findings covering areas including:

- governance and risk management
- data governance
- human oversight and staff capability
- system monitoring
- standards alignment

Each generated finding includes the underlying government-framework evidence used during the assessment.

See:

```text
examples/example_western_power_rag_assessment.md
```
## Public Health AI Assurance Example

To test the assurance workflow in a public-health context, I added a scenario involving an **Australian public health agency** considering a generative AI assistant to help staff find and summarise information from communicable-disease policies and operational guidance.

The proposed system is intended to help public-health staff locate relevant guidance quickly and support consistent interpretation of policy information.

The assessment identified considerations across:

- human oversight and accountability
- data governance and quality
- protection of sensitive and personal information
- staff capability and training

A particular concern is the quality and currency of the information available to the AI system. Outdated, unauthenticated or inaccurate public-health guidance could affect the reliability of generated outputs.

The assessment also demonstrates an important behaviour of the evidence-grounded workflow: where the retrieved framework evidence was insufficient to support a conclusion about technical source traceability, conflicting guidance or specific security architecture, the generated assessment identified those areas for **further review** rather than inventing requirements.

This example complements the technical agent-testing work in my separate AI Agent Evaluation Lab, where a document-grounded assistant is benchmarked against a real Australian national communicable-disease guideline.

See:

```text
examples/example_australian_public_health_agency_rag_assessment.md
```

## V1 → V2: Improving Retrieval

The first version of the prototype used transparent keyword matching.

Testing identified an important limitation.

In a public-document summarisation scenario, `accuracy` was supplied as the primary concern.

The prototype correctly identified **Reliability and testing** as relevant, but V1 keyword retrieval returned:

> No policy evidence retrieved.

Relevant sections of the framework instead discussed concepts such as:

- incorrect outputs
- reliability
- testing
- technical validation
- human validation

The exact word `accuracy` was not required.

### V2 semantic retrieval

V2 introduced sentence embeddings using a locally running Sentence Transformer model.

Both retrieval approaches were tested against exactly the same query:

```text
accuracy
```

**V1 — keyword retrieval**

```text
No policy evidence retrieved.
```

**V2 — semantic retrieval**

High-ranking results included framework guidance addressing:

- incorrect AI outputs
- reliability
- testing
- technical validation
- human validation

This demonstrated that semantic retrieval could identify conceptually related evidence even when the user's terminology differed from the framework.

The original keyword retriever remains in the repository as a baseline.

`compare_retrieval.py` provides a direct comparison between the two approaches.

## V2 → V2.1: Improving Evidence Quality

Testing semantic retrieval revealed another issue.

The embedding model occasionally returned chunks from the framework's table of contents or resources section because those pages contained terminology semantically related to the query.

Although mathematically similar, these sections were not useful substantive evidence.

V2.1 introduced a transparent preprocessing filter that removes known non-substantive sections before embeddings are searched.

This illustrates an important design principle in the project:

> Improving an AI system does not always require a more sophisticated model. Improving the information available to the model can also improve the result.

## V2 → V3: Moving From Retrieval to RAG

V2 could identify relevant government evidence but recommendations were still generated using predefined rules.

For example:

```text
Reliability and testing
→ predefined testing recommendation
```

That approach was transparent but could not adapt its recommendations deeply to different technical contexts.

V3 introduced an LLM after the semantic retrieval stage.

The application now follows:

```text
Agency AI problem
        ↓
Semantic retrieval
        ↓
Relevant government evidence
        ↓
Evidence-grounded LLM analysis
        ↓
Structured findings
        ↓
Source validation
        ↓
Human-verifiable report
```

This allows recommendations to reflect the specific AI system being assessed while remaining linked to retrieved government evidence.

## Project Structure

```text
public-sector-ai-evaluation-lab/
|
|-- assets/
|   `-- western_power_assessment_preview.png
|
|-- data/
|   `-- national_ai_assurance_framework.pdf (not committed; see Source document)
|
   |-- examples/
   |   |-- example_australian_public_health_agency_rag_assessment.md
   |   |-- example_department_of_communities_ai_assessment.md
   |   |-- example_western_power_ai_assessment.md
   |   `-- western_power_rag_assessment.md
|
|-- outputs/
|   `-- locally generated assessment reports
|
|-- src/
|   |-- clean_text.py
|   |-- load_document.py
|   |-- chunk_document.py
|   |-- retrieve.py
|   |-- semantic_retrieve.py
|   |-- compare_retrieval.py
|   |-- evaluate_use_case.py
|   |-- assess_use_case.py
|   |-- generate_report.py
|   |-- llm_assessment.py
|   |-- generate_rag_report.py
|   `-- run_assessment.py
|
|-- tests/
|   `-- test_assessment.py
|
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Source document

The prototype uses the *National framework for the assurance of artificial intelligence in government* (Version 1.0, 21 June 2024), a joint framework from the Australian, state and territory governments. The PDF is not included in this repository. Download it and save it as `data/national_ai_assurance_framework.pdf`.

## Running the Prototype

### 1. Create a Python environment

Create and activate a virtual environment using your preferred method.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### 2. Configure the Gemini API key

V3 uses the Gemini API for the generative stage.

Create a local `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git and should never be committed to the repository.

### 3. Run the application

```bash
python src/run_assessment.py
```

The application prompts for the AI use case.

Example:

```text
Agency or organisation:
Western Power

AI system or solution:
AI model that predicts potential failures in electricity network assets

Purpose of the AI system:
Identify assets at higher risk of failure to support maintenance planning

Data used by the AI system:
Historical asset condition, maintenance and failure data

Known concerns or risks:
safety reliability false predictions human oversight
```

The pipeline then performs semantic retrieval, evidence-grounded LLM analysis, source validation and report generation.

A Markdown report is saved in:

```text
outputs/
```

## Testing

The project includes automated tests covering important behaviours introduced during development.

Run:

```bash
python -m pytest -v
```

Current tests cover:

### Assurance classification

An explicit `accuracy` concern should trigger **Reliability and testing** rather than unrelated assurance areas.

### Missing evidence

Failure to retrieve supporting evidence must not automatically be interpreted as evidence that no risk exists.

### Semantic retrieval

The query:

```text
accuracy
```

should retrieve framework material containing conceptually related evidence such as:

- incorrect outputs
- reliability
- testing
- validation

This protects the retrieval improvement that motivated V2.

### Valid LLM source references

A source ID corresponding to evidence genuinely supplied to the LLM should pass validation.

### Invented LLM source references

A source ID that was not retrieved should be detected by the application.

For example:

```text
page_99_chunk_7
```

must not be accepted simply because it looks like a valid citation.

At the current V3 checkpoint:

```text
5 tests passed
```

The tests deliberately avoid making live Gemini calls so routine testing remains deterministic and does not consume API usage.

Note: the tests still need a `GEMINI_API_KEY` in `.env` and the framework PDF in `data/`, because some modules load these when they are imported.

## Design Decisions

### Modular architecture

The project separates:

- document processing
- retrieval
- assessment
- LLM analysis
- source validation
- report generation

This makes individual components replaceable without redesigning the entire pipeline.

For example, V1 keyword retrieval could be replaced by V2 semantic retrieval without rebuilding the reporting components.

### Local semantic retrieval

Sentence embeddings are generated locally using `sentence-transformers`.

The entire source framework therefore does not need to be sent to an external language model.

Only the use-case information and a small number of retrieved evidence chunks are supplied during the generative stage.

### Structured LLM output

Gemini is instructed to return structured JSON rather than controlling the final report format.

Python remains responsible for validating, processing and presenting the result.

### Source validation

The application does not automatically trust citations generated by the language model.

Every generated source ID is checked against evidence genuinely retrieved and supplied to the model.

### Human review

Programmatic citation validation proves that a cited source exists within the retrieved evidence.

It does **not** prove that the model interpreted the source correctly.

The original policy evidence is therefore included in the generated report for human verification.

## Technology

Current V3:

- Python
- pypdf
- sentence-transformers
- PyTorch
- local sentence embeddings
- semantic similarity retrieval
- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- structured JSON LLM output
- programmatic source validation
- Markdown report generation
- python-dotenv
- pytest

## Current Limitations

This is an exploratory prototype rather than a production assurance system.

Current limitations include:

- assurance assessment depends on the information supplied by the user
- semantic retrieval may miss or imperfectly rank relevant evidence
- semantic similarity does not guarantee substantive relevance
- the current retrieval corpus uses one primary government AI assurance framework
- only a small number of top-ranked chunks are supplied to the LLM
- language models can still misinterpret or overstate retrieved evidence
- source-ID validation confirms that a cited chunk exists but does not automatically prove that it supports the generated claim
- human verification remains necessary
- findings returned with no source IDs are not currently rejected; only invalid source IDs are detected
- semantic retrieval always returns the top 6 chunks, even when none are strongly relevant (no minimum similarity threshold)
- fixed-size character chunking can split words and sentences, which is visible in some evidence excerpts
- no automated technical testing of an actual AI model or agent is currently performed
- no production authentication or access-control layer is included
- no production cloud deployment is currently included

Generated outputs should be treated as prompts for further investigation rather than authoritative compliance, legal, safety or deployment findings.

## Future Development

Potential next iterations include:

- automated evaluation of AI-agent responses
- grounding-quality evaluation for generated findings
- reranking of semantically retrieved evidence
- configurable similarity thresholds
- support for multiple government policies and technical standards
- vector-based document storage
- improved evidence citation and provenance
- configurable assurance frameworks
- additional automated RAG evaluation tests
- provider-independent LLM interfaces
- containerisation using Docker
- deployment into a cloud or controlled environment
- lightweight web interface

## Status

**V3 — evidence-grounded RAG prototype**

V1 established the end-to-end assessment pipeline using transparent keyword retrieval and deterministic recommendations.

V2 introduced local sentence embeddings and semantic retrieval after testing demonstrated that keyword matching could miss conceptually relevant government evidence.

V2.1 improved retrieval quality by filtering known non-substantive document sections.

V3 introduces evidence-grounded LLM analysis using semantically retrieved framework material. The LLM returns structured findings, generated source references are validated programmatically, and the original source evidence is attached to each finding for human verification.

The project is intended as a learning and experimentation environment for public-sector AI evaluation, assurance and responsible implementation.