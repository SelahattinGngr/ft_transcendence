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
    USER_CREATION_FAILED = ("User creation failed", "Kullanıcı oluşturma başarısız")
    MISSING_TOKEN = ("Missing token", "Token eksik")
    EMAIL_SENDING_FAILED = ("Email sending failed", "E-posta gönderme başarısız oldu")
    VERIFICATION_EMAIL_SENT = ("Verification email sent", "Doğrulama e-postası gönderildi")
    INVALID_CODE = ("Invalid code", "Geçersiz kod")
    TOKEN_EXPIRED= ("Token expired", "Token süresi doldu")
    TWO_FACTORIAL_CODE_FAILED= ("Two factorial code failed, try again later", "İki faktörlü kod başarısız oldu, daha sonra tekrar deneyin")
    TWO_FACTORIAL_CODE_SENT= ("Two factorial code sent", "İki faktörlü kod gönderildi")
    USER_LOGGED_IN_SUCCESSFULLY= ("User logged in successfully", "Kullanıcı başarıyla giriş yaptı")

    @staticmethod
    def get_message(message_enum, language="en"):
        def normalize_language_code(language_code):
            return language_code.split(';')[0].split(',')[0].split('-')[0]

        language = normalize_language_code(language)

        lang_index = {'en': 0, 'tr': 1}

        if language not in lang_index:
            language = 'en'

        return message_enum.value[lang_index[language]]
