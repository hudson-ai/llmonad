from __future__ import annotations

from typing import Callable, Concatenate, Generic, NewType, ParamSpec, Self, TypeVar

# Placeholder
Model = NewType("Model", object)

P = ParamSpec("P")
R = TypeVar("R")

Q = ParamSpec("Q")
S = TypeVar("S")


class Function(Generic[P, R]):
    def __init__(self, func: Callable[Concatenate[Model, P], R]):
        self.func = func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Literal[R]:
        return Literal(lambda model: self.func(model, *args, **kwargs))


class Literal(Function[[], R]):
    def __call__(self) -> Self:
        return self

    def bind(self, func: Callable[[R], Function[Q, S]]) -> Function[Q, S]:
        return Function[Q, S](
            lambda model, *args, **kwds: func(self.func(model))(model, *args, **kwds)
        )


class String(Literal[str]):
    def __add__(self, other: String) -> Self:
        return String(lambda model: self.func(model) + other.func(model))
