__all__ = ("GOTO_FILTER_DEFINITIONS",)

from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

GOTO_FILTER_DEFINITIONS = FilterDefinitionCollection(
        FilterDefinition(
            physical_filter="L",
            band="L",
            alias={'L'}
            )
    )
