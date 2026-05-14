from fastapi import APIRouter, Response, status

from iris_kafka_sink.http_server.state import HealthState


def create_router(state: HealthState) -> APIRouter:
    router = APIRouter()

    @router.get("/health/live")
    def live() -> Response:
        return Response(status_code=status.HTTP_200_OK)

    @router.get("/health/ready")
    def ready() -> Response:
        snap = state.snapshot()
        if all(snap.values()):
            return Response(status_code=status.HTTP_200_OK)
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @router.get("/health")
    def health() -> dict:
        snap = state.snapshot()
        return {
            "status": "ok" if all(snap.values()) else "degraded",
            "components": snap,
        }

    return router
