import io
import imgkit

def generate_receipt_png(receipt_id: int) -> io.BytesIO:
    """
    Genera un archivo PNG renderizando HTML mediante imgkit (requiere wkhtmltoimage).
    Retorna un buffer en memoria (BytesIO) listo para StreamingResponse.
    """
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
        </style>
    </head>
    <body>
        <div class="receipt-box">
            <h1>Recibo de Arrendamiento</h1>
            <p><strong>Recibo ID:</strong> {receipt_id}</p>
            <p>Gracias por su pago.</p>
            <p>Este documento es un comprobante válido generado electrónicamente.</p>
        </div>
    </body>
    </html>
    """
    
    try:
        # Generar imagen desde el HTML string. Retorna bytes.
        options = {
            'format': 'png',
            'encoding': "UTF-8",
            'quiet': ''
        }
        img_bytes = imgkit.from_string(html_content, False, options=options)
        
        buffer = io.BytesIO(img_bytes)
        buffer.seek(0)
        return buffer
    except OSError as e:
        raise Exception("Error al generar PNG. Asegúrese de que wkhtmltopdf/wkhtmltoimage está instalado en el sistema.") from e
