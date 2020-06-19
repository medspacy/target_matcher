# target_matcher
A wrapper class for extended rule-based matching in spaCy.

# Overview
This package offers utilities for extended rule-based matching in spaCy pipelines. The main classes used in this package 
are `TargetMatcher` and `TargetRule`. Similar to other `spaCy` rule-based matching components, the `TargetMatcher` 
matches spans of text in a spaCy Doc. This class offers the followowing functionality:
- Patterns are defined using the `TargetRule` class. This class has the following attributes:
    - `literal`: An exact span of text defining the term. If `pattern` is `None`, this will be the phrase used to match 
    in the doc.
    - `category`: The label which will be assigned to any matched spans
    - `pattern (opt)`: An optional spaCy pattern. If this argument is provided, it will be used to match a span, and 
    `literal` can be used as a normalized version of the phrase
    - `attributes (opt)`: An optional dictionary of attributes to set for the `Span._`. For example, if 
    `{"is_negated": True}` is provided, then the resulting `span._.is_negated` will evaluate to `True`
    - `on_match (opt)`: Optional callback functions for the spaCy matchers
- The original rule which matched a Span will be added to `span._.target_rule`. This allows you to see which specific rule
picked up a match, which is useful for debugging and data aggregation/analysis
- By default, matching spans will be added to `doc.ents`, but by setting `add_ents` to `False`, it will instead
return tuples of `(span, category)`
- The `ConceptTagger` is a wrapper class around `TargetMatcher` which will assign token-level labels based on the 
`category` attribute for all matches

# Basic Usage

## Installation
You can install target_matcher using pip:
```bash
pip install target_matcher
```

Or clone this repository install target_matcher using the `setup.py` script:
```bash
$ python setup.py install
```

Once you've installed the package and spaCy, make sure you have a spaCy language model installed (see https://spacy.io/usage/models):

```bash
$ python -m spacy download en_core_web_sm
```

## Example
In the example below, we'll use target matcher to extract two different forms of "Type II Diabetes" and show
how they can be mapped to the same normalized ("literal") term and ICD-10 code:
```python
from target_matcher import TargetMatcher, TargetRule
import spacy
from spacy.tokens import Span

# Register a new custom attribute to store ICD-10 diagnosis codes
Span.set_extension("icd10_code", default="")

nlp = spacy.blank("en")
target_matcher = TargetMatcher(nlp)
nlp.add_pipe(target_matcher)

rules = [
    TargetRule(literal="Type II Diabetes Mellitus", category="PROBLEM",
              attributes={"icd10_code": "E11.9"}),
    TargetRule(literal="Type II Diabetes Mellitus", category="PROBLEM",
               pattern=[{"LOWER": "type"}, {"LOWER": {"IN": ["two", "ii", "2"]}}, {"LOWER": "dm"}],
              attributes={"icd10_code": "E11.9"}),
]
target_matcher.add(rules)

text = """
DIAGNOSIS: Type II Diabetes Mellitus
The patient presents today for management of Type 2 DM.
"""

doc = nlp(text)

# Even though different rules were used to match the ents,
# they have the same 'literal' value, and both are assigned "E11.9" 
# as an icd10 code
for ent in doc.ents:
    print(ent, ent._.target_rule.literal, ent._.icd10_code, sep="\t")

>>> Type II Diabetes Mellitus	Type II Diabetes Mellitus	E11.9
    Type 2 DM	Type II Diabetes Mellitus	E11.9
```