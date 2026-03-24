# 🤖 Robot Lab: Asistente de Laboratorio Autónomo

¡Bienvenido al repositorio oficial de **Robot Lab**! 

Este proyecto define un robot asistente de laboratorio diseñado y simulado en **ROS 2** y **Gazebo Ignition**. Su propósito es ayudar a humanos en entornos de investigación, combinando navegación autónoma avanzada y capacidades conversacionales naturales.

## 🌟 Características Principales

* 🧠 **Navegación Autónoma mediante RL:** A diferencia de los sistemas de navegación clásicos, este robot utiliza **Aprendizaje por Refuerzo (Reinforcement Learning)** para aprender políticas de movimiento dinámicas, esquivar obstáculos y navegar eficientemente por el laboratorio.
* 🗣️ **Interacción Humano-Robot con LLM:** Equipado con integración de Modelos de Lenguaje Grande (LLMs), el robot puede comprender instrucciones complejas en lenguaje natural, responder preguntas y asistir de manera conversacional a los investigadores.
* 👁️ **Percepción y Fusión de Sensores:** * **LiDAR 2D:** Para mapeo del entorno y detección precisa de obstáculos.
  * **Cámara RGB:** Para visión artificial, reconocimiento de objetos e interacción visual.
  * **Odometría de Encoders:** Para una estimación precisa del estado y la cinemática diferencial.

## 🛠️ Especificaciones Técnicas del Robot

* **Cinemática:** Tracción diferencial (2 ruedas motrices delanteras + 2 ruedas locas traseras de fricción cero).
* **Dimensiones del Cuerpo:** 48 cm (longitud) x 30 cm (ancho) x 79 cm (altura).
* **Masa Total:** ~14 kg.
* **Despeje del Suelo:** 10 cm.

## 🚀 Instalación y Uso

Este proyecto utiliza el sistema de construcción `colcon` de ROS 2. Sigue estos pasos para compilar y lanzar la simulación en tu máquina.

### Prerrequisitos
* ROS 2 (Humble / Iron / Jazzy - *Especifica tu versión aquí*)
* Gazebo Ignition (Fortress / Harmonic - *Especifica tu versión aquí*)
* Paquetes de ROS: `ros-gz-bridge`, `xacro`, `robot_state_publisher`

### Compilación

Clona este repositorio en la carpeta `src` de tu workspace de ROS 2:

```bash
cd ~/tu_workspace/src
git clone [https://github.com/tu-usuario/robot_lab.git](https://github.com/tu-usuario/robot_lab.git)
cd ~/tu_workspace
colcon build --packages-select robot_description


### Ejecutar la Simulación

No olvides hacer source de tu entorno antes de lanzar el robot:

source install/setup.bash
ros2 launch robot_description robot_lab_launch.py

Esto abrirá Gazebo Ignition con el robot_lab instanciado, listo para recibir comandos de velocidad (/r1/cmd_vel) y publicar los datos de sus sensores (/r1/scan, /r1/camera/image_raw).