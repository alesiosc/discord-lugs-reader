from PIL import Image, ImageDraw
import os

def create_proper_icon():
    """Create a proper Windows icon with multiple sizes for better compatibility"""
    
    # Sizes needed for Windows icons
    sizes = [16, 32, 48, 64, 128, 256]
    
    # Create a simple, clean design - blue circle with white "D" for Discord
    images = []
    
    for size in sizes:
        # Create a new image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a blue circle as background
        margin = size // 8
        draw.ellipse([margin, margin, size - margin, size - margin], 
                    fill='#5865F2', outline='#4752C4', width=2)
        
        # Draw white "D" in the center
        if size >= 32:
            # For larger sizes, draw a more detailed "D"
            font_size = size // 2
            text = "D"
            # Simple text rendering using PIL's default font
            try:
                # Try to use a bold font if available
                draw.text((size//3, size//3), text, fill='white')
            except:
                # Fallback to basic drawing
                draw.rectangle([size//3, size//3, 2*size//3, 2*size//3], fill='white')
        
        images.append(img)
    
    # Save as ICO file with multiple sizes
    icon_path = 'app_icon.ico'
    images[0].save(icon_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    
    print(f"Created proper icon: {icon_path}")
    print(f"Contains {len(images)} sizes: {[img.size for img in images]}")
    
    return icon_path

def create_backup_original_icon():
    """Keep the original red square icon as backup"""
    img = Image.new('RGB', (256, 256), color='red')
    img.save('icon.ico', format='ICO', sizes=[(256, 256)])
    print("Original icon.ico preserved as backup")

if __name__ == "__main__":
    create_backup_original_icon()
    new_icon = create_proper_icon()
    print(f"\nNew icon created: {new_icon}")
    print("To use the new icon, update monitor.spec to reference 'app_icon.ico' instead of 'icon.ico'")