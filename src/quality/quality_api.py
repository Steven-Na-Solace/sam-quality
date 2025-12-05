"""
SECOM MES Quality API Client (Async Version)

This module provides async Python functions to interact with the SECOM Manufacturing Execution System
Quality REST API endpoints. Each function is documented with Agent_card and A2A specifications
for use by AI agents in the Solace Agent Mesh framework.

API Base URL: http://localhost:8080/api/v1
Database: MariaDB 11.2

Note: All functions are async and must be called with await.
"""

import httpx
from typing import TypedDict, List, Optional, Any, Dict
from datetime import datetime


# ============================================================================
# Type Definitions (Schemas) - Based on OpenAPI Specification
# ============================================================================

class ProductType(TypedDict, total=False):
    """Product Type entity schema"""
    productTypeId: int
    productCode: str
    productName: str
    productFamily: str  # e.g., "Logic", "Memory", "Analog"
    targetYield: float
    specificationVersion: str
    createdAt: str  # datetime format: ISO 8601


class Equipment(TypedDict, total=False):
    """Equipment entity schema"""
    equipmentId: int
    equipmentCode: str
    equipmentName: str
    equipmentType: str  # e.g., "CVD", "Etcher"
    location: str
    manufacturer: str
    installDate: str  # date format: YYYY-MM-DD
    status: str
    createdAt: str  # datetime format: ISO 8601
    updatedAt: str  # datetime format: ISO 8601


class Operator(TypedDict, total=False):
    """Operator entity schema"""
    operatorId: int
    operatorCode: str
    operatorName: str
    employeeNumber: str
    department: str
    hireDate: str  # date format: YYYY-MM-DD
    email: str
    status: str
    createdAt: str  # datetime format: ISO 8601
    updatedAt: str  # datetime format: ISO 8601


class Shift(TypedDict, total=False):
    """Shift entity schema"""
    shiftId: int
    shiftCode: str  # e.g., "DAY", "SWING", "NIGHT"
    shiftName: str
    startTime: Dict[str, int]  # LocalTime: {hour, minute, second, nano}
    endTime: Dict[str, int]  # LocalTime: {hour, minute, second, nano}
    description: str
    createdAt: str  # datetime format: ISO 8601


class Lot(TypedDict, total=False):
    """Lot entity schema"""
    lotId: int
    lotNumber: str
    productType: ProductType
    equipment: Equipment
    operator: Operator
    shift: Shift
    productionStart: str  # datetime format: ISO 8601
    productionEnd: str  # datetime format: ISO 8601
    waferCount: int
    status: str  # e.g., "in_progress", "completed", "quality_hold", "released", "scrapped"
    createdAt: str  # datetime format: ISO 8601
    updatedAt: str  # datetime format: ISO 8601


class QualityResult(TypedDict, total=False):
    """Quality Result entity schema - Based on OpenAPI spec"""
    resultId: int
    lot: Lot
    classification: int  # -1 = Pass, 1 = Fail
    testTimestampRaw: str
    testDatetime: str  # datetime format: ISO 8601
    predictedRisk: float  # 0.0 to 1.0
    riskScore: float
    riskFactors: str
    modelVersion: str
    qualityScore: float
    defectType: str  # e.g., "contamination", "dimensional_oor", "electrical_fail", "surface_defect"
    defectCode: str
    defectLocation: str
    inspector: Operator
    notes: str
    reviewer: Operator
    reviewedAt: str  # datetime format: ISO 8601
    disposition: str
    createdAt: str  # datetime format: ISO 8601
    updatedAt: str  # datetime format: ISO 8601


class PageQualityResult(TypedDict, total=False):
    """Paginated Quality Result response schema"""
    totalPages: int
    totalElements: int
    size: int
    content: List[QualityResult]
    number: int
    numberOfElements: int
    last: bool
    first: bool
    empty: bool


# ============================================================================
# Configuration
# ============================================================================

# Default base URL for the API
DEFAULT_BASE_URL = "http://localhost:8080/api/v1"


# ============================================================================
# Helper Functions
# ============================================================================

async def _make_request(
    method: str,
    endpoint: str,
    base_url: str = DEFAULT_BASE_URL,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> httpx.Response:
    """
    Internal async helper function to make HTTP requests.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        base_url: Base URL of the API
        json_data: JSON payload for POST/PUT requests
        params: Query parameters
        timeout: Request timeout in seconds

    Returns:
        Response object

    Raises:
        httpx.HTTPStatusError: On request failure
    """
    url = f"{base_url}{endpoint}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.request(
            method=method,
            url=url,
            json=json_data,
            params=params,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        response.raise_for_status()
        return response


# ============================================================================
# Quality API Functions
# ============================================================================

async def get_result_by_id(result_id: int, ) -> QualityResult:
    base_url: str = DEFAULT_BASE_URL
    """
    Get quality result by ID.

    Returns a single quality inspection result by result ID from the SECOM MES database.

    Agent_card:
    -----------
    skill_id: get_result_by_id
    skill_name: Get Quality Result by ID
    description: Retrieves detailed information about a specific quality inspection result
                 using its unique result ID. Returns complete quality data including
                 inspection details, defect information, yield percentage, and risk level.
    capabilities:
      - Fetch individual quality inspection records
      - Validate quality result existence
      - Retrieve detailed inspection metrics

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - result_id
      properties:
        result_id:
          type: integer
          format: int32
          description: Unique identifier for the quality result
          example: 1

    output_schema:
      type: object
      description: Quality result object
      properties:
        resultId:
          type: integer
          format: int32
          description: Unique quality result identifier
        lot:
          type: object
          description: Associated lot information with lotId, lotNumber, productType, equipment, operator, shift, status
        classification:
          type: integer
          format: int32
          description: Classification result (-1 = Pass, 1 = Fail)
        testTimestampRaw:
          type: string
          description: Raw test timestamp string
        testDatetime:
          type: string
          format: date-time
          description: Date and time of test
        predictedRisk:
          type: number
          format: float
          description: Predicted risk score (0.0 to 1.0)
        riskScore:
          type: number
          format: float
          description: Risk score
        riskFactors:
          type: string
          description: Risk factors identified
        modelVersion:
          type: string
          description: ML model version used for prediction
        qualityScore:
          type: number
          format: float
          description: Quality score
        defectType:
          type: string
          description: Type of defect (contamination, dimensional_oor, electrical_fail, surface_defect)
        defectCode:
          type: string
          description: Defect code
        defectLocation:
          type: string
          description: Location of defect
        inspector:
          type: object
          description: Inspector operator information
        notes:
          type: string
          description: Inspection notes
        reviewer:
          type: object
          description: Reviewer operator information
        reviewedAt:
          type: string
          format: date-time
          description: Review timestamp
        disposition:
          type: string
          description: Disposition decision
        createdAt:
          type: string
          format: date-time
          description: Record creation timestamp
        updatedAt:
          type: string
          format: date-time
          description: Record update timestamp

    error_responses:
      - status: 404
        description: Quality result not found
      - status: 500
        description: Internal server error

    Args:
        result_id: The unique identifier of the quality result
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        QualityResult dictionary containing quality inspection details

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> result = await get_result_by_id(1)
        >>> print(f"Classification: {result['classification']}")  # -1 = Pass, 1 = Fail
        Classification: -1
    """
    response = await _make_request("GET", f"/quality/results/{result_id}", base_url=base_url)
    return response.json()


async def get_all_results(
    page: Optional[int] = None,
    size: Optional[int] = None
) -> PageQualityResult:
    """
    Get all quality results with optional pagination.

    Returns a paginated list of quality inspection results from the SECOM MES database.
    Supports pagination through page and size parameters.

    Agent_card:
    -----------
    skill_id: get_all_results
    skill_name: Get All Quality Results
    description: Retrieves a paginated list of quality inspection results in the system.
                 Returns comprehensive quality data including inspection records with
                 their full details for analysis and reporting.
    capabilities:
      - List all quality inspection results in the system
      - Paginate through large result sets
      - Generate quality reports
      - Perform quality analytics
      - Export quality data

    A2A Spec:
    ---------
    input_schema:
      type: object
      properties:
        page:
          type: integer
          format: int32
          description: Page number for pagination (0-based index)
          default: 0
        size:
          type: integer
          format: int32
          description: Number of results per page
          default: 20

    output_schema:
      type: object
      description: Paginated response containing quality results
      properties:
        totalPages:
          type: integer
          format: int32
          description: Total number of pages
        totalElements:
          type: integer
          format: int64
          description: Total number of elements
        size:
          type: integer
          format: int32
          description: Page size
        number:
          type: integer
          format: int32
          description: Current page number (0-based)
        content:
          type: array
          description: Array of quality results
          items:
            type: object
            properties:
              resultId:
                type: integer
                format: int32
                description: Unique quality result identifier
              lot:
                type: object
                description: Associated lot information
              classification:
                type: integer
                format: int32
                description: Classification result (-1 = Pass, 1 = Fail)
              testTimestampRaw:
                type: string
                description: Raw test timestamp string
              testDatetime:
                type: string
                format: date-time
                description: Date and time of test
              predictedRisk:
                type: number
                format: float
                description: Predicted risk score (0.0 to 1.0)
              riskScore:
                type: number
                format: float
                description: Risk score
              riskFactors:
                type: string
                description: Risk factors identified
              modelVersion:
                type: string
                description: ML model version used for prediction
              qualityScore:
                type: number
                format: float
                description: Quality score
              defectType:
                type: string
                description: Type of defect
              defectCode:
                type: string
                description: Defect code
              defectLocation:
                type: string
                description: Location of defect
              inspector:
                type: object
                description: Inspector operator information
              notes:
                type: string
                description: Inspection notes
              reviewer:
                type: object
                description: Reviewer operator information
              reviewedAt:
                type: string
                format: date-time
                description: Review timestamp
              disposition:
                type: string
                description: Disposition decision
              createdAt:
                type: string
                format: date-time
                description: Record creation timestamp
              updatedAt:
                type: string
                format: date-time
                description: Record update timestamp
        numberOfElements:
          type: integer
          format: int32
          description: Number of elements in current page
        first:
          type: boolean
          description: Whether this is the first page
        last:
          type: boolean
          description: Whether this is the last page
        empty:
          type: boolean
          description: Whether the page is empty

    error_responses:
      - status: 500
        description: Internal server error

    Args:
        page: Page number for pagination (0-based). Default is 0.
        size: Number of results per page. Default is 20.

    Returns:
        PageQualityResult with pagination info and content array of QualityResult

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> # Get first page with default size
        >>> results = await get_all_results()
        >>> print(f"Total elements: {results['totalElements']}")
        Total elements: 1567

        >>> # Get second page with 50 results
        >>> page_results = await get_all_results(page=1, size=50)
        >>> print(f"Results on page: {len(page_results['content'])}")
        Results on page: 50
    """
    params = {}
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size

    response = await _make_request("GET", "/quality/results", base_url=DEFAULT_BASE_URL, params=params if params else None)
    return response.json()


async def get_passed_results(
    page: Optional[int] = None,
    size: Optional[int] = None,

) -> PageQualityResult:
    base_url: str = DEFAULT_BASE_URL
    """
    Get passed quality results.

    Returns paginated list of all lots that passed quality inspection (classification = -1).

    Agent_card:
    -----------
    skill_id: get_passed_results
    skill_name: Get Passed Quality Results
    description: Retrieves all quality inspection results where classification = -1 (Pass).
                 Useful for analyzing successful production runs, identifying best practices,
                 and generating compliance reports.
    capabilities:
      - Filter quality results by passed status
      - Generate pass rate reports
      - Identify successful production patterns
      - Support compliance documentation

    A2A Spec:
    ---------
    input_schema:
      type: object
      properties:
        page:
          type: integer
          format: int32
          description: Page number for pagination (0-based index)
          default: 0
        size:
          type: integer
          format: int32
          description: Number of results per page
          default: 20

    output_schema:
      type: object
      description: Paginated response containing passed quality results (classification = -1)
      properties:
        totalPages:
          type: integer
          format: int32
          description: Total number of pages
        totalElements:
          type: integer
          format: int64
          description: Total number of passed results
        size:
          type: integer
          format: int32
          description: Page size
        number:
          type: integer
          format: int32
          description: Current page number (0-based)
        content:
          type: array
          description: Array of passed quality results
          items:
            type: object
            description: Quality result with classification = -1 (Pass)
        numberOfElements:
          type: integer
          format: int32
          description: Number of elements in current page
        first:
          type: boolean
          description: Whether this is the first page
        last:
          type: boolean
          description: Whether this is the last page
        empty:
          type: boolean
          description: Whether the page is empty

    error_responses:
      - status: 500
        description: Internal server error

    Args:
        page: Page number for pagination (0-based). Default is 0.
        size: Number of results per page. Default is 20.
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        PageQualityResult with pagination info and content array of passed QualityResult

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> passed = await get_passed_results()
        >>> print(f"Total passed inspections: {passed['totalElements']}")
        Total passed inspections: 1200
    """
    params = {}
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    response = await _make_request("GET", "/quality/results/passed", base_url=base_url, params=params if params else None)
    return response.json()


async def get_result_by_lot_id(lot_id: int, ) -> QualityResult:
    base_url: str = DEFAULT_BASE_URL
    """
    Get quality result by lot ID.

    Returns the quality inspection result for a specific lot from the SECOM MES database.

    Agent_card:
    -----------
    skill_id: get_result_by_lot_id
    skill_name: Get Quality Result by Lot ID
    description: Retrieves the quality inspection result associated with a specific production
                 lot using the lot ID. Returns complete quality data for the specified lot
                 including inspection details, defects, and yield information.
    capabilities:
      - Look up quality results by lot identifier
      - Trace lot quality history
      - Support lot-based quality queries
      - Enable lot quality verification

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - lot_id
      properties:
        lot_id:
          type: integer
          format: int32
          description: Unique identifier for the lot
          example: 1

    output_schema:
      type: object
      description: Quality result for the specified lot
      properties:
        resultId:
          type: integer
          format: int32
          description: Unique quality result identifier
        lot:
          type: object
          description: Associated lot information with lotId, lotNumber, productType, equipment, operator, shift, status
        classification:
          type: integer
          format: int32
          description: Classification result (-1 = Pass, 1 = Fail)
        testTimestampRaw:
          type: string
          description: Raw test timestamp string
        testDatetime:
          type: string
          format: date-time
          description: Date and time of test
        predictedRisk:
          type: number
          format: float
          description: Predicted risk score (0.0 to 1.0)
        riskScore:
          type: number
          format: float
          description: Risk score
        riskFactors:
          type: string
          description: Risk factors identified
        modelVersion:
          type: string
          description: ML model version used for prediction
        qualityScore:
          type: number
          format: float
          description: Quality score
        defectType:
          type: string
          description: Type of defect (contamination, dimensional_oor, electrical_fail, surface_defect)
        defectCode:
          type: string
          description: Defect code
        defectLocation:
          type: string
          description: Location of defect
        inspector:
          type: object
          description: Inspector operator information
        notes:
          type: string
          description: Inspection notes
        reviewer:
          type: object
          description: Reviewer operator information
        reviewedAt:
          type: string
          format: date-time
          description: Review timestamp
        disposition:
          type: string
          description: Disposition decision
        createdAt:
          type: string
          format: date-time
          description: Record creation timestamp
        updatedAt:
          type: string
          format: date-time
          description: Record update timestamp

    error_responses:
      - status: 404
        description: Quality result for specified lot not found
      - status: 500
        description: Internal server error

    Args:
        lot_id: The unique identifier of the lot
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        QualityResult dictionary for the specified lot

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> result = await get_result_by_lot_id(1)
        >>> print(f"Lot {result['lot']['lotNumber']} classification: {result['classification']}")  # -1 = Pass
        Lot LOT-001 classification: -1
    """
    response = await _make_request("GET", f"/quality/results/lot/{lot_id}", base_url=base_url)
    return response.json()


async def get_high_risk_results(
    threshold: float = 0.7,

) -> List[QualityResult]:
    base_url: str = DEFAULT_BASE_URL
    """
    Get high risk quality results.

    Returns lots with predicted risk above threshold from the SECOM MES database.

    Agent_card:
    -----------
    skill_id: get_high_risk_results
    skill_name: Get High Risk Quality Results
    description: Retrieves all quality inspection results where the predicted risk is above
                 a specified threshold (default 0.7). Critical for identifying lots that
                 require immediate attention, root cause analysis, or additional quality measures.
    capabilities:
      - Filter quality results by risk threshold
      - Support risk management workflows
      - Enable proactive quality intervention
      - Generate risk assessment reports
      - Identify critical quality issues

    A2A Spec:
    ---------
    input_schema:
      type: object
      properties:
        threshold:
          type: number
          format: float
          description: Risk threshold (0.0 to 1.0), default 0.7
          example: 0.7
          minimum: 0.0
          maximum: 1.0

    output_schema:
      type: array
      description: List of quality results with predicted risk above threshold
      items:
        type: object
        properties:
          resultId:
            type: integer
            format: int32
            description: Unique quality result identifier
          lot:
            type: object
            description: Associated lot information with lotId, lotNumber, productType, equipment, operator, shift, status
          classification:
            type: integer
            format: int32
            description: Classification result (-1 = Pass, 1 = Fail)
          testTimestampRaw:
            type: string
            description: Raw test timestamp string
          testDatetime:
            type: string
            format: date-time
            description: Date and time of test
          predictedRisk:
            type: number
            format: float
            description: Predicted risk score (above threshold)
          riskScore:
            type: number
            format: float
            description: Risk score
          riskFactors:
            type: string
            description: Risk factors identified
          modelVersion:
            type: string
            description: ML model version used for prediction
          qualityScore:
            type: number
            format: float
            description: Quality score
          defectType:
            type: string
            description: Type of defect (contamination, dimensional_oor, electrical_fail, surface_defect)
          defectCode:
            type: string
            description: Defect code
          defectLocation:
            type: string
            description: Location of defect
          inspector:
            type: object
            description: Inspector operator information
          notes:
            type: string
            description: Inspection notes
          reviewer:
            type: object
            description: Reviewer operator information
          reviewedAt:
            type: string
            format: date-time
            description: Review timestamp
          disposition:
            type: string
            description: Disposition decision
          createdAt:
            type: string
            format: date-time
            description: Record creation timestamp
          updatedAt:
            type: string
            format: date-time
            description: Record update timestamp

    error_responses:
      - status: 500
        description: Internal server error

    Args:
        threshold: Risk threshold (0.0 to 1.0), default 0.7
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        List of QualityResult dictionaries with predicted risk above threshold

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> high_risk = await get_high_risk_results(threshold=0.8)
        >>> print(f"High risk lots requiring attention: {len(high_risk)}")
        High risk lots requiring attention: 5
    """
    params = {"threshold": threshold}
    response = await _make_request("GET", "/quality/results/high-risk", base_url=base_url, params=params)
    return response.json()


async def get_failed_results(
    page: Optional[int] = None,
    size: Optional[int] = None,
) -> PageQualityResult:
    base_url: str = DEFAULT_BASE_URL
    """
    Get failed quality results.

    Returns paginated list of all lots that failed quality inspection (classification = 1).

    Agent_card:
    -----------
    skill_id: get_failed_results
    skill_name: Get Failed Quality Results
    description: Retrieves all quality inspection results where classification = 1 (Fail).
                 Essential for failure analysis, identifying quality trends, implementing
                 corrective actions, and tracking quality improvement initiatives.
    capabilities:
      - Filter quality results by failed status
      - Support failure analysis workflows
      - Generate failure reports
      - Track quality issues over time
      - Enable root cause analysis

    A2A Spec:
    ---------
    input_schema:
      type: object
      properties:
        page:
          type: integer
          format: int32
          description: Page number for pagination (0-based index)
          default: 0
        size:
          type: integer
          format: int32
          description: Number of results per page
          default: 20

    output_schema:
      type: object
      description: Paginated response containing failed quality results (classification = 1)
      properties:
        totalPages:
          type: integer
          format: int32
          description: Total number of pages
        totalElements:
          type: integer
          format: int64
          description: Total number of failed results
        size:
          type: integer
          format: int32
          description: Page size
        number:
          type: integer
          format: int32
          description: Current page number (0-based)
        content:
          type: array
          description: Array of failed quality results
          items:
            type: object
            description: Quality result with classification = 1 (Fail)
        numberOfElements:
          type: integer
          format: int32
          description: Number of elements in current page
        first:
          type: boolean
          description: Whether this is the first page
        last:
          type: boolean
          description: Whether this is the last page
        empty:
          type: boolean
          description: Whether the page is empty

    error_responses:
      - status: 500
        description: Internal server error

    Args:
        page: Page number for pagination (0-based). Default is 0.
        size: Number of results per page. Default is 20.
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        PageQualityResult with pagination info and content array of failed QualityResult

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> failed = await get_failed_results()
        >>> print(f"Total failed inspections: {failed['totalElements']}")
        Total failed inspections: 367
    """
    params = {}
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    response = await _make_request("GET", "/quality/results/failed", base_url=base_url, params=params if params else None)
    return response.json()


async def get_results_by_defect_type(defect_type: str, ) -> List[QualityResult]:
    base_url: str = DEFAULT_BASE_URL
    """
    Get quality results by defect type.

    Returns all quality inspection results with a specific defect type from the SECOM MES database.

    Agent_card:
    -----------
    skill_id: get_results_by_defect_type
    skill_name: Get Quality Results by Defect Type
    description: Retrieves all quality inspection results filtered by a specific defect type.
                 Supports defect-specific analysis, identifying equipment or process issues
                 related to particular defect categories, and targeted quality improvement.
    capabilities:
      - Filter quality results by defect type
      - Support defect trend analysis
      - Enable defect-specific reporting
      - Identify defect patterns
      - Support targeted quality improvement initiatives

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - defect_type
      properties:
        defect_type:
          type: string
          description: Type of defect to filter by
          example: "electrical_fail"
          enum: ["contamination", "dimensional_oor", "electrical_fail", "surface_defect"]

    output_schema:
      type: array
      description: List of quality results filtered by defect type
      items:
        type: object
        properties:
          resultId:
            type: integer
            format: int32
            description: Unique quality result identifier
          lot:
            type: object
            description: Associated lot information with lotId, lotNumber, productType, equipment, operator, shift, status
          classification:
            type: integer
            format: int32
            description: Classification result (-1 = Pass, 1 = Fail)
          testTimestampRaw:
            type: string
            description: Raw test timestamp string
          testDatetime:
            type: string
            format: date-time
            description: Date and time of test
          predictedRisk:
            type: number
            format: float
            description: Predicted risk score (0.0 to 1.0)
          riskScore:
            type: number
            format: float
            description: Risk score
          riskFactors:
            type: string
            description: Risk factors identified
          modelVersion:
            type: string
            description: ML model version used for prediction
          qualityScore:
            type: number
            format: float
            description: Quality score
          defectType:
            type: string
            description: Type of defect (matches input filter)
          defectCode:
            type: string
            description: Defect code
          defectLocation:
            type: string
            description: Location of defect
          inspector:
            type: object
            description: Inspector operator information
          notes:
            type: string
            description: Inspection notes
          reviewer:
            type: object
            description: Reviewer operator information
          reviewedAt:
            type: string
            format: date-time
            description: Review timestamp
          disposition:
            type: string
            description: Disposition decision
          createdAt:
            type: string
            format: date-time
            description: Record creation timestamp
          updatedAt:
            type: string
            format: date-time
            description: Record update timestamp

    error_responses:
      - status: 404
        description: No results found for specified defect type
      - status: 500
        description: Internal server error

    Args:
        defect_type: Type of defect to filter by (contamination, dimensional_oor, electrical_fail, surface_defect)
        base_url: Base URL for the API (default: http://localhost:8080/api/v1)

    Returns:
        List of QualityResult dictionaries with the specified defect type

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> electrical_defects = await get_results_by_defect_type("electrical_fail")
        >>> print(f"Found {len(electrical_defects)} lots with electrical failures")
        Found 25 lots with electrical failures
    """
    response = await _make_request("GET", f"/quality/results/defect/{defect_type}", base_url=base_url)
    return response.json()


# ============================================================================
# Utility Functions for AI Agents
# ============================================================================

async def get_quality_summary(result_id: int, ) -> Dict[str, Any]:
    base_url: str = DEFAULT_BASE_URL
    """
    Get comprehensive quality summary for a result.

    This is a convenience function that provides a quality result with additional
    context for AI agents needing complete information.

    Agent_card:
    -----------
    skill_id: get_quality_summary
    skill_name: Get Comprehensive Quality Summary
    description: Retrieves complete quality information including inspection details
                 and contextual analysis. Provides a comprehensive view of a quality
                 result with derived metrics and status indicators.
    capabilities:
      - Generate comprehensive quality profiles
      - Support quality performance analysis
      - Enable holistic quality assessment
      - Facilitate quality reporting

    A2A Spec:
    ---------
    input_schema:
      type: object
      required:
        - result_id
      properties:
        result_id:
          type: integer
          format: int32
          description: The unique identifier of the quality result
          example: 1

    output_schema:
      type: object
      properties:
        result:
          type: object
          description: Full quality result details
        is_passed:
          type: boolean
          description: Whether the inspection passed (classification = -1)
        is_high_risk:
          type: boolean
          description: Whether the result is high risk (predictedRisk > 0.7)
        has_defects:
          type: boolean
          description: Whether defects were found (defectType is not null)
        summary_generated_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp when the summary was generated

    error_responses:
      - status: 404
        description: Quality result with specified ID not found
      - status: 500
        description: Internal server error

    Args:
        result_id: The unique identifier of the quality result
        base_url: Base URL for the API

    Returns:
        Dictionary with quality details and derived metrics

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> summary = await get_quality_summary(1)
        >>> print(f"Result passed: {summary['is_passed']}, High risk: {summary['is_high_risk']}")
    """
    result = await get_result_by_id(result_id, base_url)

    return {
        "result": result,
        "is_passed": result.get("classification") == -1,
        "is_high_risk": result.get("predictedRisk", 0) > 0.7,
        "has_defects": result.get("defectType") is not None,
        "summary_generated_at": datetime.now().isoformat()
    }


async def get_quality_statistics() -> Dict[str, Any]:
    base_url: str = DEFAULT_BASE_URL
    """
    Get quality statistics overview.

    Calculates aggregate statistics across all quality results for reporting
    and dashboard purposes.

    Agent_card:
    -----------
    skill_id: get_quality_statistics
    skill_name: Get Quality Statistics
    description: Calculates and returns aggregate quality statistics including
                 pass/fail rates, average quality score, and risk level breakdown.
                 Ideal for quality dashboards and KPI reporting.
    capabilities:
      - Calculate quality KPIs
      - Generate statistical summaries
      - Support quality dashboards
      - Enable trend analysis

    A2A Spec:
    ---------
    input_schema:
      type: object
      properties: {}

    output_schema:
      type: object
      properties:
        total_results:
          type: integer
          description: Total number of quality results
        passed_count:
          type: integer
          description: Number of passed inspections (classification = -1)
        failed_count:
          type: integer
          description: Number of failed inspections (classification = 1)
        high_risk_count:
          type: integer
          description: Number of high risk results (predictedRisk > 0.7)
        pass_rate:
          type: number
          format: float
          description: Percentage of passed inspections
        average_quality_score:
          type: number
          format: float
          description: Average qualityScore across all results
        statistics_generated_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp when statistics were generated

    error_responses:
      - status: 500
        description: Internal server error

    Args:
        base_url: Base URL for the API

    Returns:
        Dictionary with aggregate quality statistics

    Raises:
        httpx.HTTPStatusError: If the API request fails

    Example:
        >>> stats = await get_quality_statistics()
        >>> print(f"Pass rate: {stats['pass_rate']:.1f}%")
        Pass rate: 85.3%
    """
    all_results_page = await get_all_results()
    passed_results_page = await get_passed_results(base_url=base_url)
    failed_results_page = await get_failed_results(base_url=base_url)
    high_risk_results = await get_high_risk_results(base_url=base_url)

    total = all_results_page.get("totalElements", 0)
    passed_count = passed_results_page.get("totalElements", 0)
    failed_count = failed_results_page.get("totalElements", 0)

    # Calculate average quality score from content
    content = all_results_page.get("content", [])
    avg_quality_score = sum(r.get("qualityScore", 0) or 0 for r in content) / len(content) if content else 0

    return {
        "total_results": total,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "high_risk_count": len(high_risk_results),
        "pass_rate": (passed_count / total * 100) if total > 0 else 0,
        "average_quality_score": avg_quality_score,
        "statistics_generated_at": datetime.now().isoformat()
    }


async def safe_get_result(result_id: int, ) -> Optional[QualityResult]:
    base_url: str = DEFAULT_BASE_URL
    """
    Safely get quality result by ID with error handling.

    Returns None if result not found instead of raising an exception.
    Useful for AI agents that need graceful error handling.

    Args:
        result_id: The unique identifier of the quality result
        base_url: Base URL for the API

    Returns:
        QualityResult dictionary or None if not found or on error

    Example:
        >>> result = await safe_get_result(999)
        >>> if result is None:
        ...     print("Quality result not found")
    """
    try:
        return await get_result_by_id(result_id, base_url)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise
    except httpx.HTTPError:
        return None


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Type definitions
    'QualityResult',
    'Lot',

    # Core API functions (matching OpenAPI spec)
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
