import pygame
import os
class Ship():
    """ 初始化飞船并设置其初始位置 """
    def __init__(self, screen,ai_settings):
        self.screen = screen
        # 加载飞船图像并获取其外接矩形        
        path = os.path.dirname(__file__)
        path = os.path.join(path,"images","ship.png")
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.ai_settings = ai_settings
        self.moving_right = False
        self.moving_left = False
    def blitme(self):
        """ 在指定位置绘制飞船 """
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center