"""
Profile Storage - сохранение и загрузка профилей спуфинга

Профиль сохраняется вместе с токеном чтобы использовать
тот же fingerprint при работе с аккаунтом.
"""

import json
from pathlib import Path
from typing import Optional
from .profile import BaseConfig, ProfileConfig, PROFILE_SCHEMA_VERSION, SpoofProfile, get_profiles_dir


class ProfileStorage:
    """Хранилище профилей спуфинга"""
    
    def __init__(self, base_dir: Path | None = None):
        if base_dir is None:
            self.profiles_dir = get_profiles_dir()
        else:
            base_dir = Path(base_dir)
            self.profiles_dir = base_dir if base_dir.name.lower() == 'profiles' else base_dir / 'profiles'
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def _get_profile_path(self, email: str) -> Path:
        """Путь к файлу профиля для email"""
        safe_name = email.replace('@', '_at_').replace('.', '_')
        return self.profiles_dir / f"{safe_name}.json"
    
    def save(self, email: str, profile: SpoofProfile) -> bool:
        """Сохраняет профиль для аккаунта"""
        try:
            path = self._get_profile_path(email)
            stored = ProfileConfig(
                base_config=BaseConfig(profile_id=email, adapter_id='chromium'),
                extra_config=profile.to_dict(),
                profile_schema_version=PROFILE_SCHEMA_VERSION,
            )
            data = stored.to_dict()
            data['email'] = email
            data['saved_at'] = __import__('datetime').datetime.now().isoformat()
            path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            return True
        except Exception as e:
            print(f"[ProfileStorage] Failed to save: {e}")
            return False
    
    def load(self, email: str) -> Optional[SpoofProfile]:
        """Загружает профиль для аккаунта"""
        try:
            path = self._get_profile_path(email)
            if not path.exists():
                return None
            data = json.loads(path.read_text(encoding='utf-8'))
            if isinstance(data, dict) and data.get('profile_schema_version') == PROFILE_SCHEMA_VERSION:
                extra = data.get('extra_config') or {}
                return SpoofProfile.from_dict(extra)
            return SpoofProfile.from_dict(data if isinstance(data, dict) else {})
        except Exception as e:
            print(f"[ProfileStorage] Failed to load: {e}")
            return None

    def exists(self, email: str) -> bool:
        """Проверяет есть ли сохранённый профиль"""
        return self._get_profile_path(email).exists()
    
    def delete(self, email: str) -> bool:
        """Удаляет профиль"""
        try:
            path = self._get_profile_path(email)
            if path.exists():
                path.unlink()
            return True
        except Exception:
            return False
    
    def get_or_create(self, email: str) -> SpoofProfile:
        """
        Загружает существующий профиль или создаёт новый.
        
        Это основной метод - гарантирует консистентность fingerprint.
        """
        profile = self.load(email)
        if profile:
            print(f"[ProfileStorage] Loaded existing profile for {email}")
            return profile
        
        # Создаём новый профиль
        from .profile import generate_random_profile
        profile = generate_random_profile()
        self.save(email, profile)
        print(f"[ProfileStorage] Created new profile for {email}")
        return profile
