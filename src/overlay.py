"""
Overlay system for captions and progress bar.
"""
import numpy as np
import cv2
from typing import List, Tuple


class Overlay:
    """Handles caption and progress bar overlays."""
    
    def __init__(self, config):
        """Initialize overlay system.
        
        Args:
            config: GenerationConfig instance
        """
        self.config = config
        self.captions = []
        
    def add_caption(self, text: str, start_frame: int):
        """Add a caption to display.
        
        Args:
            text: Caption text
            start_frame: Frame to start displaying caption
        """
        end_frame = start_frame + int(self.config.caption_duration * self.config.fps)
        self.captions.append({
            'text': text,
            'start': start_frame,
            'end': end_frame
        })
    
    def draw_caption(self, frame: np.ndarray, text: str, 
                    alpha: float = 1.0) -> np.ndarray:
        """Draw caption on frame.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            text: Caption text
            alpha: Opacity (0.0 to 1.0)
            
        Returns:
            Frame with caption
        """
        h, w = frame.shape[:2]
        result = frame.copy()
        
        # Position in upper third
        pos_y = int(h * 0.25)
        
        # Font settings
        font = cv2.FONT_HERSHEY_BOLD
        font_scale = self.config.caption_font_size / 30.0
        thickness = 3
        
        # Calculate text size
        (text_w, text_h), baseline = cv2.getTextSize(text, font, 
                                                     font_scale, thickness)
        
        # Center horizontally
        pos_x = (w - text_w) // 2
        
        # Draw shadow/outline (black)
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    cv2.putText(result, text, 
                              (pos_x + dx, pos_y + dy),
                              font, font_scale, (0, 0, 0),
                              thickness + 1, cv2.LINE_AA)
        
        # Draw main text (white)
        cv2.putText(result, text, (pos_x, pos_y),
                   font, font_scale, (255, 255, 255),
                   thickness, cv2.LINE_AA)
        
        # Apply alpha blending if needed
        if alpha < 1.0:
            result = cv2.addWeighted(frame, 1 - alpha, result, alpha, 0)
        
        return result
    
    def draw_progress_bar(self, frame: np.ndarray, 
                         progress: float) -> np.ndarray:
        """Draw progress bar on frame.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            progress: Progress value (0.0 to 1.0)
            
        Returns:
            Frame with progress bar
        """
        h, w = frame.shape[:2]
        result = frame.copy()
        
        # Progress bar dimensions
        bar_height = self.config.progress_bar_height
        bar_y = h - int(h * 0.05)  # Bottom 5% of frame
        bar_width = int(w * 0.9)  # 90% of width
        bar_x = (w - bar_width) // 2
        
        # Background bar (dark)
        cv2.rectangle(result, 
                     (bar_x, bar_y), 
                     (bar_x + bar_width, bar_y + bar_height),
                     (40, 40, 40), -1)
        
        # Progress fill (neon color)
        fill_width = int(bar_width * progress)
        neon_color = self.config.neon_colors[0]  # Cyan
        neon_bgr = (neon_color[2], neon_color[1], neon_color[0])
        
        if fill_width > 0:
            cv2.rectangle(result,
                         (bar_x, bar_y),
                         (bar_x + fill_width, bar_y + bar_height),
                         neon_bgr, -1)
        
        # Apply opacity
        overlay = result.copy()
        alpha = self.config.progress_bar_opacity
        result = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
        
        return result
    
    def apply_overlays(self, frame: np.ndarray, 
                      frame_idx: int, total_frames: int) -> np.ndarray:
        """Apply all overlays to frame.
        
        Args:
            frame: Input frame (H, W, C) in BGR
            frame_idx: Current frame index
            total_frames: Total number of frames
            
        Returns:
            Frame with overlays
        """
        result = frame.copy()
        
        # Draw captions
        for caption in self.captions:
            if caption['start'] <= frame_idx < caption['end']:
                # Calculate fade in/out
                fade_frames = self.config.fps // 5  # 0.2s fade
                
                if frame_idx < caption['start'] + fade_frames:
                    # Fade in
                    alpha = (frame_idx - caption['start']) / fade_frames
                    # Scale animation
                    scale = 0.9 + 0.1 * alpha
                elif frame_idx > caption['end'] - fade_frames:
                    # Fade out
                    alpha = (caption['end'] - frame_idx) / fade_frames
                    scale = 1.0
                else:
                    alpha = 1.0
                    scale = 1.0
                
                result = self.draw_caption(result, caption['text'], alpha)
        
        # Draw progress bar
        progress = frame_idx / total_frames
        result = self.draw_progress_bar(result, progress)
        
        return result
