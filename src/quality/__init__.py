"""
SECOM MES Quality API Client Package

This package provides async Python functions to interact with the SECOM Manufacturing
Execution System Quality REST API endpoints for the Solace Agent Mesh framework.

All functions are async and must be called with await.

Example:
    >>> from src.quality import get_all_results, get_result_by_id
    >>> results = await get_all_results()
    >>> result = await get_result_by_id(1)
"""

from .quality_api import (
    # Type definitions
    QualityResult,
    Lot,

    # Core API functions
    get_result_by_id,
    get_all_results,
    get_passed_results,
    get_result_by_lot_id,
    get_high_risk_results,
    get_failed_results,
    get_results_by_defect_type,

    # Utility functions
    get_quality_summary,
    get_quality_statistics,
    safe_get_result,

    # Configuration
    DEFAULT_BASE_URL,
)

__all__ = [
    # Type definitions
    'QualityResult',
    'Lot',

    # Core API functions
    'get_result_by_id',
    'get_all_results',
    'get_passed_results',
    'get_result_by_lot_id',
    'get_high_risk_results',
    'get_failed_results',
    'get_results_by_defect_type',

    # Utility functions
    'get_quality_summary',
    'get_quality_statistics',
    'safe_get_result',

    # Configuration
    'DEFAULT_BASE_URL',
]
