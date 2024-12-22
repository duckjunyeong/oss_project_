import glob
import math
import random
import time
from turtle import left

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self, blocks, items): 
        self.alive = False;
        blocks.remove(self);

        if random.random() < 0.9:
            item_pos_x = random.randint(0,config.display_dimension[0])
            item_pos_y = 10
            item_color = config.red_color
            if (random.random() < 0.5):
                item_color = config.blue_color
            
            items.append(Item(item_color, (item_pos_x, item_pos_y)))

class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list, items: list):
         for block in blocks:
            if self.rect.colliderect(block.rect):
                if (self.rect.centerx >= block.rect.right | self.rect.centerx <= block.rect.left):
                    self.dir = 180 - self.dir + random.randint(-5, 5)
                else:
                    self.dir = -self.dir + random.randint(-5, 5)
                block.collide(blocks, items)


    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
         if self.rect.right >= 590:
            self.dir = 180 - self.dir + random.randint(-5, 5)
         if self.rect.left <= 10:
            self.dir = 180 - self.dir + random.randint(-5, 5)
         if self.rect.top <= 10:
            self.dir = -self.dir + random.randint(-5, 5)

    
    def alive(self):
       if self.rect.bottom >= 790:
            return False
       return True


class Item(Basic):
    def __init__(self, color: tuple, pos: tuple):
        super().__init__(color, config.item_speed, pos, config.item_size)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)
    
    def collide_paddle(self, paddle: Paddle, balls: list, items: list):
        if self.rect.colliderect(paddle.rect):
            items.remove(self)
            if self.color == config.red_color:
                balls.append(
                    Ball(
                        (
                            paddle.rect.centerx,
                            config.paddle_pos[1] - config.paddle_size[1],
                        )
                    )
                )