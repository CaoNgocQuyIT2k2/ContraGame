import pygame

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        # Khởi tạo một Button với các thông số đầu vào
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input

        # Render văn bản và hình ảnh nếu không được cung cấp
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text

        # Khởi tạo hình chữ nhật và vị trí của văn bản
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        # Cập nhật hình ảnh và văn bản trên màn hình
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        # Kiểm tra xem người dùng đã nhấp vào nút không
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(
            self.rect.top, self.rect.bottom
        ):
            return True
        return False

    def changeColor(self, position):
        # Thay đổi màu của văn bản khi di chuột qua nút
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(
            self.rect.top, self.rect.bottom
        ):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
