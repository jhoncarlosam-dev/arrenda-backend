from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.security.dependencies import require_role
from app.export import pdf_service, png_service

router = APIRouter()

@router.get("/{id}/export/pdf", summary="Exportar recibo a PDF")
def export_receipt_pdf(
    id: int,
    current_user: User = Depends(require_role(RoleEnum.ARRENDATARIO.value)),
) -> StreamingResponse:
    """
    Export receipt as PDF.
    Only ARRENDATARIO can access this.
    """
    try:
        pdf_buffer = pdf_service.generate_receipt_pdf(receipt_id=id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error generating PDF: {str(e)}"
        )
        
    headers = {
        "Content-Disposition": f"attachment; filename=receipt_{id}.pdf"
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)

@router.get("/{id}/export/png", summary="Exportar recibo a PNG")
def export_receipt_png(
    id: int,
    current_user: User = Depends(require_role(RoleEnum.ARRENDATARIO.value)),
) -> StreamingResponse:
    """
    Export receipt as PNG.
    Only ARRENDATARIO can access this.
    """
    try:
        png_buffer = png_service.generate_receipt_png(receipt_id=id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error generating PNG: {str(e)}"
        )
        
    headers = {
        "Content-Disposition": f"attachment; filename=receipt_{id}.png"
    }
    return StreamingResponse(png_buffer, media_type="image/png", headers=headers)
