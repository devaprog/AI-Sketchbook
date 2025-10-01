import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
INITIAL_WIDTH, INITIAL_HEIGHT = 1000, 700
SLIDER_SECTION_WIDTH = 350
GRAPH_MARGIN = 60
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 150, 0)
DARK_BLUE = (0, 0, 150)
LIGHT_BLUE = (173, 216, 230)

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Create resizable window
screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sigmoid Activation Function Visualizer")
clock = pygame.time.Clock()

# Range input properties
range_min = -10.0
range_max = 10.0
min_input_active = False
max_input_active = False
min_input_text = str(range_min)
max_input_text = str(range_max)
input_box_height = 35
input_box_width = 100

# Slider properties
slider_value = 0.0
slider_knob_radius = 10
dragging = False

# Fonts
font = None
title_font = None
small_font = None

def initialize_fonts():
    global font, title_font, small_font
    # Scale fonts based on window height
    base_size = max(16, INITIAL_HEIGHT // 40)
    font = pygame.font.SysFont('Arial', base_size)
    title_font = pygame.font.SysFont('Arial', base_size + 8, bold=True)
    small_font = pygame.font.SysFont('Arial', base_size - 4)

initialize_fonts()

def draw_input_box(x, y, width, height, text, active):
    color = BLUE if active else GRAY
    # Draw box
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    pygame.draw.rect(screen, WHITE, (x + 2, y + 2, width - 4, height - 4))
    
    # Draw text (truncate if too long)
    display_text = text
    text_surface = small_font.render(display_text, True, BLACK)
    max_text_width = width - 20
    if text_surface.get_width() > max_text_width:
        # Find how many characters fit
        for i in range(len(text), 0, -1):
            test_surface = small_font.render(text[:i], True, BLACK)
            if test_surface.get_width() <= max_text_width:
                display_text = text[:i]
                break
    
    text_surface = small_font.render(display_text, True, BLACK)
    screen.blit(text_surface, (x + 5, y + (height - text_surface.get_height()) // 2))
    
    return pygame.Rect(x, y, width, height)

def parse_float_input(text, default):
    try:
        return float(text)
    except ValueError:
        return default

def update_range_from_input():
    global range_min, range_max, slider_value, max_input_text
    
    # Parse current input texts
    new_min = parse_float_input(min_input_text, range_min)
    new_max = parse_float_input(max_input_text, range_max)
    
    # Ensure valid range
    if new_min >= new_max:
        new_max = new_min + 1.0
        max_input_text = f"{new_max:.2f}"
    
    range_min = new_min
    range_max = new_max
    
    # Ensure slider value stays within new range
    slider_value = max(range_min, min(range_max, slider_value))

# Main loop
running = True
while running:
    current_width, current_height = screen.get_size()
    
    # Recalculate dimensions based on current window size
    slider_section_width = max(300, current_width * 0.35)
    graph_section_width = current_width - slider_section_width
    graph_margin = max(40, current_height * 0.06)
    
    # Update fonts if window size changed significantly
    if current_height != INITIAL_HEIGHT:
        base_size = max(14, current_height // 45)
        font = pygame.font.SysFont('Arial', base_size)
        title_font = pygame.font.SysFont('Arial', base_size + 6, bold=True)
        small_font = pygame.font.SysFont('Arial', base_size - 2)
    
    # === LEFT SIDE LAYOUT ===
    left_section_top_margin = 40
    left_section_bottom_margin = 40
    
    # Calculate vertical spacing for left panel
    available_height = current_height - left_section_top_margin - left_section_bottom_margin
    section_spacing = available_height // 8  # Divide into 8 equal sections
    
    # Position elements in left panel with proper spacing
    range_title_y = left_section_top_margin + section_spacing * 1
    input_boxes_y = left_section_top_margin + section_spacing * 2
    instructions_y = left_section_top_margin + section_spacing * 3
    slider_title_y = left_section_top_margin + section_spacing * 4
    slider_y = left_section_top_margin + section_spacing * 5
    slider_labels_y = left_section_top_margin + section_spacing * 6
    input_value_y = left_section_top_margin + section_spacing * 7
    
    slider_x = 40
    slider_length = slider_section_width - 80
    
    # Update slider knob position
    slider_knob_x = slider_x + (slider_value - range_min) / (range_max - range_min) * slider_length
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check range input boxes
            min_input_rect = pygame.Rect(slider_x, input_boxes_y, input_box_width, input_box_height)
            max_input_rect = pygame.Rect(slider_x + 120, input_boxes_y, input_box_width, input_box_height)
            
            min_input_active = min_input_rect.collidepoint(mouse_x, mouse_y)
            max_input_active = max_input_rect.collidepoint(mouse_x, mouse_y)
            
            # Check if mouse is on the slider knob
            if ((mouse_x - slider_knob_x) ** 2 + (mouse_y - slider_y) ** 2) <= slider_knob_radius ** 2:
                dragging = True
            else:
                # Check if clicking on slider track
                slider_rect = pygame.Rect(slider_x, slider_y - 8, slider_length, 16)
                if slider_rect.collidepoint(mouse_x, mouse_y):
                    slider_knob_x = max(slider_x, min(slider_x + slider_length, mouse_x))
                    slider_value = range_min + (slider_knob_x - slider_x) / slider_length * (range_max - range_min)
                    dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Update slider knob position
                slider_knob_x = max(slider_x, min(slider_x + slider_length, mouse_x))
                # Calculate slider value
                slider_value = range_min + (slider_knob_x - slider_x) / slider_length * (range_max - range_min)
        
        elif event.type == pygame.KEYDOWN:
            if min_input_active:
                if event.key == pygame.K_RETURN:
                    update_range_from_input()
                    min_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    min_input_text = min_input_text[:-1]
                    update_range_from_input()  # Auto-update while typing
                elif event.key == pygame.K_TAB:
                    min_input_active = False
                    max_input_active = True
                else:
                    # Allow numbers, decimal point, and minus sign
                    if event.unicode.isdigit() or event.unicode == '.' or (event.unicode == '-' and len(min_input_text) == 0):
                        min_input_text += event.unicode
                        update_range_from_input()  # Auto-update while typing
            
            elif max_input_active:
                if event.key == pygame.K_RETURN:
                    update_range_from_input()
                    max_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    max_input_text = max_input_text[:-1]
                    update_range_from_input()  # Auto-update while typing
                elif event.key == pygame.K_TAB:
                    max_input_active = False
                    min_input_active = True
                else:
                    # Allow numbers, decimal point, and minus sign
                    if event.unicode.isdigit() or event.unicode == '.' or (event.unicode == '-' and len(max_input_text) == 0):
                        max_input_text += event.unicode
                        update_range_from_input()  # Auto-update while typing
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw section backgrounds
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, slider_section_width, current_height))
    pygame.draw.rect(screen, WHITE, (slider_section_width, 0, graph_section_width, current_height))
    pygame.draw.line(screen, GRAY, (slider_section_width, 0), (slider_section_width, current_height), 2)
    
    # === LEFT SIDE: INPUT CONTROLS ===
    
    # Draw title for input section
    input_title = title_font.render("Input Controls", True, DARK_BLUE)
    screen.blit(input_title, (slider_section_width // 2 - input_title.get_width() // 2, 20))
    
    # Draw range input section
    range_title = font.render("Set Range:", True, BLACK)
    screen.blit(range_title, (slider_x, range_title_y))
    
    min_label = small_font.render("Min:", True, BLACK)
    max_label = small_font.render("Max:", True, BLACK)
    screen.blit(min_label, (slider_x, input_boxes_y - 20))
    screen.blit(max_label, (slider_x + 120, input_boxes_y - 20))
    
    # Draw input boxes with proper spacing
    min_input_rect = draw_input_box(slider_x, input_boxes_y, input_box_width, input_box_height, min_input_text, min_input_active)
    max_input_rect = draw_input_box(slider_x + 120, input_boxes_y, input_box_width, input_box_height, max_input_text, max_input_active)
    
    # Draw instructions with better spacing
    instructions = [
        "Click on Min/Max boxes to edit",
        "Press Enter to confirm, Tab to switch",
        "Drag slider or click on track"
    ]
    for i, instruction in enumerate(instructions):
        instr_text = small_font.render(instruction, True, DARK_BLUE)
        screen.blit(instr_text, (slider_x, instructions_y + i * 25))
    
    # Draw slider title
    slider_title = font.render("Input Slider:", True, BLACK)
    screen.blit(slider_title, (slider_x, slider_title_y))
    
    # Draw slider background
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y - 8, slider_length, 16))
    pygame.draw.rect(screen, LIGHT_BLUE, (slider_x, slider_y - 6, slider_length, 12))
    
    # Draw slider knob
    pygame.draw.circle(screen, BLUE, (int(slider_knob_x), slider_y), slider_knob_radius)
    pygame.draw.circle(screen, WHITE, (int(slider_knob_x), slider_y), slider_knob_radius - 3)
    
    # Draw slider labels with proper positioning
    min_label = small_font.render(f"{range_min:.1f}", True, BLACK)
    max_label = small_font.render(f"{range_max:.1f}", True, BLACK)
    screen.blit(min_label, (slider_x - min_label.get_width() // 2, slider_labels_y))
    screen.blit(max_label, (slider_x + slider_length - max_label.get_width() // 2, slider_labels_y))
    
    # Draw current input value with better layout
    value_bg = pygame.Rect(slider_x, input_value_y, slider_length, 35)
    pygame.draw.rect(screen, LIGHT_BLUE, value_bg)
    pygame.draw.rect(screen, BLUE, value_bg, 2)
    
    value_text = font.render(f"Input: {slider_value:.4f}", True, DARK_BLUE)
    screen.blit(value_text, (slider_x + slider_length // 2 - value_text.get_width() // 2, input_value_y + 8))
    
    # === RIGHT SIDE: SIGMOID GRAPH ===
    
    graph_x = slider_section_width + graph_margin
    graph_width = int(graph_section_width - 2 * graph_margin)
    graph_height = current_height - 2 * graph_margin
    
    # Draw graph title with proper spacing
    graph_title = title_font.render("Sigmoid Function", True, DARK_BLUE)
    screen.blit(graph_title, (slider_section_width + graph_section_width // 2 - graph_title.get_width() // 2, 20))
    
    # Draw function formula with proper spacing below title
    formula_text = small_font.render("σ(x) = 1 / (1 + e⁻ˣ)", True, BLACK)
    screen.blit(formula_text, (graph_x + graph_width // 2 - formula_text.get_width() // 2, 60))
    
    # Draw axes with proper margins
    axis_y_center = graph_margin + 40 + (graph_height - 80) // 2
    pygame.draw.line(screen, BLACK, (graph_x, axis_y_center), (graph_x + graph_width, axis_y_center), 2)  # x-axis
    pygame.draw.line(screen, BLACK, (graph_x, graph_margin + 40), (graph_x, graph_margin + 40 + graph_height - 80), 2)  # y-axis
    
    # Draw axis labels
    x_label = font.render("x", True, BLACK)
    y_label = font.render("σ(x)", True, BLACK)
    screen.blit(x_label, (graph_x + graph_width + 5, axis_y_center - 10))
    screen.blit(y_label, (graph_x - 25, graph_margin + 40))
    
    # Draw grid lines
    for i in range(1, 10):
        # Vertical grid lines
        grid_x = graph_x + (i / 10) * graph_width
        pygame.draw.line(screen, (230, 230, 230), (grid_x, graph_margin + 40), (grid_x, graph_margin + 40 + graph_height - 80), 1)
        
        # Horizontal grid lines
        grid_y = graph_margin + 40 + (i / 10) * (graph_height - 80)
        pygame.draw.line(screen, (230, 230, 230), (graph_x, grid_y), (graph_x + graph_width, grid_y), 1)
    
    # Draw axis values with better spacing
    for i in range(0, 11, 2):
        # x-axis values
        x_val = range_min + (i / 10) * (range_max - range_min)
        x_text = small_font.render(f"{x_val:.1f}", True, BLACK)
        x_pos = graph_x + (i / 10) * graph_width - x_text.get_width() // 2
        screen.blit(x_text, (x_pos, axis_y_center + 10))
        
        # y-axis values (only show 0.0, 0.5, 1.0 for clarity)
        if i in [0, 5, 10]:
            y_val = i / 10.0
            y_text = small_font.render(f"{y_val:.1f}", True, BLACK)
            y_pos = graph_margin + 40 + graph_height - 80 - (i / 10) * (graph_height - 80) - y_text.get_height() // 2
            screen.blit(y_text, (graph_x - 35, y_pos))
    
    # Draw sigmoid curve
    points = []
    for i in range(graph_width):
        x = range_min + (i / graph_width) * (range_max - range_min)
        y = sigmoid(x)
        pixel_x = graph_x + i
        pixel_y = axis_y_center - (y - 0.5) * (graph_height - 80)
        points.append((pixel_x, pixel_y))
    
    if len(points) > 1:
        pygame.draw.lines(screen, RED, False, points, 3)
    
    # Draw current point on sigmoid curve
    current_y = sigmoid(slider_value)
    point_x = graph_x + (slider_value - range_min) / (range_max - range_min) * graph_width
    point_y = axis_y_center - (current_y - 0.5) * (graph_height - 80)
    
    # Draw connecting lines
    pygame.draw.line(screen, BLUE, (point_x, axis_y_center), (point_x, point_y), 1)
    pygame.draw.line(screen, BLUE, (graph_x, point_y), (point_x, point_y), 1)
    
    # Draw the point
    pygame.draw.circle(screen, BLUE, (int(point_x), int(point_y)), 8)
    pygame.draw.circle(screen, WHITE, (int(point_x), int(point_y)), 3)
    
    # Draw output value display with proper spacing at bottom
    output_bg = pygame.Rect(graph_x, current_height - 50, graph_width, 35)
    pygame.draw.rect(screen, LIGHT_GRAY, output_bg)
    pygame.draw.rect(screen, GREEN, output_bg, 2)
    
    output_text = font.render(f"Sigmoid Output: {current_y:.6f}", True, GREEN)
    screen.blit(output_text, (graph_x + graph_width // 2 - output_text.get_width() // 2, current_height - 42))
    
    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()