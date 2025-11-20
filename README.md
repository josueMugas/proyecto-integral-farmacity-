# proyecto-integral-farmacity-

Farmacity, una cadena de farmacias necesita un sistema para gestionar
inventario de medicamentos, ventas, clientes y reportes. El sistema debe
combinar estructuras de datos avanzadas (para operaciones rápidas) y una
base de datos relacional (para almacenamiento persistente).

�� Objetivos
1. Diseñar una base de datos normalizada (hasta 3FN) con tablas para
medicamentos, clientes, empleados y ventas.
2. Implementar estructuras de datos en memoria:
a. Tabla hash: Para búsqueda rápida de medicamentos por código
de barras.
b. Árbol: Para organizar medicamentos por categoría (ej:
&quot;Analgésicos&quot;).
c. Cola prioritaria: Gestionar pedidos de medicamentos urgentes
(prioridad alta).
d. Grafos: Modelar interacciones entre medicamentos
(contraindicaciones).
3. Conectar ambas partes:
a. Sincronizar datos entre estructuras y BD mediante operaciones
CRUD.
b. Optimizar consultas SQL con índices y claves foráneas.

�� Requisitos Mínimos
1. Base de Datos (SQL)
 Tablas:
o Medicamentos (ID, nombre, categoría, precio, stock,
código_barras).
o Clientes (ID, nombre, DNI, historial_compras).
o Ventas (ID, ID_Medicamento, ID_Cliente, fecha, cantidad).
o Empleados (ID, nombre, rol).
 Relaciones: Claves primarias/foráneas entre ventas, medicamentos y
clientes.
 Consultas complejas:
o Top 5 medicamentos más vendidos.
o Medicamentos con stock crítico (&lt; 10 unidades).
o Clientes frecuentes (más de 5 compras en el último mes).

Proyecto: Sistema de Gestión para Farmacity.
Asignaturas:
 Base de Datos
 Lab. de Algoritmos y Estructuras de Datos
Curso: 4to Año

2. Estructuras de Datos (Código)
 Tabla hash: Búsqueda en O(1) de medicamentos por código de barras.
 Árbol: Ordenar medicamentos por categoría para filtros rápidos.
 Cola prioritaria: Atender pedidos urgentes (ej: medicamentos
refrigerados).
 Grafos: Alertar sobre contraindicaciones al vender medicamentos.
3. Integración
 Lenguaje: Python + MySQL.
 Funcionalidades:
o Registrar venta (actualizar BD y estructuras).
o Buscar medicamento (usar tabla hash + árbol).
o Generar reportes:
 &quot;Medicamentos próximos a vencer&quot; (SQL + código).
 &quot;Ventas por empleado&quot; (SQL + código).
