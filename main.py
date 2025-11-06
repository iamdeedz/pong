import pygame as p
from screeninfo import get_monitors
from time import time

p.init()
screen_width = 700
screen_height = 420
for monitor in get_monitors():
    if monitor.is_primary:
        screen_width = monitor.width
        screen_height = monitor.height

paddle_speed = 600
paddle_width = 15
paddle_height = 125
l_paddle_y = r_paddle_y = (screen_height / 2) - (paddle_height / 2)

ball_x = screen_width / 2 - 12.5
ball_y = screen_height / 2 - 12.5
ball_x_velocity = ball_y_velocity = 550

left_score = right_score = 0


def update(delta_time):
    global l_paddle_y, r_paddle_y, ball_x, ball_y, ball_x_velocity, ball_y_velocity, left_score, right_score
    # Move paddles
    keys_pressed = p.key.get_pressed()
    if keys_pressed[p.K_w]:
        l_paddle_y -= paddle_speed * delta_time if l_paddle_y - (paddle_speed * delta_time) > 0 else 0
    if keys_pressed[p.K_s]:
        l_paddle_y += paddle_speed * delta_time if l_paddle_y + (
                    paddle_speed * delta_time) < screen_height - paddle_height else 0

    if keys_pressed[p.K_UP]:
        r_paddle_y -= paddle_speed * delta_time if r_paddle_y - (paddle_speed * delta_time) > 0 else 0
    if keys_pressed[p.K_DOWN]:
        r_paddle_y += paddle_speed * delta_time if r_paddle_y + (
                    paddle_speed * delta_time) < screen_height - paddle_height else 0

    # Check if goal scored
    if ball_x > screen_width - 50 - paddle_width:
        left_score += 1
        ball_x = screen_width / 2 - 12.5
        ball_y = screen_height / 2 - 12.5
        ball_x_velocity = -ball_x_velocity
        ball_y_velocity = -ball_y_velocity
    elif ball_x < 50 + paddle_width:
        right_score += 1
        ball_x = screen_width / 2 - 12.5
        ball_y = screen_height / 2 - 12.5
        ball_x_velocity = -ball_x_velocity
        ball_y_velocity = -ball_y_velocity

    # Check for bounce
    next_ball_pos = (ball_x + ball_x_velocity * delta_time, ball_y + ball_y_velocity * delta_time)
    if (next_ball_pos[1] < 12.5) or \
            (ball_y + ball_y_velocity * delta_time > screen_height - 12.5):
        ball_y_velocity = -ball_y_velocity

    if (next_ball_pos[0] > screen_width - 50 - paddle_width - 12.5 and r_paddle_y < next_ball_pos[1]+12.5 and next_ball_pos[1]-12.5 < r_paddle_y + paddle_height) or \
            (next_ball_pos[0] < 50 + paddle_width + 12.5 and l_paddle_y < next_ball_pos[1]+12.5 and next_ball_pos[1]-12.5 < l_paddle_y + paddle_height):
        ball_x_velocity = -ball_x_velocity

    # Move ball
    ball_x += ball_x_velocity * delta_time
    ball_y += ball_y_velocity * delta_time


def main():
    screen = p.display.set_mode((screen_width, screen_height), p.FULLSCREEN)
    clock = p.time.Clock()

    running = True
    started = False
    last_time = time()
    while running:
        delta_time = time() - last_time
        last_time = time()

        for event in p.event.get():
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                running = False
            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                started = True

        if started:
            update(delta_time)

        screen.fill("black")

        # Draw paddles
        p.draw.rect(screen, "white", p.Rect(50, l_paddle_y, paddle_width, paddle_height))
        p.draw.rect(screen, "white", p.Rect(screen_width-50-paddle_width, r_paddle_y, paddle_width, paddle_height))

        # Draw ball
        if started:
            p.draw.circle(screen, "white", (ball_x, ball_y), 12.5)

        # Text
        font = p.font.Font(None, 100)
        score_text = font.render(f"{left_score} - {right_score}", True, "white")
        start_text = font.render("Press Space To Start", True, "white")

        if started:
            screen.blit(score_text, ((screen_width/2)-(score_text.get_width()/2), 100))
        else:
            screen.blit(start_text, ((screen_width/2)-(start_text.get_width()/2), (screen_height/2)-(start_text.get_height()/2)))

        p.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
