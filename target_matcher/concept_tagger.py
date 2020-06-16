from . import TargetMatcher

class ConceptTagger:
    name = "concept_tagger"

    def __init__(self, nlp, attr_name="concept_tag"):
        self.nlp = nlp
        self.attr_name = attr_name
        self.target_matcher = TargetMatcher(nlp, add_ents=False)
        self.rules = []

    def add(self, rules):
        self.target_matcher.add(rules)
        for rule in rules:
            self.rules.append(rule)

    def __call__(self, doc):
        spans = self.target_matcher(doc)
        for span in spans:
            for token in span:
                setattr(token._, self.attr_name, span.label_)

        return doc
