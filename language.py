from __future__ import annotations

import functools
import itertools
import operator


class Language:
    def __init__(self):
        pass

    def generate(self):
        return [""]

    def __str__(self):
        return str(list(self.generate()))

    def __add__(self, other: Language | str):
        return Concatenate(self, other)

    def __or__(self, other: Language):
        return Union(self, other)

    def __invert__(self):
        return Union(self, Language())

    def lgenerate(self):
        return list(self.generate())

    def __iter__(self):
        self.generated = iter(self.generate())
        return self

    def __next__(self):
        return next(self.generated)

    def lower(self):
        return map(lambda item: item.lower(), self)


class BinaryOperator(Language):
    def __init__(self, left: Language, right: Language):
        self.left = left
        self.right = right


class String(Language):
    def __init__(self, string):
        self.string = string

    def generate(self):
        return [self.string]


class LanguageCombinator(Language):
    def __init__(self, *languages: Language | str):
        self.languages = [
            String(language) if isinstance(language, str) else language
            for language in languages
        ]


class Union(LanguageCombinator):
    def generate(self):
        return itertools.chain.from_iterable(
            map(operator.methodcaller("generate"), self.languages)
        )


class Enumeration(Union):
    def __init__(self, *args: str):
        super().__init__(*map(String, args))


class Concatenate(LanguageCombinator):
    def generate(self):
        return functools.reduce(
            lambda ll, rl: list(
                itertools.chain.from_iterable(
                    map(
                        lambda rs: map(lambda ls: (ls + " " + rs).strip(), ll),
                        rl.generate(),
                    )
                )
            ),
            self.languages,
            # The empty string is the multiplicative identity
            [""],
        )
