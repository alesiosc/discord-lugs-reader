from PIL import Image

# Create a simple red square icon
img = Image.new('RGB', (256, 256), color='red')
img.save('icon.ico', format='ICO', sizes=[(256, 256)])

print("Icon file created successfully.")