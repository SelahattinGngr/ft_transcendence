from enum import Enum

class Messages(Enum):
    EMAIL_ALREADY_EXISTS = ("Email already exists", "E-posta zaten mevcut")
    USERNAME_ALREADY_EXISTS = ("Username already exists", "Kullanıcı adı zaten mevcut")
    USER_CREATED_SUCCESSFULLY = ("User created successfully. Please verify your email.", "Kullanıcı başarıyla oluşturuldu. Lütfen e-postanızı doğrulayın")
    INVALID_REQUEST_METHOD = ("Invalid request method", "Geçersiz istek metodu")
    USER_NOT_FOUND = ("User not found", "Kullanıcı bulunamadı")
    USER_CREATION_FAILED = ("User creation failed", "Kullanıcı oluşturma başarısız")
    PROFILE_UPDATE_FAILED = ("Profile update failed", "Profil güncelleme başarısız")
    INVALID_BIO_LENGTH = ("Bio length must be between 0 and 255", "Bio uzunluğu 0 ile 255 arasında olmalıdır")
    CANNOT_ADD_YOURSELF_AS_FRIEND = ("You cannot add yourself as a friend", "Kendinizi arkadaş olarak ekleyemezsiniz")
    FRIEND_ADD_FAILED = ("Friend add failed", "Arkadaş ekleme başarısız")
    ALREADY_FRIENDS = ("You are already friends", "Zaten arkadaşsınız")

    @staticmethod
    def get_message(message_enum, language="en"):
        def normalize_language_code(language_code):
            return language_code.split(';')[0].split(',')[0].split('-')[0]

        language = normalize_language_code(language)

        lang_index = {'en': 0, 'tr': 1}

        if language not in lang_index:
            language = 'en'

        return message_enum.value[lang_index[language]]