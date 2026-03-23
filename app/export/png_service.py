import io
import imgkit
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def generate_receipt_png(db: Session, receipt_id: int, user_id: int) -> io.BytesIO:
    """
    Genera un PNG renderizando HTML mediante imgkit (requiere wkhtmltoimage).
    Valida que el contrato exista y pertenezca al arrendatario solicitante.
    Retorna un BytesIO listo para StreamingResponse.
    """
    from app.models.contract import Contract

    contract = db.query(Contract).filter(Contract.id == receipt_id).first()
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    if contract.arrendatario_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this receipt")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 40px;
                color: #333;
                background-color: #fff;
            }}
            .receipt-box {{
                border: 2px solid #ddd;
                padding: 20px;
                border-radius: 8px;
                max-width: 600px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            p {{ margin: 8px 0; }}
        </style>
    </head>
    <body>
        <div class="receipt-box">
            <h1>Recibo de Arrendamiento</h1>
            <p><strong>Contrato ID:</strong> {contract.id}</p>
            <p><strong>Dirección:</strong> {contract.direccion}</p>
            <p><strong>Tipo:</strong> {contract.tipo}</p>
            <p><strong>Valor:</strong> ${contract.valor}</p>
            {'<p><strong>Servicios:</strong> ' + contract.servicios + '</p>' if contract.servicios else ''}
        </div>
    </body>
    </html>
    """

    try:
        options = {'format': 'png', 'encoding': 'UTF-8', 'quiet': ''}
        img_bytes = imgkit.from_string(html_content, False, options=options)
        buffer = io.BytesIO(img_bytes)
        buffer.seek(0)
        return buffer
    except OSError as e:
        raise Exception(
            "Error al generar PNG. Asegúrese de que wkhtmltopdf/wkhtmltoimage está instalado en el sistema."
        ) from e
