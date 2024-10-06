from enum import Enum

class Messages(Enum):
    EMAIL_ALREADY_EXISTS = ("Email already exists", "E-posta zaten mevcut")
    USERNAME_ALREADY_EXISTS = ("Username already exists", "Kullanıcı adı zaten mevcut")
    USER_CREATED_SUCCESSFULLY = ("User created successfully. Please verify your email.", "Kullanıcı başarıyla oluşturuldu. Lütfen e-postanızı doğrulayın")
    INVALID_REQUEST_METHOD = ("Invalid request method", "Geçersiz istek metodu")
    ACCOUNT_VERIFIED_SUCCESSFULLY = ("Account verified successfully", "Hesap başarıyla doğrulandı")
    INVALID_OR_EXPIRED_VERIFICATION_TOKEN = ("Invalid or expired verification token", "Geçersiz veya süresi dolmuş doğrulama kodu")
    EXPIRED_OR_INVALID_REFRESH_TOKEN = ("Expired or invalid refresh token", "Süresi dolmuş veya geçersiz refresh token")
    AN_ERROR_OCCURRED = ("An error occurred", "Bir hata oluştu")
    INVALID_CREDENTIALS = ("Invalid credentials", "Geçersiz kimlik bilgileri")
    UNACTIVATE_ACCOUNT = ("Unactivated account", "Aktive edilmemiş hesap")
    USER_NOT_FOUND = ("User not found", "Kullanıcı bulunamadı")
    SIGNUP_FAILED = ("Signup failed", "Kayıt başarısız oldu")
    WEAK_PASSWORD = ("Weak password", "Zayıf şifre")
    INVALID_EMAIL_FORMAT = ("Invalid email format", "Geçersiz e-posta formatı")
    USER_LOGGED_OUT_SUCCESSFULLY = ("User logged out successfully", "Kullanıcı başarıyla çıkış yaptı")
    INVALID_REFRESH_TOKEN = ("Invalid refresh token", "Geçersiz refresh token")
    INVALID_ACCESS_TOKEN = ("Invalid access token", "Geçersiz access token")
    SIGNOUT_FAILED = ("Signout failed", "Çıkış başarısız oldu")
    REFRESH_TOKEN_FAILED = ("Refresh token failed", "Refresh token başarısız oldu")
    ACCESS_TOKEN_EXPIRED = ("Access token expired", "Access token süresi doldu")
    ACCESS_TOKEN_FAILED = ("Access token failed", "Access token başarısız oldu")
    TOKEN_EXPIRED_NEW_SENT = ("Token expired. New token sent to your email", "Token süresi doldu. Yeni token e-postanıza gönderildi")
    FAILED_TO_RETRIEVE_TOKEN = ("Failed to retrieve token", "Token alınamadı")
    FAILED_TO_RETRIEVE_USER = ("Failed to retrieve user", "Kullanıcı alınamadı")
    AUTHORIZATION_CODE_NOT_PROVIDED = ("Authorization code not provided", "Yetkilendirme kodu sağlanmadı")


    def get_message(message_enum, language="en"):
        lang_index = {'en' : 0, 'tr' : 1}
        return message_enum.value[lang_index[language]]