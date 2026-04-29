from django.db import models


class Vocabulary(models.Model):
    # Mirrors the PostgreSQL enum values and validates API input before insert.
    class CefrLevel(models.TextChoices):
        A1 = "A1", "A1"
        A2 = "A2", "A2"
        B1 = "B1", "B1"
        B2 = "B2", "B2"
        C1 = "C1", "C1"
        C2 = "C2", "C2"

    # Keep this list in sync with the database `pos_type` enum.
    class PartOfSpeech(models.TextChoices):
        NOUN = "noun", "Noun"
        VERB = "verb", "Verb"
        ADJECTIVE = "adjective", "Adjective"
        ADVERB = "adverb", "Adverb"
        PREPOSITION = "preposition", "Preposition"
        PRONOUN = "pronoun", "Pronoun"
        CONJUNCTION = "conjunction", "Conjunction"
        DETERMINER = "determiner", "Determiner"
        INTERJECTION = "interjection", "Interjection"
        NUMBER = "number", "Number"

    headword = models.CharField(max_length=255)
    pos = models.CharField(max_length=55, choices=PartOfSpeech.choices)
    cefr = models.CharField(max_length=2, choices=CefrLevel.choices)

    class Meta:
        db_table = "vocabulary"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.headword
