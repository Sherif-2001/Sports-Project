def kick_ball(current_projectile):
    if 0 < theta < 90:
        if not current_projectile or current_projectile.flying_velocity_x == 0:
            ball_kick_sfx.play()
            projectiles_group.empty()
            new_projectile = Projectile(initial_velocity, theta)
            projectiles_group.add(new_projectile)
            current_projectile = new_projectile
