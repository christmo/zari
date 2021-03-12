# zari
Bot Conversacional NLP para Retail

Zari es un proyecto enfocado en proveer a distintas tiendas un asistente virtual, capaz de ofrecer sus productos de forma automática, para que los clientes puedan tener un canal como Telegram para comprar ciertos productos o servicios.

Roadmap de Implementación:

Lista de dominios y subdominios:
  - Small talk
		- Saludo, despedida, etc
		- Preguntas personales del usuario al VA
	- Mostrar opciones de productos
		- Producto concreto
		- Por categoría ("quiero ver camisas / zapatos / ...")
		- Promociones
		- Productos similares
		- ¿Más vendidos?
	- Compra de productos
		- Incluir al carrito
		- Gestión del carrito
		- Pagar ("quiero pagar") -> Pasarela de pago
	- Ayuda
		- ¿Diferentes modos?
			- Cuando el usuario pregunte
			- Al realizar el onboarding
			- Al iniciar la aplicación
		- Quejas e incidencias
		- Dudas típicas (QnA)
	- Perfil
		- Añadir / modificar / eliminar datos personales
		- Compras recientes
		- Customer journey
	- None
		- Respuesta cuando no puede resolver una respuesta o consulta -> discutir
	Otros
		- Casos de uso con imágenes
			- Mostrar imágenes además de texto en la respuesta del asistente
		- Ayuda en tienda
		- Análisis de sentimiento
		- Redes sociales

# RUN

```zsh
gcloud functions deploy zari_webhook --runtime python38 --trigger-http --allow-unauthenticated --set-env-vars DB_USER=postgres,DB_PASS=postgres,DB_NAME=postgres,DB_HOST=IP:5432
```

docker run --name postgres -e POSTGRES_PASSWORD=postgres -d postgres

DB_USER=postgres DB_PASS=postgres DB_NAME=postgres DB_HOST=127.0.01:5433 functions-framework --target=zari_webhook
