import os
import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger("zoo_bot.media")

async def generate_result_image(
    animal_image: str,
    animal_name: str,
    user_name: str
) -> str:
    """
    Генерирует изображение с результатом викторины:
    - Накладывает имя животного и имя пользователя.
    - Добавляет полупрозрачные плашки под текст для улучшения читаемости.
    - Вставляет логотип зоопарка (если доступен).
    """
    logger.info(f"Начинаем генерацию изображения для {animal_name} и пользователя {user_name}")

    try:
        base = Image.open(animal_image).convert("RGBA")
    except Exception as e:
        logger.error(f"Не удалось открыть исходное изображение: {animal_image}")
        raise RuntimeError(f"Ошибка при открытии изображения: {e}") from e

    # Создаём слой для плашек
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    margin = 25

    # Пути к шрифтам
    fonts_dir = "media/fonts"
    bold_font_path = os.path.join(fonts_dir, "ALS_Story_2.0_B.otf")
    regular_font_path = os.path.join(fonts_dir, "ALS_Story_2.0_I.otf")

    # Загрузка шрифтов
    try:
        title_font = ImageFont.truetype(bold_font_path, 48)
    except Exception:
        logger.warning(f"Шрифт {bold_font_path} недоступен. Используется стандартный.")
        title_font = ImageFont.load_default()

    try:
        text_font = ImageFont.truetype(regular_font_path, 36)
    except Exception:
        logger.warning(f"Шрифт {regular_font_path} недоступен. Используется стандартный.")
        text_font = ImageFont.load_default()

    # Рисуем подпись пользователя сверху
    caption = f"{user_name}, твое тотемное животное:"
    caption_width, caption_height = draw.textlength(caption, font=text_font), text_font.size

    # Позиция верхней плашки
    caption_rect_position = (
        # margin - 10,
        0,
        margin - 10,
        base.width,
        margin + caption_height + 20
    )

    draw.rounded_rectangle(caption_rect_position, radius=0, fill=(255, 255, 255, 150))
    # text_x = (caption_rect_position[0] + caption_rect_position[2] - caption_width) // 2
    text_x = margin
    text_y = (caption_rect_position[1] + caption_rect_position[3] - caption_height) // 2 + 1
    draw.text((text_x, text_y), caption, font=text_font, fill="black")

    #  Рисуем название животного внизу слева (не по центру!)
    title_text = animal_name
    title_width, title_height = draw.textlength(title_text, font=title_font), title_font.size

    # Позиция нижней плашки — слева, чуть выше логотипа
    title_rect_position = (
        0,
        base.height - margin - title_height - 30,  # делаем больше отступа, чтобы освободить место для логотипа
        margin + title_width + 10,
        base.height - margin - 10
    )

    draw.rounded_rectangle(title_rect_position, radius=0, fill=(0, 0, 0, 120))
    text_x = margin
    text_y = (title_rect_position[1] + title_rect_position[3] - title_height) // 2 + 4
    draw.text((text_x, text_y), title_text, font=title_font, fill="white")

    # Объединяем основное изображение и оверлей с подложками
    base = Image.alpha_composite(base.convert("RGBA"), overlay)

    # Логотип зоопарка
    logo_path = "media/logo/mzoo_logo.png"
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_width = base.width // 5
            logo = logo.resize(
                (logo_width, int(logo_width * logo.height / logo.width)),
                Image.Resampling.LANCZOS
            )

            position = (base.width - logo.width - margin, base.height - logo.height - margin)

            # Добавляем подложку под логотип
            overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rounded_rectangle(
                [
                    position[0] - 10,
                    position[1] - 10,
                    position[0] + logo.width + 10,
                    position[1] + logo.height + 10
                ],
                fill=(255, 255, 255, 150),
                radius=100
            )
            base = Image.alpha_composite(base, overlay)
            base.paste(logo, position, mask=logo)
        except Exception as e:
            logger.exception(f"Ошибка при добавлении логотипа: {logo_path} — {e}")
    else:
        logger.warning(f"Логотип не найден по пути: {logo_path}")

    # Сохранение результата
    output_dir = "media/generated"
    os.makedirs(output_dir, exist_ok=True)
    safe_user_name = "".join(char for char in user_name if char.isalnum())
    filename = f"{safe_user_name}_{animal_name}.jpg"
    output_path = os.path.join(output_dir, filename)

    try:
        # Конвертируем в RGB перед сохранением как JPEG
        final_image = base.convert("RGB")
        final_image.save(output_path, "JPEG", quality=85)
        logger.info(f"Изображение успешно сохранено: {output_path}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении изображения: {output_path} — {e}")
        raise RuntimeError(f"Не удалось сохранить изображение: {e}") from e

    return output_path