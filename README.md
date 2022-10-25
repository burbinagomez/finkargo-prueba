# Instrucciones

El siguiente proyecto contiene la solucion a la prueba tecnica de finkargo

## Arquitectura
Se realizo el siguiente [diagrama](https://lucid.app/lucidchart/8ff7dffe-f60c-4120-8c0e-a2bcd32fca83/edit?viewport_loc=-1151%2C-379%2C4039%2C2027%2CteUxap1cgRFU&invitationId=inv_8dabf1f2-44fe-4415-a106-796fda6066f5) para el modelo de datos
### Tecnologias
Flask para la creacion del api, peewee para orm, jwt para el manejo del login 

## Requerimientos
Python 3.8

## Instalacion local

Usar el administrador de paquetes  [pip](https://pip.pypa.io/en/stable/) para instalar todos los requerimientos.

```bash
pip install -r requirements.txt
```

## Ejecucion con docker

```bash
docker build -t finkargo .
docker run -d -p 5000:5000 finkargo