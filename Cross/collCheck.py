class CollisionChecker:
    @staticmethod
    def check_collision(pos, pw, ph, collider):
        player_left = pos[0]
        player_right = pos[0] + pw
        player_top = pos[1]
        player_bottom = pos[1] + ph
        
        collider_left = collider[0]
        collider_right = collider[0] + collider[2]
        collider_top = collider[1]
        collider_bottom = collider[1] + collider[3]
        
        if (player_bottom < collider_top or
            player_top > collider_bottom or
            player_right < collider_left or
            player_left > collider_right):
            return False
        
        if (player_bottom >= collider_top and
            player_top < collider_top and
            player_right > collider_left and
            player_left < collider_right):
            return "feet"
        
        if (player_top <= collider_bottom and
            player_bottom > collider_bottom and
            player_right > collider_left and
            player_left < collider_right):
            return "head"
        
        if (player_right >= collider_left and
            player_left <= collider_right):
            if player_right <= collider_left + (collider_right - collider_left) / 2:
                return "left_side"
            if player_left >= collider_left + (collider_right - collider_left) / 2:
                return "right_side"
        
        return False
