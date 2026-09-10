import os
import random
import logging
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

IMAGE_PATH = "menu.jpg"
SHIPPING_IMAGE_PATH = "spedizione.jpg"

# Dizionario testi multilingua (5 Lingue)
TEXTS = {
    "it": {
        "disclaimer": (
            "⚠️ <b>ATTENZIONE LEGGERE ATTENTAMENTE QUESTO MESSAGGIO!</b>\n\n"
            "Ciao, siamo venuti a conoscenza da diversi clienti che su Telegram e TikTok girano molti scammer! "
            "Chiediamo la massima attenzione e soprattutto chiediamo di segnalare il più possibile questi soggetti.\n\n"
            "Non siamo qui per giocare.\n"
            "Non siamo qui per ascoltare problemi.\n"
            "Non siamo qui per fare beneficenza.\n\n"
            "Siamo un team esperto in questo settore, mettiamo la nostra piena conoscenza e fiducia!\n\n"
            "Cerchiamo solo persone con la testa sulle spalle e che abbiano voglia di svoltare la propria vita!\n\n"
            "Da quando abbiamo iniziato a lavorare in questo settore abbiamo aiutato più di 300 persone, "
            "abbiamo riscontrato molti problemi tra ban e problemi con i clienti, "
            "ma non abbiamo mai mollato perché il successo è sempre dietro l’angolo!"
        ),
        "btn_read": "✅ HO LETTO!",
        "captcha_title": "🤖 <b>VERIFICA DI SICUREZZA</b>\n\nSeleziona l'icona corrispondente a: <b>{target_name}</b>",
        "captcha_wrong": "❌ Errato! Riprova con un nuovo captcha.",
        "welcome": "👋 Ciao <b>{name}</b>!\nBenvenuto nel nostro bot ufficiale.\nScegli un'opzione dal menu qui sotto:",
        "btn_banknotes": "💵 Banconote (10/20/50)",
        "btn_videos": "🎥 Video Qualità",
        "btn_shipping": "📦 Spedizioni",
        "btn_payments": "💳 Metodi di Pagamento",
        "btn_feedback": "⭐ Recensioni & Feedback",
        "btn_support": "✍️ Assistenza / Limitati",
        "btn_lang": "🌐 Cambia Lingua",
        "btn_back": "🔙 Menu Principale",
        "banknotes_info": (
            "💵 <b>BANCONOTE DISPONIBILI</b>\n\n"
            "Tagli disponibili di altissima qualità:\n"
            "• <b>10€</b> - Ottima fattura, superano i test base.\n"
            "• <b>20€</b> - Ologramma riflettente, carta in cotone.\n"
            "• <b>50€</b> - Texture UV completa e banda magnetica reattiva.\n\n"
            "Per listini prezzi e ordini contatta il supporto."
        ),
        "videos_info": (
            "🎥 <b>VIDEO QUALITÀ</b>\n\n"
            "I nostri video dimostrativi mostrano i dettagli UV, la reattività ai pen test "
            "e l'accuratezza visiva delle banconote.\n\n"
            "Richiedi l'accesso al canale prove tramite il supporto."
        ),
        "shipping_info": (
            "📦 <b>SPEDIZIONI & CONSEGNA</b>\n\n"
            "• Spedizione 100% anonima e sottovuoto (stealth packaging).\n"
            "• Corriere espresso tracciato 24/48h.\n"
            "• Nessun riferimento al contenuto sul pacco."
        ),
        "payments_info": (
            "💳 <b>METODI DI PAGAMENTO</b>\n\n"
            "Accettiamo esclusivamente pagamenti sicuri, istantanei e anonimi:\n"
            "• <b>Bitcoin (BTC)</b>\n"
            "• <b>USDT (Tether TRC20)</b>\n"
            "• <b>Monero (XMR)</b>"
        ),
        "feedback_info": (
            "⭐ <b>RECENSIONI & FEEDBACK</b>\n\n"
            "Oltre 300 clienti soddisfatti dal nostro ingresso in questo settore.\n"
            "La serietà e la precisione sono la nostra priorità assoluta."
        ),
        "support_prompt": (
            "✍️ <b>ASSISTENZA CLIENTI (ANCHE PER LIMITATI)</b>\n\n"
            "Invia qui sotto il tuo messaggio o la tua richiesta.\n"
            "Riceverai risposta direttamente qui nel bot appena un operatore sarà disponibile."
        ),
        "support_sent": "✅ <b>Messaggio inviato al supporto!</b>\nTi risponderemo direttamente qui a breve.",
        "support_reply_header": "💬 <b>RISPOSTA DALL'ASSISTENZA:</b>\n\n",
        "btn_reply_again": "✍️ Rispondi all'Assistenza",
        "cancel": "❌ Annulla",
        "cancelled": "Operazione annullata."
    },
    "en": {
        "disclaimer": (
            "⚠️ <b>WARNING READ THIS MESSAGE CAREFULLY!</b>\n\n"
            "Hello, we have been informed by several clients that there are many scammers on Telegram and TikTok! "
            "We ask for maximum attention and above all, we ask you to report these individuals as much as possible.\n\n"
            "We are not here to play.\n"
            "We are not here to listen to problems.\n"
            "We are not here to do charity.\n\n"
            "We are an experienced team in this field, offering our full knowledge and trust!\n\n"
            "We are only looking for responsible people who want to turn their lives around!\n\n"
            "Since we started working in this field, we have helped over 300 people. "
            "We faced many issues including bans and customer difficulties, but we never gave up because success is always around the corner!"
        ),
        "btn_read": "✅ I HAVE READ!",
        "captcha_title": "🤖 <b>SECURITY CHECK</b>\n\nSelect the icon matching: <b>{target_name}</b>",
        "captcha_wrong": "❌ Incorrect! Try again with a new captcha.",
        "welcome": "👋 Hello <b>{name}</b>!\nWelcome to our official bot.\nChoose an option from the menu below:",
        "btn_banknotes": "💵 Banknotes (10/20/50)",
        "btn_videos": "🎥 Quality Videos",
        "btn_shipping": "📦 Shipping",
        "btn_payments": "💳 Payment Methods",
        "btn_feedback": "⭐ Reviews & Feedback",
        "btn_support": "✍️ Support / Restricted",
        "btn_lang": "🌐 Change Language",
        "btn_back": "🔙 Main Menu",
        "banknotes_info": "💵 <b>AVAILABLE BANKNOTES</b>\n\nHigh-grade 10€, 20€, and 50€ notes with full security features.",
        "videos_info": "🎥 <b>QUALITY VIDEOS</b>\n\nInspect UV marks, pen tests, and paper quality. Contact support for proof channel.",
        "shipping_info": "📦 <b>SHIPPING</b>\n\n100% stealth and vacuum-sealed shipping via tracked 24/48h couriers.",
        "payments_info": "💳 <b>PAYMENTS</b>\n\nWe accept secure, anonymous crypto payments:\n• Bitcoin (BTC)\n• USDT (TRC20)\n• Monero (XMR)",
        "feedback_info": "⭐ <b>REVIEWS</b>\n\nOver 300 satisfied clients. Quality and discretion are guaranteed.",
        "support_prompt": "✍️ <b>SUPPORT DESK</b>\n\nSend your message below. We will reply to you directly inside this bot.",
        "support_sent": "✅ <b>Message sent to support!</b>\nWe will get back to you shortly.",
        "support_reply_header": "💬 <b>REPLY FROM SUPPORT:</b>\n\n",
        "btn_reply_again": "✍️ Reply to Support",
        "cancel": "❌ Cancel",
        "cancelled": "Operation cancelled."
    },
    "es": {
        "disclaimer": (
            "⚠️ <b>¡ATENCIÓN LEA ESTE MENSAJE ATENTAMENTE!</b>\n\n"
            "¡Hola, varios clientes nos han informado que hay muchos estafadores en Telegram y TikTok! "
            "Pedimos la máxima atención y sobre todo pedimos denunciar a estos sujetos lo más posible.\n\n"
            "No estamos aquí para jugar.\n"
            "No estamos aquí para escuchar problemas.\n"
            "No estamos aquí para hacer caridad.\n\n"
            "¡Somos un equipo experto en este sector, ponemos todo nuestro conocimiento y confianza!\n\n"
            "¡Buscamos únicamente personas sensatas y con ganas de cambiar su vida!\n\n"
            "Desde que empezamos hemos ayudado a más de 300 personas, "
            "enfrentamos muchos problemas entre bloqueos y dificultades, ¡pero nunca nos rendimos!"
        ),
        "btn_read": "✅ ¡HE LEÍDO!",
        "captcha_title": "🤖 <b>CONTROL DE SEGURIDAD</b>\n\nSelecciona el icono: <b>{target_name}</b>",
        "captcha_wrong": "❌ ¡Incorrecto! Inténtalo de nuevo.",
        "welcome": "👋 ¡Hola <b>{name}</b>!\nBienvenido a nuestro bot oficial.\nSelecciona una opción:",
        "btn_banknotes": "💵 Billetes (10/20/50)",
        "btn_videos": "🎥 Videos de Calidad",
        "btn_shipping": "📦 Envíos",
        "btn_payments": "💳 Métodos de Pago",
        "btn_feedback": "⭐ Opiniones & Reseñas",
        "btn_support": "✍️ Soporte / Limitados",
        "btn_lang": "🌐 Cambiar Idioma",
        "btn_back": "🔙 Menú Principal",
        "banknotes_info": "💵 <b>BILLETES DISPONIBLES</b>\n\nBilletes de 10€, 20€ y 50€ con todas las marcas de agua y bandas reactivas.",
        "videos_info": "🎥 <b>VIDEOS DE CALIDAD</b>\n\nPruebas UV y de reactividad con rotulador disponibles en soporte.",
        "shipping_info": "📦 <b>ENVÍOS</b>\n\nEnvíos 100% discretos al vacío con entrega express 24/48h.",
        "payments_info": "💳 <b>MÉTODOS DE PAGO</b>\n\nAceptamos pagos anónimos en criptomonedas (BTC, USDT, XMR).",
        "feedback_info": "⭐ <b>OPINIONES</b>\n\nMás de 300 clientes satisfechos respaldan nuestro trabajo.",
        "support_prompt": "✍️ <b>ATENCIÓN AL CLIENTE</b>\n\nEscribe tu consulta abajo y te responderemos aquí mismo.",
        "support_sent": "✅ <b>¡Mensaje enviado al soporte!</b>",
        "support_reply_header": "💬 <b>RESPUESTA DEL SOPORTE:</b>\n\n",
        "btn_reply_again": "✍️ Responder al Soporte",
        "cancel": "❌ Cancelar",
        "cancelled": "Operación cancelada."
    },
    "fr": {
        "disclaimer": (
            "⚠️ <b>ATTENTION LISEZ CE MESSAGE ATTENTIVEMENT !</b>\n\n"
            "Bonjour, plusieurs clients nous ont informés que de nombreux arnaqueurs tournent sur Telegram et TikTok ! "
            "Nous demandons la plus grande vigilance et surtout de signaler ces individus.\n\n"
            "Nous ne sommes pas là pour jouer.\n"
            "Nous ne sommes pas là pour écouter des plaintes.\n"
            "Nous ne sommes pas là pour faire la charité.\n\n"
            "Nous sommes une équipe expérimentée, nous offrons toute notre confiance et expertise !\n\n"
            "Nous cherchons uniquement des personnes sérieuses voulant changer de vie !\n\n"
            "Depuis nos débuts, nous avons aidé plus de 300 personnes. Malgré les blocages, nous n'avons jamais baissé les bras !"
        ),
        "btn_read": "✅ J'AI LU !",
        "captcha_title": "🤖 <b>VÉRIFICATION DE SÉCURITÉ</b>\n\nSélectionnez l'icône : <b>{target_name}</b>",
        "captcha_wrong": "❌ Incorrect ! Réessayez.",
        "welcome": "👋 Bonjour <b>{name}</b> !\nBienvenue sur notre bot officiel.\nChoisissez une option ci-dessous :",
        "btn_banknotes": "💵 Billets (10/20/50)",
        "btn_videos": "🎥 Vidéos Qualité",
        "btn_shipping": "📦 Livraisons",
        "btn_payments": "💳 Modes de Paiement",
        "btn_feedback": "⭐ Avis & Retours",
        "btn_support": "✍️ Support / Limités",
        "btn_lang": "🌐 Changer de Langue",
        "btn_back": "🔙 Menu Principal",
        "banknotes_info": "💵 <b>BILLETS DISPONIBLES</b>\n\nCoupures 10€, 20€ et 50€ avec hologrammes et réactivité UV parfaite.",
        "videos_info": "🎥 <b>VIDÉOS QUALITÉ</b>\n\nTests UV et authenticité disponibles via le support.",
        "shipping_info": "📦 <b>LIVRAISON</b>\n\nEmballage 100% discret sous vide, expédition express 24/48h.",
        "payments_info": "💳 <b>PAIEMENTS</b>\n\nPaiements sécurisés et anonymes via Crypto (BTC, USDT, XMR).",
        "feedback_info": "⭐ <b>AVIS</b>\n\nPlus de 300 clients réguliers et satisfaits.",
        "support_prompt": "✍️ <b>SUPPORT CLIENT</b>\n\nÉcrivez votre message ci-dessous, nous vous répondrons directement ici.",
        "support_sent": "✅ <b>Message envoyé au support !</b>",
        "support_reply_header": "💬 <b>RÉPONSE DU SUPPORT :</b>\n\n",
        "btn_reply_again": "✍️ Répondre au Support",
        "cancel": "❌ Annuler",
        "cancelled": "Opération annulée."
    },
    "de": {
        "disclaimer": (
            "⚠️ <b>ACHTUNG LESEN SIE DIESE NACHRICHT AUFMERKSAM!</b>\n\n"
            "Hallo, wir wurden von mehreren Kunden gewarnt, dass auf Telegram und TikTok viele Scammer unterwegs sind! "
            "Wir bitten um höchste Wachsamkeit und vor allem darum, solche Profile zu melden.\n\n"
            "Wir sind nicht zum Spielen hier.\n"
            "Wir sind nicht hier, um Probleme anzuhören.\n"
            "Wir sind nicht für Wohltätigkeit hier.\n\n"
            "Wir sind ein erfahrenes Team in diesem Bereich und bieten volles Vertrauen und Wissen!\n\n"
            "Wir suchen nur verantwortungsvolle Menschen, die ihr Leben verändern wollen!\n\n"
            "Seit Beginn haben wir über 300 Personen geholfen. Trotz vieler Hürden haben wir nie aufgegeben!"
        ),
        "btn_read": "✅ GELESEN!",
        "captcha_title": "🤖 <b>SICHERHEITSABFRAGE</b>\n\nWählen Sie das Symbol für: <b>{target_name}</b>",
        "captcha_wrong": "❌ Falsch! Bitte erneut versuchen.",
        "welcome": "👋 Hallo <b>{name}</b>!\nWillkommen bei unserem offiziellen Bot.\nWählen Sie eine Option:",
        "btn_banknotes": "💵 Banknoten (10/20/50)",
        "btn_videos": "🎥 Qualitätsvideos",
        "btn_shipping": "📦 Versand",
        "btn_payments": "💳 Zahlungsmethoden",
        "btn_feedback": "⭐ Kundenbewertungen",
        "btn_support": "✍️ Support / Eingeschränkte",
        "btn_lang": "🌐 Sprache ändern",
        "btn_back": "🔙 Hauptmenü",
        "banknotes_info": "💵 <b>VERFÜGBARE BANKNOTEN</b>\n\n10€, 20€ und 50€ Scheine mit vollen UV- und Sicherheitsmerkmalen.",
        "videos_info": "🎥 <b>QUALITÄTSVIDEOS</b>\n\nStifttests und UV-Beweise erhalten Sie beim Support.",
        "shipping_info": "📦 <b>VERSAND</b>\n\n100% vakuumverpackter und anonymer Expressversand (24-48h).",
        "payments_info": "💳 <b>ZAHLUNGEN</b>\n\nSicher und anonym per Krypto (BTC, USDT, XMR).",
        "feedback_info": "⭐ <b>BEWERTUNGEN</b>\n\nÜber 300 zufriedene Kunden seit Gründung.",
        "support_prompt": "✍️ <b>KUNDENSUPPORT</b>\n\nSchreiben Sie Ihre Nachricht unten. Die Antwort erhalten Sie direkt im Chat.",
        "support_sent": "✅ <b>Nachricht an den Support gesendet!</b>",
        "support_reply_header": "💬 <b>ANTWORT VOM SUPPORT:</b>\n\n",
        "btn_reply_again": "✍️ Dem Support antworten",
        "cancel": "❌ Abbrechen",
        "cancelled": "Vorgang abgebrochen."
    }
}

CAPTCHA_ITEMS = [
    {"name": {"it": "Mela", "en": "Apple", "es": "Manzana", "fr": "Pomme", "de": "Apfel"}, "emoji": "🍎"},
    {"name": {"it": "Auto", "en": "Car", "es": "Coche", "fr": "Voiture", "de": "Auto"}, "emoji": "🚗"},
    {"name": {"it": "Fulmine", "en": "Lightning", "es": "Rayo", "fr": "Éclair", "de": "Blitz"}, "emoji": "⚡"},
    {"name": {"it": "Cane", "en": "Dog", "es": "Perro", "fr": "Chien", "de": "Hund"}, "emoji": "🐶"},
    {"name": {"it": "Pizza", "en": "Pizza", "es": "Pizza", "fr": "Pizza", "de": "Pizza"}, "emoji": "🍕"},
    {"name": {"it": "Aereo", "en": "Plane", "es": "Avión", "fr": "Avion", "de": "Flugzeug"}, "emoji": "✈️"}
]

def get_user_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "it")

def get_disclaimer_markup(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    keyboard = [
        [
            InlineKeyboardButton("🇮🇹 IT", callback_data="setlang_it"),
            InlineKeyboardButton("🇬🇧 EN", callback_data="setlang_en"),
            InlineKeyboardButton("🇪🇸 ES", callback_data="setlang_es"),
            InlineKeyboardButton("🇫🇷 FR", callback_data="setlang_fr"),
            InlineKeyboardButton("🇩🇪 DE", callback_data="setlang_de"),
        ],
        [InlineKeyboardButton(t["btn_read"], callback_data="action_read_disclaimer")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_markup(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    t = TEXTS[get_user_lang(context)]
    keyboard = [
        [InlineKeyboardButton(t["btn_banknotes"], callback_data="menu_banknotes")],
        [InlineKeyboardButton(t["btn_videos"], callback_data="menu_videos"), InlineKeyboardButton(t["btn_shipping"], callback_data="menu_shipping")],
        [InlineKeyboardButton(t["btn_payments"], callback_data="menu_payments"), InlineKeyboardButton(t["btn_feedback"], callback_data="menu_feedback")],
        [InlineKeyboardButton(t["btn_support"], callback_data="user_start_support")],
        [InlineKeyboardButton(t["btn_lang"], callback_data="menu_changelang")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def update_view(query, photo_path: str, caption: str, reply_markup: InlineKeyboardMarkup):
    """Sostituisce dinamicamente l'immagine e la didascalia associata."""
    if photo_path and os.path.exists(photo_path):
        try:
            with open(photo_path, "rb") as photo:
                await query.edit_message_media(
                    media=InputMediaPhoto(media=photo, caption=caption, parse_mode=ParseMode.HTML),
                    reply_markup=reply_markup
                )
                return
        except Exception:
            pass

    try:
        await query.edit_message_caption(caption=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except Exception:
        try:
            await query.edit_message_text(text=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except Exception:
            await query.message.reply_text(text=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

# Gestione comando /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lang"] = context.user_data.get("lang", "it")
    context.user_data["verified"] = False
    context.user_data["state"] = None

    lang = get_user_lang(context)
    caption = TEXTS[lang]["disclaimer"]
    reply_markup = get_disclaimer_markup(lang)

    chat_id = update.effective_chat.id

    if os.path.exists(IMAGE_PATH):
        with open(IMAGE_PATH, "rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

# Generatore Captcha Casuale
async def present_captcha(query, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    selected = random.sample(CAPTCHA_ITEMS, 4)
    target = random.choice(selected)
    context.user_data["captcha_target"] = target["emoji"]

    target_name = target["name"].get(lang, target["name"]["it"])
    caption = TEXTS[lang]["captcha_title"].format(target_name=target_name)

    buttons = [
        InlineKeyboardButton(item["emoji"], callback_data=f"captcha_{item['emoji']}")
        for item in selected
    ]
    reply_markup = InlineKeyboardMarkup([buttons])

    await update_view(query, IMAGE_PATH, caption, reply_markup)

# Router Callback Query
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_lang = get_user_lang(context)

    await query.answer()

    # Cambio lingua nella schermata di avviso iniziale
    if data.startswith("setlang_"):
        new_lang = data.split("_")[1]
        context.user_data["lang"] = new_lang
        await update_view(query, IMAGE_PATH, TEXTS[new_lang]["disclaimer"], get_disclaimer_markup(new_lang))
        return

    # Click su HO LETTO! -> Avvia il Captcha
    if data == "action_read_disclaimer":
        await present_captcha(query, context)
        return

    # Verifica Captcha
    if data.startswith("captcha_"):
        chosen = data.split("_")[1]
        target = context.user_data.get("captcha_target")

        if chosen == target:
            context.user_data["verified"] = True
            name = update.effective_user.mention_html()
            text = TEXTS[user_lang]["welcome"].format(name=name)
            await update_view(query, IMAGE_PATH, text, get_main_menu_markup(context))
        else:
            await query.answer(TEXTS[user_lang]["captcha_wrong"], show_alert=True)
            await present_captcha(query, context)
        return

    # Blocco se non verificato
    if not context.user_data.get("verified", False):
        await update_view(query, IMAGE_PATH, TEXTS[user_lang]["disclaimer"], get_disclaimer_markup(user_lang))
        return

    # Navigazione Menu
    if data == "menu_main":
        name = update.effective_user.mention_html()
        text = TEXTS[user_lang]["welcome"].format(name=name)
        await update_view(query, IMAGE_PATH, text, get_main_menu_markup(context))

    elif data == "menu_banknotes":
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(TEXTS[user_lang]["btn_back"], callback_data="menu_main")]])
        await update_view(query, IMAGE_PATH, TEXTS[user_lang]["banknotes_info"], markup)

    elif data == "menu_videos":
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(TEXTS[user_lang]["btn_back"], callback_data="menu_main")]])
        await update_view(query, IMAGE_PATH, TEXTS[user_lang]["videos_info"], markup)

    # Visualizzazione schermata SPEDIZIONI con la foto del pacco e locker InPost
    elif data == "menu_shipping":
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(TEXTS[user_lang]["btn_back"], callback_data="menu_main")]])
        await update_view(query, SHIPPING_IMAGE_PATH, TEXTS[user_lang]["shipping_info"], markup)

    elif data == "menu_payments":
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(TEXTS[user_lang]["btn_back"], callback_data="menu_main")]])
        await update_view(query, IMAGE_PATH, TEXTS[user_lang]["payments_info"], markup)

    elif data == "menu_feedback":
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(TEXTS[user_lang]["btn_back"], callback_data="menu_main")]])
        await update_view(query, IMAGE_PATH, TEXTS[user_lang]["feedback_info"], markup)

    elif data == "menu_changelang":
        buttons = [
            [
                InlineKeyboardButton("🇮🇹 IT", callback_data="menulang_it"),
                InlineKeyboardButton("🇬🇧 EN", callback_data="menulang_en"),
                InlineKeyboardButton("🇪🇸 ES", callback_data="menulang_es"),
                InlineKeyboardButton("🇫🇷 FR", callback_data="menulang_fr"),
                InlineKeyboardButton("🇩🇪 DE", callback_data="menulang_de"),
            ],
            [InlineKeyboardButton(TEXTS[user_lang]["btn_back"], callback_data="menu_main")]
        ]
        await update_view(query, IMAGE_PATH, "🌐 <b>Seleziona la tua lingua:</b>", InlineKeyboardMarkup(buttons))

    elif data.startswith("menulang_"):
        new_lang = data.split("_")[1]
        context.user_data["lang"] = new_lang
        name = update.effective_user.mention_html()
        text = TEXTS[new_lang]["welcome"].format(name=name)
        await update_view(query, IMAGE_PATH, text, get_main_menu_markup(context))

    # Supporto Utente (anche per limitati)
    elif data == "user_start_support":
        context.user_data["state"] = "WAITING_SUPPORT_MESSAGE"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(TEXTS[user_lang]["cancel"], callback_data="cancel_action")]])
        await update_view(query, IMAGE_PATH, TEXTS[user_lang]["support_prompt"], markup)

    # Risposta Admin
    elif data.startswith("admin_reply_"):
        target_id = data.split("_")[2]
        context.user_data["state"] = f"ADMIN_TYPING_REPLY_{target_id}"
        await query.message.reply_text(
            f"✍️ <b>Scrivi la risposta per l'utente</b> <code>{target_id}</code>:\n(Oppure scrivi /cancel per annullare)",
            parse_mode=ParseMode.HTML
        )

    elif data == "cancel_action":
        context.user_data["state"] = None
        name = update.effective_user.mention_html()
        text = TEXTS[user_lang]["welcome"].format(name=name)
        await update_view(query, IMAGE_PATH, text, get_main_menu_markup(context))

# Gestione Messaggi di Testo (Chat Bidirezionale Assistenza)
async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    state = context.user_data.get("state")
    user_lang = get_user_lang(context)

    # Inoltro richiesta utente -> Admin
    if state == "WAITING_SUPPORT_MESSAGE":
        context.user_data["state"] = None
        user_msg = update.message.text

        if ADMIN_ID != 0:
            admin_text = (
                f"📩 <b>NUOVO MESSAGGIO DAL BOT</b>\n\n"
                f"👤 <b>Utente:</b> {user.full_name} (@{user.username or 'Nessun username'})\n"
                f"🆔 <b>ID Utente:</b> <code>{user.id}</code>\n"
                f"🌐 <b>Lingua:</b> {user_lang.upper()}\n\n"
                f"💬 <b>Messaggio:</b>\n{user_msg}"
            )
            admin_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"✍️ Rispondi a {user.first_name}", callback_data=f"admin_reply_{user.id}")]
            ])
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_text,
                reply_markup=admin_markup,
                parse_mode=ParseMode.HTML
            )

        user_confirm = TEXTS[user_lang]["support_sent"]
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(TEXTS[user_lang]["btn_back"], callback_data="menu_main")]])
        await update.message.reply_text(user_confirm, reply_markup=markup, parse_mode=ParseMode.HTML)
        return

    # Risposta Admin -> Utente
    if state and state.startswith("ADMIN_TYPING_REPLY_"):
        target_user_id = int(state.split("_")[3])
        context.user_data["state"] = None
        admin_reply_text = update.message.text

        try:
            target_lang = "it"
            user_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[target_lang]["btn_reply_again"], callback_data="user_start_support")],
                [InlineKeyboardButton(TEXTS[target_lang]["btn_back"], callback_data="menu_main")]
            ])

            await context.bot.send_message(
                chat_id=target_user_id,
                text=f"{TEXTS[target_lang]['support_reply_header']}{admin_reply_text}",
                reply_markup=user_markup,
                parse_mode=ParseMode.HTML
            )
            await update.message.reply_text("✅ Risposta inoltrata correttamente all'utente!")
        except Exception as e:
            await update.message.reply_text(f"❌ Impossibile recapitare il messaggio all'utente: {e}")
        return

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = None
    lang = get_user_lang(context)
    await update.message.reply_text(TEXTS[lang]["cancelled"])

def main():
    if not BOT_TOKEN:
        print("ERRORE: Inserisci il BOT_TOKEN nelle variabili d'ambiente (.env o Railway)!")
        return

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    print("🤖 Bot avviato e perfettamente operativo...")
    application.run_polling()

if __name__ == "__main__":
    main()
