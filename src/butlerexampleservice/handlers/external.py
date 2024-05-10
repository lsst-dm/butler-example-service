"""Handlers for the app's external root, ``/butler-example-service/``."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from lsst.daf.butler import LabeledButlerFactory
from safir.dependencies.gafaelfawr import auth_delegated_token_dependency
from safir.dependencies.logger import logger_dependency
from safir.metadata import get_metadata
from structlog.stdlib import BoundLogger

from ..config import config
from ..models import Index

__all__ = ["get_index", "external_router"]

external_router = APIRouter()
"""FastAPI router for all external handlers."""


# The Butler factory loads configuration from the DAF_BUTLER_REPOSITORIES
# environment variable by default.
#
# There should be a single global instance of this factory -- it caches
# data to allow Butler instances to be created quickly.
_BUTLER_FACTORY = LabeledButlerFactory()


# This HTTP GET handler returns the URL for a coadded image, given a position
# in the sky in Rubin's tract/patch skymap.
@external_router.get("/coadd_url")
def get_coadd_url(
    tract: int,
    patch: int,
    # This retrieves a Gafaelfawr access token from headers provided by
    # GafaelfawrIngress.
    delegated_token: Annotated[str, Depends(auth_delegated_token_dependency)],
) -> str:
    # "dp02" is Data Preview 0.2, currently the only Butler repository
    # available in the Rubin Science Platform.
    butler = _BUTLER_FACTORY.create_butler(
        label="dp02", access_token=delegated_token
    )

    ref = butler.find_dataset(
        "deepCoadd",
        data_id={"tract": tract, "patch": patch, "band": "i", "skymap": "DC2"},
        collections="2.2i/runs/DP0.2",
    )
    if ref is None:
        raise HTTPException(status_code=404, detail="Coadd not found")
    return str(butler.getURI(ref))


@external_router.get(
    "/",
    description=(
        "Document the top-level API here. By default it only returns metadata"
        " about the application."
    ),
    response_model=Index,
    response_model_exclude_none=True,
    summary="Application metadata",
)
async def get_index(
    logger: Annotated[BoundLogger, Depends(logger_dependency)],
) -> Index:
    """GET ``/butler-example-service/`` (the app's external root).

    Customize this handler to return whatever the top-level resource of your
    application should return. For example, consider listing key API URLs.
    When doing so, also change or customize the response model in
    `butlerexampleservice.models.Index`.

    By convention, the root of the external API includes a field called
    ``metadata`` that provides the same Safir-generated metadata as the
    internal root endpoint.
    """
    # There is no need to log simple requests since uvicorn will do this
    # automatically, but this is included as an example of how to use the
    # logger for more complex logging.
    logger.info("Request for application metadata")

    metadata = get_metadata(
        package_name="butler-example-service",
        application_name=config.name,
    )
    return Index(metadata=metadata)
