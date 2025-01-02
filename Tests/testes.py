import unittest
from unittest.mock import MagicMock
import pygame

from entities.characters.Character import Character


class TestCharacter(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente de teste."""
        self.xp_bar = MagicMock()  # Mock da XPBar
        self.audio_player = MagicMock()  # Mock do AudioPlayer
        self.character = Character(
            name="Knight",
            max_health=100,
            max_xp=100,
            attack=10,
            defense=5,
            speed=5,
            x=50,
            y=50,
            width=50,
            height=50
        )
        self.character.xp_bar = self.xp_bar
        self.character.audio_player = self.audio_player

    def test_gain_xp_sem_level_up(self):
        """Teste o ganho de XP sem level up"""
        self.character.xp_bar.current_xp = 40
        self.character.xp_bar.max_xp = 100

        # O personagem ganha 20 XP, mas não chega ao limite
        self.character.gain_xp(20)

        # Verifica se o XP atual foi corretamente incrementado
        self.assertEqual(self.character.xp_bar.current_xp, 60)
        # Verifica que o nível não foi alterado
        self.assertEqual(self.character.current_level, 1)

        self.xp_bar.update.assert_called_once_with(60)

    def test_gain_xp_com_level_up(self):
        """Teste o ganho de XP que resulta em level up"""
        self.character.xp_bar.current_xp = 90
        self.character.xp_bar.max_xp = 100

        # O personagem ganha 20 XP, o que ultrapassa o máximo
        self.character.gain_xp(20)

        # Verifica se o level up ocorreu
        self.assertEqual(self.character.current_level, 2)
        # Verifica se o XP foi resetado
        self.assertEqual(self.character.xp_bar.current_xp, 0)
        # Verifica se o max_xp foi atualizado corretamente
        self.assertEqual(self.character.xp_bar.max_xp, 150)  # 100 * 1.5
        # Verifica se o áudio de level up foi tocado
        self.audio_player.play_sound.assert_called_once_with('level_up', 0.2)
        # Verifica se a barra de XP foi atualizada
        self.xp_bar.update.assert_called_once_with(0)

    def test_level_up_multiplica_max_xp(self):
        """Testa se o max_xp aumenta corretamente após o level up"""
        self.character.xp_bar.current_xp = 100
        self.character.xp_bar.max_xp = 100

        # Ganha XP suficiente para o level up
        self.character.gain_xp(10)

        # Verifica se o nível foi incrementado
        self.assertEqual(self.character.current_level, 2)
        # Verifica se max_xp foi multiplicado por 1.5
        self.assertEqual(self.character.xp_bar.max_xp, 150)

    def test_gain_xp_sem_level_up_audio(self):
        """Verifica se o áudio não é tocado durante o ganho de XP sem level up"""
        self.character.xp_bar.current_xp = 80
        self.character.xp_bar.max_xp = 100

        # Ganha 10 XP, sem atingir o limite
        self.character.gain_xp(10)

        # O áudio de level up não deve ser tocado
        self.audio_player.play_sound.assert_not_called()

    def test_gain_xp_com_level_up_audio(self):
        """Verifica se o áudio é tocado durante o ganho de XP com level up"""
        self.character.xp_bar.current_xp = 80
        self.character.xp_bar.max_xp = 100

        # Ganha 30 XP, o que faz o level up
        self.character.gain_xp(30)

        # O áudio de level up deve ser tocado
        self.audio_player.play_sound.assert_called_once_with('level_up', 0.2)


if __name__ == "__main__":
    unittest.main()
