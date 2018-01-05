
sentences = {
    "EN": {
        "THANK_LOGGED_IN": "Thanks for your contribution! Every person that logs in helps me provide better results to everyone!",
        "FIRST_MESSAGE": "Welcome! I am BotCycle and can give you bike sharing informations",
        "ASK_LOGIN": "please login with facebook to improve recommendations",
        "GREET_BACK": "Hi there! How can I help?",
        "THANK_BACK": "You\'re welcome!",
        "PROVIDE_INFO": "I am BotCycle, a bot that can give you informations about bike sharing in your city.\nTry to ask me something! ;)",
        "CANT_BOOK": "Sorry but you can\'t book bikes",
        "UNEXPECTED_INTENT": "Unexpected intent: {intent}",
        "NO_INTENT": "Your sentence does not have an intent",
        "UNSUPPORTED_CONTENT_TYPE": "why did you send {type}?",
        "ACK_POSITION": "Ok I got your position",
        "ASK_POSITION": "Where are you?",
        "ERROR_SEARCHING": "Impossible to find informations. Something went wrong!",
        "FREE_BIKES": "You can find {count} free bikes at station {station_name}",
        "FREE_SLOTS": "You can find {count} free slots at station {station_name}",
        "TRIP": "You can find {src_count} free bikes at station {src_station_name} and {dst_count} free slots at station {dst_station_name}",
        "GEOCODING_ERROR": "Impossible to find a place named {searched}",
        "RECOMMEND_PLACE": "You could try this interesting place: {place_name}",
        "SUPPORTED_AFFIRMATIVE": "Yes, {city} is supported",
        "SUPPORTED_NEGATIVE": "Nearest supported city is {nearest_city}",
        "INCOMPLETE_TRIP": "Your trip has no source and no destination",
        "INTERCITY_TRIP": "Your trip starts at {source} and ends at {destination}. You cannot take a bike from one city and go to another one!",
        "REQUIRED_POSITION": "I didn't manage to extract a position from your sentence"
    },
    "IT": {
        "THANK_LOGGED_IN": "Grazie per il contributo! Ogni persona che effettua il login mi aiuta a fornire risultati migliori a tutti!",
        "FIRST_MESSAGE": "Benvenuto! Sono BotCycle e posso darti informazioni sul servizio di bike sharing",
        "ASK_LOGIN": "per favore accedi con facebook per ottenere consigli migliori",
        "GREET_BACK": "Ciao! Come posso aiutarti?",
        "THANK_BACK": "Prego!",
        "PROVIDE_INFO": "Sono BotCycle e posso darti informazioni sul servizio di bike sharing nella tua città.\nProva a chiedermi qualcosa! ;)",
        "CANT_BOOK": "Mi dispiace ma non posso prenotare le bici",
        "UNEXPECTED_INTENT": "Intento inaspettato: {intent}",
        "NO_INTENT": "La tua frase non contiene un intento",
        "UNSUPPORTED_CONTENT_TYPE": "Perché mi hai mandato {type}?",
        "ACK_POSITION": "Ok ho la tua posizione",
        "ASK_POSITION": "Dove sei?",
        "ERROR_SEARCHING": "Impossibile trovare le informazioni. Qualcosa è andato male!",
        "FREE_BIKES": "Puoi trovare {count} bici libere alla stazione {station_name}",
        "FREE_SLOTS": "Puoi trovare {count} parcheggi liberi alla stazione {station_name}",
        "TRIP": "Pui trovare {src_count} bici libere alla stazione {src_station_name} e {dst_count} parcheggi liberi alla stazione {dst_station_name}",
        "GEOCODING_ERROR": "Impossibile trovare un posto chiamato {searched}",
        "RECOMMEND_PLACE": "Potresti provare questo posto interessante: {place_name}",
        "SUPPORTED_AFFIRMATIVE": "Sì, {city} è supportata",
        "SUPPORTED_NEGATIVE": "La città supportata più vicina è {nearest_city}",
        "INCOMPLETE_TRIP": "Il tuo viaggio non ha né un punto di partenza né un punto di arrivo",
        "INTERCITY_TRIP": "Il tuo viaggio inizia a {source} e finisce a {destination}. Non puoi prendere una bici in una città e portarla in un'altra!",
        "REQUIRED_POSITION": "Non sono riuscito ad estrarre una posizione dalla tua frase"
    }
}

def get(lang, string):
    return sentences[lang][string]