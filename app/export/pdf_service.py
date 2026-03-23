import io
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_receipt_pdf(db: Session, receipt_id: int, user_id: int) -> io.BytesIO:
    """
    Genera un PDF para el contrato especificado usando ReportLab.
    Valida que el contrato exista y pertenezca al arrendatario solicitante.
    Retorna un BytesIO listo para StreamingResponse.
    """
    from app.models.contract import Contract

    contract = db.query(Contract).filter(Contract.id == receipt_id).first()
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    if contract.arrendatario_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this receipt")

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Recibo de Arrendamiento")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Contrato ID: {contract.id}")
    c.drawString(50, height - 110, f"Dirección: {contract.direccion}")
    c.drawString(50, height - 130, f"Tipo: {contract.tipo}")
    c.drawString(50, height - 150, f"Valor: ${contract.valor}")
    if contract.servicios:
        c.drawString(50, height - 170, f"Servicios: {contract.servicios}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
