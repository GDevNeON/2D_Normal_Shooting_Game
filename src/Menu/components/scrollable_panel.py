import pygame

class ScrollablePanel:
    def __init__(self, x, y, width, height, background_color=(30, 30, 30), 
                 scroll_bar_color=(100, 100, 100), scroll_bar_hover_color=(120, 120, 120), 
                 scroll_bar_width=10, padding=5):
        """
        Initialize a scrollable panel
        
        Args:
            x, y: Position of the panel
            width, height: Dimensions of the visible area
            background_color: Background color of the panel
            scroll_bar_color: Color of the scroll bar
            scroll_bar_hover_color: Color of the scroll bar when hovered
            scroll_bar_width: Width of the scroll bar
            padding: Padding inside the panel
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.background_color = background_color
        self.scroll_bar_color = scroll_bar_color
        self.scroll_bar_hover_color = scroll_bar_hover_color
        self.scroll_bar_width = scroll_bar_width
        self.padding = padding
        
        # Content surface (can be larger than visible area)
        self.content_surface = None
        self.content_rect = pygame.Rect(0, 0, width - scroll_bar_width - padding * 2, 0)
        
        # Scroll properties
        self.scroll_y = 0
        self.scroll_speed = 20
        self.is_scrolling = False
        self.scroll_bar_hovered = False
        
        # Surface for the visible area (with scrollbar)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
    def update_content(self, content_surface):
        """Update the content of the scrollable panel"""
        self.content_surface = content_surface
        if content_surface:
            self.content_rect = pygame.Rect(0, 0, content_surface.get_width(), content_surface.get_height())
        else:
            self.content_rect = pygame.Rect(0, 0, 0, 0)
        
        # Reset scroll position when content updates
        self.scroll_y = 0
        
    def handle_event(self, event):
        """Handle events for scrolling"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll(-self.scroll_speed)
                return True
            elif event.button == 5:  # Scroll down
                self.scroll(self.scroll_speed)
                return True
            
            # Check if scroll bar is clicked
            scroll_bar_rect = self._get_scroll_bar_rect()
            if scroll_bar_rect.collidepoint(pygame.mouse.get_pos()):
                self.is_scrolling = True
                self.scroll_bar_click_y = pygame.mouse.get_pos()[1] - scroll_bar_rect.y
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_scrolling:
                self.is_scrolling = False
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            if self.is_scrolling:
                # Get current mouse position
                scroll_bar_rect = self._get_scroll_bar_rect()
                current_y = pygame.mouse.get_pos()[1] - self.rect.y
                
                # Calculate new scroll bar position
                new_y = current_y - self.scroll_bar_click_y
                
                # Calculate scroll position based on new scroll bar position
                visible_area = self.rect.height - 2 * self.padding
                max_scroll = max(0, self.content_rect.height - visible_area)
                scroll_ratio = (new_y - self.padding) / (self.rect.height - 2 * self.padding - scroll_bar_rect.height)
                self.scroll_y = max(0, min(max_scroll, scroll_ratio * max_scroll))
                return True
                
            # Check if mouse is over scroll bar
            scroll_bar_rect = self._get_scroll_bar_rect()
            self.scroll_bar_hovered = scroll_bar_rect.collidepoint(pygame.mouse.get_pos())
            
        return False
        
    def scroll(self, dy):
        """Scroll the content by dy pixels"""
        if self.content_surface is None:
            return
            
        # Calculate new scroll position
        new_scroll = self.scroll_y + dy
        
        # Clamp scroll position
        visible_area = self.rect.height - 2 * self.padding
        max_scroll = max(0, self.content_rect.height - visible_area)
        self.scroll_y = max(0, min(max_scroll, new_scroll))
        
    def _get_scroll_bar_rect(self):
        """Get the rectangle for the scroll bar"""
        if self.content_rect.height <= self.rect.height - 2 * self.padding:
            return pygame.Rect(0, 0, 0, 0)
            
        # Calculate scroll bar height based on content ratio
        visible_ratio = (self.rect.height - 2 * self.padding) / self.content_rect.height
        scroll_bar_height = max(30, (self.rect.height - 2 * self.padding) * visible_ratio)
        
        # Calculate scroll bar position based on scroll position
        visible_area = self.rect.height - 2 * self.padding
        max_scroll = max(1, self.content_rect.height - visible_area)  # Avoid division by zero
        scroll_ratio = self.scroll_y / max_scroll
        scroll_bar_y = self.rect.y + self.padding + scroll_ratio * (self.rect.height - 2 * self.padding - scroll_bar_height)
        
        return pygame.Rect(
            self.rect.right - self.scroll_bar_width - 2,
            scroll_bar_y,
            self.scroll_bar_width,
            scroll_bar_height
        )
        
    def update(self):
        """Update the scrollable panel state"""
        # Currently no per-frame updates needed, but the method is required by the caller
        pass
        
    def draw(self, screen):
        """Draw the scrollable panel"""
        # Clear the surface
        self.surface.fill((0, 0, 0, 0))
        
        # Draw background
        pygame.draw.rect(self.surface, self.background_color, 
                        (0, 0, self.rect.width, self.rect.height), 
                        border_radius=5)
        
        if self.content_surface is None:
            screen.blit(self.surface, self.rect)
            return
            
        # Calculate content area
        content_width = self.rect.width - self.scroll_bar_width - 3 * self.padding
        content_height = self.rect.height - 2 * self.padding
        
        # Create a clip rect for the content
        clip_rect = pygame.Rect(
            self.rect.x + self.padding,
            self.rect.y + self.padding,
            content_width,
            content_height
        )
        
        # Save the current clip rect
        old_clip = screen.get_clip()
        screen.set_clip(clip_rect)
        
        # Calculate source and destination rectangles for blitting
        source_rect = pygame.Rect(
            0,
            self.scroll_y,
            content_width,
            min(content_height, self.content_rect.height - self.scroll_y)
        )
        
        dest_rect = pygame.Rect(
            self.rect.x + self.padding,
            self.rect.y + self.padding,
            content_width,
            min(content_height, self.content_rect.height - self.scroll_y)
        )
        
        # Draw the visible portion of the content
        screen.blit(self.content_surface, dest_rect, source_rect)
        
        # Restore the old clip rect
        screen.set_clip(old_clip)
        
        # Draw scroll bar if needed
        if self.content_rect.height > self.rect.height - 2 * self.padding:
            scroll_bar_rect = self._get_scroll_bar_rect()
            
            # Draw scroll bar track
            pygame.draw.rect(
                self.surface, 
                (50, 50, 50, 100),
                (
                    self.rect.width - self.scroll_bar_width - 2,
                    self.padding,
                    self.scroll_bar_width,
                    self.rect.height - 2 * self.padding
                ),
                border_radius=5
            )
            
            # Draw scroll bar thumb
            pygame.draw.rect(
                self.surface,
                self.scroll_bar_hover_color if self.scroll_bar_hovered else self.scroll_bar_color,
                (
                    scroll_bar_rect.x - self.rect.x,
                    scroll_bar_rect.y - self.rect.y,
                    scroll_bar_rect.width,
                    scroll_bar_rect.height
                ),
                border_radius=5
            )
        
        # Draw the panel surface
        screen.blit(self.surface, self.rect)
        
        # Draw border
        pygame.draw.rect(screen, (100, 100, 100, 150), self.rect, 1, border_radius=5)
