"""Constants for the list_cars module."""

# CSV Column names
COLUMN_TITLE = "Título"
COLUMN_PRICE = "Precio"
COLUMN_LINK = "Enlace"

# CSV fieldnames in order
CSV_FIELDNAMES = [COLUMN_TITLE, COLUMN_PRICE, COLUMN_LINK]

# Field priority order for car attributes
FIELD_PRIORITY = [
    # High priority fields
    "Enlace",
    "ImagenURL",
    "Título",
    "Score",
    "Precio",
    "Marca",
    "Modelo",
    "Versión",
    "Motor",
    "Año",
    "Kilómetros",
    "Color",
    "Control de tracción",
    "Dirección",
    "Potencia",
    "Puertas",
    "Capacidad de personas",
    "Capacidad del tanque",
    "Tipo de carrocería",
    "Tipo de combustible",
    "Transmisión",
    "Ubicación",

    # Safety and functional features
    "Airbag conductor",
    "Airbag para conductor y pasajero",
    "Frenos ABS",
    "Control de estabilidad",
    "Cierre centralizado de puertas",
    "Vidrios eléctricos",
    "Cierre automático de vidrios",
    "Desempañador trasero",
    "Aire acondicionado",
    "Climatizador",
    "Sensor de parqueo",
    "Sensor de lluvia",
    "Con cámara de reversa",
    "Computadora de abordo",
    "Blindado",

    # Multimedia and connectivity
    "Bluetooth",
    "CD",
    "AM/FM",
    "Reproductor de MP3",
    "Entrada USB",
    "Entrada auxiliar",
    "DVD",
    "Comando remoto para radio en el volante",

    # Extras and comfort
    "Techo corredizo",
    "Tapizado de cuero",
    "Tercera luz de freno led",
    "Alarma",
    "Alarma de luces encendidas",
    "Apertura remota de baúl",
    "Limpia/lava luneta",
    "Faros antinieblas traseros",
    "Luces con regulación automática",
    "Piloto automático",
    "Porta vasos",
    "Porta equipaje en techo",
    "Soporte para llanta de repuesto",
    "Llantas de aleación",
    "Defensa delantera",
    "Sistema ISOFIX",

    # Warranties and commercial conditions
    "Con garantía de fábrica",
    "Con garantía mecánica",
    "Con precio negociable",
    "Venpermuta",
    "Único dueño",

    # Technical complements
    "Distancia entre ejes",
    "Largo x Ancho",
    "Largo x Altura x Ancho",
    "Válvulas por cilindro",
    "Último dígito de la placa",
    "Paridad de la placa",

    # Electric
    "Autonomia de la batería",
    "Capacidad de la batería",
    "Tipo de batería",
    "Tiempo de carga",
    "Tipo de cargador",
]
