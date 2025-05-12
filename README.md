# README

Este documento explica cómo preparar y ejecutar la **Calculadora de Matrices** paso a paso.

## 1. Requisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python** (versión 3.x)
- Acceso al repositorio del **proyecto** en tu máquina

## 2. Crear el _entorno virtual_

En el directorio raíz del **proyecto**, crea un _entorno virtual_ con el siguiente comando:

_python -m venv matrixenv_

Este paso aísla las dependencias del **proyecto** del resto de tu sistema.

## 3. Activar el _entorno virtual_

Para empezar a usar el _entorno virtual_, ejecuta:

_.\matrixenv\Scripts\activate_

(verifica que el prompt de la terminal muestre el prefijo `(matrixenv)`)

## 4. Instalar las **dependencias**

Con el _entorno virtual_ activo, instala todas las **dependencias** listadas en el archivo `requirements.txt`:

_pip install -r requirements.txt_

Esto descargará e instalará las librerías necesarias para el **proyecto**.

## 5. Ejecutar la **aplicación**

Una vez instaladas las **dependencias**, inicia la **aplicación** con:

_python -m src.gui.main_

Se abrirá la ventana de la Calculadora de Matrices, lista para usar.

## 6. Desactivar el _entorno virtual_

Cuando hayas terminado de trabajar, puedes salir del _entorno virtual_ con:

_deactivate_

De esta manera tu terminal volverá a usar las configuraciones globales de Python.
