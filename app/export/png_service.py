import io
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from PIL import Image, ImageDraw, ImageFont


def generate_receipt_png(db: Session, receipt_id: int, user_id: int) -> io.BytesIO:
    """
    Genera un PNG del recibo usando Pillow (sin dependencias del sistema).
    Valida que el contrato exista y pertenezca al arrendatario solicitante.
    Retorna un BytesIO listo para StreamingResponse.
    """
    from app.models.contract import Contract

    contract = db.query(Contract).filter(Contract.id == receipt_id).first()
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    if contract.arrendatario_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this receipt")

    width, height = 640, 400
    bg_color = (255, 255, 255)
    border_color = (221, 221, 221)
    title_color = (44, 62, 80)
    text_color = (51, 51, 51)
    accent_color = (52, 152, 219)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_body = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    # Border box
    draw.rectangle([20, 20, width - 20, height - 20], outline=border_color, width=2)

    # Title
    draw.text((40, 40), "Recibo de Arrendamiento", font=font_title, fill=title_color)
    # Accent underline
    draw.line([40, 68, 400, 68], fill=accent_color, width=2)

    # Body fields
    lines = [
        f"Contrato ID:  {contract.id}",
        f"Dirección:    {contract.direccion}",
        f"Tipo:         {contract.tipo}",
        f"Valor:        ${contract.valor}",
    ]
    if contract.servicios:
        lines.append(f"Servicios:    {contract.servicios}")

    y = 90
    for line in lines:
        draw.text((40, y), line, font=font_body, fill=text_color)
        y += 28

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
