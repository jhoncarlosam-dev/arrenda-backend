import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_receipt_pdf(receipt_id: int) -> io.BytesIO:
    """
    Genera un archivo PDF para el recibo especificado utilizando ReportLab.
    Retorna un buffer en memoria (BytesIO) listo para ser enviado en un StreamingResponse.
    """
    buffer = io.BytesIO()
    
    # Crear el lienzo PDF
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título y contenido simple
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Recibo de Arrendamiento")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Recibo ID: {receipt_id}")
    c.drawString(50, height - 100, "Gracias por su pago.")
    c.drawString(50, height - 120, "Este documento es un comprobante válido.")
    
    # Guardar y posicionar al inicio
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer
