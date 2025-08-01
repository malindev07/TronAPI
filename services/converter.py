from dataclasses import dataclass


@dataclass
class Converter:

    async def convert_schema_to_model(self, schema):
        pass

    async def convert_model_to_schema(self, model):
        pass
