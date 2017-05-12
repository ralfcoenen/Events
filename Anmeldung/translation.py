from modeltranslation.translator import translator, TranslationOptions
from .models import Event, Teilnehmer, texte


class EventTranslationOptions(TranslationOptions):
    fields = ('bezeichnung', 'kurzbeschreibung', 'beschreibung')

class texteTranslationOptions(TranslationOptions):
    fields = ('headertext', 'langtext')


translator.register(Event, EventTranslationOptions)
translator.register(texte,texteTranslationOptions)