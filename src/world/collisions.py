"""Module that deals with resolving collisions."""
import pygame as pg

from src.sprites.effects.explosion import Explosion


def collide_hit_rect(sprite_a, sprite_b) -> bool:
    """ Checks whether the sprites' hit_rect rectangles overlap.

    :param sprite_a: A BaseSprite object.
    :param sprite_b: A BaseSprite object.
    :return: boolean, indicating whether the sprite's hit_rect rectangles overlapped.
    """
    return sprite_a.hit_rect.colliderect(sprite_b.hit_rect)


def bullet_collide_owner(bullet, sprite) -> bool:
    """Checks whether a Bullet has hit a sprite that didn't fire the bullet.

    :param bullet: The Bullet object involved in the collision check.
    :param sprite: Second BaseSprite object involved in the collision check.
    :return: boolean, whether the collision takes place.
    """
    return bullet.owner != sprite and collide_hit_rect(bullet, sprite)


def handle_obstacle_collisions(sprite, displacement: pg.math.Vector2) -> bool:
    """Corrects a sprite's displacement in the event the sprite has hit an obstacle.

    :param sprite: BaseSprite with a MoveMixin undergoing a displacement.
    :param displacement: vector representing the attempted displacement of the sprite.
    :return: boolean, whether the sprite hit an obstacle.
    """
    colliders = sprite.all_groups['obstacles']
    hit_wall = False

    # Collision in x direction.
    sprite.pos.x += displacement.x
    sprite.hit_rect.centerx = sprite.pos.x
    collider = pg.sprite.spritecollideany(sprite, colliders, collide_hit_rect)

    if collider:
        # Hit left of collider.
        if sprite.pos.x < collider.rect.centerx:
            sprite.pos.x = collider.rect.left - sprite.hit_rect.width / 2
        # Hit right side of collider.
        else:
            sprite.pos.x = collider.rect.right + sprite.hit_rect.width / 2
        sprite.vel.x = 0
        sprite.hit_rect.centerx = sprite.pos.x
        hit_wall = True

    # Collision in y direction.
    sprite.pos.y += displacement.y
    sprite.hit_rect.centery = sprite.pos.y
    collider = pg.sprite.spritecollideany(sprite, colliders, collide_hit_rect)

    if collider:
        # Hit top of collider.
        if sprite.pos.y < collider.rect.centery:
            sprite.pos.y = collider.rect.top - sprite.hit_rect.height / 2
        # Hit bottom of collider.
        else:
            sprite.pos.y = collider.rect.bottom + sprite.hit_rect.height / 2
        sprite.vel.y = 0
        sprite.hit_rect.centery = sprite.pos.y
        hit_wall = True
    sprite.rect.center = sprite.pos
    return hit_wall


def handle_collisions(groups) -> None:
    """Resolves the collisions of the game world.

    :param groups: Dictionary of sprite groups owned by the game world.
    :return: None
    """
    # Tank/tank collision.
    all_tanks = list(groups['tanks'])
    for i in range(0, len(all_tanks)):
        tank_a = all_tanks[i]
        for tank_b in all_tanks[i + 1:]:
            if collide_hit_rect(tank_a, tank_b):
                knock_back_dir = tank_b.rot
                tank_a.vel += pg.math.Vector2(tank_b.KNOCK_BACK, 0).rotate(knock_back_dir)
                tank_b.vel -= pg.math.Vector2(tank_b.KNOCK_BACK, 0).rotate(knock_back_dir)

    # Handle item pick-up.
    hits = pg.sprite.groupcollide(groups['tanks'], groups['items'], False, True)
    for tank, items in hits.items():
        for item in items:
            tank.pickup(item)

    # Concurrent modification of iterator issue...?
    for bullet in list(groups['bullets']):
        # Destroy boxes to spawn new items
        for box in groups['item_boxes']:
            if bullet_collide_owner(bullet, box):
                bullet.kill()
                box.wear_out()

        # Hitting obstacles makes the bullet disappear.
        for obstacle in groups['obstacles']:
            if bullet_collide_owner(bullet, obstacle):
                bullet.kill()

        # Damageable things (likely turret and tanks).
        for sprite in groups['damageable']:
            if bullet_collide_owner(bullet, sprite):
                bullet.kill()
                Explosion(bullet.pos.x, bullet.pos.y, groups)
                sprite.inflict_damage(bullet.damage)
                if sprite.health <= 0:
                    sprite.kill()
