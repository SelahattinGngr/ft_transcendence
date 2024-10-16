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
    def get_message(message_enum, language="en"):
        lang_index = {'en' : 0, 'tr' : 1}
        return message_enum.value[lang_index[language]]