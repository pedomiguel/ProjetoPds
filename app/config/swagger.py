from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class SwaggerConfig:
    @staticmethod
    def setup(app: FastAPI):
        return lambda: SwaggerConfig._generate_schema(app)

    @staticmethod
    def _generate_schema(app: FastAPI):
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="IA + Music",
            version="1.0.0",
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }

        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", []).append({"BearerAuth": []})

        app.openapi_schema = openapi_schema
        return openapi_schema
