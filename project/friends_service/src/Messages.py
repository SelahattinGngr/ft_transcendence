from enum import Enum

class Messages(Enum):
    CANNOT_ADD_SELF = ("You cannot add yourself as a friend.", "Kendinizi arkadaş olarak ekleyemezsiniz.")
    REQUEST_ALREADY_EXISTS = ("Friend request already exists.", "Arkadaşlık isteği zaten mevcut.")
    REQUEST_SENT_SUCCESS = ("Friend request sent successfully.", "Arkadaşlık isteği başarıyla gönderildi.")
    INVALID_METHOD = ("Invalid method.", "Geçersiz metod.")
    INVALID_STATUS = ("Invalid status.", "Geçersiz durum.")
    NO_PENDING_REQUEST = ("No pending request found.", "Bekleyen istek bulunamadı.")
    REQUEST_ACCEPTED = ("Friend request accepted.", "Arkadaşlık isteği kabul edildi.")
    REQUEST_REJECTED = ("Friend request rejected.", "Arkadaşlık isteği reddedildi.")
    NO_ACCESS_TOKEN = ("No access token provided.", "Token sağlanmadı.")
    INVALID_ACCESS_TOKEN = ("Invalid access token.", "Geçersiz token.")
    REQUEST_ALREADY_ANSWERED = ("Friend request already answered.", "Arkadaşlık isteği zaten yanıtlandı.")
    REQUEST_ALREADY_SENT = ("Friend request already sent.", "Arkadaşlık isteği zaten gönderildi.")
    REQUEST_NOT_FOUND = ("Friend request not found.", "Arkadaşlık isteği bulunamadı.")
    
    def get_message(message_enum, language="en"):
        lang_index = {'en' : 0, 'tr' : 1}
        return message_enum.value[lang_index[language]]