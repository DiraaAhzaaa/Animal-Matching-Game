import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animals Matching Games - Multi Round")

# === 🔊 Backsound ===
pygame.mixer.music.load("kingdom.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# === Tambahkan background ===
background = pygame.image.load("ntt.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.SysFont(None, 22)
bigfont = pygame.font.SysFont(None, 36)

# === Data hewan per ronde ===
round_data = [
    [  # Ronde 1
        {"name": "Harimau", "habitat": "Hutan", "food": "Daging", "threat": "Perburuan"},
        {"name": "Gajah", "habitat": "Sabana", "food": "Rumput", "threat": "Perburuan"},
        {"name": "Ikan Paus", "habitat": "Laut", "food": "Plankton", "threat": "Polusi"},
        {"name": "Burung Hantu", "habitat": "Hutan", "food": "Tikus", "threat": "Kerusakan hutan"},
        {"name": "Panda", "habitat": "Pegunungan", "food": "Bambu", "threat": "Kelangkaan makanan"},
    ],
    [  # Ronde 2
        {"name": "Serigala", "habitat": "Hutan", "food": "Daging", "threat": "Perburuan"},
        {"name": "Kangguru", "habitat": "Padang Rumput", "food": "Rumput", "threat": "Kehilangan habitat"},
        {"name": "Hiu", "habitat": "Laut", "food": "Ikan", "threat": "Penangkapan berlebihan"},
        {"name": "Burung Elang", "habitat": "Pegunungan", "food": "Daging", "threat": "Kerusakan lingkungan"},
        {"name": "Koala", "habitat": "Hutan Eukaliptus", "food": "Daun", "threat": "Kebakaran hutan"},
    ],
    [  # Ronde 3
        {"name": "Rusa", "habitat": "Hutan", "food": "Daun", "threat": "Pemburu liar"},
        {"name": "Penguin", "habitat": "Kutub Selatan", "food": "Ikan", "threat": "Pemanasan global"},
        {"name": "Kucing Besar", "habitat": "Hutan Tropis", "food": "Daging", "threat": "Perburuan"},
        {"name": "Beruang Kutub", "habitat": "Kutub Utara", "food": "Anjing laut", "threat": "Mencairnya es"},
        {"name": "Lumba-lumba", "habitat": "Laut", "food": "Ikan", "threat": "Jaring nelayan"},
    ]
]

# === Fungsi membuat kartu berdasarkan data hewan ===
def create_cards(animal_list):
    info_positions = [50 + i*100 for i in range(len(animal_list))]
    animal_positions = [50 + i*100 for i in range(len(animal_list))]
    random.shuffle(info_positions)
    random.shuffle(animal_positions)

    info_cards = []
    animal_cards = []
    for i, animal in enumerate(animal_list):
        info = f"Habitat: {animal['habitat']}\nMakanan: {animal['food']}\nAncaman: {animal['threat']}"
        info_cards.append({
            "rect": pygame.Rect(50, info_positions[i], 270, 90),
            "text": info,
            "index": i,
            "matched": False
        })
        animal_cards.append({
            "rect": pygame.Rect(750, animal_positions[i], 200, 90),
            "text": animal["name"],
            "index": i,
            "matched": False
        })
    return info_cards, animal_cards


# === Game utama ===
current_round = 0
max_rounds = len(round_data)
info_cards, animal_cards = create_cards(round_data[current_round])

selected_info = None
selected_animal = None
running = True
win = False
lose = False
attempts = 0
max_attempts = 5

# === Timer ===
time_limit = 30  # detik per ronde
start_ticks = pygame.time.get_ticks()

while running:
    screen.blit(background, (0, 0))

    # --- Hitung waktu tersisa ---
    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, time_limit - seconds_passed)

    # --- Gambar kartu info ---
    for card in info_cards:
        color = (182, 244, 255) if not card["matched"] else (65, 133, 145)
        pygame.draw.rect(screen, color, card["rect"])
        lines = card["text"].split('\n')
        for j, line in enumerate(lines):
            txt = font.render(line, True, (0, 0, 0))
            screen.blit(txt, (card["rect"].x + 10, card["rect"].y + 8 + j * 20))
        if selected_info == card:
            pygame.draw.rect(screen, (255, 0, 0), card["rect"], 3)

    # --- Gambar kartu hewan ---
    for card in animal_cards:
        color = (182, 244, 255) if not card["matched"] else (65, 133, 145)
        pygame.draw.rect(screen, color, card["rect"])
        txt = bigfont.render(card["text"], True, (0, 0, 0))
        screen.blit(txt, (card["rect"].x + 10, card["rect"].y + 25))
        if selected_animal == card:
            pygame.draw.rect(screen, (255, 0, 0), card["rect"], 3)

    # --- Event ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if win or lose:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for card in info_cards:
                if card["rect"].collidepoint(mx, my) and not card["matched"]:
                    selected_info = card
            for card in animal_cards:
                if card["rect"].collidepoint(mx, my) and not card["matched"]:
                    selected_animal = card
            if selected_info and selected_animal:
                if selected_info["index"] == selected_animal["index"]:
                    selected_info["matched"] = True
                    selected_animal["matched"] = True
                else:
                    attempts += 1
                pygame.time.wait(300)
                selected_info = None
                selected_animal = None

    # --- Cek kondisi ronde ---
    if all(card["matched"] for card in info_cards):
        if current_round < max_rounds - 1:
            txt = bigfont.render(f"Ronde {current_round+1} Selesai!", True, (255, 255, 255))
            screen.blit(txt, (360, 500))
            pygame.display.flip()
            pygame.time.wait(1500)
            current_round += 1
            info_cards, animal_cards = create_cards(round_data[current_round])
            attempts = 0
            start_ticks = pygame.time.get_ticks()  # reset timer
        else:
            txt = bigfont.render("Semua ronde selesai! Kamu menang!", True, (255, 255, 255))
            screen.blit(txt, (250, 500))
            win = True

    elif attempts >= max_attempts or time_left <= 0:
        txt = bigfont.render("Kamu kalah! Coba lagi ya!", True, (200, 0, 0))
        screen.blit(txt, (320, 500))
        lose = True

    # --- Info ronde, percobaan, timer ---
    round_text = font.render(f"Ronde: {current_round+1}/{max_rounds}", True, (0, 0, 0))
    counter = font.render(f"Salah: {attempts}/{max_attempts}", True, (0, 0, 0))
    timer_text = font.render(f"Waktu: {time_left}s", True, (0, 0, 0))
    screen.blit(round_text, (10, 10))
    screen.blit(counter, (10, 35))
    screen.blit(timer_text, (880, 10))

    pygame.display.flip()

pygame.quit()

