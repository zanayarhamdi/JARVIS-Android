import pyttsx3
import speech_recognition as sr
from core.logger import create_logger
import os
import sys

logger = create_logger("VOICE")

class VoiceEngine:
    def __init__(self):
        try:
            # TTS (متن به صوت)
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 120)
            self.tts.setProperty('volume', 1.0)
            
            # STT (صوت به متن)
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 4000
            self.microphone = sr.Microphone()
            
            logger.info("Voice engine initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing voice engine: {e}")
            self.tts = None
            self.recognizer = None
    
    def speak(self, text):
        """جارویس صحبت می‌کند"""
        try:
            if self.tts:
                print(f"\n🔊 JARVIS: {text}\n")
                self.tts.say(text)
                self.tts.runAndWait()
            else:
                print(f"\nJARVIS: {text}\n")
        except Exception as e:
            logger.error(f"Error speaking: {e}")
            print(f"\nJARVIS: {text}\n")
    
    def listen(self, timeout=10):
        """شنوایی صدای کاربر"""
        try:
            if not self.recognizer:
                return input("You: ").strip()
            
            with self.microphone as source:
                print("\n🎤 در حال شنوایی...\n")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # تشخیص فارسی
            text = self.recognizer.recognize_google(audio, language='fa-IR')
            print(f"You: {text}\n")
            return text
        
        except sr.UnknownValueError:
            self.speak("متاسفانه متوجه نشدم. دوباره بگو")
            return None
        except sr.RequestError:
            print("\n⚠️  اینترنت برقرار نیست یا سرویس صوتی دردسترس نیست\n")
            return None
        except Exception as e:
            logger.error(f"Error listening: {e}")
            return input("You: ").strip()
