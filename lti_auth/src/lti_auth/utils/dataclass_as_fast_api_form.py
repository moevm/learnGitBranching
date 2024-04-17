import inspect
from typing import Annotated

from fastapi import Form


def as_form(cls):
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default or "",
            annotation=Annotated[model_field.annotation, *model_field.metadata, Form()],
        )
        for field_name, model_field in cls.model_fields.items()
    ]

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_params)
    as_form_func.__signature__ = sig  # type: ignore
    cls.as_form = as_form_func
    return cls
