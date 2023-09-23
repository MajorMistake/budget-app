from components.container import container

import reflex as rx

def auth_layout(*args):
    """The shared layout for the login and sign up pages."""
    return rx.box(
        container(
            rx.heading(
                rx.span("Welcome to Jackson's Budget App!"),
                rx.span("Sign in or sign up to save your work."),
                display="flex",
                flex_direction="column",
                align_items="center",
                text_align="center",
            ),
            *args,
            border_top_radius="lg",
            box_shadow="0 4px 60px 0 rgba(0, 0, 0, 0.08), 0 4px 16px 0 rgba(0, 0, 0, 0.08)",
            display="flex",
            flex_direction="column",
            align_items="center",
            py=12,
            gap=4,
        ),
        h="100vh",
        pt=16,
        background="url(bg.svg)",
        background_repeat="no-repeat",
        background_size="cover",
    )