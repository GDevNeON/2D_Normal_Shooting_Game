import pygame

def draw_text(surface, text, font, text_color, x, y, wrap_width=None):
    """
    Draw text on a surface at the specified position with optional word wrapping
    
    Args:
        surface: The pygame surface to draw on
        text: The text to draw
        font: The pygame font to use
        text_color: The color of the text (RGB tuple)
        x: X position (center x if wrap_width is provided, left otherwise)
        y: Y position (top position for the text block)
        wrap_width: Optional maximum width for text wrapping. If provided, text will be centered.
    """
    if wrap_width is None:
        img = font.render(text, True, text_color)
        surface.blit(img, (x - img.get_width() // 2, y))
        return
    
    # Split text into words and build lines
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        # Create a test line with the new word
        test_line = ' '.join(current_line + [word])
        test_width = font.size(test_line)[0]
        
        if test_width <= wrap_width or not current_line:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    # Render each line
    line_height = font.get_linesize()
    for i, line in enumerate(lines):
        img = font.render(line, True, text_color)
        surface.blit(img, (x - img.get_width() // 2, y + i * line_height))

def draw_image(surface, img, scale, x, y):
    """
    Draw a scaled image on a surface at the specified position
    
    Args:
        surface: The pygame surface to draw on
        img: The image to draw
        scale: Scale factor for the image
        x: X position
        y: Y position
    """
    sub_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    surface.blit(sub_img, (x, y))
